---
name: prime-implement
description: Prime context for feature development and implementation
argument-hint: [feature description]
---

# Implementation Context Priming

Use the orchestrator agent to prepare for feature development: $ARGUMENTS

## Purpose
Load focused context for implementing new features, following existing patterns and conventions.

## Workflow
1. **Analyze existing patterns** - Code style, architecture, testing patterns
2. **Plan implementation approach** - Break down feature into components
3. **Identify dependencies** - Required files, imports, external services
4. **Prepare development context** - Load relevant existing code and documentation

The orchestrator agent will:
- Research existing implementation patterns
- Plan the implementation approach
- Identify required code changes and new files
- Prepare context for the coder agent
- Set up testing strategy
- Consider integration points

**Feature Context**: Use $ARGUMENTS to describe the feature to implement (e.g., "user authentication", "file upload system", "API endpoint for orders")