#!/usr/bin/env python3
"""
Session cleanup and reporting (Dan's lifecycle pattern)
Triggers: SessionEnd
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def session_cleanup():
    """Handle session end cleanup and reporting"""
    try:
        data = json.load(sys.stdin)
        session_id = data.get("session_id")
        cwd = data.get("cwd", "")
        reason = data.get("reason", "unknown")

        # Create cleanup report
        cleanup_report = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "reason": reason,
            "cwd": cwd,
            "type": "session_end"
        }

        # Log session end
        Path("reports").mkdir(exist_ok=True)
        with open("reports/activity.jsonl", "a") as f:
            f.write(json.dumps(cleanup_report) + "\n")

        # Generate session summary if bundle exists
        bundle_file = f"reports/context-bundles/{session_id}_bundle.jsonl"
        if Path(bundle_file).exists():
            try:
                with open(bundle_file, "r") as f:
                    entries = [json.loads(line) for line in f if line.strip()]

                summary = {
                    "session_id": session_id,
                    "duration": f"{len(entries)} operations",
                    "tools_used": list(set(entry.get("tool", "unknown") for entry in entries)),
                    "files_modified": list(set(entry.get("file") for entry in entries if entry.get("file"))),
                        "reason": reason
                    }

                # Store summary info for hook output instead of printing
                summary_text = f"Session Summary ({reason}): {len(entries)} operations, Tools: {', '.join(summary['tools_used'][:5])}"
                if summary['files_modified']:
                    clean_files = [f for f in summary['files_modified'] if f]
                    if clean_files:
                        summary_text += f", {len(clean_files)} files modified"

            except Exception:
                pass  # Silent fail on summary generation

        # Return success with summary if available
        context_message = f"Session ended: {reason}. Cleanup completed."
        if 'summary_text' in locals():
            context_message = summary_text

        return {
            "hookSpecificOutput": {
                "hookEventName": "SessionEnd",
                "additionalContext": context_message
            }
        }

    except Exception:
        # Silent cleanup on error
        return {
            "hookSpecificOutput": {
                "hookEventName": "SessionEnd",
                "additionalContext": "Session ended - cleanup completed"
            }
        }

if __name__ == "__main__":
    result = session_cleanup()
    print(json.dumps(result))