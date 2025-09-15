# pyConductor Command System

The command system provides 10 specialized commands that leverage Claude Code's native capabilities and the focused agent system for sophisticated development workflows.

## Command Categories

### Core Workflow Commands
- `/implement` - Full feature development using orchestrator agent
- `/review` - Security and quality assessment using reviewer agent
- `/track` - Simple task progress tracking
- `/background` - Out-of-loop agent delegation

### Context Engineering Commands (Dan's ADV2 Framework)
- `/prime-research` - Context priming for analysis tasks
- `/prime-implement` - Context priming for feature development
- `/prime-debug` - Context priming for bug fixing workflows
- `/prime-review` - Context priming for security/quality review

### Bundle Management Commands
- `/loadbundle` - Restore context from previous operation trails
- `/check-conductor` - System status and validation

## Core Workflow Commands

### /implement "feature description"
**Purpose**: Complete feature implementation using orchestrated agent workflows

**Workflow Pattern**:
```
orchestrator → researcher → coder → tester → reviewer → documenter
```

**Usage Examples**:
```bash
/implement "Add OAuth2 authentication with Google provider"
/implement "Implement password reset functionality with email verification"
/implement "Add real-time chat using WebSockets"
```

**Agent Flow**:
1. **orchestrator**: Coordinates the entire workflow
2. **researcher**: Analyzes existing patterns and requirements
3. **coder**: Implements following discovered patterns
4. **tester**: Creates comprehensive tests and validates functionality
5. **reviewer**: Security and quality assessment with fixes
6. **documenter**: Updates documentation and usage examples

**Resource Limits**:
- Maximum 30 minutes per workflow
- Maximum 5 agent delegations
- Automatic progress tracking
- Graceful failure recovery

### /review [path]
**Purpose**: Security and quality review using focused reviewer agent

**Default Scope**: Entire codebase if no path specified

**Usage Examples**:
```bash
/review                    # Review entire codebase
/review src/auth/          # Review specific directory
/review src/payment.py     # Review specific file
```

**Review Focus Areas**:
- Security vulnerabilities and risk assessment
- Code quality and maintainability issues
- Performance bottlenecks and optimization opportunities
- Best practice adherence and pattern consistency

**Output Priority System**:
- **Critical**: Immediate exploitation possible
- **High**: Likely exploitation with moderate effort
- **Medium**: Possible exploitation with significant effort
- **Low**: Theoretical or requires insider access

### /track "task description"
**Purpose**: Simple task tracking with progress monitoring

**Features**:
- Logs to `reports/tasks.jsonl`
- Automatic status tracking
- Integration with session context
- Progress monitoring across sessions

**Usage Examples**:
```bash
/track "Implement real-time observability dashboard"
/track "Add single-file executable agents"
/track "Create multi-agent orchestration system"
```

**Task Entry Structure**:
```json
{
    "timestamp": "2025-09-14T15:30:45.123456",
    "session_id": "uuid-session-id",
    "task": "Implement OAuth2 authentication",
    "status": "active",
    "type": "user_task"
}
```

### /background [agent] "task"
**Purpose**: Out-of-loop agent delegation for independent processing

**Security Features**:
- Agent name validation (must be: researcher, coder, reviewer, tester, documenter, orchestrator)
- Task complexity validation (10-200 characters)
- Safe operation pattern matching
- Dangerous task pattern blocking

**Usage Examples**:
```bash
/background researcher "analyze microservices architecture patterns"
/background documenter "create comprehensive API documentation"
/background reviewer "identify security vulnerabilities in authentication module"
```

**Approved Task Patterns**:
- `analyze|research|document|review` + description
- `implement` + specific feature description (50-150 chars)
- `test` + specific test scope description
- `fix` + specific bug description

**Blocked Task Patterns**:
- System commands or shell execution requests
- Requests involving credentials, secrets, or sensitive data
- Overly complex or vague task descriptions
- Tasks requesting file system access outside project scope

**Background Processing Benefits**:
- Independent execution without context pollution
- Primary context window remains clean
- Full task execution capability maintained
- Security boundaries enforced

## Context Engineering Commands

### /prime-research [focus]
**Purpose**: Context priming for codebase analysis tasks

**Optimizes For**:
- Pattern recognition and analysis workflows
- Requirements gathering tasks
- Technology research and compatibility assessment
- Risk and impact assessment

**Usage Examples**:
```bash
/prime-research authentication    # Prime for auth analysis
/prime-research database         # Prime for DB analysis
/prime-research security         # Prime for security assessment
```

### /prime-implement [feature]
**Purpose**: Context priming for feature development workflows

**Optimizes For**:
- Implementation planning and execution
- Code integration with existing systems
- Test-ready structure development
- Pattern adherence and consistency

**Usage Examples**:
```bash
/prime-implement oauth2          # Prime for OAuth2 development
/prime-implement websockets      # Prime for WebSocket implementation
/prime-implement payment         # Prime for payment system development
```

### /prime-debug [issue]
**Purpose**: Context priming for bug fixing workflows

**Optimizes For**:
- Error analysis and reproduction
- Root cause identification
- Minimal, targeted fixes
- Testing and verification

**Usage Examples**:
```bash
/prime-debug session-timeout     # Prime for session debugging
/prime-debug memory-leak        # Prime for memory issue analysis
/prime-debug authentication     # Prime for auth bug fixes
```

### /prime-review [area]
**Purpose**: Context priming for security and quality review

