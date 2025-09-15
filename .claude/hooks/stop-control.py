#!/usr/bin/env python3
"""
Stop/SubagentStop control hook (Dan's pattern)
Triggers: Stop, SubagentStop
"""

import json
import sys
from pathlib import Path

def stop_control():
    """Control Claude's stopping behavior"""
    try:
        data = json.load(sys.stdin)
        session_id = data.get("session_id")
        hook_event = data.get("hook_event_name", "Stop")
        stop_hook_active = data.get("stop_hook_active", False)

        # Check if we have active background tasks
        try:
            if Path("reports/coordination.jsonl").exists():
                with open("reports/coordination.jsonl", "r") as f:
                    coords = [json.loads(line) for line in f if line.strip()]

                # Look for recent background tasks that might still be running
                recent_background = []
                for coord in coords[-10:]:  # Check last 10 entries
                    if (coord.get("is_background") and
                        coord.get("status") == "initiated" and
                        coord.get("session_id") != session_id):  # Different session = background
                        recent_background.append(coord.get("delegated_agent", "unknown"))

                if recent_background and not stop_hook_active:
                    return {
                        "continue": False,
                        "stopReason": f"Background agents still active: {', '.join(recent_background[:2])}. Use /status to check progress or force stop."
                    }

        except Exception:
            pass  # Silent fail on background check

        # Check for incomplete tasks in current session
        try:
            if Path("reports/task-log.ndjson").exists():
                with open("reports/task-log.ndjson", "r") as f:
                    recent_tasks = []
                    for line in f:
                        if line.strip():
                            task = json.loads(line)
                            if (task.get("session_id") == session_id and
                                task.get("event") == "task_start"):
                                recent_tasks.append(task)

                # If we have recent task starts without completion, suggest continuation
                if len(recent_tasks) > 0 and not stop_hook_active:
                    return {
                        "continue": False,
                        "stopReason": f"Tasks in progress. Consider completing current work or use /track to log progress."
                    }

        except Exception:
            pass  # Silent fail on task check

        # Allow stopping - no blocking conditions
        return {}  # Allow stop (empty response = continue)

    except Exception:
        # On error, allow stopping (fail-safe)
        return {}

if __name__ == "__main__":
    result = stop_control()
    if result is None:
        # Output empty JSON for hook compliance
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": "Stop control check completed"
            }
        }))
    else:
        print(json.dumps(result))