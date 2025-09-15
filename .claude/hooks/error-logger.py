#!/usr/bin/env python3
"""
Simple error logger for hook debugging
Used by hooks to log errors without breaking workflow
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def log_error(hook_name, error_details, silent=True):
    """Log hook errors to dedicated error log"""
    try:
        Path("reports").mkdir(exist_ok=True)

        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "hook": hook_name,
            "error": str(error_details),
            "type": "hook_error"
        }

        with open("reports/hook-errors.jsonl", "a") as f:
            f.write(json.dumps(error_entry) + "\n")

    except Exception:
        # Even error logging can fail - maintain silence
        pass

if __name__ == "__main__":
    # Can be called directly for testing
    if len(sys.argv) > 2:
        log_error(sys.argv[1], sys.argv[2])
    else:
        print("Usage: error-logger.py <hook_name> <error_message>")