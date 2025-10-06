"""
Audio processing functionality
"""

import os
import subprocess
from pathlib import Path
from typing import List

import ffmpeg
import whisper
import torch

from .models import SilencePeriod, TranscriptSegment
from .silence_detection import SilenceDetector


class AudioProcessor:
    """Handles audio extraction, transcription, and intelligent silence detection"""

    def __init__(self, temp_dir: str, config, verbose: bool = False):
        self.temp_dir = temp_dir
        self.config = config
        self.verbose = verbose
        self.silence_detector = SilenceDetector(config, verbose)
        self.whisper_model = None

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

    def _load_whisper_model(self):
        """Load Whisper model if not already loaded"""
        if self.whisper_model is None:
            if self.verbose:
                print(f"Loading Whisper model: {self.config.whisper.model}")

            # Use CUDA if available, otherwise CPU
            device = self.config.whisper.device
            if device == "auto":
                device = "cuda" if torch.cuda.is_available() else "cpu"

            self.whisper_model = whisper.load_model(
                self.config.whisper.model,
                device=device
            )

    def _detect_language(self, audio_path: str) -> str:
        """Detect the primary language in the audio file"""
        if self.verbose:
            print("Detecting audio language...")

        try:
            # Use Whisper to detect language without full transcription
            result = self.whisper_model.transcribe(
                audio_path,
                task="transcribe",  # Just for language detection
                verbose=False  # Don't show verbose output for detection
            )

            detected_language = result.get("language")
            if detected_language and detected_language in self.config.whisper.supported_languages:
                if self.verbose:
                    print(f"Detected language: {detected_language}")
                return detected_language
            else:
                if self.verbose:
                    print(f"Language detection uncertain, defaulting to English")
                return "en"

        except Exception as e:
            if self.verbose:
                print(f"Language detection failed: {e}, defaulting to English")
            return "en"

    def transcribe_audio(self, audio_path: str) -> List[TranscriptSegment]:
        """Transcribe audio using Whisper AI with automatic language detection"""
        self._load_whisper_model()

        if self.verbose:
            print(f"Transcribing audio: {audio_path}")

        # Determine language for transcription
        transcription_language = self.config.whisper.language
        if transcription_language is None:
            # Auto-detect language
            transcription_language = self._detect_language(audio_path)

        if self.verbose and transcription_language != "en":
            print(f"Using language: {transcription_language}")

        try:
            # Transcribe with word-level timestamps for precise sentence boundaries
            result = self.whisper_model.transcribe(
                audio_path,
                language=transcription_language,
                verbose=self.verbose,
                word_timestamps=True  # Enable word-level timestamps
            )

            # Convert Whisper segments to our format with precise timing
            transcript_segments = []
            for segment in result["segments"]:
                # Use word-level timestamps if available for better precision
                words = segment.get("words", [])
                if words:
                    # Create segments for each word with precise timing
                    for word in words:
                        transcript_segments.append(TranscriptSegment(
                            start_time=word["start"],
                            end_time=word["end"],
                            text=word["word"].strip(),
                            confidence=1.0  # Word-level doesn't have confidence in basic Whisper
                        ))
                else:
                    # Fallback to segment-level if word timestamps not available
                    transcript_segments.append(TranscriptSegment(
                        start_time=segment["start"],
                        end_time=segment["end"],
                        text=segment["text"].strip(),
                        confidence=segment.get("confidence", 1.0)
                    ))

            return transcript_segments

        except Exception as e:
            if self.verbose:
                print(f"Whisper transcription failed: {e}")
            return []

    def detect_speech_silence(self, audio_path: str) -> List[SilencePeriod]:
        """Detect silence periods based on speech transcription (intelligent detection)"""
        transcript_segments = self.transcribe_audio(audio_path)

        if not transcript_segments:
            if self.verbose:
                print("No speech detected, falling back to volume-based detection")
            return self.silence_detector.detect_silence(audio_path)

        # Convert transcript segments to silence periods (gaps between speech)
        silence_periods = []

        # Add silence at the beginning if there's a gap
        if transcript_segments[0].start_time > 0:
            silence_periods.append(SilencePeriod(
                start_time=0,
                end_time=transcript_segments[0].start_time,
                duration=transcript_segments[0].start_time
            ))

        # Add silences between speech segments
        for i in range(len(transcript_segments) - 1):
            current_end = transcript_segments[i].end_time
            next_start = transcript_segments[i + 1].start_time

            if next_start - current_end > 0.1:  # Only add if gap > 100ms
                silence_periods.append(SilencePeriod(
                    start_time=current_end,
                    end_time=next_start,
                    duration=next_start - current_end
                ))

        # Add silence at the end if there's a gap
        if transcript_segments:
            last_segment = transcript_segments[-1]
            try:
                # Get audio duration
                probe = ffmpeg.probe(audio_path)
                total_duration = float(probe['streams'][0]['duration'])
            except:
                total_duration = last_segment.end_time + 1  # Fallback

            if total_duration - last_segment.end_time > 0.1:
                silence_periods.append(SilencePeriod(
                    start_time=last_segment.end_time,
                    end_time=total_duration,
                    duration=total_duration - last_segment.end_time
                ))

        return silence_periods

    def detect_silence(self, audio_path: str) -> List[SilencePeriod]:
        """Detect silence periods in audio file using intelligent speech detection"""
        return self.detect_speech_silence(audio_path)
