#!/usr/bin/env python3
"""
Security filtering with automatic decisions (Dan's pattern)
Triggers: PreToolUse
"""

import json
import sys
import re

# Dan's security patterns
DANGEROUS_PATTERNS = [
    r'rm\s+-rf\s+/',
    r'sudo\s+rm',
    r'>\s*/dev/sd[a-z]',
    r'dd\s+if=.*of=/dev',
    r'mkfs\.',
    r'fdisk',
    r':(){ :|:& };:',
    r'curl.*\|\s*sh',
    r'wget.*\|\s*sh',
]

CAUTION_PATTERNS = [
    r'git\s+push\s+--force',
    r'git\s+reset\s+--hard',
    r'git\s+clean\s+-fd',
    r'npm\s+publish',
    r'pip\s+install.*--break-system-packages',
    r'sudo\s+',
    r'rm\s+-rf\s+\S+',
]

# Safe operations that should auto-approve
SAFE_PATTERNS = [
    r'git\s+status',
    r'git\s+log',
    r'git\s+diff',
    r'ls\s+',
    r'cat\s+',
    r'grep\s+',
    r'find\s+',
]

def security_check():
    """Check tool use for security issues"""
    try:
        # Read input from stdin
        input_text = sys.stdin.read().strip()
        if not input_text:
            return {}

        data = json.loads(input_text)

        # Only check Bash commands
        if data.get("tool_name") != "Bash":
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "permissionDecisionReason": "Non-Bash command auto-approved"
                }
            }

        command = data.get('tool_input', {}).get('command', '')
        if not command:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "permissionDecisionReason": "Empty command auto-approved"
                }
            }

        # Check for dangerous patterns first
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": f"🚨 BLOCKED: Dangerous command pattern detected: {command[:50]}..."
                    }
                }

        # Check for caution patterns
        for pattern in CAUTION_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "ask",
                        "permissionDecisionReason": f"⚠️ CAUTION: Potentially risky operation: {command[:50]}..."
                    }
                }

        # Auto-approve safe operations
        for pattern in SAFE_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "allow",
                        "permissionDecisionReason": "Safe operation auto-approved"
                    }
                }

        # Default: allow for other operations
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "Standard operation approved"
            }
        }

    except Exception as e:
        # Silent fail-safe: allow on error
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "Error in security filter, defaulting to allow"
            }
        }

if __name__ == "__main__":
    result = security_check()
    print(json.dumps(result))