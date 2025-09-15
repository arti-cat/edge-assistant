# Output Styles Best Practices (.claude/output-styles/*.md)

## What this is

Output styles customize Claude Code’s core behavior by replacing the system prompt, making it suitable for different modes (e.g., explanatory, learning, auditing) while retaining tools and workflows.

## Where they live

- Project: `.claude/output-styles/*.md`
- User: `~/.claude/output-styles/*.md`

## When to use

- You need a consistent voice or behavior across a team.
- You’re shifting from “do” to “explain/teach/audit.”
- You want predictable JSON output for downstream automation.

## Template

```markdown
---
name: <style-name>
description: <brief description of what this style does>
---

# Custom Style Instructions

<Define the assistant behavior for this style>

## Specific Behaviors
- [Behavior 1]
- [Behavior 2]

## Output Conventions
- Prefer concise responses with bullet points.
- When `--output-format json` is requested, emit machine-parseable results.
```

## Example: Explanatory PR Reviewer

```markdown
---
name: explanatory-pr-reviewer
description: Educational, example-heavy explanations for PR reviews
---

# Custom Style Instructions
Adopt a patient, explanatory tone. Avoid changing code unless requested. Provide step-by-step rationales with short code snippets.

## Specific Behaviors
- Start with a short summary.
- Show corrected code snippets when appropriate.
- Offer alternatives and trade-offs.

## Output Conventions
- Use headings and lists.
- Keep each list item under 2 lines.
```

## JSON output formats

When using the CLI with `--output-format json`, expect a structure similar to:

```json
{
  "result": "Response content",
  "total_cost_usd": 0.01234,
  "duration_ms": 2300,
  "model": "claude-3-5-sonnet-20241022"
}
```

For automation-heavy workflows, define a section in the style or agent asking the assistant to include an explicit machine-readable block when needed, e.g., a fenced `json` snippet that the workflow engine can parse.

## Verification

- Switch styles via `/output-style [name]` and validate the tone and structure.
- Keep styles minimal and orthogonal to agents; styles define “how,” agents define “who/what.”
- Avoid embedding environment-specific assumptions; keep them in agents/commands instead.
