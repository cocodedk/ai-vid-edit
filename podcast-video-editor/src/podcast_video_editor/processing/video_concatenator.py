"""
Video concatenation functionality
"""

import os
from pathlib import Path

import ffmpeg


class VideoConcatenator:
    """Concatenates video segments into output file"""

    def __init__(self, temp_dir: str, config, verbose: bool = False):
        self.temp_dir = temp_dir
        self.config = config
        self.verbose = verbose

    def concatenate_segments(self, temp_files: list, output_path: Path) -> str:
        """Concatenate video segments into output file"""
        if not temp_files:
            raise RuntimeError("No segments to concatenate")

        # Create file list for concatenation
        concat_file = os.path.join(self.temp_dir, "concat_list.txt")
        with open(concat_file, 'w') as f:
            for temp_file in temp_files:
                f.write(f"file '{temp_file}'\n")

        # Concatenate segments
        try:
            stream = ffmpeg.input(concat_file, format='concat', safe=0)
            stream = ffmpeg.output(stream, str(output_path), c='copy')
            ffmpeg.run(stream, overwrite_output=True, quiet=not self.verbose)
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to concatenate segments: {e}")

        # Clean up temporary files
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except OSError:
                pass

        try:
            os.remove(concat_file)
        except OSError:
            pass

        return str(output_path)
