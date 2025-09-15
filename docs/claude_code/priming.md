
  🎯 Context Priming Strategy Matrix

  Scenario 1: New Projects

  Main Claude Agent:
  1. Automatic: SessionStart → context-prime.py loads basic project structure
  2. Manual: /prime-research to analyze codebase patterns and architecture
  3. Bundle: No existing bundles, starts fresh context trail

  Background Claude Agent:
  - Inherits context through /background [agent] "task" command
  - Gets focused context specific to delegated task
  - Creates isolated context bundle for the background work

  Sub-Agents (via Task tool):
  - Receive system prompts with domain expertise (researcher, coder, etc.)
  - Inherit current session context when spawned
  - Work in partially forked context (Dan's pattern)

  Scenario 2: Continuing Existing Projects

  Main Claude Agent:
  1. Automatic: context-prime.py + bundle-manager.py suggest recent bundles
  2. Manual: /loadbundle reports/context-bundles/session_bundle.jsonl
  3. Task-Specific: /prime-implement "new feature" for focused work

  Background Claude Agent:
  - Can inherit restored context from main agent's bundle loading
  - Or start with fresh focused context for new background tasks
  - Example: /loadbundle session.jsonl then /background coder "implement 
  feature"

  Sub-Agents:
  - Inherit current context from main agent (after bundle loading)
  - Get domain-specific system prompts
  - Access to restored file context from bundle reconstruction

  Scenario 3: New Features in Existing Project

  Main Claude Agent:
  1. Prime for Implementation: /prime-implement "OAuth authentication"
    - Orchestrator agent analyzes existing patterns
    - Loads relevant code and architecture context
    - Prepares implementation roadmap

  Background Agents (Out-of-Loop Pattern):
  # After priming main context
  /background researcher "analyze existing auth patterns and security 
  requirements"
  - Gets focused research context without cluttering main agent
  - Works independently with specific task context

  Sub-Agents (Multi-Agent Workflows):
  # Within main context after priming
  Use orchestrator agent to "implement OAuth with existing user system"
  - researcher → coder → tester → reviewer → documenter
  - Each gets inherited context + domain expertise

  📋 Context Flow Patterns

  Pattern 1: Fresh Start

  New Project → context-prime.py → /prime-research → Work begins

  Pattern 2: Context Restoration

  Session Start → bundle-manager.py suggests bundles → /loadbundle → Continue
  work

  Pattern 3: Feature Implementation

  /prime-implement "feature" → orchestrator agent → researcher/coder/tester
  chain

  Pattern 4: Background Delegation

  Main context ready → /background agent "task" → Independent background work

  🔄 Context Inheritance Hierarchy

  Main Agent Context:
  - Automatic session priming
  - Bundle restoration capability
  - Task-specific priming commands

  ↓ Inherits to Background Agents:
  - Current session context
  - Specific task focus
  - Isolated bundle creation

  ↓ Inherits to Sub-Agents (Task tool):
  - Session context + System prompt
  - Domain expertise + Current context
  - Shared context window

  🎯 Best Practices by Scenario

  Starting New Work:

  1. Let automatic priming run (context-prime.py)
  2. Use appropriate prime command:
    - /prime-research for understanding
    - /prime-implement for building
    - /prime-debug for fixing
    - /prime-review for security

  Continuing Work:

  1. Accept bundle suggestions from bundle-manager.py
  2. /loadbundle relevant session
  3. Continue with primed context

  Complex Features:

  1. /prime-implement "feature description"
  2. Use orchestrator for multi-agent coordination
  3. Background agents for parallel work

  Long-Running Work:

  1. Work until context window stress
  2. Natural bundle creation happens automatically
  3. New session: bundle restoration → continue

  🚀 The Context Engineering Advantage

  Everyone Gets Context Because:

  1. Main Agent: Dynamic priming + bundle restoration + task-specific priming
  2. Background Agents: Inherit context + focused delegation + isolated work
  3. Sub-Agents: Session context + domain expertise + system prompts

  Result: No context loss, maximum focus, scalable workflows