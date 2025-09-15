# pyConductor Quick Start Guide

Get up and running with pyConductor's multi-agent development framework in minutes. This guide provides practical examples for immediate productivity.

## Getting Started

### 1. Initial Session
When you start a Claude Code session in the pyConductor directory, the context-prime hook automatically provides essential project information:

```
🎯 pyConductor Session Started | 2025-09-14 15:30

Git Status: Working tree clean
Recent Activity: security-filter.py, activity-logger.py, bundle-manager.py
Recent Agents: researcher, coder, reviewer
Project: Multi-agent development framework with simplified workflows
Agents: 6 focused agents available via Task tool delegation
Directories: .claude, docs, reports
Active Tasks: 0

Key Commands:
- /implement "feature" - Full feature development workflow
- /review [path] - Security and quality assessment
- /track "task" - Simple task progress tracking
- /background [agent] "task" - Out-of-loop agent delegation
```

### 2. System Health Check
Verify your pyConductor installation:

```bash
/check-conductor
```

Expected output:
```
pyConductor System Status:
✅ 6 Agents: researcher, coder, reviewer, tester, documenter, orchestrator
✅ 6 Hooks: All lifecycle events configured and executable
✅ Permissions: 81 allow patterns, 18 deny patterns active
✅ Reports: activity.jsonl (150 entries), coordination.jsonl (25 entries)
✅ Context Bundles: 12 bundles available for restoration
✅ Background Tasks: 0 active, 3 completed today
```

## Essential Workflows

### Full Feature Implementation
Use the `/implement` command for complete feature development with orchestrated agent workflows:

```bash
/implement "Add OAuth2 authentication with Google provider"
```

**What happens**:
1. **orchestrator** coordinates the entire workflow
2. **researcher** analyzes existing authentication patterns
3. **coder** implements OAuth2 following discovered patterns
4. **tester** creates comprehensive tests
5. **reviewer** conducts security assessment
6. **documenter** updates API documentation

### Security & Quality Review
Review your codebase for security vulnerabilities and quality issues:

```bash
# Review entire codebase
/review

# Review specific directory
/review src/auth/

# Review specific file
/review src/payment.py
```

**Output includes**:
- **Critical**: Immediate security fixes needed
- **High**: Important quality improvements
- **Medium**: Optimization opportunities
- **Low**: Minor improvements

### Task Tracking
Track development tasks and progress:

```bash
/track "Implement real-time WebSocket notifications"
/track "Add comprehensive error handling to payment system"
/track "Optimize database query performance"
```

Tasks are logged to `reports/tasks.jsonl` and appear in session context for continuity.

### Background Processing
Delegate work to background agents for parallel processing:

```bash
# Background research while you continue working
/background researcher "analyze microservices architecture patterns"

# Background documentation creation
/background documenter "create comprehensive API documentation"

# Background security review
/background reviewer "audit authentication system for vulnerabilities"
```

## Direct Agent Usage

### Using Individual Agents
Work directly with specialized agents for focused tasks:

```bash
# Research and analysis
Use researcher agent to "analyze existing database schema design patterns"

# Implementation
Use coder agent to "implement password reset functionality following security best practices"

# Testing
Use tester agent to "create integration tests for the new authentication flow"

# Security review
Use reviewer agent to "identify potential SQL injection vulnerabilities in user input handling"

# Documentation
Use documenter agent to "update API documentation for new OAuth2 endpoints"
```

### Agent Specialization Examples

#### researcher Agent
```bash
# Analysis and pattern recognition
researcher: "analyze existing error handling patterns in the codebase"
researcher: "research best practices for implementing WebSocket connections"
researcher: "identify dependencies that need updating for security patches"
```

#### coder Agent
```bash
# Implementation following patterns
coder: "implement rate limiting for API endpoints"
coder: "add comprehensive logging to the authentication module"
coder: "fix the memory leak in the background task processor"
```

#### tester Agent
```bash
# Test creation and execution
tester: "create unit tests for the new user registration flow"
tester: "develop performance tests for database query optimization"
tester: "implement end-to-end tests for the payment processing workflow"
```

## Context Engineering

### Context Priming Commands
Optimize context for specific workflow types:

```bash
# Prime for analysis tasks
/prime-research authentication
researcher: "analyze OAuth2 implementation patterns"

# Prime for implementation
/prime-implement websockets
coder: "implement real-time notifications using WebSockets"

# Prime for debugging
/prime-debug memory-leak
reviewer: "identify and fix memory leaks in background processing"

# Prime for security review
/prime-review security
reviewer: "conduct comprehensive security audit"
```

### Bundle Management
Restore context from previous sessions:

```bash
# Auto-suggest recent bundles
/loadbundle

# Load specific bundle
/loadbundle reports/context-bundles/session-abc123_bundle.jsonl
```

## Practical Examples

