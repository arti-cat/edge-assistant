# pyConductor System Overview

**pyConductor** is a sophisticated multi-agent framework that leverages Claude Code's native capabilities to orchestrate complex development workflows through focused agent delegation.

## System Architecture

### Core Philosophy

> "A focused agent is a performant agent" - Context Engineering Framework

The system is built on Dan's R&D framework principles:
- **Reduce** - Minimize context overhead through dynamic priming and security filtering
- **Delegate** - Use specialized agents for domain expertise via Claude Code's Task tool

### Key Components

#### 1. Focused Agent System (6 Agents)
- **researcher.md** - Codebase analysis, pattern recognition, requirements gathering
- **coder.md** - Clean implementation following discovered patterns
- **reviewer.md** - Security and quality issues with minimal fixes
- **tester.md** - Test creation, execution, and failure analysis
- **documenter.md** - API docs, README updates, usage examples
- **orchestrator.md** - Multi-agent workflow coordination using Task tool

#### 2. Command System (10 Commands)
- **Core Commands**: `/implement`, `/review`, `/track`, `/background`
- **Context Engineering**: `/prime-research`, `/prime-implement`, `/prime-debug`, `/prime-review`
- **Bundle Management**: `/loadbundle`, `/check-conductor`

#### 3. Hook Lifecycle System (6 Hooks)
- **SessionStart** → context-prime.py, bundle-manager.py
- **PreToolUse** → security-filter.py
- **PostToolUse** → activity-logger.py, agent-coordinator.py
- **UserPromptSubmit** → task-tracker.py
- **SessionEnd** → session-end.py
- **Stop** → stop-control.py

#### 4. Security & Permissions System
- **Granular permissions** with allow/deny patterns in `.claude/settings.json`
- **Multi-pattern validation** for dangerous commands
- **Credential sanitization** with 10+ patterns for sensitive data
- **Safe file access** with specific file type restrictions

#### 5. Observability System
- **Activity logging** to `reports/activity.jsonl`
- **Context bundles** in `reports/context-bundles/`
- **Agent coordination** tracking via `reports/coordination.jsonl`
- **Task tracking** with `/track` command logging

## System Benefits

### Production-Grade Security
- **Automatic security filtering** prevents dangerous operations
- **Credential sanitization** protects sensitive information in logs
- **Permission boundaries** enforce safe operation scope
- **Resource constraints** prevent runaway processes

### Intelligent Context Management
- **Dynamic context priming** loads only essential project state
- **Context bundle trails** enable session restoration (Dan's ADV2 pattern)
- **Background delegation** keeps primary context clean
- **Focused agent specialization** optimizes performance

### Native Claude Code Integration
- **Task tool delegation** for true agent coordination
- **Built-in agent system** rather than external orchestration
- **Hook lifecycle integration** for programmable middleware
- **Status line integration** for real-time project awareness

## Workflow Patterns

### Standard Implementation Flow
```
orchestrator → researcher → coder → tester → reviewer → documenter
```

### Security-First Flow
```
orchestrator → researcher → reviewer → coder → tester → documenter
```

### Background Delegation ("Out-of-Loop" Pattern)
```bash
/background researcher "analyze authentication patterns"
# Spawns independent agent work without context pollution
```

## Current Status

✅ **PRODUCTION READY** - Advanced Claude Code implementation with:
- Comprehensive permissions system
- Full lifecycle hooks (6 events)
- Dan's R&D framework implementation
- Real-time status line integration
- Context bundle auto-suggestion
- Background task detection
- Enterprise-grade security
- Complete examples suite (`examples/` directory with 7 comprehensive demos)

## Project Structure

```
pyConductor/
├── .claude/
│   ├── agents/          # 6 focused agents
│   ├── commands/        # 10 specialized commands
│   ├── hooks/          # 6 lifecycle hooks
│   └── settings.json   # Permissions & configuration
├── examples/           # 7 comprehensive examples (basic to expert)
├── reports/
│   ├── activity.jsonl       # Tool usage logging
│   ├── coordination.jsonl   # Agent delegation events
│   ├── tasks.jsonl         # User-tracked tasks
│   └── context-bundles/    # Session restoration data
├── docs/pyConductor/   # Comprehensive documentation
├── README.md          # Public-facing project overview
└── CLAUDE.md          # Main project instructions
```

## Key Innovations

1. **Task Tool Native Delegation** - Uses Claude Code's built-in Task tool instead of external CLI spawning
2. **Context Bundle Trails** - Dan's ADV2 pattern for operation reconstruction
3. **Security-First Architecture** - Multiple validation layers with credential sanitization
4. **Focused Agent Philosophy** - Each agent specialized for maximum performance
5. **Background Processing** - "Out-of-loop" pattern for context window optimization

The system represents a mature implementation of multi-agent workflows using Claude Code's native capabilities, following proven architectural patterns while maintaining enterprise-grade security and observability.