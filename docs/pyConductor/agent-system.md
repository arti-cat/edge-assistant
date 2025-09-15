# pyConductor Agent System

The agent system implements the "focused agent philosophy" through 6 specialized agents that use Claude Code's native Task tool for delegation and coordination.

## Agent Philosophy

> "A focused agent is a performant agent" - Context Engineering Framework

Each agent has a single, well-defined domain of expertise to maximize performance and minimize context overhead. The system uses Claude Code's built-in Task tool for native delegation rather than external orchestration.

## Agent Overview

| Agent | Model | Primary Focus | Tools | Output |
|-------|-------|---------------|-------|---------|
| **researcher** | claude-3-5-sonnet-20241022 | Analysis & Requirements | Read, Grep, Search, WebFetch, Bash(git:*) | Structured findings with recommendations |
| **coder** | claude-3-5-sonnet-20241022 | Implementation | Read, Edit, MultiEdit, Write, Bash(git:*) | Working code with test-ready structure |
| **reviewer** | claude-3-5-sonnet-20241022 | Security & Quality | Read, Grep, Search | Priority issues with specific solutions |
| **tester** | claude-3-5-haiku-20241022 | Test Creation & Execution | Read, Write, Edit, Bash(pytest:*), Search, Grep | Working tests with clear pass/fail results |
| **documenter** | claude-3-5-haiku-20241022 | Documentation & Examples | Read, Write, Edit, Search, Grep | Updated docs matching implemented features |
| **orchestrator** | claude-3-5-sonnet-20241022 | Workflow Coordination | Task, Read, Grep, Search | Completed workflows with summaries |

## Detailed Agent Specifications

### 1. researcher.md
**Domain**: Codebase analysis, pattern recognition, requirements gathering

**Core Responsibilities**:
- Deep codebase analysis and pattern recognition
- Requirements gathering and clarification
- Technology research and compatibility assessment
- Existing implementation discovery
- Risk and impact assessment

**Focus Areas**:
- Broad searches narrowed to specific patterns
- Multi-file type analysis (source, config, docs, tests)
- Import/dependency pattern analysis
- Recent change and commit history review
- Best practice identification

**Usage Pattern**:
```bash
researcher: "analyze existing authentication patterns in the codebase"
researcher: "identify security vulnerabilities in the payment module"
researcher: "research best practices for implementing OAuth2"
```

### 2. coder.md
**Domain**: Clean implementation following discovered patterns

**Core Responsibilities**:
- Clean implementation following established patterns
- Bug fixes with minimal, targeted changes
- Code structure adherence to project conventions
- Integration with existing systems
- Preparation for testing phase

**Implementation Approach**:
- Follow patterns identified by researcher agent
- Make minimal, safe changes that preserve existing interfaces
- Write clear, maintainable code
- Prepare code structure for comprehensive testing
- Document implementation decisions in code comments when necessary

**Usage Pattern**:
```bash
coder: "implement OAuth2 authentication following the patterns researched"
coder: "fix the session timeout bug identified in review"
coder: "add password reset functionality to the user module"
```

### 3. reviewer.md
**Domain**: Security and quality issues with minimal fixes

**Core Responsibilities**:
- Security vulnerability identification
- Code quality assessment
- Performance issue detection
- Maintainability review
- Provide concrete, minimal fixes

**Security Focus Areas**:
- Authentication and authorization vulnerabilities
- Input validation and injection attacks (SQL, XSS, command injection)
- Cryptographic implementations and key management
- Session management and token security
- Data exposure and information leakage
- Dependency vulnerabilities

**Priority System**:
- **Critical**: Immediate exploitation possible
- **High**: Likely exploitation with moderate effort
- **Medium**: Possible exploitation with significant effort
- **Low**: Theoretical or requires insider access

**Usage Pattern**:
```bash
reviewer: "security review the new authentication system"
reviewer: "identify quality issues in the payment processing module"
reviewer: "review for SQL injection vulnerabilities in user input handling"
```

### 4. tester.md
**Domain**: Test creation, execution, and failure analysis

**Model**: claude-3-5-haiku-20241022 (optimized for systematic testing tasks)

**Core Responsibilities**:
- Unit test creation for individual functions and classes
- Integration test development for component interactions
- Test execution and failure analysis
- Coverage analysis and gap identification
- Performance testing when appropriate
- Test fixture and mock object creation

**Test Types**:
- **Unit tests**: Individual function/method behavior
- **Integration tests**: Component interactions
- **Parameterized tests**: Multiple input scenarios
- **Error handling tests**: Exception cases and edge conditions
- **Boundary tests**: Edge cases and limits
- **Mock-based tests**: External dependency isolation

**Usage Pattern**:
```bash
tester: "create comprehensive tests for the new authentication system"
tester: "run all tests and analyze any failures"
tester: "create integration tests for the payment processing workflow"
```

### 5. documenter.md
**Domain**: API docs, README updates, usage examples

**Model**: claude-3-5-haiku-20241022 (optimized for clear, consistent documentation)

**Core Responsibilities**:
- API documentation generation from code
- README file creation and maintenance
- Usage examples and tutorials
- Architecture and design documentation
- Installation and setup guides
- Code comment generation for complex logic

**Documentation Types**:
- **API docs**: Function/method signatures, parameters, return values
- **README files**: Project overview, installation, usage
- **Usage examples**: Practical implementation examples
- **Architecture docs**: System design and component relationships
- **User guides**: How-to documentation for end users
- **Developer guides**: Contribution and development setup

