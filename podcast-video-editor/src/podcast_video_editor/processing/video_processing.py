"""
Video processing functionality
"""

import os
from pathlib import Path
from typing import List, Tuple

import ffmpeg

from .models import SilencePeriod
from .segment_extractor import SegmentExtractor
from .video_concatenator import VideoConcatenator


class VideoProcessor:
    """Handles video cutting and concatenation"""

    def __init__(self, temp_dir: str, config, verbose: bool = False):
        self.temp_dir = temp_dir
        self.config = config
        self.verbose = verbose
        self.segment_extractor = SegmentExtractor(temp_dir, config, verbose)
        self.video_concatenator = VideoConcatenator(temp_dir, config, verbose)

    def get_video_duration(self, video_path: Path) -> float:
        """Get duration of video file"""
        try:
            probe = ffmpeg.probe(str(video_path))
            return float(probe['format']['duration'])
        except Exception:
            return 0.0

    def extract_speech_segments(self, input_path: Path, silence_periods: List[SilencePeriod]) -> List[Tuple[float, float]]:
        """Generate speech segments from silence periods"""
        # Generate cut segments (keep speech parts)
        speech_segments = []
        prev_end = 0.0

        for silence in silence_periods:
            if silence.start_time > prev_end:
                speech_segments.append((prev_end, silence.start_time))
            prev_end = silence.end_time

        # Add final segment if there's speech after last silence
        if prev_end < self.get_video_duration(input_path):
            try:
                probe = ffmpeg.probe(str(input_path))
                total_duration = float(probe['format']['duration'])
                if prev_end < total_duration:
                    speech_segments.append((prev_end, total_duration))
            except Exception:
                pass

        return speech_segments

    def create_output_video(self, input_path: Path, output_path: Path, segments: List[Tuple[float, float]]) -> str:
        """Create output video from speech segments"""
        if self.verbose:
            print(f"Creating output video with {len(segments)} segments")

        # Extract segments
        temp_files = self.segment_extractor.extract_segments(input_path, segments)

        if not temp_files:
            raise RuntimeError("No segments could be extracted")

        # Concatenate segments
        return self.video_concatenator.concatenate_segments(temp_files, output_path)
