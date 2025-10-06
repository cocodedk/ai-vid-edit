# Podcast Video Editor

An AI-powered video editing platform that automatically transforms raw podcast recordings into polished, professional videos through intelligent silence removal, transcript-based editing, and automated post-production.

## Features

- **AI-powered Speech Transcription**: Uses Whisper AI for accurate speech-to-text transcription with word-level timestamps
- **Smart Silence Detection**: Identifies and removes silent periods between speech segments
- **Automated Video Processing**: Complete workflow from raw recording to polished video
- **Configurable Settings**: Adjustable silence thresholds and processing parameters
- **Multiple Output Formats**: Support for MP4, MOV, AVI formats
- **Progress Reporting**: Real-time processing status and time estimates

## Installation

### Using uv (recommended)

```bash
# Navigate to the project directory
cd podcast-video-editor

# Install dependencies
uv sync

# Install the CLI tool
uv tool install --editable .
```

### Using pip

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Usage

### Command Line Interface

#### Process a Video

```bash
# Basic processing
podcast-editor process input_video.mp4

# With custom output location
podcast-editor process input_video.mp4 --output edited_video.mp4

# With custom settings
podcast-editor process input_video.mp4 \
    --whisper-model medium \
    --silence-threshold -35 \
    --min-silence-duration 0.8
```

#### Preview Processing Results

```bash
# Preview without processing
podcast-editor preview input_video.mp4

# Preview with custom config
podcast-editor preview input_video.mp4 --config custom_config.json
```

#### Configuration

```bash
# Create default configuration file
podcast-editor configure

# Create custom configuration file
podcast-editor configure --config-file my_config.json
```

### Configuration File

The configuration file (`.podcast-editor.json`) allows you to customize processing parameters:

```json
{
  "whisper": {
    "model": "base",
    "language": "en",
    "device": "auto"
  },
  "silence_detection": {
    "threshold_db": -40.0,
    "min_duration_ms": 500
  },
  "transitions": {
    "type": "crossfade",
    "duration_ms": 500
  },
  "output": {
    "format": "mp4",
    "quality": "high",
    "include_intro": true,
    "include_outro": true
  }
}
```

### Command Line Options

#### Process Command

- `--output, -o`: Output video file path
- `--config, -c`: Configuration file path
- `--whisper-model`: Whisper model size (tiny, base, small, medium, large)
- `--silence-threshold`: Silence detection threshold in dB (default: -40.0)
- `--min-silence-duration`: Minimum silence duration in seconds (default: 0.5)
- `--verbose, -v`: Enable verbose output

#### Preview Command

- `--config, -c`: Configuration file path
- `--whisper-model`: Whisper model size
- `--verbose, -v`: Enable verbose output

## Supported Input Formats

- MP4 (recommended)
- MOV
- AVI
- MKV

## Processing Pipeline

1. **Input Analysis**: Examine video file properties and validate format
2. **Audio Extraction**: Isolate audio track for processing
3. **Silence Detection**: Identify gaps between speech segments using configurable thresholds
4. **Video Cutting**: Remove silence segments while preserving speech content
5. **Final Assembly**: Combine edited segments into polished output video

## Quality Requirements

- **Transcription Accuracy**: >95% word recognition rate
- **Silence Detection**: <100ms precision for cut points
- **Video Quality**: Maintain original resolution and bitrate
- **Processing Speed**: Complete editing within 2x video duration

## Development

### Project Structure

```
podcast-video-editor/
├── src/podcast_video_editor/
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Command-line interface
│   ├── config.py            # Configuration management
│   └── processor.py         # Video processing engine
├── .podcast-editor.json     # Default configuration
└── README.md                # This file
```

### Adding New Features

The codebase follows SOLID principles and is designed for extensibility:

1. **Configuration**: Add new settings in `config.py`
2. **Processing**: Extend `VideoProcessor` class in `processor.py`
3. **CLI**: Add new commands or options in `cli.py`

### Testing

```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=podcast_video_editor

# Run linting
black src/
isort src/
mypy src/
```

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: Ensure FFmpeg is installed and available in PATH
2. **Permission denied**: Check file permissions for input/output paths
3. **Out of memory**: Use smaller Whisper models for large files
4. **Poor silence detection**: Adjust threshold values in configuration

### Debug Mode

Use the `--verbose` flag to enable detailed logging:

```bash
podcast-editor process video.mp4 --verbose
```

## Roadmap

- **Phase 1 (Current)**: CLI tool with core functionality ✅
- **Phase 2**: Flask web application with upload/processing
- **Phase 3**: Advanced web platform with collaborative features
- **Phase 4**: Android mobile application

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues and questions, please open an issue on the project repository.
