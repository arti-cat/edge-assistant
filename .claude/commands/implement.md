---
name: implement
description: Full feature implementation using agent delegation
argument-hint: [feature description]
---

Implement feature: $ARGUMENTS

Use the orchestrator agent to coordinate a complete implementation workflow:

The orchestrator will use Claude Code's native Task tool to delegate work through the standard flow:
1. **Research** - Analyze existing patterns and requirements
2. **Implementation** - Code the feature following discovered patterns
3. **Testing** - Create comprehensive tests and validate functionality
4. **Review** - Security and quality assessment with fixes
5. **Documentation** - Update docs and usage examples

This leverages Claude Code's built-in agent delegation rather than external orchestration systems.

Use orchestrator agent to "coordinate full implementation of: $ARGUMENTS"