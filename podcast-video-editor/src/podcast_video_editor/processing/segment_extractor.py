"""
Video segment extraction functionality
"""

import os
from pathlib import Path
from typing import List, Tuple

import ffmpeg


class SegmentExtractor:
    """Extracts video segments from input file"""

    def __init__(self, temp_dir: str, config, verbose: bool = False):
        self.temp_dir = temp_dir
        self.config = config
        self.verbose = verbose

    def extract_segments(self, input_path: Path, segments: List[Tuple[float, float]]) -> List[str]:
        """Extract video segments and return temporary file paths"""
        temp_files = []

        for i, (start, end) in enumerate(segments):
            temp_file = os.path.join(self.temp_dir, f"segment_{i:03d}.mp4")

            # Extract segment
            try:
                stream = ffmpeg.input(str(input_path))
                stream = ffmpeg.output(
                    stream,
                    temp_file,
                    ss=start,
                    t=end-start,
                    vcodec='copy',
                    acodec='copy'
                )
                ffmpeg.run(stream, overwrite_output=True, quiet=not self.verbose)
                temp_files.append(temp_file)
            except ffmpeg.Error as e:
                if self.verbose:
                    print(f"Warning: Failed to extract segment {i}: {e}")
                continue

        return temp_files
