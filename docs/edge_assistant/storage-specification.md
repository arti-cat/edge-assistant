# Storage Specification

This document defines the storage architecture, data structures, and file management used by edge-assistant.

## Storage Architecture

### XDG Base Directory Compliance

edge-assistant follows XDG Base Directory Specification for cross-platform compatibility:

```python
# Primary paths (Linux/Mac)
CONFIG_DIR = ~/.config/edge-assistant/
DATA_DIR = ~/.local/share/edge-assistant/

# Fallback paths (when platformdirs unavailable)
CONFIG_DIR = ~/.config/
DATA_DIR = ~/.local/share/
```

### Storage Locations

| Data Type | Path | Purpose |
|-----------|------|---------|
| Thread State | `~/.local/share/edge-assistant/state.json` | Multimodal conversation threads |
| Configuration | `~/.config/edge-assistant/config.json` | User preferences (future) |
| Cache | `~/.cache/edge-assistant/` | Temporary data (future) |
| Logs | `~/.local/share/edge-assistant/logs/` | Error and debug logs (future) |

## Data Structures

### Main State File: `state.json`

```json
{
  "conversation_threads": {
    "thread-name": "resp_abc123...",
    "another-thread": "resp_def456..."
  },
  "kb_file_ids": [
    "file-abc123",
    "file-def456"  
  ],
  "multimodal_threads": {
    "thread-name": {
      "content_counts": {
        "text": 5,
        "image": 2, 
        "audio": 0,
        "video": 0,
        "file": 1
      },
      "last_activity": 1703123456,
      "response_id": "resp_xyz789",
      "model_used": "gpt-4o",
      "total_interactions": 8
    }
  },
  "vision_threads": {
    "legacy-thread": {
      "image_count": 3,
      "last_activity": 1703123456,
      "response_id": "resp_legacy123"
    }
  }
}
```

### Schema Definitions

#### Thread Metadata
```python
@dataclass
class ThreadMetadata:
    content_counts: Dict[str, int]  # Count by content type
    last_activity: int              # Unix timestamp
    response_id: str               # OpenAI response ID
    model_used: str                # Last model used
    total_interactions: int        # Total interaction count
```

#### Content Types
```python
SUPPORTED_CONTENT_TYPES = {
    "text": "Text-only conversations",
    "image": "Image analysis (JPEG, PNG, GIF, WebP)",
    "audio": "Audio analysis (future)",
    "video": "Video analysis (future)", 
    "file": "Document analysis (PDF, TXT, MD, code)"
}
```

## State Management Operations

### Core Functions: `state.py`

#### Thread Operations
```python
def get_multimodal_thread_info(name: str) -> Dict[str, Any]:
    """Get comprehensive thread metadata"""
    
def update_multimodal_thread(name: str, response_id: str, content_type: str, model: str) -> None:
    """Update thread with new interaction metadata"""
    
def clear_multimodal_thread(name: str) -> bool:
    """Remove specific thread and return success status"""
    
def cleanup_old_multimodal_threads(max_age_days: int = 7) -> int:
    """Auto-cleanup threads older than specified days"""
```

#### Legacy Compatibility
```python
def get_vision_thread_info(name: str) -> Dict[str, Any]:
    """Legacy vision thread compatibility wrapper"""
    
def update_vision_thread(name: str, response_id: str, increment_images: bool = True) -> None:
    """Legacy vision thread update wrapper"""
```

### File Operations

#### JSON Persistence
```python
def _load() -> Dict[str, Any]:
    """Load state from JSON file with error handling"""
    try:
        with open(state_file) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def _save(state: Dict[str, Any]) -> None:
    """Atomically save state to JSON file"""
    # Ensure directory exists
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    
    # Atomic write via temp file
    with open(f"{state_file}.tmp", 'w') as f:
        json.dump(state, f, indent=2)
    os.rename(f"{state_file}.tmp", state_file)
```

## Content Storage

### Local Files (Not Stored)
- **Images**: Processed as base64, not cached locally
- **Documents**: Uploaded to OpenAI, file ID stored
- **Audio/Video**: Future implementation

### OpenAI File Storage
```python
# File upload for knowledge base
def upload_for_kb(self, path) -> str:
    with open(path, "rb") as f:
        file = client.files.create(file=f, purpose="file_search")
    return file.id  # Stored in kb_file_ids array
```

### File ID Management
```python
def add_kb_ids(ids: List[str]) -> None:
    """Add file IDs to knowledge base registry"""
    s = _load()
    prev = set(s.get("kb_file_ids", []))
    prev.update(ids)
    s["kb_file_ids"] = sorted(prev)
    _save(s)
```

## Data Lifecycle

### Thread Lifecycle
1. **Creation**: Thread created on first interaction
2. **Updates**: Metadata updated after each interaction  
3. **Aging**: `last_activity` timestamp maintained
4. **Cleanup**: Auto-removed after 7 days of inactivity

### File Lifecycle
1. **Upload**: Files uploaded to OpenAI for analysis
2. **Storage**: File IDs stored locally for reuse
3. **Reuse**: Same file ID used for multiple queries
4. **Cleanup**: Manual cleanup only (files persist on OpenAI)

## Performance Considerations

### Storage Size
- **State file**: Typically < 100KB for active users
- **Memory usage**: Entire state loaded into memory
- **Write frequency**: Updated after each threaded interaction

### Optimization Strategies
```python
# Lazy loading
state = None
def _load():
    global state
    if state is None:
        state = load_from_disk()
    return state

# Batch updates (future optimization)
def batch_update_threads(updates: List[ThreadUpdate]):
    """Update multiple threads in single write operation"""
```

## Security & Privacy

### Data Protection
- **No sensitive content**: Only metadata and IDs stored locally
- **No API keys**: Stored in environment variables only
- **File contents**: Never cached locally, processed via OpenAI

### File Permissions
```bash
# State file permissions
chmod 600 ~/.local/share/edge-assistant/state.json

# Directory permissions  
chmod 700 ~/.local/share/edge-assistant/
```

## Backup & Recovery

### State Backup
```python
def backup_state(backup_path: str):
    """Create backup of current state"""
    shutil.copy2(state_file, backup_path)

def restore_state(backup_path: str):
    """Restore state from backup"""
    shutil.copy2(backup_path, state_file)
```

### Migration Support
```python
def migrate_legacy_threads():
    """Convert old vision threads to new multimodal format"""
    # Automatic migration handled in state.py
```

## Error Handling

### File System Errors
```python
try:
    state = _load()
except PermissionError:
    # Fallback to read-only mode
except json.JSONDecodeError:
    # Reset to empty state with user warning
```

### Recovery Strategies
- **Corrupted state**: Reset to empty state
- **Missing directories**: Auto-create on first write
- **Permission issues**: Graceful degradation

## Future Enhancements

### Planned Storage Features
- **Configuration management**: User preferences and defaults
- **Local caching**: Response caching for offline access
- **Export/import**: Thread backup and sharing
- **Analytics**: Usage statistics and insights