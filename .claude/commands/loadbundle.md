---
name: loadbundle
description: Load context bundle to restore previous agent operation context
argument-hint: [bundle file path]
---

# Context Bundle Loader

Restore agent context from previous operation trail: $ARGUMENTS

## Purpose
Reconstruct agent context from a previous session's operation bundle, enabling continuation after context window explosion or session interruption.

## Workflow
1. **Load bundle file** - Read the specified context bundle JSONL file
2. **Parse operations** - Extract file reads, edits, and agent delegations
3. **Reconstruct context** - Re-read relevant files to restore understanding
4. **Summarize previous work** - Provide overview of completed operations
5. **Prepare continuation** - Set context for next steps

## Usage
```bash
# Load specific bundle file
/loadbundle reports/context-bundles/session-id_bundle.jsonl

# Load recent bundle (will prompt for selection)
/loadbundle
```

## Bundle Format
Context bundles contain operation trails with:
- **Read operations**: Files that were analyzed
- **Write/Edit operations**: Files that were modified (summary only)
- **Agent delegations**: Sub-agents that were used
- **Command operations**: System commands that were executed

## Context Reconstruction Process
1. **Re-read files** from Read operations to restore file content context
2. **Summarize modifications** from Write/Edit operations without re-executing
3. **Note agent work** from delegation operations
4. **Provide timeline** of what was accomplished

This enables seamless continuation of work after context window limits are reached.