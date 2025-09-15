#!/usr/bin/env python3
"""
Dynamic context priming using Dan's R&D framework
Triggers: SessionStart
"""

import json
import sys
import subprocess
import os
from datetime import datetime
from pathlib import Path

def get_git_status():
    """Get concise git status"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'],
                               capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().splitlines()
            return f"{len(lines)} changes" if lines else "Working tree clean"
    except:
        pass
    return "Unknown"

def get_active_tasks():
    """Get active tasks from task tracking"""
    try:
        # Check new task tracking system first
        if Path("reports/tasks.jsonl").exists():
            with open("reports/tasks.jsonl", "r") as f:
                tasks = [json.loads(line) for line in f if line.strip()]
                active = [t for t in tasks if t.get("status") == "active"]
                return len(active)

        # Fall back to task-log.ndjson for session-based tracking
        if Path("reports/task-log.ndjson").exists():
            with open("reports/task-log.ndjson", "r") as f:
                lines = list(f)
                if lines:
                    # Get recent task events from current session
                    recent_tasks = [json.loads(line) for line in lines[-10:] if line.strip()]
                    # Simple heuristic: if we have recent session activity, consider it "active"
                    return 1 if recent_tasks else 0
    except:
        pass
    return 0

def check_project_structure():
    """Check key directories"""
    key_dirs = ['.claude', 'src', 'docs', 'tests', 'reports']
    existing = [d for d in key_dirs if Path(d).exists()]
    return existing

def get_recent_activity():
    """Get recent file activity from activity.jsonl"""
    try:
        if Path("reports/activity.jsonl").exists():
            with open("reports/activity.jsonl", "r") as f:
                activities = [json.loads(line) for line in f if line.strip()]
                if activities:
                    # Get last 5 unique files edited
                    recent_files = []
                    for activity in reversed(activities[-10:]):
                        if activity.get("file") and activity.get("success"):
                            filename = Path(activity["file"]).name
                            if filename not in recent_files:
                                recent_files.append(filename)
                            if len(recent_files) >= 5:
                                break
                    return recent_files
    except:
        pass
    return []

def get_recent_agents():
    """Get recent agent delegations from coordination.jsonl"""
    try:
        if Path("reports/coordination.jsonl").exists():
            with open("reports/coordination.jsonl", "r") as f:
                coords = [json.loads(line) for line in f if line.strip()]
                if coords:
                    # Get last 3 unique agents used
                    recent_agents = []
                    for coord in reversed(coords[-5:]):
                        agent = coord.get("delegated_agent")
                        if agent and agent != "unknown" and agent not in recent_agents:
                            recent_agents.append(agent)
                        if len(recent_agents) >= 3:
                            break
                    return recent_agents
    except:
        pass
    return []

def get_background_tasks():
    """Get active background tasks"""
    try:
        if Path("reports/coordination.jsonl").exists():
            with open("reports/coordination.jsonl", "r") as f:
                coords = [json.loads(line) for line in f if line.strip()]
                if coords:
                    # Count recent background tasks (last hour)
                    from datetime import datetime, timedelta
                    one_hour_ago = datetime.now() - timedelta(hours=1)

                    background_tasks = []
                    for coord in coords:
                        if coord.get("is_background") and coord.get("status") == "initiated":
                            task_time = datetime.fromisoformat(coord["timestamp"])
                            if task_time > one_hour_ago:
                                agent = coord.get("delegated_agent", "unknown")
                                background_tasks.append(agent)

                    return len(background_tasks), background_tasks[:2]  # count, first 2 agents
    except:
        pass
    return 0, []

def get_session_context():
    """Get context from previous sessions"""
    try:
        if Path("reports/task-log.ndjson").exists():
            with open("reports/task-log.ndjson", "r") as f:
                lines = list(f)
                if len(lines) > 5:
                    # Look for session patterns or significant events
                    recent_events = [json.loads(line) for line in lines[-20:] if line.strip()]

                    # Simple heuristic: if we have multiple tool uses, there was active work
                    tool_uses = [e for e in recent_events if e.get("event") == "tool_use"]
                    if len(tool_uses) > 3:
                        return "Previous session: active development work"
                    elif tool_uses:
                        return "Previous session: light development activity"
                    else:
                        return "Previous session: planning/discussion"
    except:
        pass
    return None

def prime_context():
    """Load essential project context dynamically"""

    git_status = get_git_status()
    active_tasks = get_active_tasks()
    existing_dirs = check_project_structure()
    recent_files = get_recent_activity()
    recent_agents = get_recent_agents()
    background_count, background_agents = get_background_tasks()
    session_context = get_session_context()

    # Build context with progressive detail
    context_parts = [
        f"🎯 pyConductor Session Started | {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Git Status: {git_status}",
    ]

    # Add recent activity if available
    if recent_files:
        files_str = ", ".join(recent_files[:3])
        if len(recent_files) > 3:
            files_str += f" (+{len(recent_files)-3} more)"
        context_parts.append(f"Recent Activity: {files_str}")

    # Add recent agent usage if available
    if recent_agents:
        agents_str = ", ".join(recent_agents)
        context_parts.append(f"Recent Agents: {agents_str}")

    # Add background tasks if any
    if background_count > 0:
        bg_str = f"{background_count} background task{'s' if background_count > 1 else ''}"
        if background_agents:
            bg_str += f" ({', '.join(background_agents)})"
        context_parts.append(f"Background Tasks: {bg_str}")

    # Add session continuity if available
    if session_context:
        context_parts.append(f"Session Context: {session_context}")

    context_parts.extend([
        f"Project: Multi-agent development framework with simplified workflows",
        f"Agents: 6 focused agents available via Task tool delegation",
        f"Directories: {', '.join(existing_dirs)}",
        "",
        f"Active Tasks: {active_tasks}",
        "",
        "Key Commands:",
        "- /implement \"feature\" - Full feature development workflow",
        "- /review [path] - Security and quality assessment",
        "- /track \"task\" - Simple task progress tracking",
        "- /background [agent] \"task\" - Out-of-loop agent delegation",
        "",
        "Agent Delegation Patterns:",
        "- Use orchestrator agent for complex workflows",
        "- Use specific agents directly for focused tasks",
        "- Use Task tool for true background delegation",
        "",
        "Ready for focused, performant agent workflows."
    ])

    context = "\n".join(context_parts)

    # Return context as JSON hook output instead of printing
    return {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context
        }
    }

if __name__ == "__main__":
    result = prime_context()
    if result:
        print(json.dumps(result))
    else:
        # Fallback JSON output
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "Session context loading completed"
            }
        }))