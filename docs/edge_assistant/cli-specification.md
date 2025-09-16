# CLI Specification

This document provides comprehensive documentation of the edge-assistant command-line interface, including all commands, options, and usage examples.

## Overview

edge-assistant provides a unified CLI for multimodal AI analysis, web research, knowledge base management, file editing, and tool-calling agent functionality. All commands support threading for maintaining context across interactions.

## Global Commands

### analyze
**Unified multimodal analysis** supporting text, images, PDFs, and documents with threading.

```bash
edge-assistant analyze [CONTENT_PATH] [USER_PROMPT]
```

**Parameters:**
- `CONTENT_PATH` - Optional path to content file (images, PDFs, documents)
- `USER_PROMPT` - Analysis question or instruction

**Options:**
- `--system, -s TEXT` - System/developer prompt for analysis context
- `--model, -m TEXT` - Model to use (auto-selected based on content type)
- `--thread, -t TEXT` - Thread name to maintain context across interactions
- `--type TEXT` - Content type: auto, text, image, audio, video, file (default: auto)
- `--max-interactions INTEGER` - Maximum interactions per thread (default: 20)
- `--clear-thread` - Clear the specified thread before analysis
- `--save TEXT` - Save output to a new file (provide filename or use 'auto' for automatic naming)

**Examples:**
```bash
# Text analysis
edge-assistant analyze "Explain quantum computing"

# Image analysis with threading
edge-assistant analyze photo.jpg "What's in this image?" --thread "photo-session"

# PDF analysis with custom model
edge-assistant analyze document.pdf "Summarize key points" --model gpt-4o

# Save analysis output
edge-assistant analyze report.pdf "Extract action items" --save auto

# Clear thread before new session
edge-assistant analyze data.csv "Analyze trends" --thread "data-analysis" --clear-thread
```

### ask
Interactive text chat with optional threading and system instructions.

```bash
edge-assistant ask [PROMPT]
```

**Parameters:**
- `PROMPT` - Text question or conversation input

**Options:**
- `--thread, -t TEXT` - Thread name to maintain context
- `--stream, -s` - Stream tokens as they arrive
- `--system TEXT` - Optional system instructions
- `--multimodal/--legacy` - Use unified multimodal engine (recommended, default: True)

**Examples:**
```bash
# Simple question
edge-assistant ask "What is machine learning?"

# Threaded conversation
edge-assistant ask "Let's discuss Python" --thread "python-chat"
edge-assistant ask "What are decorators?" --thread "python-chat"

# With system context
edge-assistant ask "Review this code" --system "You are a senior Python developer"

# Streaming response
edge-assistant ask "Explain neural networks" --stream
```

### research
Web research with structured JSON output and source citations.

```bash
edge-assistant research [QUERY]
```

**Parameters:**
- `QUERY` - Research question or topic

**Options:**
- `--json` - Return JSON instead of markdown (default: False)

**Examples:**
```bash
# Research with markdown output
edge-assistant research "Latest developments in AI safety"

# JSON output for programmatic use
edge-assistant research "Climate change solutions 2024" --json
```

## Knowledge Base Commands

### kb-index
Index local files for knowledge base search.

```bash
edge-assistant kb-index [FOLDER]
```

**Parameters:**
- `FOLDER` - Directory path containing files to index

**Supported File Types:**
- `.md` - Markdown files
- `.txt` - Text files
- `.pdf` - PDF documents
- `.py` - Python source code
- `.rst` - reStructuredText files

**Examples:**
```bash
# Index documentation folder
edge-assistant kb-index ./docs

# Index project source code
edge-assistant kb-index ./src
```

### kb-list
List all indexed knowledge base files.

```bash
edge-assistant kb-list
```

**Output:** Displays all files currently indexed in the knowledge base with their file IDs and paths.

### kb-research
Query indexed knowledge base with citations.

```bash
edge-assistant kb-research [QUERY]
```

**Parameters:**
- `QUERY` - Search query for knowledge base

**Examples:**
```bash
# Search documentation
edge-assistant kb-research "API authentication methods"

# Find code examples
edge-assistant kb-research "error handling patterns"
```

## File Management Commands

### edit
Safe file editing with unified diff preview.

```bash
edge-assistant edit [FILEPATH] [INSTRUCTIONS]
```

**Parameters:**
- `FILEPATH` - Path to file to edit
- `INSTRUCTIONS` - Editing instructions for the AI

**Options:**
- `--apply` - Write changes to disk (default: False, dry-run mode)

**Examples:**
```bash
# Preview changes (dry-run mode)
edge-assistant edit script.py "Add error handling to the main function"

# Apply changes to disk
edge-assistant edit config.yaml "Update the database connection timeout to 30 seconds" --apply
```

## Agent Commands

### agent
Tool-calling agent mode with file system access.

```bash
edge-assistant agent [TASK]
```

**Parameters:**
- `TASK` - Task description for the agent to execute

**Options:**
- `--approve` - Approve file writes without confirmation (default: False)

**Examples:**
```bash
# Agent with write confirmation
edge-assistant agent "Create a Python script to process CSV files"

# Agent with automatic approval
edge-assistant agent "Refactor the utils module for better organization" --approve
```

