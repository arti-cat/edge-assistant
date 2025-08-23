# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

edge-assistant is a CLI tool for AI-assisted research, local knowledge base indexing, and safe file editing using the OpenAI Responses API. It provides commands for web research, local document indexing/search, conversational AI, and file editing with diff previews.

## Development Setup

1. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install in editable mode:
```bash
pip install --upgrade pip
pip install -e .
```

3. Set OpenAI API key:
```bash
export OPENAI_API_KEY="sk-..."
```

## Testing

Run tests with pytest:
```bash
pip install pytest
pytest -q
```

## Architecture

The codebase is organized into 4 main modules:

- `cli.py` - Typer-based CLI interface with 5 main commands (ask, research, kb-index, kb-research, edit, agent)
- `engine.py` - Lightweight wrapper around OpenAI Responses API with streaming support and lazy client initialization
- `tools.py` - Utility functions for diffs, text extraction, URL parsing, and function tool definitions
- `state.py` - XDG-compliant state management for conversation threads and knowledge base file IDs

### Key Commands

- `ask` - Interactive chat with optional threading and system instructions
- `research` - Web research with structured JSON output and source citations
- `kb-index` - Index local files (.md, .txt, .pdf, .py, .rst) for knowledge base search
- `kb-research` - Query indexed knowledge base with citations
- `edit` - Safe file editing with unified diff preview (dry-run by default, use --apply to write)
- `agent` - Tool-calling agent mode with file system access (requires --approve for writes)

### State Management

Uses XDG directories with JSON persistence:
- Conversation threads tracked by name
- Knowledge base file IDs stored for reuse
- Fallback to `~/.config` and `~/.local/share` when platformdirs unavailable

The edit command always shows diffs before applying changes and supports automatic backup creation.