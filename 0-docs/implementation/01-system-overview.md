# System Overview

The Podcast Video Editor is an AI-powered platform that uses Whisper AI transcription to intelligently identify and remove silence from podcast videos. By analyzing actual speech content rather than just audio volume, it preserves ambient sounds while removing true silence between spoken words. The system provides both a command-line interface and a web-based interface for easy access.

## Main Components

**CLI Interface** (`cli_main.py`):
- Entry point for command-line usage
- Provides commands for processing, preview, and configuration
- Uses the Click library for command handling

**Web Interface** (`web_app/`):
- Flask-based web application
- Allows users to upload videos through a browser
- Processes videos in the background and provides download links

**Core Processing Engine** (`VideoProcessor`):
- Main class that coordinates video processing
- Handles video analysis and silence removal
- Uses temporary directories for intermediate files

**Audio Processing** (`AudioProcessor`):
- Extracts audio from video files using FFmpeg
- Uses Whisper AI for intelligent speech-to-text transcription with word-level timestamps
- Intelligently detects silence as gaps between actual speech segments
- Distinguishes between true silence and ambient background noise

**Video Segment Processing** (`VideoSegmentProcessor`):
- Extracts precise speech segments based on Whisper transcript timing
- Creates final output by concatenating only segments containing actual speech
- Preserves ambient audio while removing true silence periods
- Leverages transcript data for content-aware editing decisions

**Configuration System** (`Config` class):
- Manages all processing settings
- Supports configuration files and command-line overrides
- Includes models for Whisper AI, silence detection, and output settings
