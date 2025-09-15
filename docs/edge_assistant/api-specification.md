# API Specification

This document outlines the API interfaces and external service integrations used by edge-assistant.

## OpenAI Responses API Integration

### Primary Interface: `engine.py`

The tool is built on OpenAI's latest Responses API for optimal threading and multimodal support.

#### Core Method: `analyze_multimodal_content()`

```python
def analyze_multimodal_content(
    self, 
    content_path: str = None, 
    user_prompt: str = "", 
    system_prompt: Optional[str] = None, 
    model: Optional[str] = None, 
    previous_response_id: Optional[str] = None, 
    content_type: str = "auto"
) -> Response
```

**Parameters:**
- `content_path`: Path to content file (None for text-only)
- `user_prompt`: User's question/instruction
- `system_prompt`: Optional system context
- `model`: Model override (auto-selected by default)
- `previous_response_id`: For threading context
- `content_type`: auto/text/image/audio/video/file

**Returns:** OpenAI Response object with threading support

### Content Type Handling

#### Text Analysis
```python
# Responses API call
response = client.responses.create(
    model=model or "gpt-4o-mini",
    input=user_prompt,
    instructions=system_prompt,
    previous_response_id=previous_response_id,
    max_output_tokens=1000
)
```

#### Image Analysis
```python
# Multimodal input format for Responses API
input_content = [{
    "role": "user",
    "content": [{
        "type": "input_image",
        "image_url": f"data:{mime_type};base64,{base64_image}"
    }, {
        "type": "input_text", 
        "text": user_prompt
    }]
}]

response = client.responses.create(
    model="gpt-4o",
    input=input_content,
    instructions=system_prompt,
    previous_response_id=previous_response_id,
    max_output_tokens=1000
)
```

#### File Analysis
```python
# Upload file for analysis
file = client.files.create(file=f, purpose="file_search")

response = client.responses.create(
    model="gpt-4o",
    input=user_prompt,
    attachments=[{
        "file_id": file.id, 
        "tools": [{"type": "file_search"}]
    }],
    instructions=system_prompt,
    previous_response_id=previous_response_id,
    max_output_tokens=1000
)
```

### Model Selection Strategy

| Content Type | Default Model | Capabilities |
|--------------|---------------|--------------|
| text | gpt-4o-mini | Fast text processing |
| image | gpt-4o | Vision + reasoning |
| file | gpt-4o | Document analysis + file search |
| audio | gpt-4o | Future: Audio analysis |
| video | gpt-4o | Future: Video analysis |

### Error Handling

```python
try:
    response = client.responses.create(...)
    return response
except OpenAIError as e:
    # Log error details
    # Fallback to Chat Completions if needed
    # Return user-friendly error message
```

## Web Research API

### Search Integration
Uses OpenAI's built-in web search tool via Responses API:

```python
response = client.responses.create(
    model="gpt-4o",
    input=query,
    tools=[{"type": "web_search"}]
)
```

## Knowledge Base API

### File Upload Interface
```python
def upload_for_kb(self, path) -> str:
    with open(path, "rb") as f:
        file = client.files.create(file=f, purpose="file_search")
    return file.id
```

### Vector Search
Utilizes OpenAI's file search capability:
```python
response = client.responses.create(
    model=model,
    input=query,
    attachments=[{"file_id": file_id, "tools": [{"type": "file_search"}]}]
)
```

## Rate Limiting & Optimization

### Token Management
- **Image Analysis**: ~1000 tokens per image (varies by resolution)
- **Text Analysis**: Input + output tokens counted
- **File Analysis**: Document size + query tokens
- **Max Output**: 1000 tokens per response (configurable)

### Caching Strategy
- **Thread State**: Server-side via Responses API
- **File IDs**: Local storage for reuse
- **Model Responses**: No local caching (relies on OpenAI)

## Authentication

### API Key Management
```python
# Environment variable (traditional)
OPENAI_API_KEY="sk-..."

# .env file (recommended)
echo 'OPENAI_API_KEY="sk-..."' > .env
```

### Client Initialization
```python
def _get_client(self):
    if not self._client_inst:
        self._client_inst = OpenAI()  # Auto-loads from env
    return self._client_inst
```

## Future API Extensions

### Audio Analysis (Planned)
```python
# When supported by Responses API
response = client.responses.create(
    model="gpt-4o",
    input=[{
        "role": "user",
        "content": [{
            "type": "input_audio",
            "audio_url": f"data:audio/wav;base64,{base64_audio}"
        }, {
            "type": "input_text",
            "text": user_prompt
        }]
    }]
)
```

### Video Analysis (Planned)
```python
# When supported by Responses API
response = client.responses.create(
    model="gpt-4o",
    input=[{
        "role": "user", 
        "content": [{
            "type": "input_video",
            "video_url": f"data:video/mp4;base64,{base64_video}"
        }, {
            "type": "input_text",
            "text": user_prompt
        }]
    }]
)
```