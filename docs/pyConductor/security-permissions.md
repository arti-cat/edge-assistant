# pyConductor Security & Permissions System

The security system implements enterprise-grade protection through multi-layer validation, credential sanitization, and granular permissions while maintaining workflow flexibility.

## Security Architecture

### Multi-Layer Protection
1. **Permission Boundaries** - File and tool access control
2. **Command Filtering** - Pattern-based security validation
3. **Credential Sanitization** - Automatic sensitive data redaction
4. **Resource Constraints** - Timeouts and delegation limits
5. **Agent Boundaries** - Role-based access restrictions

### Security Philosophy
- **Fail-Safe Defaults** - Allow operations by default, block explicitly dangerous ones
- **Defense in Depth** - Multiple validation layers prevent bypass
- **Context Preservation** - Security doesn't break workflows
- **Transparent Operation** - Clear security decisions with reasons

## Permission System

### Configuration Location
Permissions are defined in `.claude/settings.json` with allow/deny patterns:

```json
{
  "permissions": {
    "allow": [
      // File access patterns
      "Read(./src/**/*.py)",
      "Read(./docs/**)",
      "Write(./docs/**)",
      "Edit(./src/**/*.py)",

      // Tool access patterns
      "Bash(git:*)",
      "Bash(npm run:*)",
      "Bash(python:*)"
    ],
    "deny": [
      // Sensitive files
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",

      // Dangerous operations
      "Bash(rm -rf /*)",
      "Bash(sudo rm:*)",
      "Bash(chmod 777:*)"
    ]
  }
}
```

### Allow Patterns (81 Active Patterns)

#### File Type Access
```json
"Read(./src/**/*.py)",      // Python source files
"Read(./src/**/*.js)",      // JavaScript files
"Read(./src/**/*.ts)",      // TypeScript files
"Read(./src/**/*.tsx)",     // React TypeScript files
"Read(./src/**/*.java)",    // Java files
"Read(./src/**/*.go)",      // Go files
"Read(./src/**/*.rs)",      // Rust files
"Read(./src/**/*.cpp)",     // C++ files
"Read(./src/**/*.c)",       // C files
"Read(./src/**/*.h)"        // Header files
```

#### Configuration Access
```json
"Read(./config/**/*.yaml)",
"Read(./config/**/*.yml)",
"Read(./config/**/*.json)",
"Edit(./config/**/*.yaml)",
"Edit(./config/**/*.yml)",
"Edit(./config/**/*.json)"
```

#### Documentation Access
```json
"Read(./docs/**)",
"Write(./docs/**)",
"Edit(./docs/**)"
```

#### Project Files
```json
"Read(./package.json)",
"Read(./requirements.txt)",
"Read(./Cargo.toml)",
"Read(./go.mod)",
"Read(./setup.py)",
"Read(./pyproject.toml)"
```

#### Safe Command Access
```json
"Bash(git:*)",              // All git operations
"Bash(npm run:*)",          // NPM scripts only
"Bash(python:*)",           // Python execution
"Bash(ls:*)",               // Directory listing
"Bash(cat:*)",              // File content display
"Bash(grep:*)",             // Text searching
"Bash(find:*)"              // File finding
```

### Deny Patterns (18 Security Restrictions)

#### Sensitive File Protection
```json
"Read(./.env)",             // Environment files
"Read(./.env.*)",           // Environment variations
"Read(./secrets/**)",       // Secret directories
"Read(./sensitive/**)",     // Sensitive directories
"Read(/etc/passwd)",        // System password file
"Read(/etc/shadow)",        // System shadow file
"Read(/home/*/.ssh/**)"     // SSH keys and config
```

#### Write Protection
```json
"Write(./.env)",
"Write(./.env.*)",
"Write(./secrets/**)",
"Write(./sensitive/**)",
"Edit(./.env)",
"Edit(./.env.*)",
"Edit(./secrets/**)",
"Edit(./sensitive/**)"
```

#### Dangerous Command Prevention
```json
"Bash(rm -rf /*)",          // System destruction
"Bash(sudo rm:*)",          // Privileged deletion
"Bash(chmod 777:*)"         // Dangerous permissions
```

## Command Security Filtering

### security-filter.py Hook
The `security-filter.py` hook implements real-time command validation with pattern matching:

