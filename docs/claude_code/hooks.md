# Hooks Best Practices (.claude/settings.json)

## What this is

Hooks run external commands when certain events happen inside Claude Code (e.g., before/after tool use). They enable automation, policy enforcement, and integrations.

## Where they live

- Project: `.claude/settings.json`
- User: `~/.claude/settings.json`
- Local override (gitignored): `.claude/settings.local.json`

## Events

- `SessionStart`, `SessionEnd`
- `UserPromptSubmit`
- `PreToolUse`, `PostToolUse`
- `Stop`, `SubagentStop`
- `PreCompact`, `Notification`

## Configuration shape

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",  // Optional for global events
        "hooks": [
          { "type": "command", "command": "your-command-here", "timeout": 60000 }
        ]
      }
    ]
  }
}
```

- `matcher` examples: `Bash`, `Edit|MultiEdit|Write`, `mcp__.*__write.*` (regex allowed)
- Exit codes: `0 = continue`, `1 = warn`, `2 = block`
- Env: `CLAUDE_PROJECT_DIR` is available to hook commands

## Common patterns

- Log bash usage (audit)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "jq -r '.tool_input.command' >> ~/.claude/bash-log.txt" }
        ]
      }
    ]
  }
}
```

- Block edits to sensitive files

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json,sys; d=json.load(sys.stdin); p=d.get('tool_input',{}).get('file_path',''); sys.exit(2 if any(s in p for s in ['.env','/.git/']) else 0)\""
          }
        ]
      }
    ]
  }
}
```

- Auto-format after writes

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format-on-write.py" }
        ]
      }
    ]
  }
}
```

Example `format-on-write.py`:

```python
#!/usr/bin/env python3
import subprocess, sys, json
payload=json.load(sys.stdin)
path=payload.get('tool_input',{}).get('file_path','')
if path.endswith('.py'):
    subprocess.run(['python','-m','black',path])
    subprocess.run(['python','-m','isort',path])
```

## Safety tips

- Keep hook code small and reviewed; they run with your user permissions.
- Prefer allowlists to denylists for write operations.
- Start with logging-only hooks before enforcing blocks.
- Use `claude --debug` to inspect hook matching and exit statuses.
