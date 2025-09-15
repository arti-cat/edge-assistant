# Commands Best Practices (.claude/commands/*.md)

## What this is

Custom commands are reusable prompts with arguments and (optionally) restricted tool permissions. They complement built-in slash commands and MCP prompts.

## Where they live

- Project: `.claude/commands/*.md`
- User: `~/.claude/commands/*.md`

## When to use

- You repeat a task often (e.g., making commits, preparing releases).
- You want team-standardized phrasing and tool permissions.
- You need dynamic context injection from the shell.

## Template

```markdown
---
argument-hint: [args]
description: <what this command does>
# Optional: restrict risky tools (least-privilege)
# allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
# Optional: default model
# model: claude-3-5-haiku-20241022
---

<Your prompt template using $ARGUMENTS or $1, $2, ...>

# Optional: include files
# @path/to/file
```

## Arguments and context

- `$ARGUMENTS` for the full string.
- `$1`, `$2`, `$3` for positional args.
- `@file` to embed file contents.
- Dynamic context with shell execution:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*)
---
Current changes:
!`git status --porcelain`

Create a concise commit message based on the above.
```

## Examples

- Commit helper

```markdown
---
argument-hint: [message]
description: Create a conventional commit from staged changes
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
model: claude-3-5-haiku-20241022
---

Summarize the staged changes from:
!`git diff --cached --name-status`

Compose a conventional commit message. If $ARGUMENTS is provided, incorporate it.
```

- PR review shortcut (MCP example)

```text
/mcp__github__pr_review 456
```

## Verification

- Keep commands short and task-specific; avoid creeping scope.
- Review allowed-tools; remove write/exec permissions unless necessary.
- Test with and without arguments; ensure safe defaults.
