# pyConductor Background Delegation

The background delegation system implements Dan's "out-of-loop" pattern for context window optimization, enabling independent agent processing without primary context pollution.

## Background Delegation Philosophy

### "Out-of-Loop" Pattern
The background delegation pattern addresses context window limitations by spawning independent agent work that doesn't interfere with the primary conversation thread:

- **Context Isolation** - Background tasks maintain their own context space
- **Independent Processing** - Agents work autonomously without blocking primary workflow
- **Result Aggregation** - Background results integrate when needed
- **Resource Optimization** - Parallel processing without context competition

### Security-First Approach
All background delegation includes comprehensive security validation:
- Agent name validation against allowed agents
- Task complexity and safety pattern matching
- Content sanitization and credential protection
- Resource constraint enforcement

## /background Command Implementation

### Command Structure
```bash
/background [agent] "task description"
```

**Parameters**:
- `agent`: Must be one of 6 valid agents (researcher, coder, reviewer, tester, documenter, orchestrator)
- `task`: 10-200 character description matching approved patterns

### Security Validation Process

#### 1. Agent Name Validation
```python
VALID_AGENTS = [
    'researcher',    # Analysis and requirements gathering
    'coder',        # Implementation and bug fixes
    'reviewer',     # Security and quality assessment
    'tester',       # Test creation and execution
    'documenter',   # Documentation and examples
    'orchestrator'  # Multi-agent workflow coordination
]

def validate_agent_name(agent_name):
    """Validate agent name against allowed list"""
    if agent_name not in VALID_AGENTS:
        return False, f"Invalid agent '{agent_name}'. Valid agents: {', '.join(VALID_AGENTS)}"
    return True, "Agent validated"
```

#### 2. Task Complexity Validation
```python
def validate_task_complexity(task_description):
    """Validate task description length and content"""
    if len(task_description) < 10:
        return False, "Task description too short (minimum 10 characters)"
    if len(task_description) > 200:
        return False, "Task description too long (maximum 200 characters)"

    return True, "Task complexity validated"
```

#### 3. Approved Task Pattern Matching
```python
APPROVED_TASK_PATTERNS = [
    r'\b(analyze|research|document|review)\b.*',        # Analysis tasks
    r'\bimplement\s+[\w\s]{10,100}.*',                 # Implementation (specific scope)
    r'\btest\s+[\w\s]{10,100}.*',                      # Testing tasks
    r'\bfix\s+[\w\s]{10,100}.*'                        # Bug fixing tasks
]

def validate_task_patterns(task_description):
    """Check if task matches approved patterns"""
    for pattern in APPROVED_TASK_PATTERNS:
        if re.search(pattern, task_description, re.IGNORECASE):
            return True, f"Task matches approved pattern: {pattern[:30]}..."

    return False, "Task does not match any approved patterns"
```

#### 4. Blocked Task Pattern Detection
```python
BLOCKED_TASK_PATTERNS = [
    r'.*\b(system|shell|exec|eval)\b.*',               # System access attempts
    r'.*\b(credential|password|secret|key)\b.*',        # Credential handling
    r'.*\b(sudo|root|admin|privilege)\b.*',            # Privilege escalation
    r'.*\b(rm|delete|drop|truncate)\b.*',              # Destructive operations
    r'.*\b(network|socket|port|bind)\b.*',             # Network operations
    r'.*\b(file|path|directory)\s*outside\b.*'        # File system escape attempts
]

def check_blocked_patterns(task_description):
    """Check for dangerous task patterns"""
    for pattern in BLOCKED_TASK_PATTERNS:
        if re.search(pattern, task_description, re.IGNORECASE):
            return True, f"Blocked pattern detected: {pattern[:30]}..."

    return False, "No blocked patterns detected"
```

### Validated Delegation Process

#### Context Prime Generation
When validation passes, the system creates a comprehensive context prime for the background agent:

