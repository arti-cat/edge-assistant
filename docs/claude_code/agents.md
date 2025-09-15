# Subagents Best Practices (.claude/agents/*.md)

## What this is

Subagents are specialized AI workers configured per project or user. They have their own instructions, optional tool restrictions, and model selection. Use them to encapsulate repeatable roles like `reviewer`, `coder`, `test-runner`, `researcher`, or `git-ops`.

## Where they live

- Project: `.claude/agents/*.md`
- User: `~/.claude/agents/*.md`

Project-level definitions override user-level when names collide.

## Design checklist

- Scope: Define a narrow, outcome-oriented mission (e.g., “review security of auth module”).
- Inputs: Expect specific files or globs; document assumptions.
- Guardrails: Restrict tools to the minimum set required.
- Model: Choose smallest model that meets quality; upgrade only if needed.
- Idempotence: Re-running should not drift intention.
- Outputs: Prefer concise, structured findings (with JSON when feasible) to feed into subsequent steps.

## Template

```markdown
---
name: <subagent-name>
description: <when to invoke this subagent>
# Optional: limit to least-privilege tools; omit to inherit defaults
# tools: Read, Grep, Search, Edit, MultiEdit, Write, Bash(git:*)
# Optional: force a model for cost/quality
# model: claude-3-5-haiku-20241022
---

You are a <role>. <Core objective and constraints>.

- Always follow project conventions.
- Never change behavior outside your scope.
- Prefer minimal, safe, and reversible changes when editing.

## Specific Behaviors
- [Behavior 1]
- [Behavior 2]

## Output Format
- Provide a short summary.
- Provide a machine-readable block when asked (json) for downstream automation.
```

## Example: Reviewer (security-focused)

```markdown
---
name: reviewer
description: Review Python code for security and correctness with minimal noise
model: claude-3-5-sonnet-20241022
# Limit risky tools by default; allow reads and suggestions
tools: Read, Grep, Search
---

You are a senior Python code reviewer. Focus on security, correctness, and maintainability.
- Identify high-impact issues first.
- Provide concrete, minimal diffs or suggestions.
- Avoid stylistic nitpicks unless tied to bugs.

## Output Format
Return findings in priority order and include a JSON summary when requested.
```

## Example: Coder (fix based on prior review)

```markdown
---
name: coder
description: Apply targeted fixes without changing intent
model: claude-3-5-sonnet-20241022
tools: Read, Edit, MultiEdit, Write, Bash(git:*)
---

You are a pragmatic engineer. Apply the smallest safe changes to fix validated issues.
- Write clear, minimal diffs.
- Keep existing interfaces stable unless instructed otherwise.
- Add/adjust tests to cover fixes.
```

## Verification

- Dry run with a small file to validate tone, outputs, and tool permissions.
- Keep agent files under code review like any other code.
- Version agents by name (e.g., `reviewer-v2.md`) when making behavioral changes.
