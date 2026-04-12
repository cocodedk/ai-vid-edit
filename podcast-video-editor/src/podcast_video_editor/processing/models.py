"""
Data models for video processing
"""

from dataclasses import dataclass
from typing import List


@dataclass
class SilencePeriod:
    """Represents a period of silence in the audio"""
    start_time: float  # Start time in seconds
    end_time: float    # End time in seconds
    duration: float    # Duration in seconds


@dataclass
class TranscriptSegment:
    """Represents a segment of transcribed speech"""
    start_time: float  # Start time in seconds
    end_time: float    # End time in seconds
    text: str         # Transcribed text
    confidence: float # Whisper confidence score


@dataclass
class VideoAnalysis:
    """Results of video analysis"""
    duration: float
    silence_periods: List[SilencePeriod]
    estimated_output_duration: float
    silence_reduction_percent: float
    transcript_segments: List[TranscriptSegment] = None  # Add transcript data