```python
def generate_background_context_prime(agent_name, task_description):
    """Generate context prime for background agent"""
    context_prime = f"""
CONTEXT PRIME: This is a pyConductor background task. You have access to:
- 6 focused agents via Task tool delegation
- Comprehensive hooks system for activity logging
- Context bundles in reports/context-bundles/
- Commands: /implement, /review, /track, /background
- Reports structure: activity.jsonl, coordination.jsonl
- Current project: Multi-agent development framework

BACKGROUND TASK: {task_description}

EXECUTION INSTRUCTIONS:
1. Use appropriate agents via Task tool if needed
2. Log progress to reports/background/active/{{timestamp}}_{agent_name}_task.md
3. Work independently without polluting primary context
4. Generate detailed results and move to reports/background/completed/ when finished
5. Follow security best practices - no credential access or system modifications

AGENT FOCUS: The {agent_name} agent will work autonomously on this validated task,
applying its specialized capabilities for optimal results.
"""
    return context_prime
```

#### Task Delegation Execution
```python
def execute_background_delegation(agent_name, task_description, context_prime):
    """Execute background task delegation using Claude Code Task tool"""

    # Log delegation initiation
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": get_current_session_id(),
        "delegated_agent": agent_name,
        "task_description": sanitize_text(task_description),
        "is_background": True,
        "status": "initiated",
        "context_prime_length": len(context_prime)
    }

    # Write to coordination log
    with open("reports/coordination.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    # Execute Task tool delegation
    task_result = claude_task_tool.delegate(
        agent_type=agent_name,
        description=context_prime,
        background=True
    )

    return task_result
```

## Background Processing Features

### Independent Context Management
Background agents maintain their own context space:

```python
class BackgroundContext:
    """Manages independent context for background agents"""

    def __init__(self, session_id, agent_name, task_description):
        self.session_id = session_id
        self.agent_name = agent_name
        self.task_description = task_description
        self.start_time = datetime.now()
        self.context_isolation = True

    def create_isolated_workspace(self):
        """Create isolated workspace for background processing"""
        workspace_dir = Path(f"reports/background/active/{self.session_id}_{self.agent_name}")
        workspace_dir.mkdir(parents=True, exist_ok=True)

        # Create task manifest
        manifest = {
            "task_id": f"{self.session_id}_{self.agent_name}",
            "agent": self.agent_name,
            "task": self.task_description,
            "start_time": self.start_time.isoformat(),
            "status": "active",
            "isolation": True
        }

        with open(workspace_dir / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)

        return workspace_dir
```

### Progress Tracking
Background tasks generate detailed progress reports:

```python
def create_background_progress_report(workspace_dir, agent_name, task_description):
    """Create progress tracking file for background task"""

    report_content = f"""# Background Task Progress Report

## Task Information
- **Agent**: {agent_name}
- **Task**: {task_description}
- **Start Time**: {datetime.now().isoformat()}
- **Status**: Active
- **Workspace**: {workspace_dir}

## Execution Log
<!-- Agent will append progress updates here -->

## Results
<!-- Agent will document results here -->

## Next Actions
<!-- Agent will identify follow-up actions here -->
"""

    report_file = workspace_dir / f"{agent_name}_progress.md"
    with open(report_file, "w") as f:
        f.write(report_content)

    return report_file
```

## Usage Examples

### Research Tasks
```bash
# Background analysis and research
/background researcher "analyze existing microservices architecture patterns in the codebase"
/background researcher "research OAuth2 security best practices for implementation"
/background researcher "identify performance bottlenecks in database queries"
```

### Implementation Tasks
```bash
# Background implementation work
/background coder "implement background task processing system using worker queues"
/background coder "add comprehensive error handling to authentication module"
/background coder "optimize database connection pooling configuration"
```

### Review Tasks
```bash
# Background security and quality review
/background reviewer "conduct comprehensive security audit of payment processing module"
/background reviewer "analyze code quality issues in user management system"
/background reviewer "review API endpoints for potential security vulnerabilities"
```

### Testing Tasks
```bash
# Background test development and execution
/background tester "create comprehensive integration tests for authentication workflow"
/background tester "develop performance tests for API endpoint response times"
/background tester "implement end-to-end tests for user registration process"
```

### Documentation Tasks
```bash
# Background documentation creation
/background documenter "create comprehensive API documentation for all endpoints"
/background documenter "develop user guide for OAuth2 integration process"
/background documenter "update installation and deployment documentation"
```

### Orchestration Tasks
```bash
# Background multi-agent workflows
/background orchestrator "coordinate security review and fixes for entire authentication system"
/background orchestrator "manage complete feature implementation for real-time notifications"
```

