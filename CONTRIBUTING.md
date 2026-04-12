# Contributing to ai-vid-edit

## Local Setup

1. Install [uv](https://github.com/astral-sh/uv) and Python 3.12.
2. Clone and set up:
   ```bash
   git clone https://github.com/cocodedk/ai-vid-edit.git
   cd ai-vid-edit/podcast-video-editor
   uv sync
   ```

## Install Git Hooks

```bash
./scripts/install-hooks.sh
```

## Local Git Setup

```bash
git config pull.rebase true
git config core.autocrlf input
git config push.autoSetupRemote true
git config init.defaultBranch main
```

## Build and Test Commands

```bash
cd podcast-video-editor
uv run ruff check .     # Lint
uv run pytest           # Run tests
```

## Branch Naming

| Prefix | Use |
|---|---|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `chore/` | Maintenance |
| `docs/` | Documentation |
| `ci/` | CI/CD changes |

## PR Checklist

- [ ] Lint passes.
- [ ] Tests pass.
- [ ] Manual test completed.
- [ ] Updated docs if behavior changed.
