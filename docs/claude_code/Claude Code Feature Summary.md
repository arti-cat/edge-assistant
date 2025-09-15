Claude Code Feature Summary 
# 🤖 Agents (Subagents)

* **Purpose**: Specialized AI workers that handle focused tasks (reviewing, debugging, testing).
* **Managing agents**:

  * `/agents` → interactive menu for viewing, editing, creating, deleting subagents
  * Example:

    ```
    > use the code-reviewer subagent to check the auth module
    > have the debugger subagent investigate login failures
    ```
* **Creating agents**: Store configs in `.claude/agents/` (project) or `~/.claude/agents/` (personal).
  Example :

  ```yaml
  ---
  name: test-runner
  description: Run tests and fix failures
  ---
  You are a test automation expert. Proactively run tests when code changes,
  analyze failures, and fix them without altering intent.
  ```

---

# ⌨️ Commands (Slash Commands)

* **Built-ins**: `/help`, `/clear`, `/model`, `/agents`, `/ide`, `/init`, `/mcp`
* **File references**: Use `@` to inject file content :

  ```
  Review @src/utils/helpers.js
  Compare @src/old.js with @src/new.js
  ```
* **MCP commands**: Generated from integrations, format:

  ```
  /mcp__<server>__<prompt> [args]
  ```

  Example  :

  ```
  /mcp__github__list_prs
  ```
* **Custom commands**:

  * Stored in `.claude/commands/` or `~/.claude/commands/`
  * Can use `$ARGUMENTS`, `$1`, `$2`, etc. for parameterization
  * Example:

    ```yaml
    ---
    argument-hint: [pr-number] [priority]
    description: Review pull request
    ---
    Review PR #$1 with priority $2
    ```

---

# 🪝 Hooks

* **Purpose**: Run external scripts at lifecycle events or tool use.
* **Events**:

  * `SessionStart`
  * `UserPromptSubmit`
  * `PreToolUse`, `PostToolUse` 【5†context7\_claude\_code.md】
  * `Notification`
  * `Stop`, `SubagentStop`
* **Hook configuration** :
  {
  "PreToolUse": \[
  {
  "matcher": "Bash",
  "hooks": \[{ "type": "command", "command": "log-bash.sh" }]
  }
  ]
  }
  }

  ```
  ```
* **Examples**:

  * Log Bash commands before execution
  * Prevent edits to `.env`/sensitive files
  * Auto-format Markdown or TypeScript files after writes
  * Desktop notifications on user input requests

---

# 🎨 Output Styles

* **Custom styles**: Stored as `.claude/styles/*.md` with YAML + instructions :

  ```yaml
  ---
  name: My Custom Style
  description: Helpful debugging assistant
  ---
  # Custom Style Instructions
  Always explain errors step by step.

  ## Specific Behaviors
  - Provide minimal repro code
  - Suggest fixes with reasoning
  ```
* **CLI output formats**  :

  * `text` (default) → plain human-readable
  * `json` → structured machine-readable
  * `stream-json` → incremental JSON for live integrations

  ```sh
  claude -p "analyze code" --output-format json
  ```

---

✅ **In summary**:

* **Agents** = specialized personalities.
* **Commands** = reusable triggers (built-in, MCP, or custom).
* **Hooks** = automation for tool usage and lifecycle events.
* **Output styles** = how Claude presents results, both visually and structurally.



Agents

  Built-in Agent Types (available via Task tool):
  - general-purpose - Research, code search, multi-step tasks (Tools: *)
  - coder - Code implementation with TDD (Tools: *)
  - reviewer - Code reviews for security/performance (Tools: *)
  - researcher - Documentation gathering and synthesis (Tools: *)
  - orchestrator - R&D planning and delegation (Tools: *)
  - git-ops - Complex git operations and merges (Tools: *)
  - background-runner - Self-orchestrating with infinite loops (Tools: *)
  - doc-scraper - Documentation fetching (Tools: *)

  Subagent System:
  - Location: .claude/agents/ (project) or ~/.claude/agents/ (user)
  - Format: Markdown files with YAML frontmatter
  - Configuration: Name, description, tools, system prompt
  - Context: Isolated context windows per subagent
  - Priority: Project-level overrides user-level

  Key Features

  Subagent Benefits:
  - Preserved context isolation
  - Specialized expertise domains
  - Reusability across projects
  - Flexible tool permissions

  Invocation Methods:
  - Automatic delegation based on task description
  - Explicit requests: "Use [subagent-name] to [task]"
  - Chaining for sequential workflows

  Management:
  - /agents command for interactive management
  - Direct file creation in .claude/agents/

  Example Configuration Structure

  ---
  name: subagent-name
  description: When to invoke this subagent
  tools: Read, Edit, Bash  # Optional - inherits all if omitted
  ---

  System prompt defining role and capabilities

  The documentation shows Claude Code has both built-in agent types (accessed
   via Task tool) and customizable subagents (user-defined configurations).