### Example 1: Adding User Authentication
```bash
# Start with task tracking
/track "Implement complete user authentication system"

# Full implementation workflow
/implement "Add user registration, login, logout, and password reset with email verification"

# Additional security review
/review src/auth/

# Background documentation while continuing development
/background documenter "create user authentication API guide with examples"
```

### Example 2: Performance Optimization
```bash
# Research existing performance patterns
researcher: "analyze current database query patterns and identify bottlenecks"

# Implement optimizations based on research
coder: "implement database connection pooling and query optimization"

# Create performance tests
tester: "develop benchmark tests for database query performance"

# Review for additional optimizations
reviewer: "identify additional performance improvement opportunities"
```

### Example 3: API Development
```bash
# Context priming for API development
/prime-implement api-endpoints

# Orchestrated API development
/implement "Create RESTful API endpoints for user management with OpenAPI documentation"

# Background security review
/background reviewer "audit new API endpoints for security vulnerabilities"

# Background API documentation
/background documenter "create comprehensive API usage examples and integration guide"
```

## Monitoring & Observability

### Activity Monitoring
Monitor system activity through log files:

```bash
# View recent activity
tail -f reports/activity.jsonl

# View agent coordination
tail -f reports/coordination.jsonl

# View tracked tasks
cat reports/tasks.jsonl
```

### Context Bundle Analysis
View context bundle trails for session analysis:

```bash
# List available bundles
ls reports/context-bundles/

# View bundle content
cat reports/context-bundles/latest_bundle.jsonl | jq '.'
```

### Background Task Status
Check background task status in session context or through reports:

```bash
# Active background tasks shown in session start
# Check background task workspace
ls reports/background/active/

# View completed background work
ls reports/background/completed/
```

## Best Practices

### Effective Task Planning
1. **Start with research** - Use researcher agent to understand existing patterns
2. **Track your work** - Use `/track` for important development tasks
3. **Use background processing** - Delegate parallel work to background agents
4. **Review regularly** - Use `/review` for security and quality checks

### Workflow Optimization
1. **Prime your context** - Use context priming commands for specific workflows
2. **Chain agent work** - Let each agent build on previous agent outputs
3. **Monitor resources** - Respect timeouts and delegation limits
4. **Use bundles** - Restore context from previous productive sessions

### Security Considerations
1. **Review before deployment** - Always run security review on new features
2. **Use background review** - Run security audits in background while developing
3. **Check permissions** - Verify permission system configuration
4. **Monitor logs** - Watch for security events in activity logs

## Troubleshooting

### Common Issues

#### Agent Not Responding
```bash
# Check agent configuration
cat .claude/agents/[agent-name].md

# Verify permissions
grep -A 10 -B 10 "agent-name" .claude/settings.json
```

#### Hook Failures
```bash
# Check hook execution permissions
ls -la .claude/hooks/

# Test hook execution
python3 .claude/hooks/context-prime.py
```

#### Background Tasks Not Starting
```bash
# Verify agent name is valid
/background researcher "test task"

# Check task complexity (10-200 characters)
# Verify task matches approved patterns
```

### Log Analysis
```bash
# Check for errors in activity log
grep "success.*false" reports/activity.jsonl

# View recent coordination events
tail -10 reports/coordination.jsonl

# Check session end reasons
grep "session_end" reports/activity.jsonl
```

## Advanced Features

### Multi-Agent Orchestration
```bash
# Complex feature development
orchestrator: "coordinate implementation of real-time chat system with WebSockets, user presence, and message history"
```

### Workflow Chaining
```bash
# Sequential workflow
/track "Migrate to new authentication system"
researcher: "analyze migration requirements from current auth to OAuth2"
coder: "implement migration scripts and new OAuth2 integration"
tester: "create migration tests and validation scripts"
reviewer: "security review migration process and new implementation"
documenter: "create migration guide and updated authentication docs"
```

### Parallel Development
```bash
# Start background work
/background researcher "analyze current API design patterns"
/background documenter "update installation and setup documentation"

# Continue with foreground development
coder: "implement new API endpoints for user preferences"
tester: "create tests for user preference endpoints"
```

## Getting Help

### Built-in Documentation
- Check `docs/pyConductor/` for comprehensive documentation
- Review `.claude/agents/` for agent specifications
- Examine `.claude/commands/` for command details

### Hands-on Examples
- Work through `examples/` directory for practical demonstrations
- Start with `examples/01-basic-agent-usage/` for fundamentals
- Progress to `examples/04-full-workflow/` for complete orchestration
- Explore `examples/06-background-delegation/` for advanced patterns

### System Validation
```bash
# Comprehensive system check
/check-conductor

# Review current permissions
cat .claude/settings.json | jq '.permissions'

# Check recent activity
tail -20 reports/activity.jsonl
```

pyConductor provides a sophisticated yet intuitive development environment. Start with simple commands like `/implement` and `/review`, then gradually explore advanced features like background delegation and context engineering as you become more comfortable with the system. The `examples/` directory provides hands-on guidance for all complexity levels.