from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from platformdirs import user_config_dir, user_state_dir

APP = "edge-assistant"
CFG_DIR = Path(user_config_dir(APP))
STATE_DIR = Path(user_state_dir(APP))
CFG_DIR.mkdir(parents=True, exist_ok=True)
STATE_DIR.mkdir(parents=True, exist_ok=True)

STATE_PATH = STATE_DIR / "state.json"

def _load() -> Dict[str, Any]:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            pass
    return {}

def _save(d: Dict[str, Any]) -> None:
    STATE_PATH.write_text(json.dumps(d, indent=2))

def get_thread_id(name: Optional[str]) -> Optional[str]:
    s = _load()
    if name:
        return s.get("threads", {}).get(name)
    return s.get("last_response_id")

def set_thread_id(resp_id: str, name: Optional[str]) -> None:
    s = _load()
    s.setdefault("threads", {})
    if name:
        s["threads"][name] = resp_id
    s["last_response_id"] = resp_id
    _save(s)

def kb_ids() -> List[str]:
    s = _load()
    return s.get("kb_file_ids", [])

def add_kb_ids(ids: List[str]) -> None:
    s = _load()
    prev = set(s.get("kb_file_ids", []))
    prev.update(ids)
    s["kb_file_ids"] = sorted(prev)
    _save(s)
