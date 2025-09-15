#!/usr/bin/env python3
"""
Subagent completion tracking (Dan's pattern)
Triggers: SubagentStop
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def track_completion():
    """Log subagent completion events"""
    try:
        data = json.load(sys.stdin)

        # Create reports directory
        Path("reports").mkdir(exist_ok=True)

        # Extract completion details
        session_id = data.get("session_id")
        agent_type = data.get("subagent_type", "unknown")

        # Log completion event
        completion_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "agent": agent_type,
            "event": "subagent_completed",
            "status": "completed",
            "type": "coordination"
        }

        # Append to coordination log
        with open("reports/coordination.jsonl", "a") as f:
            f.write(json.dumps(completion_entry) + "\n")

        return {
            "hookSpecificOutput": {
                "hookEventName": "SubagentStop",
                "additionalContext": f"Subagent completion logged: {agent_type}"
            }
        }

    except Exception:
        # Silent fail on errors
        return {
            "hookSpecificOutput": {
                "hookEventName": "SubagentStop",
                "additionalContext": "Completion tracking failed"
            }
        }

if __name__ == "__main__":
    result = track_completion()
    print(json.dumps(result))