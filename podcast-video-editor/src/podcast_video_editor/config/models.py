"""
Configuration data models
"""

from dataclasses import dataclass, field


@dataclass
class WhisperConfig:
    """Whisper AI configuration"""
    model: str = "base"
    language: str = None  # None for auto-detection, or specific language code (e.g., "en", "es", "fr")
    device: str = "auto"
    supported_languages: list = None  # List of supported language codes

    def __post_init__(self):
        if self.supported_languages is None:
            # Common languages supported by Whisper
            self.supported_languages = [
                "en", "zh", "de", "es", "ru", "ko", "fr", "ja", "pt", "tr",
                "pl", "ca", "nl", "ar", "sv", "it", "id", "hi", "fi", "vi",
                "he", "uk", "el", "ms", "cs", "ro", "da", "hu", "ta", "no",
                "th", "ur", "hr", "bg", "lt", "la", "mi", "ml", "cy", "sk",
                "te", "fa", "lv", "bn", "sr", "az", "sl", "kn", "et", "mk",
                "br", "eu", "is", "hy", "ne", "mn", "bs", "kk", "sq", "sw",
                "gl", "mr", "pa", "si", "km", "sn", "yo", "so", "af", "oc",
                "ka", "be", "tg", "sd", "gu", "am", "yi", "lo", "uz", "fo",
                "ht", "ps", "tk", "nn", "mt", "sa", "lb", "my", "bo", "tl",
                "mg", "as", "tt", "haw", "ln", "ha", "ba", "jw", "su"
            ]


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
