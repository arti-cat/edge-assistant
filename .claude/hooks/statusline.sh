#!/bin/bash
# Real-time status line for pyConductor (Dan's pattern)

# Get current directory info
PROJECT_NAME="pyConductor"
BRANCH=$(git branch --show-current 2>/dev/null || echo "main")

# Get git status count
GIT_CHANGES=$(git status --porcelain 2>/dev/null | wc -l)
if [ "$GIT_CHANGES" -eq 0 ]; then
    GIT_STATUS="✓"
else
    GIT_STATUS="${GIT_CHANGES}Δ"
fi

# Get active tasks count
ACTIVE_TASKS=0
if [ -f "reports/tasks.jsonl" ]; then
    ACTIVE_TASKS=$(grep -c '"status":"active"' reports/tasks.jsonl 2>/dev/null || echo 0)
fi

# Get recent agent activity
RECENT_AGENTS=""
if [ -f "reports/coordination.jsonl" ]; then
    RECENT_AGENTS=$(tail -3 reports/coordination.jsonl 2>/dev/null | \
                   grep -o '"delegated_agent":"[^"]*"' | \
                   cut -d'"' -f4 | \
                   tail -1 2>/dev/null || echo "")
fi

# Get background task count (rough estimate)
BG_TASKS=0
if [ -f "reports/coordination.jsonl" ]; then
    BG_TASKS=$(tail -10 reports/coordination.jsonl 2>/dev/null | \
              grep -c '"is_background":true' 2>/dev/null || echo "0")
    # Ensure it's a valid number
    if ! [[ "$BG_TASKS" =~ ^[0-9]+$ ]]; then
        BG_TASKS=0
    fi
fi

# Build status line components
STATUS_PARTS=()

# Project and branch
STATUS_PARTS+=("🎯 $PROJECT_NAME:$BRANCH")

# Git status
STATUS_PARTS+=("$GIT_STATUS")

# Active tasks
if [ "$ACTIVE_TASKS" -gt 0 ]; then
    STATUS_PARTS+=("${ACTIVE_TASKS}📋")
fi

# Recent agent
if [ -n "$RECENT_AGENTS" ] && [ "$RECENT_AGENTS" != "unknown" ]; then
    STATUS_PARTS+=("🤖${RECENT_AGENTS}")
fi

# Background tasks
if [ "$BG_TASKS" -gt 0 ]; then
    STATUS_PARTS+=("⚡${BG_TASKS}")
fi

# Timestamp
TIME=$(date +"%H:%M")
STATUS_PARTS+=("⏰$TIME")

# Join all parts with " | "
IFS=" | "
echo "${STATUS_PARTS[*]}"