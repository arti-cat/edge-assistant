# pyConductor Usage Guide

> **"A focused agent is a performant agent"** - Complete step-by-step guide to using the pyConductor multi-agent development framework

## Quick Start Commands

```bash
# Research a topic/site
/background researcher "analyze website.co.uk site structure and scraping requirements"

# Generate a new Python project
/generate my-scraper --template cli

# Implement a feature with full workflow
/implement "website.co.uk data scraper"

# Track simple tasks
/track "update scraper configuration for new site"

# Prime context for specific work
/prime-research website.co.uk
/prime-implement scraper-features
```

---

## 1. Understanding the Framework

### Core Components
- **6 Specialized Agents** - Each focused on one domain
- **Dynamic Hooks** - Automated lifecycle management
- **Context Bundles** - Session restoration after context limits
- **JSONL Logging** - Complete observability trail

### Agent Types
- **researcher** 🔍 - Analysis, patterns, requirements gathering
- **generator** ⚡ - Lightning-fast Python project creation with UV
- **coder** 💻 - Implementation following discovered patterns
- **tester** 🧪 - Test creation and execution
- **reviewer** 🛡️ - Security and quality assessment (read-only)
- **orchestrator** 🎯 - Multi-agent workflow coordination
- **documenter** 📚 - API docs and usage examples

---

## 2. Research-First Approach (Recommended)

### Step 1: Background Research
```bash
/background researcher "analyze website.co.uk site structure, authentication flow, and data extraction requirements"
```

**What this does:**
- Runs researcher agent independently without polluting main context
- Analyzes site structure, URL patterns, authentication
- Identifies data extraction points and challenges
- Provides structured recommendations for implementation

**Expected output:**
- Requirements analysis
- Architecture recommendations
- Technology stack suggestions
- Implementation roadmap
- Risk assessment

### Step 2: Review Research Results
The researcher will return findings. Based on results, choose next approach.

### Step 3A: Generate Project (if new project needed)
```bash
/generate auction-scraper --template cli --description "scraper with authentication and data extraction"
```

### Step 3B: Implement Feature (if extending existing)
```bash
/implement "auction data scraper with authentication, rate limiting, and data persistence based on research findings"
```

---

## 3. Direct Implementation Approach

### Single Command Full Workflow
```bash
/implement "complete website.co.uk scraper with authentication, auction data extraction, and export functionality"
```

**What happens:**
1. **Orchestrator** coordinates the full workflow
2. **Researcher** analyzes requirements and existing patterns
3. **Coder** implements following discovered patterns
4. **Tester** creates comprehensive tests
5. **Reviewer** performs security and quality assessment
6. **Documenter** updates documentation

**When to use:** When you want complete automation and trust the system to make architectural decisions.

---

## 4. Generator-First Approach

### Step 1: Create Project Foundation
```bash
/generate scraper-project --template cli
```

**Available templates:**
- `fastapi` - Web API with automatic docs
- `flask` - Traditional web app
- `cli` - Command-line tool (recommended for scrapers)
- `datascience` - Jupyter, pandas, ML tools

### Step 2: Implement Core Features
```bash
/implement "authentication handler for website.co.uk login system"
/implement "auction data extractor with rate limiting"
/implement "data persistence layer with SQLite and JSONL export"
```

**When to use:** When you want control over project structure and incremental development.

---

## 5. Context Management

### Prime Commands (Optimize Context Window)
```bash
# Prime for research tasks
/prime-research website-scraping

# Prime for implementation
/prime-implement scraper-authentication

# Prime for debugging
/prime-debug authentication-flow
```

### Bundle Management (Session Restoration)
```bash
# Save context when approaching limits
# (Automatic via hooks)

# Restore previous session
/loadbundle reports/context-bundles/session-id_bundle.jsonl

# List available bundles
/loadbundle
```

---

## 6. Task Tracking

### Simple Task Management
```bash
/track "implement authentication for website.co.uk"
```

**Features:**
- Progress tracking
- User visibility into development process
- Automatic completion detection
- Integration with hook system

---

## 7. Advanced Patterns

### Parallel Development
```bash
# Research site structure while generating project
/background researcher "analyze webbsite.co.uk authentication and data structure"
/generate auction-scraper --template cli
```

### Staged Implementation
```bash
# Phase 1: Authentication
/implement "authentication system for website.co.uk with session management"

# Phase 2: Data extraction
/implement "auction listing scraper with pagination and rate limiting"

# Phase 3: Data processing
/implement "auction data parser and export functionality"
```

### Quality Assurance
```bash
# Security and quality review
/review src/scraper/

# Background testing while continuing development
/background tester "create comprehensive test suite for authentication and scraping modules"
```

---

## 8. Troubleshooting Common Issues

### Context Window Exhaustion
**Symptoms:** Agent responses become truncated or fail
**Solution:**
```bash
/loadbundle  # Restore from bundle
/prime-implement current-feature  # Optimize context
```

### Agent Coordination Issues
**Symptoms:** Agents not finding previous work
**Solution:** Check `reports/coordination.jsonl` for delegation trails

### Security Blocks
**Symptoms:** Commands blocked by security filter
**Solution:** Check `.claude/settings.json` permissions, adjust if needed

---

## 9. Best Practices

### ✅ Do:
- Start with research for complex projects
- Use background agents for independent work
- Track progress with `/track` for visibility
- Let agents specialize (don't micromanage)
- Use prime commands to optimize context
- Review agent outputs before proceeding

### ❌ Don't:
- Mix multiple concerns in single commands
- Ignore security warnings from reviewer
- Skip research phase for unfamiliar domains
- Manually manage context (let hooks handle it)
- Override agent recommendations without justification

---

## 10. Example Workflows

### Workflow A: Complete Automation
```bash
/implement "website.co.uk scraper with authentication, data extraction, and export"
```
**Time:** ~10-15 minutes
**Control:** Low
**Quality:** High (all agents involved)

### Workflow B: Research → Generate → Implement
```bash
/background researcher "analyze website.co.uk requirements"
# Review results
/generate auction-scraper --template cli
/implement "authentication and data extraction based on research"
```
**Time:** ~15-20 minutes
**Control:** Medium
**Quality:** Very High (research-informed)

### Workflow C: Incremental Development
```bash
/generate base-scraper --template cli
/implement "basic authentication system"
/implement "auction listing extraction"
/implement "data persistence and export"
/review src/
```
**Time:** ~20-25 minutes
**Control:** High
**Quality:** High (staged development)

---

## 11. Monitoring and Observability

### Activity Logs
- `reports/activity.jsonl` - File operations and tool usage
- `reports/coordination.jsonl` - Agent delegation events
- `reports/tasks.jsonl` - User-tracked tasks
- `reports/context-bundles/` - Session restoration data

### Real-time Status
The status line shows current context, active agents, and system state.

---

## 12. Getting Help

### System Information
```bash
# View available templates
/generate --help

# Check agent capabilities
# Read .claude/agents/*.md files

# Review command options
# Read .claude/commands/*.md files
```

### Debug Commands
```bash
/prime-debug specific-issue
/review problematic-code
/background researcher "investigate specific-problem"
```

---

## Ready to Start?

Choose your approach:
1. **Full automation:** `/implement "your complete requirements"`
2. **Research first:** `/background researcher "analyze your-target-site"`
3. **New project:** `/generate project-name --template cli`

The framework will handle the rest!