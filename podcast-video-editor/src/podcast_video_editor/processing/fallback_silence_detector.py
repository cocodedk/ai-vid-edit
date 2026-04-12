"""
Fallback silence detection using audio analysis
"""

from typing import List

import ffmpeg
import numpy as np

from .models import SilencePeriod


class FallbackSilenceDetector:
    """Fallback silence detection using volume analysis"""

    def __init__(self, config, verbose: bool = False):
        self.config = config
        self.verbose = verbose

    def detect_silence(self, audio_path: str) -> List[SilencePeriod]:
        """Detect silence using volume-based analysis"""
        try:
            # Read audio data (simplified - would need proper audio processing)
            stream = ffmpeg.input(audio_path)
            stream = ffmpeg.output(stream, 'pipe:', format='s16le', ar=16000, ac=1)
            out, _ = ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)

            # Convert to numpy array (simplified)
            audio_data = np.frombuffer(out, np.int16).astype(np.float32) / 32768.0

            # Simple volume-based silence detection
            threshold = 10 ** (self.config.silence_detection.threshold_db / 20)  # Convert dB to linear

            # Find periods where volume is below threshold for minimum duration
            silence_periods = []
            current_start = None

            for i in range(0, len(audio_data), 1600):  # Process in 100ms chunks
                chunk = audio_data[i:i+1600]
                if len(chunk) == 0:
                    break

                volume = np.sqrt(np.mean(chunk ** 2))

                if volume < threshold:
                    if current_start is None:
                        current_start = i / 16000  # Convert to seconds
                else:
                    if current_start is not None:
                        duration = (i / 16000) - current_start
                        if duration >= self.config.silence_detection.min_duration_ms / 1000:
                            silence_periods.append(SilencePeriod(
                                start_time=current_start,
                                end_time=i / 16000,
                                duration=duration
                            ))
                        current_start = None

            # Handle case where file ends with silence
            if current_start is not None:
                duration = (len(audio_data) / 16000) - current_start
                if duration >= self.config.silence_detection.min_duration_ms / 1000:
                    silence_periods.append(SilencePeriod(
                        start_time=current_start,
                        end_time=len(audio_data) / 16000,
                        duration=duration
                    ))

            return silence_periods

        except Exception as e:
            if self.verbose:
                print(f"Fallback silence detection failed: {e}")
            return []
