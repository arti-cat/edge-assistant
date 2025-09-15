#!/usr/bin/env python3
"""
Hook-based agent coordination (Dan's pattern)
Triggers: PostToolUse (when Task tool used)
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def coordinate_agents():
    """Log agent coordination events"""
    try:
        data = json.load(sys.stdin)

        # Only process Task tool usage (agent delegation)
        if data.get("tool_name") != "Task":
            return None

        # Extract agent delegation details
        task_input = data.get("tool_input", {})
        task_prompt = task_input.get("prompt", "")

        # Extract agent name from subagent_type parameter
        agent_name = task_input.get("subagent_type", "unknown")
        task_type = "agent_delegation"
        is_background = False

        # Detect background task delegation
        if "background processing" in task_prompt.lower() or "reports/background/" in task_prompt:
            task_type = "background_delegation"
            is_background = True

        # Create reports directory
        Path("reports").mkdir(exist_ok=True)

        # Log agent delegation event
        coord_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": data.get("session_id"),
            "delegated_agent": agent_name,
            "task_prompt": task_prompt[:100] + "..." if len(task_prompt) > 100 else task_prompt,
            "task_type": task_type,
            "status": "initiated",
            "is_background": is_background,
            "type": "coordination"
        }

        # Log to coordination file
        with open("reports/coordination.jsonl", "a") as f:
            f.write(json.dumps(coord_entry) + "\n")

        # Return success for Task tool usage
        return {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": f"Agent coordination logged: {agent_name} task"
            }
        }

    except Exception:
        # Silent fail on errors
        return None

if __name__ == "__main__":
    result = coordinate_agents()
    if result:
        print(json.dumps(result))
    else:
        # Output empty JSON for hook compliance
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": "Coordination check completed"
            }
        }))