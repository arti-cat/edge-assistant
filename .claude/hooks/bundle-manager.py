#!/usr/bin/env python3
"""
Bundle manager for context restoration suggestions (Dan's ADV2 pattern)
Triggers: SessionStart
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

def find_recent_bundles(hours=24):
    """Find context bundles from the last N hours"""
    bundles_dir = Path("reports/context-bundles")
    if not bundles_dir.exists():
        return []

    cutoff_time = datetime.now() - timedelta(hours=hours)
    recent_bundles = []

    for bundle_file in bundles_dir.glob("*_bundle.jsonl"):
        try:
            # Get file modification time
            file_time = datetime.fromtimestamp(bundle_file.stat().st_mtime)
            if file_time > cutoff_time:
                # Read first few entries to get bundle info
                with open(bundle_file, 'r') as f:
                    lines = list(f)[:5]  # First 5 operations
                    if lines:
                        entries = [json.loads(line) for line in lines if line.strip()]
                        if entries:
                            bundle_info = {
                                "file": str(bundle_file),
                                "session_id": entries[0].get("session_id"),
                                "timestamp": entries[0].get("timestamp"),
                                "operation_count": len(lines),
                                "summary": entries[0].get("summary", "Unknown operation"),
                                "file_time": file_time.strftime("%Y-%m-%d %H:%M")
                            }
                            recent_bundles.append(bundle_info)
        except (OSError, json.JSONDecodeError, IndexError):
            continue

    # Sort by file time, most recent first
    return sorted(recent_bundles, key=lambda x: x["file_time"], reverse=True)

def get_bundle_summary(bundle_file):
    """Get a summary of operations in the bundle"""
    try:
        with open(bundle_file, 'r') as f:
            lines = list(f)
            if not lines:
                return "Empty bundle"

        entries = [json.loads(line) for line in lines if line.strip()]
        if not entries:
            return "No valid operations"

        # Count operation types
        reads = sum(1 for e in entries if e.get("action") == "read")
        writes = sum(1 for e in entries if e.get("action") in ["write", "edit"])
        commands = sum(1 for e in entries if e.get("action") == "command")
        delegations = sum(1 for e in entries if e.get("action") == "delegate")

        summary_parts = []
        if reads > 0:
            summary_parts.append(f"{reads} reads")
        if writes > 0:
            summary_parts.append(f"{writes} modifications")
        if commands > 0:
            summary_parts.append(f"{commands} commands")
        if delegations > 0:
            summary_parts.append(f"{delegations} delegations")

        return ", ".join(summary_parts) if summary_parts else "Unknown operations"

    except (OSError, json.JSONDecodeError):
        return "Error reading bundle"

def suggest_bundles():
    """Check for recent bundles and suggest loading if relevant"""
    try:
        # Only suggest if we have recent bundles
        recent_bundles = find_recent_bundles(hours=24)
        if not recent_bundles:
            return

        # Check if this is a fresh session (no recent activity)
        activity_file = Path("reports/activity.jsonl")
        session_activity = False

        if activity_file.exists():
            # Check for very recent activity (last 5 minutes)
            five_minutes_ago = datetime.now() - timedelta(minutes=5)
            with open(activity_file, 'r') as f:
                lines = list(f)[-5:]  # Check last 5 entries
                for line in lines:
                    if line.strip():
                        try:
                            entry = json.loads(line)
                            entry_time = datetime.fromisoformat(entry["timestamp"].replace('Z', '+00:00'))
                            if entry_time.replace(tzinfo=None) > five_minutes_ago:
                                session_activity = True
                                break
                        except (json.JSONDecodeError, KeyError, ValueError):
                            continue

        # Only suggest if no recent activity (fresh session)
        if not session_activity and recent_bundles:
            # Build bundle suggestion text for JSON output
            bundle_text = "🔄 Recent Context Bundles Available:\n   Use /loadbundle to restore previous work context\n\n"

            for i, bundle in enumerate(recent_bundles[:3], 1):  # Show top 3
                summary = get_bundle_summary(bundle["file"])
                session_short = bundle["session_id"][:8] if bundle["session_id"] else "unknown"
                bundle_text += f"   {i}. {bundle['file_time']} - {session_short} ({summary})\n"

            if len(recent_bundles) > 3:
                bundle_text += f"   ... and {len(recent_bundles) - 3} more\n"

            bundle_text += f"\n   Example: /loadbundle {recent_bundles[0]['file']}\n"

            return {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": bundle_text
                }
            }

        # No suggestions needed
        return None

    except Exception:
        # Silent fail - don't break workflow
        return None

if __name__ == "__main__":
    result = suggest_bundles()
    if result:
        print(json.dumps(result))
    else:
        # Output empty JSON for hook compliance
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "Bundle check completed"
            }
        }))