## Background Task Lifecycle

### 1. Initiation Phase
```python
def initiate_background_task():
    """Initiate background task with full validation"""
    # Security validation
    agent_valid, agent_msg = validate_agent_name(agent)
    task_valid, task_msg = validate_task_complexity(task)
    pattern_valid, pattern_msg = validate_task_patterns(task)
    blocked, blocked_msg = check_blocked_patterns(task)

    # Create workspace
    workspace = create_isolated_workspace()

    # Generate context prime
    context_prime = generate_background_context_prime(agent, task)

    # Execute delegation
    result = execute_background_delegation(agent, task, context_prime)

    return result
```

### 2. Execution Phase
Background agents work independently with:
- Full access to their specialized tool set
- Project context and documentation
- Ability to delegate to other agents if needed (orchestrator)
- Security boundaries and resource constraints
- Progress logging and status updates

### 3. Completion Phase
```python
def complete_background_task(task_id):
    """Complete background task and archive results"""

    # Move workspace from active to completed
    active_dir = Path(f"reports/background/active/{task_id}")
    completed_dir = Path(f"reports/background/completed/{task_id}")

    if active_dir.exists():
        shutil.move(str(active_dir), str(completed_dir))

    # Update coordination log
    completion_entry = {
        "timestamp": datetime.now().isoformat(),
        "task_id": task_id,
        "status": "completed",
        "results_location": str(completed_dir)
    }

    with open("reports/coordination.jsonl", "a") as f:
        f.write(json.dumps(completion_entry) + "\n")
```

## Background Task Monitoring

### Active Task Detection
The system tracks active background tasks through coordination logs:

```python
def get_active_background_tasks():
    """Get list of currently active background tasks"""
    active_tasks = []

    if Path("reports/coordination.jsonl").exists():
        with open("reports/coordination.jsonl", "r") as f:
            for line in f:
                entry = json.loads(line.strip())
                if entry.get("is_background") and entry.get("status") == "initiated":
                    # Check if still active (no completion entry)
                    if not has_completion_entry(entry.get("session_id")):
                        active_tasks.append(entry)

    return active_tasks
```

### Background Task Integration
Background tasks integrate with the main workflow through:

#### Session Context Display
```python
# In context-prime.py
background_count, background_agents = get_background_tasks()
if background_count > 0:
    context_parts.append(f"Background Tasks: {background_count} active ({', '.join(background_agents)})")
```

#### Stop Hook Integration
```python
# In stop-control.py
def has_active_background_tasks():
    """Check for active background tasks before stopping"""
    active_tasks = get_active_background_tasks()
    if active_tasks:
        return True, f"Active background tasks: {len(active_tasks)}"
    return False, "No active background tasks"
```

## Benefits of Background Delegation

### Context Window Optimization
- **Primary Context Preserved** - Main conversation continues uninterrupted
- **Parallel Processing** - Multiple agents can work simultaneously
- **Context Isolation** - Background work doesn't pollute primary context
- **Resource Efficiency** - Optimal use of available agent resources

### Workflow Acceleration
- **Independent Execution** - Background tasks don't block primary workflow
- **Specialized Processing** - Agents work in their domain of expertise
- **Result Integration** - Background results available when needed
- **Scalable Processing** - Multiple background tasks can run concurrently

### Security Maintenance
- **Comprehensive Validation** - All background tasks undergo security screening
- **Resource Constraints** - Background tasks respect system limits
- **Audit Trail** - Full logging and monitoring of background activities
- **Safe Execution** - Background tasks can't perform dangerous operations

## Practical Examples

### Learn Through Hands-On Experience
Explore the `examples/06-background-delegation/` directory for:
- Step-by-step background processing demonstrations
- Context optimization techniques in practice
- Performance comparison measurements
- Real-world background task scenarios

### Example Use Cases
- **Large Codebase Analysis**: Background research while continuing development
- **Security Audits**: Independent security review while implementing features
- **Documentation Generation**: Background doc creation during development
- **Performance Analysis**: Background profiling while optimizing code

The background delegation system represents a sophisticated implementation of Dan's "out-of-loop" pattern, providing enterprise-grade parallel processing capabilities while maintaining security, observability, and context optimization throughout the pyConductor system.