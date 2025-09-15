#!/usr/bin/env python3
"""
Lightweight task tracking (triggered by /track command)
Triggers: UserPromptSubmit
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def track_task():
    """Simple task tracking to JSONL"""
    try:
        data = json.load(sys.stdin)
        prompt = data.get("user_prompt", "")

        # Only process /track commands
        if not prompt.startswith("/track"):
            return None

        # Extract task description
        task_desc = prompt.replace("/track", "").strip()
        if not task_desc:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": "❌ Please provide a task description: /track \"your task here\""
                }
            }

        # Create reports directory
        Path("reports").mkdir(exist_ok=True)

        # Create simple task entry
        task_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": data.get("session_id"),
            "task": task_desc,
            "status": "active",
            "type": "user_tracked"
        }

        # Log task to JSONL
        with open("reports/tasks.jsonl", "a") as f:
            f.write(json.dumps(task_entry) + "\n")

        return {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": f"✅ Task tracked: {task_desc}"
            }
        }

    except Exception:
        # Silent fail on errors
        return None

if __name__ == "__main__":
    result = track_task()
    if result:
        print(json.dumps(result))
    else:
        # Output empty JSON for hook compliance
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "Task tracking completed"
            }
        }))