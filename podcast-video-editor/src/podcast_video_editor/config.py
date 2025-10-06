"""
Configuration management for Podcast Video Editor

This module provides the main Config class that uses the config package modules.
"""

# Import the main Config class from the config package
from .config import Config

# Also export individual config components for convenience
from .config import (
    WhisperConfig,
    SilenceDetectionConfig,
    TransitionsConfig,
    OutputConfig
)

__all__ = [
    "Config",
    "WhisperConfig",
    "SilenceDetectionConfig",
    "TransitionsConfig",
    "OutputConfig"
]
