"""
Main video processing engine for Podcast Video Editor
"""

import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

# Import ffmpeg (optional dependency)
try:
    import ffmpeg
except ImportError:
    ffmpeg = None

from .config import Config
from .processing import AudioProcessor, VideoAnalysis, VideoSegmentProcessor


class VideoProcessor:
    """Main video processing engine"""

    def __init__(
        self,
        config: Config,
        verbose: bool = False,
        run_directory: Optional[Path] = None,
        cleanup_run_directory: bool = False,
    ):
        self.config = config
        self.verbose = verbose
        self._temp_dir: Optional[str] = None
        self.run_directory: Optional[Path] = Path(run_directory) if run_directory else None
        self.cleanup_run_directory = cleanup_run_directory

    @staticmethod
    def create_run_directory(input_path: Path, base_output_dir: Optional[Path] = None) -> Path:
        """Create and return a unique directory for a processing run."""

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        unique_suffix = uuid4().hex[:6]

        if base_output_dir is not None:
            base_dir = Path(base_output_dir)
        else:
            env_dir = os.environ.get("PODCAST_EDITOR_RUNS_DIR")
            if env_dir:
                base_dir = Path(env_dir)
            else:
                base_dir = input_path.parent / "processed"

        run_dir = base_dir / f"{input_path.stem}_{timestamp}_{unique_suffix}"
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir

    def __enter__(self):
        if self.run_directory is None:
            self.run_directory = Path(tempfile.mkdtemp(prefix="podcast_editor_run_"))
        else:
            self.run_directory.mkdir(parents=True, exist_ok=True)

        self._temp_dir = tempfile.mkdtemp(prefix="temp_", dir=str(self.run_directory))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._temp_dir and os.path.exists(self._temp_dir):
            shutil.rmtree(self._temp_dir)

        if self.cleanup_run_directory and self.run_directory and self.run_directory.exists():
            shutil.rmtree(self.run_directory, ignore_errors=True)

    def analyze_video(self, video_path: str) -> VideoAnalysis:
        """Analyze video to determine processing results"""
        video_path = Path(video_path)

        # Get video duration
        try:
            probe = ffmpeg.probe(str(video_path))
            duration = float(probe['format']['duration'])
        except Exception as e:
            raise RuntimeError(f"Failed to get video duration: {e}")

        # Extract audio for analysis using new audio processor
        audio_processor = AudioProcessor(self._temp_dir, self.config, self.verbose)
        audio_path = audio_processor.extract_audio(str(video_path))

        # Detect silence periods using intelligent speech detection
        silence_periods = audio_processor.detect_silence(audio_path)

        # Also get transcript segments for advanced analysis
        transcript_segments = audio_processor.transcribe_audio(audio_path)

        # Calculate total silence duration
        total_silence = sum(period.duration for period in silence_periods)
        estimated_output = duration - total_silence

        # Calculate reduction percentage
        reduction_percent = (total_silence / duration) * 100 if duration > 0 else 0

        return VideoAnalysis(
            duration=duration,
            silence_periods=silence_periods,
            estimated_output_duration=estimated_output,
            silence_reduction_percent=reduction_percent,
            transcript_segments=transcript_segments
        )

    def process_video(self, input_path: str, output_path: str) -> str:
        """Process video file by removing silence periods"""
        input_path = Path(input_path)
        output_path = Path(output_path)

        if self.verbose:
            print(f"Processing video: {input_path} -> {output_path}")

        # Extract audio for analysis
        audio_processor = AudioProcessor(self._temp_dir, self.config, self.verbose)
        audio_path = audio_processor.extract_audio(str(input_path))

        # Detect silence periods using intelligent speech detection
        silence_periods = audio_processor.detect_silence(audio_path)

        # Get transcript for advanced processing if needed
        transcript_segments = audio_processor.transcribe_audio(audio_path)

        if not silence_periods:
            if self.verbose:
                print("No silence periods detected, copying original file")

            # No silence to remove, just copy the file
            shutil.copy2(input_path, output_path)
            return str(output_path)

        # Extract speech segments using video processor
        video_processor = VideoSegmentProcessor(self._temp_dir, self.config, self.verbose)
        speech_segments = video_processor.extract_speech_segments(input_path, silence_periods)

        if not speech_segments:
            if self.verbose:
                print("No speech segments found, copying original file")
            shutil.copy2(input_path, output_path)
            return str(output_path)

        # Create output video by concatenating speech segments
        return video_processor.create_output_video(input_path, output_path, speech_segments)
