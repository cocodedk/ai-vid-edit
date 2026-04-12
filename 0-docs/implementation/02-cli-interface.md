# Command-Line Interface

The system provides a command-line interface built with Click that allows users to process podcast videos directly from the terminal.

## Available Commands

**Main Entry Point** (`cli_main.py`):
- Provides the main CLI group with version information
- Registers all available commands
- Handles environment variable loading

**Process Command** (`commands/process.py`):
- Main command for processing video files
- Takes an input video file path as required argument
- Supports optional output path specification
- Allows configuration file override
- Provides options for Whisper model selection, language selection, silence threshold, and minimum silence duration
- Uses the `VideoProcessor` class to handle the actual processing
- Shows progress and results to the user

**Preview Command** (`commands/preview.py`):
- Allows users to preview what would be removed before processing
- Shows analysis results including total duration and estimated output length
- Helps users understand the impact of different settings

**Configure Command** (`commands/configure.py`):
- Helps users create and modify configuration files
- Guides through setting up processing parameters
- Saves settings for reuse in future processing jobs

## Key Features

- **Flexible Input/Output**: Supports custom input and output file paths
- **Configuration Management**: Can use config files or command-line overrides
- **Progress Feedback**: Shows what's happening during processing
- **Error Handling**: Clear error messages and optional verbose output for debugging
- **Model Selection**: Choose from different Whisper AI model sizes based on accuracy needs vs speed
- **Language Support**: Automatic language detection or manual language selection for international content

## Usage Flow

1. User runs the process command with a video file
2. System loads configuration (from file or defaults)
3. Configuration is overridden by command-line options if provided
4. VideoProcessor performs Whisper AI transcription for intelligent analysis
5. AudioProcessor uses transcript data to identify gaps between actual speech
6. VideoSegmentProcessor extracts precise speech segments based on word-level timing
7. System creates output preserving ambient audio while removing true silence
8. User receives the intelligently processed video file with transcript data
