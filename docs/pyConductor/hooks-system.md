# pyConductor Hooks System

The hook system provides sophisticated lifecycle event management through executable Python scripts that integrate directly with Claude Code's hook architecture.

## Hook Architecture Overview

The pyConductor hooks system implements 6 lifecycle events with specialized processing for each stage of the development workflow.

### Hook Events & Triggers

| Hook Event | Files | Description | Timeout |
|------------|--------|-------------|---------|
| **SessionStart** | `context-prime.py`, `bundle-manager.py` | Dynamic context loading and bundle suggestions | 10s, 5s |
| **PreToolUse** | `security-filter.py` | Command validation and security filtering | 5s |
| **PostToolUse** | `activity-logger.py`, `agent-coordinator.py` | Activity logging and agent coordination tracking | 10s, 5s |
| **UserPromptSubmit** | `task-tracker.py` | Task tracking and progress logging | 3s |
| **SessionEnd** | `session-end.py` | Session cleanup and final logging | 5s |
| **Stop** | `stop-control.py` | Background task management and stop control | 5s |

## Individual Hook Documentation

### 1. SessionStart Hooks

#### context-prime.py
**Purpose**: Dynamic project context priming using Dan's R&D framework

**Key Features**:
- Git status analysis
- Active task detection from `reports/tasks.jsonl`
- Recent file activity from `reports/activity.jsonl`
- Recent agent usage from `reports/coordination.jsonl`
- Background task detection
- Session continuity analysis

**Context Output Example**:
```
🎯 pyConductor Session Started | 2025-09-14 15:30

Git Status: Working tree clean
Recent Activity: security-filter.py, activity-logger.py, bundle-manager.py
Recent Agents: researcher, coder, reviewer
Background Tasks: 2 background tasks (researcher, documenter)
Project: Multi-agent development framework with simplified workflows
Agents: 6 focused agents available via Task tool delegation
Directories: .claude, docs, reports
Active Tasks: 1

Key Commands:
- /implement "feature" - Full feature development workflow
- /review [path] - Security and quality assessment
- /track "task" - Simple task progress tracking
- /background [agent] "task" - Out-of-loop agent delegation
```

#### bundle-manager.py
**Purpose**: Context bundle auto-suggestion for session restoration

**Key Features**:
- Scans `reports/context-bundles/` for recent bundles
- Suggests most relevant bundles based on timestamps and activity
- Provides bundle loading commands
- Implements Dan's ADV2 context reconstruction pattern

### 2. PreToolUse Hook

#### security-filter.py
**Purpose**: Automatic security filtering with multi-pattern validation

**Security Patterns**:

**Dangerous Patterns (Auto-Block)**:
```python
DANGEROUS_PATTERNS = [
    r'rm\s+-rf\s+/',
    r'sudo\s+rm',
    r'>\s*/dev/sd[a-z]',
    r'dd\s+if=.*of=/dev',
    r'mkfs\.',
    r'fdisk',
    r':(){ :|:& };:',  # Fork bomb
    r'curl.*\|\s*sh',  # Pipe to shell
    r'wget.*\|\s*sh'
]
```

**Caution Patterns (Request Confirmation)**:
```python
CAUTION_PATTERNS = [
    r'git\s+push\s+--force',
    r'git\s+reset\s+--hard',
    r'git\s+clean\s+-fd',
    r'npm\s+publish',
    r'pip\s+install.*--break-system-packages',
    r'sudo\s+',
    r'rm\s+-rf\s+\S+'
]
```

**Safe Patterns (Auto-Approve)**:
```python
SAFE_PATTERNS = [
    r'git\s+status',
    r'git\s+log',
    r'git\s+diff',
    r'ls\s+',
    r'cat\s+',
    r'grep\s+',
    r'find\s+'
]
```

**Decision Flow**:
1. Check dangerous patterns → **deny** with reason
2. Check caution patterns → **ask** for confirmation
3. Check safe patterns → **allow** automatically
4. Default → **allow** (fail-safe approach)

### 3. PostToolUse Hooks

#### activity-logger.py
**Purpose**: Enhanced activity logging with context bundle trails

**Credential Sanitization Patterns**:
```python
SENSITIVE_PATTERNS = [
    (r'password\s*[=:]\s*[\'"]?([^\s\'"]+)', 'password=[REDACTED]'),
    (r'token\s*[=:]\s*[\'"]?([^\s\'"]+)', 'token=[REDACTED]'),
    (r'api[_-]?key\s*[=:]\s*[\'"]?([^\s\'"]+)', 'api_key=[REDACTED]'),
    (r'secret\s*[=:]\s*[\'"]?([^\s\'"]+)', 'secret=[REDACTED]'),
    (r'bearer\s+([a-zA-Z0-9\-._~+/]+=*)', 'bearer [REDACTED]'),
    (r'ssh-rsa\s+[^\s]+', 'ssh-rsa [REDACTED]'),
    (r'-----BEGIN[^-]+-----[^-]+-----END[^-]+-----', '[REDACTED CERTIFICATE]'),
    (r'/home/[^/]+/\.ssh/[^\s]+', '/home/[USER]/.ssh/[REDACTED]'),
    (r'/.*\.env[^/]*', '[REDACTED ENV FILE]'),
    (r'/.*secrets?[^/]*', '[REDACTED SECRETS]')
]
```