#### Dangerous Patterns (Auto-Block)
```python
DANGEROUS_PATTERNS = [
    r'rm\s+-rf\s+/',              # System deletion
    r'sudo\s+rm',                 # Privileged deletion
    r'>\s*/dev/sd[a-z]',          # Disk writing
    r'dd\s+if=.*of=/dev',         # Disk imaging
    r'mkfs\.',                    # Filesystem creation
    r'fdisk',                     # Disk partitioning
    r':(){ :|:& };:',             # Fork bomb
    r'curl.*\|\s*sh',             # Remote execution
    r'wget.*\|\s*sh'              # Remote execution
]
```

#### Caution Patterns (Request Confirmation)
```python
CAUTION_PATTERNS = [
    r'git\s+push\s+--force',      # Force push
    r'git\s+reset\s+--hard',      # Hard reset
    r'git\s+clean\s+-fd',         # Force clean
    r'npm\s+publish',             # Package publishing
    r'pip\s+install.*--break-system-packages',  # System package override
    r'sudo\s+',                   # Any sudo command
    r'rm\s+-rf\s+\S+'             # Recursive deletion
]
```

#### Safe Patterns (Auto-Approve)
```python
SAFE_PATTERNS = [
    r'git\s+status',              # Git status
    r'git\s+log',                 # Git history
    r'git\s+diff',                # Git differences
    r'ls\s+',                     # Directory listing
    r'cat\s+',                    # File reading
    r'grep\s+',                   # Text searching
    r'find\s+'                    # File finding
]
```

### Security Decision Flow
1. **Check Dangerous Patterns** → `deny` with security reason
2. **Check Caution Patterns** → `ask` for user confirmation
3. **Check Safe Patterns** → `allow` automatically
4. **Default Behavior** → `allow` (fail-safe approach)

### Security Response Format
```json
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny|ask|allow",
        "permissionDecisionReason": "Security explanation"
    }
}
```

## Credential Sanitization System

### activity-logger.py Protection
The activity logging system implements comprehensive credential sanitization:

#### Sensitive Pattern Detection
```python
SENSITIVE_PATTERNS = [
    # Authentication credentials
    (r'password\s*[=:]\s*[\'"]?([^\s\'"]+)', 'password=[REDACTED]'),
    (r'token\s*[=:]\s*[\'"]?([^\s\'"]+)', 'token=[REDACTED]'),
    (r'api[_-]?key\s*[=:]\s*[\'"]?([^\s\'"]+)', 'api_key=[REDACTED]'),
    (r'secret\s*[=:]\s*[\'"]?([^\s\'"]+)', 'secret=[REDACTED]'),

    # OAuth and JWT tokens
    (r'bearer\s+([a-zA-Z0-9\-._~+/]+=*)', 'bearer [REDACTED]'),

    # SSH keys and certificates
    (r'ssh-rsa\s+[^\s]+', 'ssh-rsa [REDACTED]'),
    (r'-----BEGIN[^-]+-----[^-]+-----END[^-]+-----', '[REDACTED CERTIFICATE]'),

    # File paths with sensitive content
    (r'/home/[^/]+/\.ssh/[^\s]+', '/home/[USER]/.ssh/[REDACTED]'),
    (r'/.*\.env[^/]*', '[REDACTED ENV FILE]'),
    (r'/.*secrets?[^/]*', '[REDACTED SECRETS]')
]
```

#### Sanitization Process
1. **Input Validation** - Check for string type and content
2. **Pattern Matching** - Apply regex patterns with case-insensitive matching
3. **Content Replacement** - Replace matches with safe placeholders
4. **Logging Protection** - Sanitized content written to logs

#### Protected Log Entry Example
```json
// Original command (never logged):
// "curl -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIs...' https://api.example.com"

// Sanitized log entry:
{
    "timestamp": "2025-09-14T15:30:45.123456",
    "tool": "Bash",
    "command": "curl -H 'Authorization: bearer [REDACTED]' https://api.example.com",
    "success": true
}
```

## Agent Security Boundaries

### Role-Based Access Control
Each agent has specific tool restrictions enforced in agent configurations:

#### Read-Only Agents
```yaml
# reviewer.md - Security analysis only
tools: Read, Grep, Search  # No write capabilities
```

#### Implementation Agents
```yaml
# coder.md - Code modification
tools: Read, Edit, MultiEdit, Write, Bash(git:*)
```

#### Testing Agents
```yaml
# tester.md - Test execution
tools: Read, Write, Edit, Bash(pytest:*), Bash(npm:*), Search, Grep
```

