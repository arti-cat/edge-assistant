---
name: prime-debug
description: Prime context for debugging and bug fixing workflows
argument-hint: [issue description]
---

# Debug Context Priming

Use the researcher agent to analyze and prepare context for debugging: $ARGUMENTS

## Purpose
Load focused context for understanding, reproducing, and fixing bugs or issues.

## Workflow
1. **Analyze issue context** - Understand the problem description
2. **Identify relevant files** - Find code areas related to the issue
3. **Examine error patterns** - Look for logs, tests, or reproduction steps
4. **Map dependencies** - Understand code flow and related components
5. **Prepare debug context** - Load relevant code and documentation

The researcher agent will:
- Locate code areas most likely related to the issue
- Examine existing tests and error patterns
- Map out code flow and dependencies
- Identify potential root causes
- Prepare context for focused debugging
- Note similar patterns or previous fixes

**Issue Context**: Use $ARGUMENTS to describe the bug or issue (e.g., "login fails on mobile", "API returns 500 error", "memory leak in background tasks")