Commands

  Built-in Slash Commands

  Core Session Management:
  - /help - Get help with commands and usage
  - /clear - Clear conversation history
  - /cost - Show token usage and cost statistics
  - /doctor - Check installation health
  - /add-dir - Add additional working directories
  - /init - Initialize project memory (CLAUDE.md file)
  - /agents - Manage subagents (create, edit, delete)

  Code Review & Git:
  - /review - Request code review
  - claude commit - Create git commits directly
  - claude -c - Continue previous conversation
  - claude -r - Resume session

  Custom Commands System

  Command Locations:
  - Project Commands: .claude/commands/ (shared with team)
  - Personal Commands: ~/.claude/commands/ (user-specific across all
  projects)

  Command Format:
  ---
  allowed-tools: Bash(git add:*), Bash(git status:*)
  argument-hint: [message]
  description: Create a git commit
  model: claude-3-5-haiku-20241022
  ---

  Your prompt template with $ARGUMENTS or $1, $2, etc.

  Argument Handling:
  - $ARGUMENTS - All arguments as single string
  - $1, $2, $3 - Individual positional arguments
  - @filename - Include file contents

  MCP Commands

  Format: /mcp__<server-name>__<prompt-name> [arguments]

  Examples:
  /mcp__github__list_prs
  /mcp__github__pr_review 456
  /mcp__jira__create_issue "Bug title" high

  Command Features

  Dynamic Context with ! prefix:
  ---
  allowed-tools: Bash(git add:*)
  ---
  Current status: !`git status`
  Create commit based on above changes.

  File References:
  # Reference specific files
  /optimize @src/utils/helpers.js

  # Compare files  
  /compare @src/old.js @src/new.js

  CLI Usage Patterns

  Interactive Mode:
  claude                    # Start interactive session
  claude "fix the build"    # One-time command
  claude -p "explain this"  # Print mode (no interaction)

  Configuration:
  claude config list              # Show all settings
  claude config set key value     # Set configuration
  claude config add key value     # Add to list setting

  Installation & Health:
  claude doctor               # Check installation
  which claude               # Verify PATH (Unix)
  where claude              # Verify PATH (Windows)

  The command system is highly extensible through custom commands, MCP
  integration, and hooks for advanced automation workflows.

Hooks

   Claude Code Hooks System Documentation

  Hook Events and Lifecycle

  Available Hook Events:
  - SessionStart - When Claude session begins
  - SessionEnd - When Claude session ends
  - UserPromptSubmit - Before processing user prompts
  - PreToolUse - Before any tool execution
  - PostToolUse - After tool execution completes
  - Stop - When Claude finishes responding
  - SubagentStop - When subagent stops
  - PreCompact - Before conversation compacting
  - Notification - When Claude sends notifications

  Configuration Structure

  Hook Configuration Format:
  {
    "hooks": {
      "EventName": [
        {
          "matcher": "ToolPattern",  // Optional for global events
          "hooks": [
            {
              "type": "command",
              "command": "your-command-here",
              "timeout": 60000  // Optional, ms
            }
          ]
        }
      ]
    }
  }

  Configuration Locations:
  - User: ~/.claude/settings.json
  - Project: .claude/settings.json
  - Local: .claude/settings.local.json
  - Enterprise: Managed policy paths

  Hook Input/Output

  Common Input Fields:
  {
    "session_id": "string",
    "transcript_path": "string",
    "cwd": "string",
    "hook_event_name": "string"
  }

  Control Output Fields:
  {
    "continue": true,              // Whether to continue processing
    "stopReason": "string",        // Message when stopping
    "suppressOutput": true,        // Hide from transcript
    "systemMessage": "string",     // Warning to user
    "decision": "allow|deny|block|ask",  // Permission control
    "hookSpecificOutput": {        // Event-specific data
      "additionalContext": "string"
    }
  }

  Tool Matching Patterns

  Matcher Examples:
  - "Bash" - All Bash commands
  - "Edit|MultiEdit|Write" - Multiple tools (regex)
  - "mcp__.*__write.*" - MCP tool patterns
  - "" or omitted - All events (global)

  Environment Variables

  Available in Hook Commands:
  - CLAUDE_PROJECT_DIR - Project root directory path

  Common Use Cases

  PreToolUse Hooks:
  {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> 
  ~/.claude/bash-log.txt"
          }
        ]
      }
    ]
  }

  PostToolUse Hooks:
  {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/formatter.py"
          }
        ]
      }
    ]
  }

  File Protection:
  {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json,sys; 
  data=json.load(sys.stdin); 
  path=data.get('tool_input',{}).get('file_path',''); sys.exit(2 if any(p in 
  path for p in ['.env', '.git/']) else 0)\""
          }
        ]
      }
    ]
  }

  Security Considerations

  - Hooks run with current user credentials
  - Always review hook code before deployment
  - Use exit codes to control behavior:
    - 0 - Success, continue
    - 1 - Warning, continue
    - 2 - Error, block tool execution
  - Environment variables available to hook processes

  Debugging

  Debug Mode:
  claude --debug

  Shows detailed hook execution information including matching, command
  execution, and exit status.

  Hooks provide powerful automation and control over Claude Code's behavior,
  enabling custom workflows, validation, formatting, and security policies.