**Optimizes For**:
- Security vulnerability identification
- Quality assessment workflows
- Performance optimization
- Best practice validation

**Usage Examples**:
```bash
/prime-review security          # Prime for security review
/prime-review performance       # Prime for performance analysis
/prime-review quality           # Prime for quality assessment
```

## Bundle Management Commands

### /loadbundle [path]
**Purpose**: Restore context from previous operation trails (Dan's ADV2 pattern)

**Context Bundle Features**:
- Session-specific operation trails
- Tool usage and file modification history
- Agent delegation sequences
- Automatic context reconstruction

**Bundle Auto-Suggestion**:
- Recent bundles offered at session start
- Timestamp-based relevance scoring
- Activity-based bundle ranking

**Usage Examples**:
```bash
/loadbundle                                    # Auto-suggest recent bundles
/loadbundle reports/context-bundles/latest     # Load specific bundle
/loadbundle reports/context-bundles/session-123_bundle.jsonl
```

**Bundle Structure**:
```json
{
    "timestamp": "2025-09-14T15:30:45.123456",
    "session_id": "uuid-session-id",
    "tool": "Edit",
    "action": "edit",
    "file": "src/auth.py",
    "summary": "edit: auth.py",
    "context_type": "file_modification"
}
```

### /check-conductor
**Purpose**: System status validation and health check

**Validation Areas**:
- Agent system availability and configuration
- Hook system status and functionality
- Permission system validation
- Report system health
- Context bundle integrity
- Background task status

**Health Check Output**:
```bash
pyConductor System Status:
✅ 6 Agents: researcher, coder, reviewer, tester, documenter, orchestrator
✅ 6 Hooks: All lifecycle events configured and executable
✅ Permissions: 81 allow patterns, 18 deny patterns active
✅ Reports: activity.jsonl (150 entries), coordination.jsonl (25 entries)
✅ Context Bundles: 12 bundles available for restoration
✅ Background Tasks: 0 active, 3 completed today
```

**Troubleshooting Information**:
- Reports missing agents or invalid configurations
- Identifies permission conflicts or syntax errors
- Validates hook executable permissions and functionality
- Checks report file accessibility and structure
- Verifies context bundle integrity and availability

## Command Integration Features

### Hook System Integration
All commands integrate with the comprehensive hook system:
- **SessionStart**: Commands available in context prime
- **PreToolUse**: Security filtering for all command operations
- **PostToolUse**: Activity logging and agent coordination tracking
- **UserPromptSubmit**: Task tracking detection and logging

### Security Integration
Commands respect the granular permissions system:
```json
{
  "permissions": {
    "allow": [
      "Read(./docs/**)",
      "Write(./docs/**)",
      "Edit(./src/**/*.py)",
      "Bash(git:*)"
    ],
    "deny": [
      "Read(./.env)",
      "Write(./secrets/**)",
      "Bash(rm -rf /*)"
    ]
  }
}
```

### Logging Integration
All command usage is comprehensively logged:
- Activity logging to `reports/activity.jsonl`
- Agent coordination to `reports/coordination.jsonl`
- Task tracking to `reports/tasks.jsonl`
- Context bundle creation for session restoration

## Advanced Command Patterns

### Chained Workflows
```bash
# Sequential command chaining
/track "Implement authentication system"
/implement "OAuth2 authentication with Google provider"
/review src/auth/
/background documenter "create OAuth2 integration guide"
```

### Context-Aware Operations
```bash
# Context priming followed by focused work
/prime-implement oauth2
Use coder agent to "implement OAuth2 following primed patterns"
Use tester agent to "create OAuth2 integration tests"
```

### Background Processing Workflows
```bash
# Parallel processing pattern
/background researcher "analyze existing authentication patterns"
/background documenter "update API documentation structure"
# Continue with foreground work while background tasks execute
/implement "session management improvements"
```

## Error Handling & Recovery

### Command Validation
- Syntax validation before execution
- Agent availability verification
- Resource constraint checking
- Security pattern validation

### Graceful Failures
- Clear error messages with suggested fixes
- Automatic fallback to safe operations
- Context preservation on failures
- Recovery guidance for common issues

### Resource Management
- Timeout enforcement (30 minutes max for `/implement`)
- Agent delegation limits (5 agents max per workflow)
- Background task limits and cleanup
- Memory and context optimization

## Command Learning Path

### Hands-On Experience
Master the command system through structured examples:

#### Entry Level
- `examples/01-basic-agent-usage/` - Basic agent delegation patterns
- `examples/02-code-generation/` - Implementation command usage

#### Intermediate
- `examples/03-security-review/` - `/review` command in depth
- `examples/05-multi-agent-collaboration/` - Sequential command workflows

#### Advanced
- `examples/04-full-workflow/` - `/implement` command orchestration
- `examples/06-background-delegation/` - `/background` command optimization
- `examples/07-context-restoration/` - `/loadbundle` and context management

### Real-World Command Usage
The command system excels in:
- **Rapid Prototyping**: `/implement` for quick feature development
- **Quality Assurance**: `/review` for security and quality validation
- **Project Management**: `/track` for development task coordination
- **Performance Optimization**: `/background` for parallel processing
- **Team Coordination**: `/loadbundle` for shared context restoration

The command system provides a comprehensive, secure, and intelligent interface for sophisticated multi-agent development workflows while maintaining simplicity and clarity for users.