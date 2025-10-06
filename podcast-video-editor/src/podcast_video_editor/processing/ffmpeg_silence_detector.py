"""
FFmpeg-based silence detection
"""

import subprocess
from typing import List

import ffmpeg

from .models import SilencePeriod


class FFMpegSilenceDetector:
    """Detects silence using FFmpeg silencedetect filter"""

    def __init__(self, config, verbose: bool = False):
        self.config = config
        self.verbose = verbose

    def detect_silence(self, audio_path: str) -> List[SilencePeriod]:
        """Detect silence periods using FFmpeg"""
        # Read audio file
        try:
            audio = ffmpeg.probe(audio_path)
            duration = float(audio['streams'][0]['duration'])
        except Exception as e:
            raise RuntimeError(f"Failed to probe audio file: {e}")

        # Use ffmpeg silencedetect filter
        output = subprocess.run([
            'ffmpeg', '-i', audio_path,
            '-af', f'silencedetect=noise={self.config.silence_detection.threshold_db}dB:d={self.config.silence_detection.min_duration_ms/1000}',
            '-f', 'null', '-'
        ], capture_output=True, text=True, check=True)

        # Parse output for silence periods
        lines = output.stderr.split('\n')
        current_silence = None
        silence_periods = []

        for line in lines:
            if 'silence_start' in line:
                # Start of silence period
                start_time = float(line.split('silence_start: ')[1])
                current_silence = {'start': start_time}
            elif 'silence_end' in line and current_silence:
                # End of silence period
                end_time = float(line.split('silence_end: ')[1].split(' ')[0])
                duration = end_time - current_silence['start']

                if duration >= self.config.silence_detection.min_duration_ms / 1000:
                    silence_periods.append(SilencePeriod(
                        start_time=current_silence['start'],
                        end_time=end_time,
                        duration=duration
                    ))

                current_silence = None

        return silence_periods