## Legacy Commands

### analyze-image
**Deprecated:** Legacy image analysis command. Use `analyze` instead.

```bash
edge-assistant analyze-image [IMAGE_PATH] [PROMPT]
```

**Migration:**
```bash
# Old command
edge-assistant analyze-image photo.jpg "Describe this image"

# New unified command
edge-assistant analyze photo.jpg "Describe this image"
```

## Advanced Usage Patterns

### Threading Workflows
Maintain context across multiple interactions using named threads:

```bash
# Start a project analysis thread
edge-assistant analyze codebase/ "Overview of this project" --thread "project-review"

# Continue in the same thread
edge-assistant analyze requirements.txt "Are dependencies up to date?" --thread "project-review"

# Add more context
edge-assistant ask "What improvements would you suggest?" --thread "project-review"
```

### Multi-Step Analysis
Chain commands for comprehensive analysis:

```bash
# Step 1: Analyze data
edge-assistant analyze data.csv "Identify trends" --thread "data-analysis" --save trends.md

# Step 2: Research context
edge-assistant research "Data analysis best practices 2024" --json > research.json

# Step 3: Generate recommendations
edge-assistant ask "Based on the trends and research, provide recommendations" --thread "data-analysis"
```

### Knowledge Base Workflow
Build and query a knowledge base:

```bash
# Index project documentation
edge-assistant kb-index ./docs
edge-assistant kb-index ./api-specs

# Query the knowledge base
edge-assistant kb-research "authentication flow"
edge-assistant kb-research "error codes"

# List indexed files
edge-assistant kb-list
```

## Thread Management

### Thread Naming Conventions
- Use descriptive names: `--thread "api-design"` instead of `--thread "t1"`
- Project-based: `--thread "project-refactor"`
- Date-based: `--thread "analysis-2024-01-15"`
- Feature-based: `--thread "auth-system-review"`

### Thread Cleanup
Threads automatically clean up after 7 days of inactivity. Use `--clear-thread` to manually reset:

```bash
# Clear and restart a thread
edge-assistant analyze new-data.csv "Fresh analysis" --thread "data-work" --clear-thread
```

### Thread Limits
- Maximum interactions per thread: 20 (configurable with `--max-interactions`)
- When limit is reached, use `--clear-thread` to reset

## Output Management

### Save Options
The `--save` option in the `analyze` command supports:

```bash
# Automatic filename generation
edge-assistant analyze report.pdf "Executive summary" --save auto

# Custom filename
edge-assistant analyze data.csv "Analysis results" --save "results-2024.md"

# Save to specific directory
edge-assistant analyze logs/ "Error analysis" --save "./reports/error-analysis.md"
```

### Output Formats
- **Default**: Rich markdown with formatting
- **JSON**: Structured output for programmatic use (`--json` in research command)
- **Streaming**: Real-time token streaming (`--stream` in ask command)

## Error Handling

### Common Issues and Solutions

**Thread Limit Reached:**
```bash
# Error: Thread has reached max interactions
# Solution: Clear the thread
edge-assistant analyze new-file.txt "Analyze this" --thread "full-thread" --clear-thread
```

**File Not Found:**
```bash
# Error: File path doesn't exist
# Solution: Check file path and permissions
ls -la path/to/file.ext
```

**API Key Missing:**
```bash
# Error: OpenAI API key not found
# Solution: Set environment variable
export OPENAI_API_KEY="sk-your-key-here"
```

## Performance Tips

### Optimal Usage Patterns
1. **Use threading** for related analysis tasks
2. **Choose appropriate models** - let auto-selection work or override when needed
3. **Batch similar operations** in the same thread
4. **Use knowledge base** for document-heavy workflows
5. **Enable streaming** for long responses

### Model Selection Guidelines
- **gpt-4o-mini**: Fast text processing, general questions
- **gpt-4o**: Complex analysis, images, files, reasoning tasks
- **Auto-selection**: Recommended for most use cases

### Thread Strategy
- **Short threads**: Single-task analysis
- **Long threads**: Multi-step workflows, iterative analysis
- **Named threads**: Organized by project or topic
- **Clear strategically**: When context becomes stale or irrelevant

## Integration Examples

### Shell Scripting
```bash
#!/bin/bash
# Automated analysis pipeline

echo "Analyzing project files..."
edge-assistant analyze ./src "Code quality review" --thread "review-$(date +%Y%m%d)" --save auto

echo "Researching best practices..."
edge-assistant research "Python code quality tools 2024" --json > research.json

echo "Getting recommendations..."
edge-assistant ask "Based on the code review, what tools should we implement?" --thread "review-$(date +%Y%m%d)"
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: AI Code Review
  run: |
    edge-assistant analyze . "Security and performance review" --save review-${{ github.sha }}.md
    # Upload review-*.md as artifact
```

### Development Workflow
```bash
# Daily development routine
alias analyze-changes='edge-assistant analyze $(git diff --name-only) "Review these changes"'
alias research-tech='edge-assistant research'
alias ai-edit='edge-assistant edit'

# Usage
analyze-changes --thread "daily-review"
research-tech "React 18 best practices"
ai-edit component.jsx "Add TypeScript types"
```