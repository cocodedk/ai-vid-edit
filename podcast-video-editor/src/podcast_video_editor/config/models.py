"""
Configuration data models
"""

from dataclasses import dataclass, field


@dataclass
class WhisperConfig:
    """Whisper AI configuration"""
    model: str = "base"
    language: str = "en"
    device: str = "auto"


@dataclass
class SilenceDetectionConfig:
    """Silence detection configuration"""
    threshold_db: float = -40.0
    min_duration_ms: int = 500


@dataclass
class TransitionsConfig:
    """Video transitions configuration"""
    type: str = "crossfade"
    duration_ms: int = 500


@dataclass
class OutputConfig:
    """Output configuration"""
    format: str = "mp4"
    quality: str = "high"
    include_intro: bool = True
    include_outro: bool = True