**Dual Logging System**:
1. **Activity Log** (`reports/activity.jsonl`) - Simple event logging
2. **Context Bundles** (`reports/context-bundles/{session_id}_bundle.jsonl`) - Operation trails for Dan's ADV2 pattern

**Context Bundle Entry Structure**:
```json
{
    "timestamp": "2025-09-14T15:30:45.123456",
    "session_id": "uuid-session-id",
    "tool": "Edit",
    "action": "edit",
    "file": "src/module.py",
    "summary": "edit: module.py",
    "context_type": "file_modification"
}
```

#### agent-coordinator.py
**Purpose**: Agent delegation event logging for Task tool usage

**Features**:
- Tracks all Task tool delegations
- Records agent types, task descriptions, and success status
- Logs to `reports/coordination.jsonl` for workflow analysis
- Supports background task detection and classification

### 4. UserPromptSubmit Hook

#### task-tracker.py
**Purpose**: Simple task tracking with `/track` command detection

**Task Tracking Logic**:
```python
# Detects /track commands and logs to reports/tasks.jsonl
if user_prompt.startswith("/track"):
    task_description = user_prompt[6:].strip().strip('"\'')
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "task": task_description,
        "status": "active",
        "type": "user_task"
    }
```

### 5. SessionEnd Hook

#### session-end.py
**Purpose**: Session cleanup and final activity logging

**Cleanup Operations**:
- Logs session end with reason and working directory
- Cleans up temporary files
- Finalizes context bundle entries
- Updates session statistics

### 6. Stop Hook

#### stop-control.py
**Purpose**: Background task management and graceful stopping

**Background Task Detection**:
```python
def has_active_background_tasks():
    """Check for active background tasks by analyzing coordination logs"""
    # Looks for recent Task delegations that might be running
    # Provides intelligent stopping behavior
```

## Hook Integration with Settings

The hooks are configured in `.claude/settings.json` with sophisticated matching:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/context-prime.py",
            "timeout": 10
          },
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bundle-manager.py",
            "timeout": 5
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/security-filter.py",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Read|Write|Edit|MultiEdit|Bash|Task",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/activity-logger.py",
            "timeout": 10
          }
        ]
      },
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/agent-coordinator.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

## Security Implementation

### Multi-Layer Security Approach
1. **Pattern-based filtering** in security-filter.py
2. **Credential sanitization** in activity-logger.py
3. **Permission boundaries** in settings.json
4. **Resource constraints** with timeouts and limits

### Error Handling Philosophy
All hooks implement **silent fail-safe** patterns:
- Errors don't break the workflow
- Default to safe operations (allow, log, continue)
- JSON-structured error responses
- Comprehensive logging for debugging

## Hook Development Guidelines

### Standard Hook Structure
```python
#!/usr/bin/env python3
"""
Hook description and purpose
Triggers: HookEventName
"""

import json
import sys

def hook_function():
    """Main hook logic"""
    try:
        # Read input from stdin
        input_text = sys.stdin.read().strip()
        if input_text:
            data = json.loads(input_text)

        # Hook-specific processing

        return {
            "hookSpecificOutput": {
                "hookEventName": "HookName",
                "result": "success"
            }
        }
    except Exception:
        # Silent fail-safe
        return {}

if __name__ == "__main__":
    result = hook_function()
    print(json.dumps(result))
```

### Best Practices
1. **Timeout compliance** - Respect configured timeouts
2. **JSON communication** - Use structured input/output
3. **Error resilience** - Never break the workflow
4. **Security awareness** - Sanitize sensitive data
5. **Performance optimization** - Minimize processing time

## Hook System in Practice

### Example Demonstrations
Experience the hook system through practical examples:
- **All Examples**: Every example demonstrates hooks in action
- `examples/04-full-workflow/` - Complete lifecycle hook integration
- `examples/06-background-delegation/` - Background task hook coordination
- `examples/03-security-review/` - Security filtering hooks

### Observability Benefits
The hook system provides:
- **Real-time Activity Monitoring**: Every tool use logged
- **Agent Coordination Tracking**: Complete delegation history
- **Security Event Detection**: Immediate threat identification
- **Performance Metrics**: Hook execution timing and success rates

### Customization Capabilities
While examples use standard hooks, the system supports:
- Custom hook development for domain-specific needs
- Workflow-specific middleware integration
- Team-specific quality gates and validation
- Project-specific context optimization

The hook system represents a sophisticated middleware layer that provides enterprise-grade security, comprehensive observability, and intelligent workflow management while maintaining seamless integration with Claude Code's native capabilities.