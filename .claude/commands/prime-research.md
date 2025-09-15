---
name: prime-research
description: Prime context for codebase analysis and research tasks
argument-hint: [optional focus area]
---

# Research Context Priming

Use the researcher agent to analyze the codebase and prime context for research tasks: $ARGUMENTS

## Purpose
Load focused context for codebase analysis, pattern discovery, and requirements research.

## Workflow
1. **Read key project files** - README, CLAUDE.md, main source files
2. **Analyze structure** - Directory organization, import patterns, dependencies
3. **Identify patterns** - Coding conventions, architecture decisions, frameworks
4. **Report findings** - Structured summary of codebase understanding

The researcher agent will:
- Discover existing patterns and conventions
- Analyze technology stack and dependencies
- Identify key files and entry points
- Map out directory structure and organization
- Note architectural decisions and patterns
- Flag potential areas for improvement

**Focus Areas**: Use $ARGUMENTS to specify research focus (e.g., "authentication patterns", "API design", "test structure")