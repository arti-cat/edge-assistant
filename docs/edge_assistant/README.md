# Technical Documentation

This directory contains comprehensive technical specifications for the edge-assistant project.

## Documentation Index

### 📋 [API Specification](api-specification.md)
- OpenAI Responses API integration patterns
- Multimodal content processing
- Rate limiting and optimization strategies
- Authentication and error handling
- Future API extensions (audio/video)

### 🖥️ [CLI Specification](cli-specification.md)
- Complete command reference and usage examples
- Threading workflows and context management
- Knowledge base operations (kb-index, kb-list, kb-research)
- File editing and agent functionality
- Advanced usage patterns and integration examples

### 🏗️ [Architecture Overview](architecture-overview.md)  
- System architecture and component interactions
- Design principles and patterns
- Data flow diagrams
- Performance characteristics
- Security architecture
- Extension points and future roadmap

### 🗄️ [Storage Specification](storage-specification.md)
- XDG-compliant file storage architecture
- Data structures and file formats
- State management operations
- Performance considerations
- Backup and recovery procedures

### 💾 [Database Specification](database-specification.md)
- JSON-based data models and relationships
- Query patterns and operations
- Data integrity and validation
- Performance optimization strategies
- Migration and versioning support

## Quick Reference

### Core Components
- **`cli.py`** - Typer-based CLI with unified multimodal commands
- **`engine.py`** - OpenAI Responses API wrapper with threading support  
- **`state.py`** - XDG-compliant JSON storage with multimodal thread tracking
- **`tools.py`** - Utility functions for diffs, extraction, and function tools

### Key Design Patterns
- **Unified Multimodal Interface** - Single `analyze` command for all content types
- **Threading-First Architecture** - Server-side state via Responses API  
- **Safety-First Design** - Dry-run defaults with explicit approval workflows
- **Future-Ready** - Architecture prepared for audio/video capabilities

### Data Flow
1. **User Input** → CLI command with optional content file
2. **Content Detection** → Auto-detect type (text/image/file) and select model
3. **API Integration** → OpenAI Responses API with threading support
4. **State Management** → Local metadata tracking with content type breakdown
5. **Response Display** → Formatted markdown output with rich formatting

## Architecture Highlights

### Multimodal Threading
```json
{
  "thread-name": {
    "content_counts": {"text": 5, "image": 2, "file": 1},
    "total_interactions": 8,
    "last_activity": 1703123456,
    "response_id": "resp_abc123",
    "model_used": "gpt-4o"
  }
}
```

### Content Type Processing
| Type | Format | Model | API Pattern |
|------|--------|-------|-------------|
| Text | String | gpt-4o-mini | Direct input |
| Image | Base64 | gpt-4o | Multimodal array |
| File | Upload | gpt-4o | File attachment |
| Audio | Base64 | gpt-4o | Future: Multimodal |
| Video | Base64 | gpt-4o | Future: Multimodal |

### Error Handling Strategy
- **Layered Approach** - API, Command, and State level error handling
- **Graceful Degradation** - Fallback to legacy APIs when needed
- **User-Friendly** - Clear error messages with suggested actions
- **State Recovery** - Auto-repair corrupted configuration files

## Development Guidelines

### Adding New Features
1. **API Integration** - Follow existing Responses API patterns
2. **State Management** - Update multimodal thread tracking 
3. **CLI Interface** - Maintain consistency with existing commands
4. **Documentation** - Update relevant specification documents

### Testing Approach
- **CLI Testing** - Typer CliRunner for command validation
- **API Mocking** - Mock OpenAI responses for unit tests
- **State Testing** - JSON file manipulation and consistency checks
- **Integration Testing** - End-to-end workflow validation

### Performance Considerations
- **State File Size** - Monitor growth with thread count
- **API Latency** - Optimize for typical usage patterns  
- **Memory Usage** - Lazy loading and efficient data structures
- **Error Recovery** - Fast recovery from API or storage failures

## Contributing

When modifying the architecture:

1. **Update Specifications** - Keep documentation synchronized with code changes
2. **Maintain Compatibility** - Preserve existing CLI interfaces and data formats
3. **Test Thoroughly** - Validate both new features and existing functionality
4. **Document Changes** - Update relevant specification documents

## Version History

- **v1.0** - Initial unified multimodal architecture
- **v0.9** - Legacy image analysis with basic threading
- **v0.8** - Text-only analysis with web research
- **v0.7** - Basic CLI with file editing capabilities