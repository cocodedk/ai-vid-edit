# CLAUDE.md — ai-vid-edit

## Project Overview

ai-vid-edit (podcast-video-editor) is an AI-powered Python tool for editing podcast and interview videos. It uses AI for scene detection, transcript generation, and intelligent video processing.

- **Language / Runtime**: Python 3.12
- **Architecture**: Flask web app + CLI processing pipeline
- **Package / Namespace**: `podcast_video_editor`
- **Package manager**: uv

---

## Required Skills — ALWAYS Invoke These

| Situation | Skill |
|-----------|-------|
| Before any new feature or screen | `superpowers:brainstorming` |
| Planning multi-step changes | `superpowers:writing-plans` |
| Writing or fixing core logic | `superpowers:test-driven-development` |
| First sign of a bug or failure | `superpowers:systematic-debugging` |
| Before completing a feature branch | `superpowers:requesting-code-review` |
| Before claiming any task done | `superpowers:verification-before-completion` |
| Working on UI / frontend | `frontend-design:frontend-design` |
| After implementing — reviewing quality | `simplify` |

---

## Architecture

```
ai-vid-edit/
├── podcast-video-editor/
│   ├── src/podcast_video_editor/
│   │   ├── commands/    ← CLI commands
│   │   ├── config/      ← Configuration
│   │   ├── processing/  ← Video processing logic
│   │   └── web_app/     ← Flask web interface
│   ├── helpers/         ← Shell helper scripts
│   └── uv.lock          ← Locked dependencies
└── 0-docs/              ← Project documentation
```

---

## Coding Conventions

- [ ] All functions typed with Python type hints
- [ ] No hardcoded strings — use config
- [ ] `ruff` enforced on every commit

---

## Engineering Principles

### File Size
- **200-line maximum per file**

### DRY · SOLID · KISS · YAGNI
- Single Responsibility per function/class
- Extract shared logic

### TDD
- Write failing test first

### Commit hygiene
- Conventional Commits enforced by commit-msg hook

---

## Build Commands

```bash
cd podcast-video-editor
uv sync                                    # Install dependencies
uv run ruff check .                        # Lint
uv run pytest --tb=short                   # Run tests
```

---

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | This file |
| `version.txt` | Semantic version |
| `.github/workflows/` | CI, release, Pages |
| `scripts/install-hooks.sh` | Hook installer |

---

## Starting a New Session

1. Read this file
2. Run `cd podcast-video-editor && uv run ruff check .`
3. Invoke `superpowers:brainstorming` before new features
