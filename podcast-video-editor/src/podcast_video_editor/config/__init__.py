"""
Configuration management modules
"""

from dataclasses import dataclass, field

from .models import WhisperConfig, SilenceDetectionConfig, TransitionsConfig, OutputConfig


@dataclass
class Config:
    """Main configuration class"""

    whisper: WhisperConfig = field(default_factory=WhisperConfig)
    silence_detection: SilenceDetectionConfig = field(default_factory=SilenceDetectionConfig)
    transitions: TransitionsConfig = field(default_factory=TransitionsConfig)
    output: OutputConfig = field(default_factory=OutputConfig)

    @classmethod
    def from_file(cls, config_path: str):
        """Load configuration from JSON file"""
        from .manager import ConfigManager
        return ConfigManager.from_file(config_path)

    @classmethod
    def from_dict(cls, data):
        """Create configuration from dictionary"""
        from .manager import ConfigManager
        return ConfigManager.from_dict(data)

    def to_dict(self):
        """Convert configuration to dictionary"""
        from .manager import ConfigManager
        return ConfigManager.to_dict(self)

    def save(self, config_path: str) -> None:
        """Save configuration to JSON file"""
        from .manager import ConfigManager
        ConfigManager.save(self, config_path)

    def validate(self) -> None:
        """Validate configuration values"""
        from .manager import ConfigManager
        ConfigManager.validate(self)


__all__ = ["Config", "WhisperConfig", "SilenceDetectionConfig", "TransitionsConfig", "OutputConfig"]
