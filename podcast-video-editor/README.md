# Podcast Video Editor

An AI-powered video editing platform that automatically transforms raw podcast recordings into polished, professional videos through intelligent silence removal, transcript-based editing, and automated post-production.

## 🚀 Quick Start

### For Beginners (5-minute setup)

1. **Install the tool:**
   ```bash
   cd podcast-video-editor
   uv sync && uv tool install --editable .
   ```

2. **Process your first video:**
   ```bash
   podcast-editor process my_podcast.mp4
   ```

3. **Your edited video and run artifacts will be saved in a unique folder at** `processed/my_podcast_<timestamp>_<id>/`

> 💡 Every run gets its own timestamped directory so that temporary files, logs, and the final render all stay grouped together. Set `PODCAST_EDITOR_RUNS_DIR=/custom/path` if you want to aggregate runs elsewhere.

That's it! The AI will automatically remove silences and create a polished video.

## ✨ Features

- **AI-powered Speech Transcription**: Uses Whisper AI for accurate speech-to-text transcription with word-level timestamps
- **Smart Silence Detection**: Identifies and removes silent periods between speech segments
- **Automated Video Processing**: Complete workflow from raw recording to polished video
- **Configurable Settings**: Adjustable silence thresholds and processing parameters
- **Multiple Output Formats**: Support for MP4, MOV, AVI formats
- **Progress Reporting**: Real-time processing status and time estimates
- **Web Interface**: Upload and process videos through a user-friendly web app
- **CLI & GUI**: Choose between command-line efficiency or visual interface
- **Adaptive Diagnostics**: Wizard can scan your file and hardware to suggest optimal processing defaults

## 📦 Installation

### Option 1: Using uv (recommended)

```bash
# Navigate to the project directory
cd podcast-video-editor

# Install dependencies
uv sync

# Install the CLI tool
uv tool install --editable .
```

### Option 2: Using pip

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

## 🎯 Usage Guide

### Method 1: Command Line Interface (Fast & Scriptable)

#### Basic Video Processing

```bash
# Simple processing (removes silences automatically)
podcast-editor process my_podcast.mp4

# Specify output file name (stored inside the run folder)
podcast-editor process input.mp4 --output polished_podcast.mp4

# Use higher quality transcription (takes longer but more accurate)
podcast-editor process input.mp4 --whisper-model medium
```

#### Advanced Configuration

```bash
# Fine-tune silence detection
podcast-editor process input.mp4 \
    --silence-threshold -35 \        # Lower = more sensitive (default: -40)
    --min-silence-duration 0.8 \     # Minimum silence to remove in seconds
    --whisper-model small            # Model size: tiny/base/small/medium/large
```

#### Preview Before Processing

```bash
# See what silences will be removed without processing
podcast-editor preview my_podcast.mp4

# Preview with your custom settings
podcast-editor preview input.mp4 --config my_settings.json
```

### Diagnostic Recommendations

When you run the interactive wizard (`./ai-video-editor.sh`), you can launch a diagnostic scan right after selecting your video. The tool inspects duration, file size, and GPU availability to recommend:

- The most suitable Whisper model for the workload
- Whether to stick with CPU or enable GPU acceleration
- Baseline silence detection thresholds tailored to clip length

Those suggestions feed into later prompts—for example, choosing the *Balanced* quality option will adopt the diagnostic model automatically, and the GPU prompt highlights the recommended device.

### Method 2: Web Interface (User-Friendly)

1. **Start the web application:**
   ```bash
   # From the podcast-video-editor directory
   python -m podcast_video_editor.web
   ```

2. **Open your browser** to `http://127.0.0.1:5000`

3. **Upload your video** using the web interface

4. **Configure settings** with the visual controls

5. **Process and download** your edited video

#### Web App Features:
- Drag-and-drop file upload
- Real-time processing progress
- Visual configuration options
- Download processed videos directly

## ⚙️ Configuration

### Default Configuration File

Create a configuration file for your preferred settings:

```bash
# Generate default config
podcast-editor configure

# Create custom config file
podcast-editor configure --config-file my_podcast_settings.json
```

### Configuration Options

```json
{
  "whisper": {
    "model": "base",           // tiny, base, small, medium, large
    "language": "en",          // Language code (en, es, fr, etc.)
    "device": "auto"           // auto, cpu, cuda
  },
  "silence_detection": {
    "threshold_db": -40.0,     // Silence sensitivity (lower = more sensitive)
    "min_duration_ms": 500     // Minimum silence to remove (milliseconds)
  },
  "transitions": {
    "type": "crossfade",       // crossfade, fade, cut
    "duration_ms": 500         // Transition length
  },
  "output": {
    "format": "mp4",           // mp4, mov, avi
    "quality": "high",         // low, medium, high
    "include_intro": true,     // Keep intro before first speech
    "include_outro": true      // Keep outro after last speech
  }
}
```

## 📋 Command Reference

### Process Command Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--output, -o` | Output file name (stored in run folder) | `{input}_edited.mp4` | `--output final.mp4` |
| `--config, -c` | Configuration file path | `.podcast-editor.json` | `--config custom.json` |
| `--whisper-model` | AI model size | `base` | `--whisper-model medium` |
| `--silence-threshold` | Silence sensitivity (dB) | `-40.0` | `--silence-threshold -35` |
| `--min-silence-duration` | Min silence to remove (seconds) | `0.5` | `--min-silence-duration 0.8` |
| `--verbose, -v` | Detailed progress output | `false` | `--verbose` |

