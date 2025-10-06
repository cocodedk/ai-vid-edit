"""
Flask web application for Podcast Video Editor

This module provides the main web application entry point using the web_app package.
"""

# Import the main web application from the web_app package
from .web_app import VideoProcessingApp, create_app

__all__ = ["VideoProcessingApp", "create_app"]
