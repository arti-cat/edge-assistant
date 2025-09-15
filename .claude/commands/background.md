---
name: background
description: Delegate work to background agent using Task tool
argument-hint: [agent] [task description]
---

# Background Agent Delegation

## Security Validation

**Agent Validation:** $1
**Task Validation:** $2

### Agent Verification
Valid agents: researcher, coder, reviewer, tester, documenter, orchestrator

### Task Security Check
Validating task complexity and safety patterns...

## Task Execution

I'll validate and delegate this work to the **$1** agent for background processing using Claude Code's native Task tool delegation.

**Background Task Setup:**
- **Agent Type:** $1 (specialized for focused work)
- **Task Scope:** $2 (validated for background execution)
- **Execution Mode:** Independent background processing
- **Report Location:** `reports/background/active/`
- **Pattern:** Dan's "out-of-loop" workflow for context window optimization

## Security Validation Process

Before delegation, I'll validate:

1. **Agent Name Validation:**
   - Must be one of: researcher, coder, reviewer, tester, documenter, orchestrator
   - Reject unrecognized agent names

2. **Task Complexity Validation:**
   - Task description length: 10-200 characters
   - Must match safe operation patterns
   - Block potentially dangerous task descriptions

3. **Approved Task Patterns:**
   - `analyze|research|document|review` + description
   - `implement` + specific feature description (50-150 chars)
   - `test` + specific test scope description
   - `fix` + specific bug description

4. **Blocked Task Patterns:**
   - System commands or shell execution requests
   - Requests involving credentials, secrets, or sensitive data
   - Overly complex or vague task descriptions
   - Tasks requesting file system access outside project scope

## Validated Delegation Command

If validation passes, use Task tool to spawn **$1** agent with proper context:

**Task Description:** "CONTEXT PRIME: This is a pyConductor background task. You have access to:
- 6 focused agents via Task tool delegation
- Comprehensive hooks system for activity logging
- Context bundles in reports/context-bundles/
- Commands: /implement, /review, /track, /background
- Reports structure: activity.jsonl, coordination.jsonl
- Current project: Multi-agent development framework

BACKGROUND TASK: $2

EXECUTION INSTRUCTIONS:
1. Use appropriate agents via Task tool if needed
2. Log progress to reports/background/active/{timestamp}_{agent}_task.md
3. Work independently without polluting primary context
4. Generate detailed results and move to reports/background/completed/ when finished
5. Follow security best practices - no credential access or system modifications"

**Context Transfer:** Essential project knowledge provided to background agent

**Agent Focus:** The $1 agent will work autonomously on this validated task, applying its specialized capabilities for optimal results.

This implements secure background agent delegation - freeing up the primary context window while maintaining security boundaries and full task execution capability.