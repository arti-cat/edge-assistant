# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

edge-assistant is a unified multimodal CLI assistant built on OpenAI's latest Responses API. It provides seamless analysis across text, images, documents, and other content types with advanced threading capabilities. The tool offers web research, knowledge base management, safe file editing, and tool-calling AI agent functionality.

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

- `cli.py` - Typer-based CLI interface with unified multimodal commands (analyze, ask, research, kb-index, kb-research, edit, agent)
- `engine.py` - OpenAI Responses API wrapper with multimodal support, threading, and content type detection
- `tools.py` - Utility functions for diffs, text extraction, URL parsing, and function tool definitions
- `state.py` - XDG-compliant state management for multimodal threads and knowledge base file IDs

### Key Commands

- `analyze` - **Unified multimodal analysis** supporting text, images, PDFs, and documents with threading (NEW!)
- `ask` - Interactive text chat with optional threading and system instructions (enhanced with multimodal engine)
- `research` - Web research with structured JSON output and source citations
- `kb-index` - Index local files (.md, .txt, .pdf, .py, .rst) for knowledge base search
- `kb-research` - Query indexed knowledge base with citations
- `edit` - Safe file editing with unified diff preview (dry-run by default, use --apply to write)
- `agent` - Tool-calling agent mode with file system access (requires --approve for writes)
- `analyze-image` - Legacy image analysis (deprecated, use `analyze` instead)

### State Management

Uses XDG directories with JSON persistence:
- **Multimodal threads** tracked by name with content type breakdown and metadata
- **Legacy thread compatibility** maintained for existing text and vision threads  
- **Knowledge base file IDs** stored for reuse across sessions
- **Auto-cleanup** of threads older than 7 days
- Fallback to `~/.config` and `~/.local/share` when platformdirs unavailable

### Key Features

- **Unified Multimodal Threading**: Seamless context preservation across text, images, and documents
- **Content Type Detection**: Automatic file type detection with manual override capability
- **Smart Model Selection**: Optimal model chosen based on content type (gpt-4o for vision, etc.)
- **Safety-First Design**: All destructive operations use dry-run by default with explicit approval
- **Future Ready**: Architecture prepared for audio, video, and other upcoming OpenAI modalities

The edit command always shows diffs before applying changes and supports automatic backup creation.