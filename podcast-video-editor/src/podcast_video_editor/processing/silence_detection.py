"""
Silence detection functionality
"""

from typing import List

from .models import SilencePeriod
from .ffmpeg_silence_detector import FFMpegSilenceDetector
from .fallback_silence_detector import FallbackSilenceDetector


class SilenceDetector:
    """Detects silence periods in audio files"""

    def __init__(self, config, verbose: bool = False):
        self.config = config
        self.verbose = verbose
        self.ffmpeg_detector = FFMpegSilenceDetector(config, verbose)
        self.fallback_detector = FallbackSilenceDetector(config, verbose)

    def detect_silence(self, audio_path: str) -> List[SilencePeriod]:
        """Detect silence periods in audio file"""
        if self.verbose:
            print("Detecting silence periods...")

        # Try FFmpeg silence detection first
        try:
            return self.ffmpeg_detector.detect_silence(audio_path)
        except Exception:
            if self.verbose:
                print("FFmpeg detection failed, using fallback method")

        # Fallback to volume-based analysis
        return self.fallback_detector.detect_silence(audio_path)