Output Styles

 Claude Code Output Styles Documentation

  What are Output Styles?

  Purpose: Output styles enable customizing Claude Code for different use cases beyond traditional
   software engineering while retaining core capabilities (file operations, scripts, TODOs).

  How They Work: Output styles directly modify Claude's system prompt by "turning off" software
  engineering-specific instructions and replacing them with custom behavior definitions.

  Built-in Styles

  Available Styles:
  - Default - Efficient software engineering tasks
  - Explanatory - Educational insights and detailed explanations
  - Learning - Collaborative learn-by-doing with human contributions

  Style Management Commands

  View/Change Styles:
  /output-style              # Access style menu
  /output-style [style-name] # Direct style selection
  /output-style explanatory  # Example: switch to explanatory

  Create Custom Styles:
  /output-style:new I want an output style that [description]

  Custom Style Structure

  File Format (.claude/output-styles/ or ~/.claude/output-styles/):
  ---
  name: My Custom Style
  description: Brief description of what this style does
  ---

  # Custom Style Instructions

  You are an interactive CLI tool that helps users with software engineering
  tasks. [Your custom instructions here...]

  ## Specific Behaviors

  [Define how the assistant should behave in this style...]

  Output Format Control

  CLI Output Formats:
  # Text output (default)
  claude -p "query" --output-format text

  # Structured JSON with metadata
  claude -p "query" --output-format json

  # Streaming JSON (real-time)
  claude -p "query" --output-format stream-json

  JSON Output Structure:
  {
    "result": "Response content",
    "total_cost_usd": 0.01234,
    "duration_ms": 2300,
    "model": "claude-3-5-sonnet-20241022"
  }

  Status Line Integration

  Status Line Script Input (JSON via stdin):
  {
    "session_id": "abc123",
    "model": {"display_name": "Opus"},
    "workspace": {
      "current_dir": "/path/to/project",
      "project_dir": "/original/path"
    },
    "output_style": {"name": "default"},
    "cost": {
      "total_cost_usd": 0.01234,
      "total_duration_ms": 45000
    }
  }

  Example Status Line Script:
  #!/bin/bash
  input=$(cat)
  MODEL=$(echo "$input" | jq -r '.model.display_name')
  DIR=$(echo "$input" | jq -r '.workspace.current_dir')
  echo "[$MODEL] 📁 ${DIR##*/}"

  Key Differences

  Output Styles vs Other Customization:
  - Output Styles: Replace core system prompt, fundamental behavior change
  - CLAUDE.md: Adds context as user message after system prompt
  - --append-system-prompt: Appends to existing system prompt without disabling core instructions
  - Agents/Subagents: Handle specific tasks with additional configurations (model, tools, context)

  Formatting and Automation

  Automatic Formatting via Hooks:
  {
    "hooks": {
      "PostToolUse": [
        {
          "matcher": "Edit|MultiEdit|Write",
          "hooks": [
            {
              "type": "command",
              "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/formatter.py"
            }
          ]
        }
      ]
    }
  }

  Output styles provide flexible customization for different workflows while maintaining Claude
  Code's core functionality and tool ecosystem integration.

---

## Further reading

For practical project setup and guidance, see:

- docs/claude/README.md — `.claude/` directory structure and quickstart
- docs/claude/agents.md — subagents design and templates
- docs/claude/commands.md — custom commands patterns
- docs/claude/hooks.md — hooks configuration and safety
- docs/claude/output-styles.md — output styles and JSON usage
