# ai-vid-edit

AI-powered Python tool for editing podcast and interview videos with automatic scene detection, transcription, and intelligent video processing.

## Website

- [English](https://cocodedk.github.io/ai-vid-edit/)
- [فارسی (Persian)](https://cocodedk.github.io/ai-vid-edit/fa/)

## Download

[**Download ai-vid-edit**](https://github.com/cocodedk/ai-vid-edit/releases/latest/download/ai-vid-edit.zip)

## Features

- AI scene detection — Automatic identification of scene boundaries
- Transcription — AI-powered speech-to-text for podcasts
- Web UI — Flask-based interface for upload and processing
- CLI — Scriptable processing pipeline
- Batch processing — Handle multiple videos efficiently

## Build from Source

```bash
git clone https://github.com/cocodedk/ai-vid-edit.git
cd ai-vid-edit/podcast-video-editor
uv sync
uv run python -m podcast_video_editor --help
```

## Architecture

```
ai-vid-edit/
├── podcast-video-editor/
│   ├── src/podcast_video_editor/
│   │   ├── commands/    ← CLI commands
│   │   ├── config/      ← Configuration
│   │   ├── processing/  ← Video processing logic
│   │   └── web_app/     ← Flask web interface
│   └── helpers/         ← Shell helper scripts
```

| Component | Technology |
|-----------|-----------|
| Video processing | Python + FFmpeg |
| Web UI | Flask 3.0 |
| Package manager | uv |
| Language | Python 3.12 |

## Author

**Babak Bandpey** — [cocode.dk](https://cocode.dk) | [LinkedIn](https://linkedin.com/in/babakbandpey) | [GitHub](https://github.com/cocodedk)

## License

Apache-2.0 | © 2026 [Cocode](https://cocode.dk) | Created by [Babak Bandpey](https://linkedin.com/in/babakbandpey)
