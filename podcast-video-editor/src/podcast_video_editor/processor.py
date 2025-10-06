"""
Main video processing engine for Podcast Video Editor
"""

import os
import shutil
import tempfile
from pathlib import Path

import ffmpeg

from .config import Config
from .processing import AudioProcessor, VideoAnalysis, VideoSegmentProcessor


class VideoProcessor:
    """Main video processing engine"""

    def __init__(self, config: Config, verbose: bool = False):
        self.config = config
        self.verbose = verbose
        self._temp_dir = None

    def __enter__(self):
        self._temp_dir = tempfile.mkdtemp()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._temp_dir and os.path.exists(self._temp_dir):
            shutil.rmtree(self._temp_dir)

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

        # Detect silence periods
        silence_periods = audio_processor.detect_silence(audio_path)

        # Calculate total silence duration
        total_silence = sum(period.duration for period in silence_periods)
        estimated_output = duration - total_silence

        # Calculate reduction percentage
        reduction_percent = (total_silence / duration) * 100 if duration > 0 else 0

        return VideoAnalysis(
            duration=duration,
            silence_periods=silence_periods,
            estimated_output_duration=estimated_output,
            silence_reduction_percent=reduction_percent
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

        # Detect silence periods
        silence_periods = audio_processor.detect_silence(audio_path)

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