### Preview Command Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--config, -c` | Configuration file path | `.podcast-editor.json` | `--config preview.json` |
| `--whisper-model` | AI model size | `base` | `--whisper-model small` |
| `--device` | Processing device | `auto` | `--device cpu` |
| `--verbose, -v` | Detailed output | `false` | `--verbose` |

## 🎬 Real-World Examples

### Example 1: Podcast Interview (1 hour long)

```bash
# Process a long interview with strict silence removal
podcast-editor process interview.mp4 \
    --whisper-model medium \
    --silence-threshold -45 \
    --min-silence-duration 1.2 \
    --output interview_edited.mp4
```
*Result: Removes long pauses, keeps natural conversation flow*

### Example 2: Educational Content (30 minutes)

```bash
# Keep some breathing room for emphasis
podcast-editor process lecture.mp4 \
    --whisper-model small \
    --silence-threshold -35 \
    --min-silence-duration 0.6
```
*Result: Faster paced, removes distractions*

### Example 3: Noisy Recording (20 minutes)

```bash
# More sensitive to catch background noise as "silence"
podcast-editor process noisy_podcast.mp4 \
    --whisper-model large \
    --silence-threshold -50 \
    --min-silence-duration 0.3
```
*Result: Cleaner output despite poor audio quality*

## 📁 Supported Input Formats

| Format | Recommended | Notes |
|--------|-------------|-------|
| **MP4** | ✅ Best choice | Most compatible, widely supported |
| **MOV** | ✅ Good | Apple ecosystem standard |
| **AVI** | ⚠️ Works | Older format, larger file sizes |
| **MKV** | ⚠️ Works | Good quality but less common |

## 🔧 Processing Pipeline

1. **Input Analysis** - Validates video format and extracts metadata
2. **Audio Extraction** - Isolates audio track for AI processing
3. **Speech Transcription** - Whisper AI converts speech to text with timestamps
4. **Silence Detection** - Identifies gaps between speech segments
5. **Smart Cutting** - Removes silence while preserving speech content
6. **Final Assembly** - Combines edited segments with smooth transitions

## ⚡ Performance Tips

### Speed Optimization
- **Use smaller Whisper models** for faster processing (`tiny` or `base`)
- **Pre-process audio** to remove background noise if possible
- **Process shorter videos** in batches rather than one large file

### Quality Optimization
- **Use larger Whisper models** (`medium` or `large`) for better accuracy
- **Fine-tune silence thresholds** based on your audio quality
- **Test with preview mode** before processing long videos

## 🚨 Troubleshooting

### Common Issues & Solutions

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| **"FFmpeg not found"** | Missing system dependency | Install FFmpeg: `sudo apt install ffmpeg` (Ubuntu/Debian) or `brew install ffmpeg` (Mac) |
| **"Permission denied"** | File access issues | Check file permissions: `chmod 644 input.mp4` |
| **"Out of memory"** | Large video + big AI model | Use smaller Whisper model or process in segments |
| **"Poor silence detection"** | Wrong threshold settings | Start with `-40` dB threshold, adjust by ±5 dB |
| **"Processing hangs"** | Very long video | Use `--verbose` to monitor progress, consider splitting video |

### Getting Help

1. **Enable verbose mode** for detailed error messages:
   ```bash
   podcast-editor process video.mp4 --verbose
   ```

2. **Check the logs** in the console output

3. **Test with a short sample** before processing full videos

## 📈 Quality Standards

- **Transcription Accuracy**: >95% word recognition rate
- **Silence Detection**: <100ms precision for cut points
- **Video Quality**: Maintains original resolution and bitrate
- **Processing Speed**: Completes within 2x video duration
- **Output Size**: Typically 60-80% smaller than original

## 🛠️ Development

### Project Structure

```
podcast-video-editor/
├── src/podcast_video_editor/
│   ├── __init__.py              # Package initialization
│   ├── cli_main.py              # Main CLI entry point
│   ├── commands/                # CLI command implementations
│   │   ├── process.py           # Video processing command
│   │   ├── preview.py           # Preview command
│   │   └── configure.py         # Configuration command
│   ├── config/                  # Configuration management
│   │   ├── manager.py           # Config file handling
│   │   └── models.py            # Configuration data models
│   ├── processing/              # Core processing logic
│   │   ├── audio_processing.py  # Audio analysis and transcription
│   │   ├── silence_detection.py # Silence identification
│   │   └── video_processing.py  # Video editing operations
│   ├── web_app/                 # Flask web application
│   └── processor.py             # Main processing orchestrator
├── uploads/                     # Temporary upload directory
├── processed/                   # Output directory
└── README.md                    # This file
```

### Adding New Features

The codebase follows SOLID principles for easy extensibility:

1. **Configuration**: Add settings in `config/models.py`
2. **Processing**: Extend classes in `processing/` modules
3. **CLI**: Add commands in `commands/` directory
4. **Web**: Add routes in `web_app/routes.py`

## 🗺️ Roadmap

- **Phase 1 (Current)**: ✅ CLI tool with core functionality
- **Phase 2**: 🔄 Flask web application with upload/processing
- **Phase 3**: 📋 Advanced web platform with collaborative features
- **Phase 4**: 📱 Android mobile application

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

See [LICENSE](../LICENSE) file for details.

## 💬 Support

For issues and questions:
1. Check this README first
2. Review existing GitHub issues
3. Open a new issue with details about your problem

---

**Quick Reminder**: Start with the Quick Start section above - you can process your first video in under 5 minutes! 🎉
