"""
Audio processing functionality
"""

import os
import subprocess
from pathlib import Path
from typing import List

import ffmpeg

from .models import SilencePeriod
from .silence_detection import SilenceDetector


class AudioProcessor:
    """Handles audio extraction and silence detection"""

    def __init__(self, temp_dir: str, config, verbose: bool = False):
        self.temp_dir = temp_dir
        self.config = config
        self.verbose = verbose
        self.silence_detector = SilenceDetector(config, verbose)

    def extract_audio(self, video_path: str) -> str:
        """Extract audio from video file"""
        video_path = Path(video_path)

        if self.verbose:
            print(f"Extracting audio from: {video_path}")

        # Create output audio file in temp directory
        audio_path = os.path.join(self.temp_dir, f"{video_path.stem}_audio.wav")

        try:
            # Use ffmpeg to extract audio
            stream = ffmpeg.input(str(video_path))
            stream = ffmpeg.output(stream, audio_path, acodec='pcm_s16le', ar=16000)
            ffmpeg.run(stream, overwrite_output=True, quiet=not self.verbose)
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to extract audio: {e}")

        return audio_path

    def detect_silence(self, audio_path: str) -> List[SilencePeriod]:
        """Detect silence periods in audio file"""
        return self.silence_detector.detect_silence(audio_path)