**Usage Pattern**:
```bash
documenter: "update API documentation for new authentication endpoints"
documenter: "create usage examples for the OAuth2 integration"
documenter: "update README with new installation requirements"
```

### 6. orchestrator.md
**Domain**: Multi-agent workflow coordination using Task tool

**Special Role**: Coordination-only agent that delegates work without implementing

**Core Responsibilities**:
- Multi-agent workflow coordination using Task tool delegation
- Agent capability matching to requirements
- Workflow sequencing and dependency management
- Progress monitoring and result aggregation
- Context handoff between agents

**Resource Constraints**:
- **Timeout**: 30 minutes maximum per workflow
- **Max Delegations**: 5 agents maximum per workflow
- **Coordination Only**: No direct code implementation
- **Context Management**: Maintain workflow state across delegations

**Standard Workflow Patterns**:

**Full Implementation Flow**:
```
orchestrator → researcher → coder → tester → reviewer → documenter
```

**Security-First Flow**:
```
orchestrator → researcher → reviewer → coder → tester → documenter
```

**Quality-Focused Flow**:
```
orchestrator → researcher → coder → reviewer → tester → documenter
```

**Usage Pattern**:
```bash
orchestrator: "coordinate full implementation of user authentication system"
orchestrator: "manage security review and fixes for payment module"
```

## Task Tool Delegation

### Native Claude Code Integration
The agents use Claude Code's built-in Task tool rather than external CLI spawning:

```bash
# Direct agent usage
researcher: "analyze existing patterns"
coder: "implement following discovered patterns"

# Orchestrated workflows
orchestrator: "coordinate full feature implementation"
```

### Delegation Tracking
All Task tool usage is tracked by the `agent-coordinator.py` hook:
- Logs to `reports/coordination.jsonl`
- Records agent type, task description, timestamps
- Supports background task classification
- Enables workflow analysis and optimization

### Background Delegation Pattern
The system supports "out-of-loop" background processing:

```bash
# Background delegation via /background command
/background researcher "analyze microservices architecture patterns"
/background documenter "create comprehensive API documentation"
```

**Background Features**:
- Independent execution without context pollution
- Security validation before delegation
- Report generation to `reports/background/`
- Agent specialization maintained in background

## Agent Coordination Patterns

### Sequential Workflows
```bash
# Standard implementation sequence
1. researcher: "analyze existing authentication patterns"
2. coder: "implement OAuth2 based on research findings"
3. tester: "create comprehensive authentication tests"
4. reviewer: "security review of authentication implementation"
5. documenter: "update documentation with new auth endpoints"
```

### Parallel Processing
```bash
# Independent parallel tasks
/background researcher "analyze security vulnerabilities"
/background documenter "update installation guides"
# Continue with main workflow while background tasks execute
```

### Error Recovery
```bash
# Failed step recovery
If tester agent finds critical issues:
→ reviewer: "identify root cause of test failures"
→ coder: "implement fixes based on reviewer findings"
→ tester: "re-run tests after fixes"
```

## Agent Specialization Benefits

### Context Efficiency
- Each agent has minimal, focused context
- No irrelevant information diluting performance
- Specialized tools matched to agent domain
- Clear input/output interfaces between agents

### Security Boundaries
- Read-only agents (reviewer) cannot modify code
- Testing agents isolated to test environments
- Security validation before delegation
- Credential sanitization in all agent communication

### Quality Assurance
- Each agent validates work from previous agents
- Multiple perspectives on the same codebase
- Specialized expertise applied at each stage
- Comprehensive coverage through agent coordination

### Performance Optimization
- Haiku models for systematic tasks (tester, documenter)
- Sonnet models for complex reasoning (researcher, coder, reviewer)
- Task-appropriate model selection
- Resource constraints prevent runaway processes

## Integration with Hook System

The agent system integrates seamlessly with the hook system:

- **SessionStart**: Available agents displayed in context prime
- **PostToolUse**: Agent delegations tracked by `agent-coordinator.py`
- **Security**: All agent communication filtered by `security-filter.py`
- **Logging**: Agent activities logged with credential sanitization

## Examples and Practical Applications

### Learning Path
Start with the examples directory for hands-on experience:
- `examples/01-basic-agent-usage/` - Foundation agent delegation patterns
- `examples/02-code-generation/` - Implementation following patterns
- `examples/05-multi-agent-collaboration/` - Sequential agent coordination
- `examples/04-full-workflow/` - Complete orchestrated workflows

### Real-World Applications
The agent system excels in:
- **Feature Development**: Complete implementation lifecycle
- **Code Quality**: Systematic review and improvement
- **Security Assessment**: Comprehensive vulnerability analysis
- **Documentation**: API docs and usage examples
- **Technical Debt**: Pattern analysis and modernization

## Best Practices

### Effective Agent Usage
1. **Match agent to task domain** - Use researcher for analysis, coder for implementation
2. **Provide specific instructions** - Clear, actionable task descriptions
3. **Use sequential workflows** - Let each agent build on previous work
4. **Monitor resource usage** - Respect timeouts and delegation limits
5. **Learn from examples** - Study patterns in `examples/` directory

### Workflow Design
1. **Start with research** - Understand before implementing
2. **Implement incrementally** - Small, testable changes
3. **Test comprehensively** - Validate all functionality
4. **Review for security** - Check for vulnerabilities
5. **Document thoroughly** - Update all relevant documentation

The agent system provides a sophisticated, secure, and highly performant approach to multi-agent development workflows through focused specialization and native Claude Code integration.