#!/usr/bin/env python3
"""
Enhanced activity logging with context bundle trails (Dan's ADV2 pattern)
Triggers: PostToolUse
"""

import json
import sys
import os
import re
from datetime import datetime
from pathlib import Path

# Security patterns to sanitize from logs
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
    (r'/.*secrets?[^/]*', '[REDACTED SECRETS]'),
]

def sanitize_text(text):
    """Remove sensitive information from text"""
    if not text or not isinstance(text, str):
        return text

    sanitized = text
    for pattern, replacement in SENSITIVE_PATTERNS:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

    return sanitized

def create_bundle_entry(data, tool_name, tool_input, tool_response, session_id):
    """Create context bundle entry for operation trail"""
    bundle_entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "tool": tool_name,
    }

    # Add tool-specific context for bundle reconstruction
    if tool_name == "Read":
        file_path = tool_input.get("file_path", "")
        bundle_entry.update({
            "action": "read",
            "file": sanitize_text(file_path),
            "summary": f"Read {Path(file_path).name if file_path else 'unknown'}",
            "context_type": "file_content"
        })
    elif tool_name in ["Write", "Edit", "MultiEdit"]:
        file_path = tool_input.get("file_path", "")
        bundle_entry.update({
            "action": "write" if tool_name == "Write" else "edit",
            "file": sanitize_text(file_path),
            "summary": f"{tool_name.lower()}: {Path(file_path).name if file_path else 'unknown'}",
            "context_type": "file_modification"
        })
    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        sanitized_command = sanitize_text(command)
        bundle_entry.update({
            "action": "command",
            "command": sanitized_command[:100],  # Truncate long commands
            "summary": f"Executed: {sanitized_command.split()[0] if sanitized_command else 'unknown'}",
            "context_type": "system_command"
        })
    elif tool_name == "Task":
        description = tool_input.get("description", "")
        agent = tool_input.get("subagent_type", "unknown")
        sanitized_desc = sanitize_text(description)
        bundle_entry.update({
            "action": "delegate",
            "agent": agent,
            "task": sanitized_desc[:100],  # Truncate long descriptions
            "summary": f"Delegated to {agent}: {sanitized_desc[:50]}...",
            "context_type": "agent_delegation"
        })
    else:
        # Generic tool logging
        bundle_entry.update({
            "action": "tool_use",
            "summary": f"Used {tool_name}",
            "context_type": "generic"
        })

    return bundle_entry

def log_activity():
    """Log tool activity with enhanced context bundle trails"""
    try:
        data = json.load(sys.stdin)

        # Create reports directories
        Path("reports").mkdir(exist_ok=True)
        Path("reports/context-bundles").mkdir(exist_ok=True)

        # Extract relevant information
        session_id = data.get("session_id")
        tool_name = data.get("tool_name")
        tool_input = data.get("tool_input", {})
        tool_response = data.get("tool_response", {})

        # Create simple activity log entry (existing functionality)
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "tool": tool_name,
            "file": sanitize_text(tool_input.get("file_path")),
            "command": sanitize_text(tool_input.get("command")),
            "success": tool_response.get("success", True),
            "type": "activity"
        }

        # Remove empty fields to keep logs clean
        log_entry = {k: v for k, v in log_entry.items() if v is not None}

        # Append to activity log (existing functionality)
        with open("reports/activity.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        # Create context bundle entry (Dan's ADV2 pattern)
        if session_id and tool_name in ["Read", "Write", "Edit", "MultiEdit", "Bash", "Task"]:
            bundle_entry = create_bundle_entry(data, tool_name, tool_input, tool_response, session_id)

            # Create session-specific bundle file
            bundle_file = f"reports/context-bundles/{session_id}_bundle.jsonl"
            with open(bundle_file, "a") as f:
                f.write(json.dumps(bundle_entry) + "\n")

    except Exception:
        # Silent fail - don't break workflow on logging errors
        pass

if __name__ == "__main__":
    log_activity()