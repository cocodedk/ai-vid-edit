"""
Configuration management functionality
"""

import json
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..config import Config


class ConfigManager:
    """Handles configuration loading, saving, and validation"""

    @staticmethod
    def from_file(config_path: str):
        """Load configuration from JSON file"""
        from ..config import Config

        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return ConfigManager.from_dict(data)

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """Create configuration from dictionary"""
        from ..config import Config

        config = Config()

        # Update whisper config
        if "whisper" in data:
            for key, value in data["whisper"].items():
                if hasattr(config.whisper, key):
                    setattr(config.whisper, key, value)

        # Update silence detection config
        if "silence_detection" in data:
            for key, value in data["silence_detection"].items():
                if hasattr(config.silence_detection, key):
                    setattr(config.silence_detection, key, value)

        # Update transitions config
        if "transitions" in data:
            for key, value in data["transitions"].items():
                if hasattr(config.transitions, key):
                    setattr(config.transitions, key, value)

        # Update output config
        if "output" in data:
            for key, value in data["output"].items():
                if hasattr(config.output, key):
                    setattr(config.output, key, value)

        return config

    @staticmethod
    def to_dict(config) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "whisper": {
                "model": config.whisper.model,
                "language": config.whisper.language,
                "device": config.whisper.device,
            },
            "silence_detection": {
                "threshold_db": config.silence_detection.threshold_db,
                "min_duration_ms": config.silence_detection.min_duration_ms,
            },
            "transitions": {
                "type": config.transitions.type,
                "duration_ms": config.transitions.duration_ms,
            },
            "output": {
                "format": config.output.format,
                "quality": config.output.quality,
                "include_intro": config.output.include_intro,
                "include_outro": config.output.include_outro,
            }
        }

    @staticmethod
    def save(config, config_path: str) -> None:
        """Save configuration to JSON file"""
        path = Path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(ConfigManager.to_dict(config), f, indent=2)

    @staticmethod
    def validate(config) -> None:
        """Validate configuration values"""
        if config.whisper.model not in ["tiny", "base", "small", "medium", "large"]:
            raise ValueError(f"Invalid whisper model: {config.whisper.model}")

        if not -60 <= config.silence_detection.threshold_db <= 0:
            raise ValueError(f"Invalid silence threshold: {config.silence_detection.threshold_db}")

        if config.silence_detection.min_duration_ms < 100:
            raise ValueError(f"Minimum silence duration too small: {config.silence_detection.min_duration_ms}")

        if config.transitions.duration_ms < 0:
            raise ValueError(f"Invalid transition duration: {config.transitions.duration_ms}")

        if config.output.format not in ["mp4", "mov", "avi", "mkv"]:
            raise ValueError(f"Unsupported output format: {config.output.format}")