### Agent Delegation Security
The `agent-coordinator.py` hook tracks all Task tool usage:
- Logs agent type and task description
- Records delegation timestamps
- Supports background task classification
- Enables security audit trails

## Background Task Security

### /background Command Validation
Multi-layer validation for background agent delegation:

#### Agent Name Validation
```python
VALID_AGENTS = ['researcher', 'coder', 'reviewer', 'tester', 'documenter', 'orchestrator']
```

#### Task Complexity Validation
- Length: 10-200 characters
- Content: Must match safe operation patterns
- Scope: Project-specific tasks only

#### Approved Task Patterns
```python
APPROVED_PATTERNS = [
    r'analyze|research|document|review',         # Analysis tasks
    r'implement\s+\w+.*',                       # Implementation (50-150 chars)
    r'test\s+\w+.*',                           # Testing tasks
    r'fix\s+\w+.*'                             # Bug fixes
]
```

#### Blocked Task Patterns
```python
BLOCKED_PATTERNS = [
    r'.*\b(system|shell|exec|eval)\b.*',        # System access
    r'.*\b(credential|password|secret|key)\b.*', # Credential access
    r'.*\b(sudo|root|admin)\b.*',               # Privilege escalation
    r'.*\b(rm|delete|drop|truncate)\b.*'        # Destructive operations
]
```

## Resource Security Controls

### Timeout Management
All operations have enforced timeouts:
- **Hook Timeouts**: 3-10 seconds per hook
- **Agent Delegation**: 30 minutes maximum
- **Command Operations**: Tool-specific limits
- **Background Tasks**: Independent timeout management

### Resource Constraints
```json
{
    "max_delegations": 5,           // Per workflow
    "session_timeout": 1800,        // 30 minutes
    "hook_timeout": 10,             // Seconds
    "background_task_limit": 10     // Concurrent limit
}
```

### Memory Protection
- Context bundle size limits
- Log rotation and cleanup
- Session state cleanup on exit
- Background task garbage collection

## Security Monitoring & Auditing

### Comprehensive Logging
All security events are logged with full context:

#### Activity Logs (`reports/activity.jsonl`)
```json
{
    "timestamp": "2025-09-14T15:30:45.123456",
    "session_id": "uuid",
    "tool": "Bash",
    "command": "[SANITIZED COMMAND]",
    "success": true,
    "type": "activity"
}
```

#### Coordination Logs (`reports/coordination.jsonl`)
```json
{
    "timestamp": "2025-09-14T15:30:45.123456",
    "session_id": "uuid",
    "delegated_agent": "researcher",
    "task_description": "[SANITIZED TASK]",
    "is_background": false,
    "status": "initiated"
}
```

### Security Event Detection
- Failed permission checks logged with reasons
- Dangerous command attempts recorded
- Agent boundary violations tracked
- Resource limit violations monitored

### Audit Trail Features
- Immutable log entries (append-only)
- Session correlation across all logs
- Credential sanitization verification
- Security decision audit trail

## Security Best Practices

### Deployment Security
1. **Review permissions** before production deployment
2. **Test security filtering** with dangerous command attempts
3. **Validate credential sanitization** with test credentials
4. **Monitor resource usage** during agent workflows

### Operational Security
1. **Regular permission audits** - Review allow/deny patterns
2. **Log monitoring** - Watch for security events
3. **Agent behavior analysis** - Verify proper tool usage
4. **Background task monitoring** - Track out-of-loop processing

### Development Security
1. **Secure coding practices** - Follow agent security boundaries
2. **Credential management** - Never hardcode sensitive data
3. **Testing with security** - Include security tests in workflows
4. **Documentation security** - Keep security docs updated

## Security in Practice

### Example-Driven Learning
See security features in action through the examples directory:
- `examples/03-security-review/` - Comprehensive security assessment patterns
- `examples/04-full-workflow/` - Security integration in complete workflows
- `examples/06-background-delegation/` - Background task security validation

### Security Validation Testing
Test security features with the provided examples:
- Credential sanitization verification
- Dangerous command blocking demonstrations
- Permission boundary enforcement
- Background task security validation

### Enterprise Deployment
The security system is designed for production environments with:
- **Zero Trust Architecture**: Every operation validated
- **Defense in Depth**: Multiple security layers
- **Audit Compliance**: Complete activity trails
- **Incident Response**: Comprehensive logging and monitoring

The pyConductor security system provides comprehensive protection while maintaining the flexibility and performance needed for sophisticated multi-agent development workflows.