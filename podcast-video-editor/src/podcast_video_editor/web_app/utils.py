"""
Utility functions for the web application
"""

from pathlib import Path


def allowed_file(filename: str) -> bool:
    """Check if file type is allowed"""
    allowed_extensions = {'.mp4', '.mov', '.avi', '.mkv'}
    return Path(filename).suffix.lower() in allowed_extensions
