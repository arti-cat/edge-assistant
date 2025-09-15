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

## IMPORTANT INFORMATION 

You are the main Claude agent in the pyConductor system. You MUST ALWAYS follow the the below guidance when working on a project. 

# pyConductor - Multi-Agent Development Framework

> "A focused agent is a performant agent" - Context Engineering Framework

Production-ready framework leveraging Claude Code's native capabilities for sophisticated multi-agent development workflows.

## Core Philosophy

- **Reduce** context overhead through dynamic priming and security filtering
- **Delegate** specialized processing to focused agents via Task tool
- Use hooks for programmable middleware, JSONL for observability
- Follow Dan's R&D framework for context window optimization

## Essential Commands

### Primary Workflows
- `/implement "feature"` - Full development workflow: research → code → test → review → document
- `/review [path]` - Security and quality assessment
- `/background [agent] "task"` - Out-of-loop agent delegation
- `/track "task"` - Simple development task tracking

### Context Engineering
- `/prime-research [focus]` - Optimize context for analysis tasks
- `/prime-implement [feature]` - Prime for feature development
- `/loadbundle [path]` - Restore from previous operation trails
- Context7 MCP tools are available with full documentation of most libraries and dependencies - this should be used by agents when appropriate. 

## Focused Agent System

**6 specialized agents** (`.claude/agents/`) - Each does one thing exceptionally well:
- **researcher** - Analysis, patterns, requirements
- **coder** - Implementation following discovered patterns
- **tester** - Test creation and execution
- **reviewer** - Security and quality (read-only analysis)
- **documenter** - API docs and usage examples
- **orchestrator** - Multi-agent workflow coordination

## Hook System

**Automated lifecycle management** (`.claude/hooks/`):
- **SessionStart** - Dynamic context priming with git status, tasks, agents
- **PreToolUse** - Security filtering with dangerous command blocking
- **PostToolUse** - Activity logging and agent coordination tracking
- **UserPromptSubmit** - Task tracking when `/track` used

## Security & Permissions

- **Granular permissions** with allow/deny patterns
- **Credential sanitization** in all logs
- **Multi-pattern validation** for dangerous operations
- **Safe file access** with type restrictions

## Key Patterns

### Standard Flow
```bash
/implement "Add OAuth2 authentication"
# orchestrator → researcher → coder → tester → reviewer → documenter
```

### Background Delegation
```bash
/background researcher "analyze microservices patterns"
# Runs independently without polluting primary context
```

### Context Restoration
```bash
/loadbundle reports/context-bundles/session-abc123_bundle.jsonl
# Restore previous session context from operation trails
```

## Observability

Simple JSONL logging in `reports/`:
- `activity.jsonl` - File operations and tool usage
- `coordination.jsonl` - Agent delegation events
- `tasks.jsonl` - User-tracked development tasks
- `context-bundles/` - Session restoration data (Dan's ADV2 pattern)

## Full workflow example

# 1. Track the main project
  /track "build AI pair programmer for wife's research using pyConductor"

  # 2. Prime context for domain
  /prime-research cli and llm programming-patterns

  # 3. Background research with primed context
  /background researcher "analyze cli tools in..."

  # 4. Generate project foundation
  /generate cli-assistant --template datascience

  # 5. Prime for implementation  
  /prime-implement cli-features

  # 6. Staged implementation
  /implement "PDF parser for documents with OCR"
  /implement "data parser with validation"
  /implement "fuzzy name matching for spelling variations"
  /implement "interactive data visualization"

  # 7. Quality assurance
  /review cli-assistant/

  # 8. Background documentation
  /background documenter "create beginner-friendly programming guide"

  # 9. Context bundling for future sessions
  # (automatic via hooks when context limits approached)


## Documentation

Comprehensive docs in `docs/pyConductor/` - Use for reference, not loaded by default to prevent context bloat.