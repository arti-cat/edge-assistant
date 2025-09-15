========================
CODE SNIPPETS
========================
TITLE: Native Install of Claude Code for Windows PowerShell
DESCRIPTION: Installs Claude Code natively on Windows systems using PowerShell's `Invoke-RestMethod` (irm) to download and execute an installation script. This native installation method is currently in beta.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: PowerShell
CODE:
```
irm https://claude.ai/install.ps1 | iex
```

----------------------------------------

TITLE: Install and Get Started with Claude Code CLI
DESCRIPTION: This snippet provides the commands to install Claude Code globally using npm, navigate to a project directory, and initialize the Claude Code CLI. It notes that a login prompt will appear on first use.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/index

LANGUAGE: Shell
CODE:
```
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Navigate to your project
cd your-awesome-project

# Start coding with Claude
claude
# You'll be prompted to log in on first use
```

----------------------------------------

TITLE: Ask Claude Code Questions about its Capabilities
DESCRIPTION: Examples of interactive commands to inquire about Claude Code's own features and functionalities. Users can ask about its capabilities, how to use slash commands, or its compatibility with other tools like Docker.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: Shell
CODE:
```
> what can Claude Code do?

> how do I use slash commands in Claude Code?

> can Claude Code work with Docker?
```

----------------------------------------

TITLE: Native Install of Claude Code for Windows CMD
DESCRIPTION: Installs Claude Code natively on Windows systems using the Command Prompt (CMD) by downloading an installation script via curl, executing it, and then deleting the script. This native installation method is currently in beta.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: Shell
CODE:
```
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

----------------------------------------

TITLE: Navigate to project and start Claude Code CLI
DESCRIPTION: After installing Claude Code, use these commands to change into your project directory and then launch the Claude Code CLI. This initiates the tool within your project context.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/setup

LANGUAGE: Shell
CODE:
```
cd your-awesome-project
claude
```

----------------------------------------

TITLE: Start an Interactive Claude Code Session
DESCRIPTION: Navigates to a specific project directory and then launches an interactive Claude Code session. This command is the entry point for using the AI assistant within the context of a code project.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: Shell
CODE:
```
cd /path/to/your/project
claude
```

----------------------------------------

TITLE: Native Install of Claude Code for macOS, Linux, and WSL
DESCRIPTION: Performs a native installation of Claude Code on Unix-like operating systems (macOS, Linux, and Windows Subsystem for Linux) by executing a script downloaded via curl. This native installation method is currently in beta.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: Shell
CODE:
```
curl -fsSL https://claude.ai/install.sh | bash
```

----------------------------------------

TITLE: Ask Claude Code Questions for Project Understanding
DESCRIPTION: Examples of interactive commands to query Claude Code about the current project. Claude can analyze files to provide summaries, identify technologies, locate main entry points, and explain folder structures.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: Shell
CODE:
```
> what does this project do?

> what technologies does this project use?

> where is the main entry point?

> explain the folder structure
```

----------------------------------------

TITLE: Install Claude Code CLI via NPM
DESCRIPTION: Installs the Claude Code command-line interface globally using npm. This method requires Node.js version 18 or newer to be installed on the system.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: JavaScript
CODE:
```
npm install -g @anthropic-ai/claude-code
```

----------------------------------------

TITLE: Common Development Workflows with Claude Code
DESCRIPTION: Provides examples of how Claude Code can assist with various development tasks such as refactoring code, writing unit tests, updating documentation, and performing code reviews using natural language prompts.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: Prompt
CODE:
```
> refactor the authentication module to use async/await instead of callbacks
```

LANGUAGE: Prompt
CODE:
```
> write unit tests for the calculator functions
```

LANGUAGE: Prompt
CODE:
```
> update the README with installation instructions
```

LANGUAGE: Prompt
CODE:
```
> review my changes and suggest improvements
```

----------------------------------------

TITLE: Migrate Claude Code Installer to Local (NPM)
DESCRIPTION: Command to migrate the Claude Code installer to a local setup after a global npm installation, helping to avoid autoupdater permission issues.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/setup

LANGUAGE: Shell
CODE:
```
claude migrate-installer
```

----------------------------------------

TITLE: Essential Claude Code CLI Commands
DESCRIPTION: Lists fundamental command-line interface commands for interacting with Claude Code, including starting interactive mode, running one-time tasks, continuing conversations, managing sessions, and performing Git commits directly.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: Shell
CODE:
```
claude
```

LANGUAGE: Shell
CODE:
```
claude "fix the build error"
```

LANGUAGE: Shell
CODE:
```
claude -p "explain this function"
```

LANGUAGE: Shell
CODE:
```
claude -c
```

LANGUAGE: Shell
CODE:
```
claude -r
```

LANGUAGE: Shell
CODE:
```
claude commit
```

LANGUAGE: Shell
CODE:
```
> /clear
```

LANGUAGE: Shell
CODE:
```
> /help
```

LANGUAGE: Shell
CODE:
```
> exit
```

----------------------------------------

TITLE: Create and run a basic Claude Code legal agent in Python
DESCRIPTION: This quick start guide demonstrates how to build a simple AI agent using the `ClaudeSDKClient` in Python. The example configures a legal assistant agent with a system prompt, sends a query, and streams the response, showcasing asynchronous interaction. Instructions for running the script and using it in IPython/Jupyter are provided.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: Python
CODE:
```
import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def main():
    async with ClaudeSDKClient(
        options=ClaudeCodeOptions(
            system_prompt="You are a legal assistant. Identify risks and suggest improvements.",
            max_turns=2
        )
    ) as client:
        # Send the query
        await client.query(
            "Review this contract clause for potential issues: 'The party agrees to unlimited liability...'"
        )

        # Stream the response
        async for message in client.receive_response():
            if hasattr(message, 'content'):
                # Print streaming content as it arrives
                for block in message.content:
                    if hasattr(block, 'text'):
                        print(block.text, end='', flush=True)

if __name__ == "__main__":
    asyncio.run(main())
```

LANGUAGE: Bash
CODE:
```
python legal-agent.py
```

LANGUAGE: Python
CODE:
```
await main()
```

----------------------------------------

TITLE: Get a Quick Codebase Overview with Claude Code
DESCRIPTION: Use Claude Code to rapidly understand the structure of a new project. Start by navigating to the project root and launching Claude Code, then ask broad questions about the codebase, architecture, data models, and authentication to gain a high-level understanding.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: Shell
CODE:
```
cd /path/to/project
```

LANGUAGE: Shell
CODE:
```
claude
```

LANGUAGE: Claude Code CLI
CODE:
```
> give me an overview of this codebase
```

LANGUAGE: Claude Code CLI
CODE:
```
> explain the main architecture patterns used here
```

LANGUAGE: Claude Code CLI
CODE:
```
> what are the key data models?
```

LANGUAGE: Claude Code CLI
CODE:
```
> how is authentication handled?
```

----------------------------------------

TITLE: Install latest Claude Code native binary on macOS/Linux/WSL
DESCRIPTION: This command downloads and executes the installation script for the *latest* version of the Claude Code native binary. It uses `curl` to fetch the script and pipes it to `bash` with the `latest` argument, ensuring the most recent build is installed.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/setup

LANGUAGE: Shell
CODE:
```
# Install latest version
curl -fsSL https://claude.ai/install.sh | bash -s latest
```

----------------------------------------

TITLE: Install Native Claude Code on macOS, Linux, and WSL
DESCRIPTION: Instructions for installing the beta native Claude Code installer on Unix-like systems. Includes commands for stable, latest, and specific version installations using `curl`.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/troubleshooting

LANGUAGE: bash
CODE:
```
# Install stable version (default)
curl -fsSL https://claude.ai/install.sh | bash

# Install latest version
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Install specific version number
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```

----------------------------------------

TITLE: Install Claude Code on Windows using PowerShell
DESCRIPTION: Provides PowerShell commands to install Claude Code, including options for installing the stable, latest, or a specific version number.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/setup

LANGUAGE: PowerShell
CODE:
```
# Install stable version (default)
irm https://claude.ai/install.ps1 | iex
```

LANGUAGE: PowerShell
CODE:
```
# Install latest version
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest
```

LANGUAGE: PowerShell
CODE:
```
# Install specific version number
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58
```

----------------------------------------

TITLE: Install stable Claude Code native binary on macOS/Linux/WSL
DESCRIPTION: This command downloads and executes the installation script for the stable version of the Claude Code native binary. It uses `curl` to fetch the script and pipes it directly to `bash` for execution, providing a fresh installation.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/setup

LANGUAGE: Shell
CODE:
```
# Install stable version (default)
curl -fsSL https://claude.ai/install.sh | bash
```

----------------------------------------

TITLE: Advanced Prompting Techniques for Claude Code
DESCRIPTION: Offers best practices for interacting with Claude Code, demonstrating how to formulate specific requests, break down complex tasks into step-by-step instructions, and allow Claude to analyze code or data before making changes.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: Prompt
CODE:
```
> 1. create a new database table for user profiles
```

LANGUAGE: Prompt
CODE:
```
> 2. create an API endpoint to get and update user profiles
```

LANGUAGE: Prompt
CODE:
```
> 3. build a webpage that allows users to see and edit their information
```

LANGUAGE: Prompt
CODE:
```
> analyze the database schema
```

LANGUAGE: Prompt
CODE:
```
> build a dashboard showing products that are most frequently returned by our UK customers
```

----------------------------------------

TITLE: Install Claude Code globally using npm
DESCRIPTION: This command installs the Claude Code CLI tool globally on your system using npm. It requires Node.js 18+ to be installed. Avoid using `sudo` to prevent permission issues.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/setup

LANGUAGE: JavaScript
CODE:
```
npm install -g @anthropic-ai/claude-code
```

----------------------------------------

TITLE: Install Claude Code on Windows using Command Prompt
DESCRIPTION: Provides CMD commands to install Claude Code, including options for stable, latest, or a specific version number, handling download and cleanup.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/setup

LANGUAGE: CMD
CODE:
```
REM Install stable version (default)
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

LANGUAGE: CMD
CODE:
```
REM Install latest version
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd latest && del install.cmd
```

LANGUAGE: CMD
CODE:
```
REM Install specific version number
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 1.0.58 && del install.cmd
```

----------------------------------------

TITLE: Verify Claude Code Installation
DESCRIPTION: Command to run a diagnostic check and verify the successful installation of Claude Code.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/setup

LANGUAGE: Shell
CODE:
```
claude doctor
```

----------------------------------------

TITLE: Making First Code Change with Claude Code
DESCRIPTION: Demonstrates how to prompt Claude Code to add new functionality to a file, showing its process of finding files, proposing changes, and seeking approval before making the edit.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: Prompt
CODE:
```
> add a hello world function to the main file
```

----------------------------------------

TITLE: Claude Code Settings Precedence File Examples
DESCRIPTION: Examples of configuration file paths demonstrating the hierarchy of settings application, from highest (enterprise policies) to lowest (user settings) precedence.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/iam

LANGUAGE: File Path
CODE:
```
.claude/settings.local.json
```

LANGUAGE: File Path
CODE:
```
.claude/settings.json
```

LANGUAGE: File Path
CODE:
```
~/.claude/settings.json
```

----------------------------------------

TITLE: Install Dependencies for Alpine Linux (musl/uClibc)
DESCRIPTION: Instructions for installing necessary dependencies (`libgcc`, `libstdc++`, `ripgrep`) on Alpine Linux and setting the `USE_BUILTIN_RIPGREP` environment variable for native build compatibility.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/setup

LANGUAGE: Shell
CODE:
```
apk add libgcc libstdc++ ripgrep
USE_BUILTIN_RIPGREP=0
```

----------------------------------------

TITLE: Install Claude Code Python SDK and its dependencies
DESCRIPTION: This section provides the necessary commands to install the `claude-code-sdk` Python package from PyPI and its required Node.js dependency, `@anthropic-ai/claude-code`, via NPM. An optional command for installing IPython for interactive development is also included.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: Bash
CODE:
```
pip install claude-code-sdk
npm install -g @anthropic-ai/claude-code
```

LANGUAGE: Bash
CODE:
```
pip install ipython
```

----------------------------------------

TITLE: Install Specific Claude Code Version (Bash/Curl)
DESCRIPTION: Demonstrates how to install a specific version of Claude Code using a curl command piped to bash, suitable for Linux/macOS systems.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/setup

LANGUAGE: Bash
CODE:
```
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```

----------------------------------------

TITLE: Start Claude Code REPL with initial prompt
DESCRIPTION: Starts an interactive REPL session, pre-populating it with an initial query.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude "explain this project"
```

----------------------------------------

TITLE: Claude Code Read & Edit File Permission Examples
DESCRIPTION: Illustrative examples demonstrating the application of absolute, home directory, settings-relative, and current directory relative paths for file read and edit rules.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/iam

LANGUAGE: Configuration
CODE:
```
Read(//Users/alice/secrets/**)
```

LANGUAGE: Configuration
CODE:
```
Read(~/Documents/*.pdf)
```

LANGUAGE: Configuration
CODE:
```
Edit(/src/**/*.ts)
```

LANGUAGE: Configuration
CODE:
```
Read(*.env)
```

LANGUAGE: Configuration
CODE:
```
Edit(/docs/**)
```

LANGUAGE: Configuration
CODE:
```
Read(~/.zshrc)
```

LANGUAGE: Configuration
CODE:
```
Edit(//tmp/scratch.txt)
```

LANGUAGE: Configuration
CODE:
```
Read(src/**)
```

----------------------------------------

TITLE: Install Claude Code via PowerShell
DESCRIPTION: These commands demonstrate how to install the Claude Code CLI tool using a PowerShell script. You can choose to install the latest available version or specify a particular version number. The installation process adds a symlink to `~/.local/bin/claude` and requires the installation directory to be in your system's PATH.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/troubleshooting

LANGUAGE: PowerShell
CODE:
```
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest
```

LANGUAGE: PowerShell
CODE:
```
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58
```

----------------------------------------

TITLE: Install Native Claude Code on Windows PowerShell
DESCRIPTION: Provides the PowerShell command to install the beta native Claude Code installer specifically for Windows environments.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/troubleshooting

LANGUAGE: powershell
CODE:
```
irm https://claude.ai/install.ps1 | iex
```

----------------------------------------

TITLE: Log in to Claude Code on First Use
DESCRIPTION: Initiates an interactive Claude Code session. If it's the first time using Claude Code, the user will be prompted to log in to their Claude.ai or Anthropic Console account. Credentials are then stored for future use.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: Shell
CODE:
```
claude
# You'll be prompted to log in on first use
```

----------------------------------------

TITLE: Configure Claude Code GitHub Action with unified parameters
DESCRIPTION: This configuration example demonstrates how to use the `anthropics/claude-code-action@v1` GitHub Action. It shows the use of `anthropic_api_key` for authentication, an optional `prompt` for instructions, and `claude_args` for passing additional CLI arguments to Claude Code.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/github-actions

LANGUAGE: YAML
CODE:
```
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Your instructions here" # Optional
    claude_args: "--max-turns 5" # Optional CLI arguments
```

----------------------------------------

TITLE: Debugging and Feature Implementation with Claude Code
DESCRIPTION: Shows how to use Claude Code to address bugs or implement new features by describing the desired outcome in natural language. Claude Code will locate relevant code, understand the context, implement a solution, and run tests if available.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: Prompt
CODE:
```
> add input validation to the user registration form
```

LANGUAGE: Prompt
CODE:
```
> there's a bug where users can submit empty forms - fix it
```

----------------------------------------

TITLE: Check Claude Code Version and Installation Details
DESCRIPTION: Use the `claude doctor` command to retrieve comprehensive information about your current Claude Code version, installation type, and system details. This command is essential for verifying your setup, understanding potential behavior changes across updates, and troubleshooting issues.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/costs

LANGUAGE: Shell
CODE:
```
claude doctor
```

----------------------------------------

TITLE: Verify Claude Bash Command Log File
DESCRIPTION: This bash command displays the contents of the `bash-command-log.txt` file, which is populated by the `PreToolUse` hook. It allows users to verify that Claude is correctly logging executed bash commands and their descriptions.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks-guide

LANGUAGE: bash
CODE:
```
cat ~/.claude/bash-command-log.txt
```

----------------------------------------

TITLE: Performing Git Operations Conversationally with Claude Code
DESCRIPTION: Illustrates how Claude Code facilitates common Git tasks through natural language prompts, enabling users to check file status, commit changes, create branches, view commit history, and resolve merge conflicts.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: Prompt
CODE:
```
> what files have I changed?
```

LANGUAGE: Prompt
CODE:
```
> commit my changes with a descriptive message
```

LANGUAGE: Prompt
CODE:
```
> create a new branch called feature/quickstart
```

LANGUAGE: Prompt
CODE:
```
> show me the last 5 commits
```

LANGUAGE: Prompt
CODE:
```
> help me resolve merge conflicts
```

----------------------------------------

TITLE: Example Claude Code settings.json Configuration
DESCRIPTION: This JSON example demonstrates how to configure permissions (allowing/denying specific Bash commands and file reads) and environment variables (`CLAUDE_CODE_ENABLE_TELEMETRY`, `OTEL_METRICS_EXPORTER`) within a `settings.json` file for Claude Code. These settings control Claude Code's behavior and access.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: JSON
CODE:
```
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl:*)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  }
}
```

----------------------------------------

TITLE: Implement Advanced Claude Code SDK Configuration in Python
DESCRIPTION: This example illustrates how to use `ClaudeSDKClient` with advanced `ClaudeCodeOptions` to customize an agent's behavior. It shows setting a custom working directory, additional context paths, specific model and token limits, fine-grained tool control (allowed/disallowed), and passing custom settings and CLI arguments. The example also demonstrates asynchronous interaction with the client to query and receive responses.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: Python
CODE:
```
import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def advanced_agent():
    """Example showcasing advanced configuration options"""
    
    async with ClaudeSDKClient(
        options=ClaudeCodeOptions(
            # Custom working directory and additional context
            cwd="/project/root",
            add_dirs=["/shared/libs", "/common/utils"],
            
            # Model and thinking configuration
            model="claude-3-5-sonnet-20241022",
            max_thinking_tokens=12000,
            
            # Advanced tool control
            allowed_tools=["Read", "Write", "Bash", "Grep"],
            disallowed_tools=["WebSearch", "Bash(rm*)"],
            
            # Custom settings and CLI args
            settings='{"editor": "vim", "theme": "dark"}',
            extra_args={
                "--verbose": None,
                "--timeout": "300"
            }
        )
    ) as client:
        await client.query("Analyze the codebase structure")
        
        async for message in client.receive_response():
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'text'):
                        print(block.text, end='', flush=True)

asyncio.run(advanced_agent())
```

----------------------------------------

TITLE: Create Dynamic API Key Helper Script for LiteLLM
DESCRIPTION: This example bash script illustrates how to dynamically fetch or generate API keys, suitable for scenarios requiring rotating keys or per-user authentication. It includes examples for fetching from a vault or generating a JWT token.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/llm-gateway

LANGUAGE: bash
CODE:
```
#!/bin/bash
# ~/bin/get-litellm-key.sh

# Example: Fetch key from vault
vault kv get -field=api_key secret/litellm/claude-code

# Example: Generate JWT token
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'

```

----------------------------------------

TITLE: Explicitly Log in or Switch Accounts in Claude Code
DESCRIPTION: Allows users to explicitly log in or switch between different Claude.ai or Anthropic Console accounts within an active Claude Code interactive session. Follow the prompts to complete the login process.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/quickstart

LANGUAGE: Shell
CODE:
```
/login
# Follow the prompts to log in with your account
```

----------------------------------------

TITLE: Install Claude Code TypeScript SDK via npm
DESCRIPTION: This snippet provides the command to install the `@anthropic-ai/claude-code` package globally using npm, which is required to use the Claude Code TypeScript SDK.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: bash
CODE:
```
npm install -g @anthropic-ai/claude-code
```

----------------------------------------

TITLE: Migrate Claude Code to Local Installation
DESCRIPTION: This command migrates an existing Claude Code installation to a local directory, typically `~/.claude/local/`. This process sets up an alias in your shell configuration, eliminating the need for `sudo` for future updates. After migration, you should restart your shell for changes to take effect.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/troubleshooting

LANGUAGE: Shell Script
CODE:
```
claude migrate-installer
```

----------------------------------------

TITLE: Configure Claude Hook for Bash Command Logging
DESCRIPTION: This JSON configuration defines a `PreToolUse` hook for Claude. It uses `jq` to extract the command and description from `tool_input` and appends them to a log file (`~/.claude/bash-command-log.txt`) before a tool is used. This allows for auditing or tracking of executed bash commands.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks-guide

LANGUAGE: json
CODE:
```
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \"No description\")\"' >> ~/.claude/bash-command-log.txt"
          }
        ]
      }
    ]
  }
}
```

----------------------------------------

TITLE: Example Bash Script for Dynamic OpenTelemetry Headers
DESCRIPTION: Provides a bash script example that demonstrates how to output valid JSON with string key-value pairs representing HTTP headers. This script can be used as the `otelHeadersHelper` to dynamically fetch authentication tokens.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: bash
CODE:
```
#!/bin/bash
# Example: Multiple headers
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

----------------------------------------

TITLE: Make Claude Markdown Formatter Script Executable
DESCRIPTION: This bash command grants execute permissions to the `markdown_formatter.py` script. This is a necessary step to allow the Claude hook to run the Python script as an external command for automatic markdown formatting.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks-guide

LANGUAGE: bash
CODE:
```
chmod +x .claude/hooks/markdown_formatter.py
```

----------------------------------------

TITLE: Valid OTEL_RESOURCE_ATTRIBUTES Examples (No Spaces)
DESCRIPTION: Provides correct examples for setting the `OTEL_RESOURCE_ATTRIBUTES` environment variable, demonstrating how to use underscores or camelCase instead of spaces to adhere to the W3C Baggage specification.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: bash
CODE:
```
# ✅ Valid - use underscores or camelCase instead
export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"
```

----------------------------------------

TITLE: Diagnose Node.js Path Issues in WSL
DESCRIPTION: Explains how to identify if your WSL environment is incorrectly using a Windows Node.js installation. Suggests verifying `npm` and `node` paths to ensure they point to Linux binaries.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/troubleshooting

LANGUAGE: bash
CODE:
```
which npm
which node
```

----------------------------------------

TITLE: Install ripgrep for Claude Code Search Functionality
DESCRIPTION: Claude Code's search and discovery features rely on `ripgrep`. These commands provide instructions for installing `ripgrep` on various operating systems using their respective package managers. Installing `ripgrep` can resolve issues where search tools, `@file` mentions, and custom agents are not functioning correctly.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/troubleshooting

LANGUAGE: Shell Script
CODE:
```
# macOS (Homebrew)  
brew install ripgrep
```

LANGUAGE: Windows Command Prompt
CODE:
```
# Windows (winget)
winget install BurntSushi.ripgrep.MSVC
```

LANGUAGE: Shell Script
CODE:
```
# Ubuntu/Debian
sudo apt install ripgrep
```

LANGUAGE: Shell Script
CODE:
```
# Alpine Linux
apk add ripgrep
```

LANGUAGE: Shell Script
CODE:
```
# Arch Linux
pacman -S ripgrep
```

----------------------------------------

TITLE: Verify Claude Code Installation
DESCRIPTION: These commands help verify that Claude Code has been successfully installed and is accessible in your system's PATH. The `which` command is used on macOS/Linux/WSL to show the alias path, while `where` is used on Windows to locate the executable. The `doctor` command provides a general health check of the installation.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/troubleshooting

LANGUAGE: Shell Script
CODE:
```
which claude  # Should show an alias to ~/.claude/local/claude
```

LANGUAGE: Windows Command Prompt
CODE:
```
where claude  # Should show path to claude executable
```

LANGUAGE: Shell Script
CODE:
```
claude doctor # Check installation health
```

----------------------------------------

TITLE: Example Claude Commands for Issue and PR Comments
DESCRIPTION: Provides examples of natural language commands that can be used within GitHub issue or pull request comments to interact with the Claude Code action. These commands trigger Claude to analyze context and provide assistance for tasks like feature implementation, authentication design, or bug fixing.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/github-actions

LANGUAGE: Plain Text
CODE:
```
@claude implement this feature based on the issue description
@claude how should I implement user authentication for this endpoint?
@claude fix the TypeError in the user dashboard component
```

----------------------------------------

TITLE: Create Subagents via Direct File Management
DESCRIPTION: This example illustrates how to create subagents by directly managing their configuration files. It shows how to create a project-level subagent by setting up a directory and writing a Markdown/YAML configuration file, defining its name, description, and behavior.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sub-agents

LANGUAGE: Bash
CODE:
```
# Create a project subagent
mkdir -p .claude/agents
echo '---
name: test-runner
description: Use proactively to run tests and fix failures
---

You are a test automation expert. When you see code changes, proactively run the appropriate tests. If tests fail, analyze the failures and fix them while preserving the original test intent.' > .claude/agents/test-runner.md

# Create a user subagent
mkdir -p ~/.claude/agents
# ... create subagent file
```

----------------------------------------

TITLE: Resolve npm OS/Platform Detection in WSL
DESCRIPTION: Addresses issues where Windows `npm` interferes with WSL installations. Provides commands to configure `npm` for Linux or force installation without OS checks.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/troubleshooting

LANGUAGE: bash
CODE:
```
npm config set os linux
npm install -g @anthropic-ai/claude-code --force --no-os-check
```

----------------------------------------

TITLE: JSON Schema for SessionStart Hook Input in Claude Code
DESCRIPTION: This JSON example demonstrates the input structure for the `SessionStart` hook. It includes common session details and a `source` field, indicating how the session was initiated (e.g., 'startup', 'resume', 'clear', or 'compact').

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: json
CODE:
```
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "hook_event_name": "SessionStart",
  "source": "startup"
}
```

----------------------------------------

TITLE: Add a PreToolUse Hook to Log Bash Commands
DESCRIPTION: This shell command, intended for a `PreToolUse` hook, uses `jq` to parse JSON input. It extracts the `command` and `description` from `tool_input`, formatting them into a string. This string is then appended to `~/.claude/bash-command-log.txt`, effectively logging every Bash command Claude Code is about to execute.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks-guide

LANGUAGE: Shell
CODE:
```
jq -r '"\(.tool_input.command) - \(.tool_input.description // "No description")"' >> ~/.claude/bash-command-log.txt
```

----------------------------------------

TITLE: Custom Notification Hook for Claude Code
DESCRIPTION: This hook configuration provides desktop notifications when Claude requires user input. It uses the 'Notification' event type and executes a 'notify-send' command to display a custom message.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks-guide

LANGUAGE: JSON
CODE:
```
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting your input'"
          }
        ]
      }
    ]
  }
}
```

----------------------------------------

TITLE: Configure Claude Hook for Automatic Markdown Formatting
DESCRIPTION: This JSON configuration defines a `PostToolUse` hook that automates markdown file formatting. It triggers after `Edit`, `MultiEdit`, or `Write` operations and executes an external Python script (`markdown_formatter.py`) located in the project's `.claude/hooks` directory. This offloads complex formatting logic to a dedicated script.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks-guide

LANGUAGE: json
CODE:
```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/markdown_formatter.py"
          }
        ]
      }
    ]
  }
}
```

----------------------------------------

TITLE: Implement Custom Permission Prompts for Claude Code SDK Tools
DESCRIPTION: This example illustrates how to implement custom permission handling for tool calls using a permission prompt tool. It configures an MCP server for security, specifies allowed and disallowed tools, and includes an example of an MCP server implementation for an `approval_prompt` function to manage tool access.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: python
CODE:
```
import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def use_permission_prompt():
    """Example using custom permission prompt tool"""

    # MCP server configuration
    mcp_servers = {
        # Example configuration - uncomment and configure as needed:
        # "security": {
        #     "command": "npx",
        #     "args": ["-y", "@modelcontextprotocol/server-security"],
        #     "env": {"API_KEY": "your-key"}
        # }
    }

    async with ClaudeSDKClient(
        options=ClaudeCodeOptions(
            permission_prompt_tool_name="mcp__security__approval_prompt",  # Changed from permission_prompt_tool
            mcp_servers=mcp_servers,
            allowed_tools=["Read", "Grep"],
            disallowed_tools=["Bash(rm*)", "Write"],
            system_prompt="You are a security auditor"
        )
    ) as client:
        await client.query("Analyze and fix the security issues")

        # Monitor tool usage and permissions
        async for message in client.receive_response():
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'type'):  # Added check for 'type' attribute
                        if block.type == 'tool_use':
                            print(f"[Tool: {block.name}] ", end='')
                    if hasattr(block, 'text'):
                        print(block.text, end='', flush=True)

            # Check for permission denials in error messages
            if type(message).__name__ == "ErrorMessage":
                if hasattr(message, 'error') and "Permission denied" in str(message.error):
                    print(f"\n⚠️ Permission denied: {message.error}")

# Example MCP server implementation (Python)
# This would be in your MCP server code
async def approval_prompt(tool_name: str, input: dict, tool_use_id: str = None):
    """Custom permission prompt handler"""
    # Your custom logic here
    if "allow" in str(input):
        return json.dumps({
            "behavior": "allow",
            "updatedInput": input
        })
    else:
        return json.dumps({
            "behavior": "deny",
            "message": f"Permission denied for {tool_name}"
        })

asyncio.run(use_permission_prompt())
```

----------------------------------------

TITLE: Perform Basic Query with Claude Code TypeScript SDK
DESCRIPTION: This example demonstrates the basic usage of the `query` function from the `@anthropic-ai/claude-code` SDK. It shows how to initiate a query with a prompt, handle streaming messages, and configure options such as `maxTurns` and `allowedTools`.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: typescript
CODE:
```
import { query } from "@anthropic-ai/claude-code";

for await (const message of query({
  prompt: "Analyze system performance",
  abortController: new AbortController(),
  options: {
    maxTurns: 5,
    systemPrompt: "You are a performance engineer",
    allowedTools: ["Bash", "Read", "WebSearch"]
  }
})) {
  if (message.type === "result") {
    console.log(message.result);
  }
}
```

----------------------------------------

TITLE: Run Claude Code in Headless Mode with Basic Query
DESCRIPTION: This example demonstrates the fundamental usage of Claude Code's headless mode. It shows how to execute a query non-interactively using the `-p` or `--print` flag, specify allowed tools, set permission modes, and define the current working directory for the operation.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: bash
CODE:
```
claude -p "Stage my changes and write a set of commits for them" \
  --allowedTools "Bash,Read" \
  --permission-mode acceptEdits \
  --cwd /path/to/project
```

----------------------------------------

TITLE: Start Claude Code interactive REPL
DESCRIPTION: Initiates an interactive Read-Eval-Print Loop (REPL) session with Claude Code.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude
```

----------------------------------------

TITLE: Importing multiple files within a CLAUDE.md configuration
DESCRIPTION: This example demonstrates how a `CLAUDE.md` file can import additional files using the `@path/to/import` syntax. It shows importing a README, a package.json, and a git-instructions.md file, illustrating the use of both relative and absolute paths.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/memory

LANGUAGE: CLAUDE.md Syntax
CODE:
```
See @README for project overview and @package.json for available npm commands for this project.

# Additional Instructions
- git workflow @docs/git-instructions.md

```

----------------------------------------

TITLE: Begin Claude Code in a specified permission mode
DESCRIPTION: Starts Claude Code with a predefined permission mode, influencing how it handles tool usage and actions.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude --permission-mode plan
```

----------------------------------------

TITLE: Execute a simple one-shot query using the Claude Code Python SDK
DESCRIPTION: This example demonstrates the `query` function for straightforward, single-turn interactions with the Claude Code SDK. It shows how to send a prompt with configuration options and extract the result from the received message, suitable for quick, non-streaming queries.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: Python
CODE:
```
from claude_code_sdk import query, ClaudeCodeOptions

async for message in query(
    prompt="Analyze system performance",
    options=ClaudeCodeOptions(system_prompt="You are a performance engineer")
):
    if type(message).__name__ == "ResultMessage":
        print(message.result)
```

----------------------------------------

TITLE: Troubleshoot VS Code Extension Installation by Verifying IDE CLI
DESCRIPTION: If the VS Code extension for Claude Code fails to install, a common cause is the absence of the IDE's command-line interface (CLI) tool in the system's PATH. This section lists the required CLI commands for various IDEs and advises on how to install them, typically through an IDE-specific 'Install command in PATH' option.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/ide-integrations

LANGUAGE: Shell
CODE:
```
code
```

LANGUAGE: Shell
CODE:
```
cursor
```

LANGUAGE: Shell
CODE:
```
windsurf
```

LANGUAGE: Shell
CODE:
```
codium
```

----------------------------------------

TITLE: Configure Claude Hook for Automatic TypeScript Formatting
DESCRIPTION: This JSON configuration sets up a `PostToolUse` hook that automatically formats TypeScript files. It triggers after `Edit`, `MultiEdit`, or `Write` operations, extracts the file path, and conditionally runs `npx prettier --write` if the file has a `.ts` extension. This ensures consistent code style.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks-guide

LANGUAGE: json
CODE:
```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -q '\\.ts$'; then npx prettier --write \"$file_path\"; fi; }"
          }
        ]
      }
    ]
  }
}
```

----------------------------------------

TITLE: Configure Claude Code to Use Dynamic API Key Helper
DESCRIPTION: This configuration snippet shows how to instruct Claude Code to use an external script (like the one provided in the previous example) to obtain API keys dynamically.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/llm-gateway

LANGUAGE: json
CODE:
```
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

----------------------------------------

TITLE: Resolve Claude Code Authentication Issues
DESCRIPTION: If you encounter persistent authentication problems with Claude Code, this command can help resolve them. It removes your stored authentication information, forcing a clean login the next time you start Claude Code. This is often a last resort after trying `/logout` and restarting the application.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/troubleshooting

LANGUAGE: Shell Script
CODE:
```
rm -rf ~/.config/claude-code/auth.json
claude
```

----------------------------------------

TITLE: Create Project-Specific Custom Slash Command for Claude Code
DESCRIPTION: This example demonstrates how to create a project-specific custom slash command. Project commands are stored within the repository's `.claude/commands/` directory and are shared with the team. The example creates an '/optimize' command.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/slash-commands

LANGUAGE: Shell
CODE:
```
mkdir -p .claude/commands
echo "Analyze this code for performance issues and suggest optimizations:" > .claude/commands/optimize.md
```

----------------------------------------

TITLE: Retrieve Default Text Output from Claude Code Query (JavaScript)
DESCRIPTION: This example illustrates how to perform a basic query using the `@anthropic-ai/claude-code` SDK and retrieve the default text output. It iterates through the messages returned by the `query` function and logs the `result` property when a message of type "result" is encountered, demonstrating the standard way to get text responses.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: JavaScript
CODE:
```
// Default text output
for await (const message of query({
  prompt: "Explain file src/components/Header.tsx"
})) {
  if (message.type === "result") {
    console.log(message.result);
    // Output: This is a React component showing...
  }
}
```

----------------------------------------

TITLE: Add Local Stdio MCP Server with Claude CLI
DESCRIPTION: Demonstrates how to add a local stdio server using the `claude mcp add` command. This method is ideal for tools requiring direct system access or custom scripts. It explains the basic syntax, provides a real example for an Airtable server, and clarifies the use of the `--` parameter to separate Claude CLI flags from server-specific commands and arguments.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
# Basic syntax
claude mcp add <name> <command> [args...]

# Real example: Add Airtable server
claude mcp add airtable --env AIRTABLE_API_KEY=YOUR_KEY \
  -- npx -y airtable-mcp-server
```

----------------------------------------

TITLE: Add Box Integration to Claude MCP
DESCRIPTION: Ask questions about your enterprise content, get insights from unstructured data, and automate content workflows with Box.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http box https://mcp.box.com/
```

----------------------------------------

TITLE: Configure Custom System Prompts for Claude Code
DESCRIPTION: Explains how to define an agent's role, expertise, and behavior using custom system prompts. It shows examples of setting a `systemPrompt` directly or appending to the default prompt with `appendSystemPrompt`.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: TypeScript
CODE:
```
import { query } from "@anthropic-ai/claude-code";

// SRE incident response agent
for await (const message of query({
  prompt: "API is down, investigate",
  options: {
    systemPrompt: "You are an SRE expert. Diagnose issues systematically and provide actionable solutions.",
    maxTurns: 3
  }
})) {
  if (message.type === "result") console.log(message.result);
}

// Append to default system prompt
for await (const message of query({
  prompt: "Refactor this function",
  options: {
    appendSystemPrompt: "Always include comprehensive error handling and unit tests.",
    maxTurns: 2
  }
})) {
  if (message.type === "result") console.log(message.result);
}
```

----------------------------------------

TITLE: Configure Automatic AWS Credential Refresh in Claude Code Settings
DESCRIPTION: Provides an example JSON configuration for Claude Code's settings file to enable automatic credential refresh. This setup is useful for AWS SSO and corporate identity providers, using `awsAuthRefresh` and `env` settings to manage credential expiry.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock

LANGUAGE: JSON
CODE:
```
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

----------------------------------------

TITLE: Analyze Images and Generate Code from Visual Content with Claude
DESCRIPTION: Learn how to provide images to Claude Code for analysis, context, and code generation. This includes various methods for adding images (drag-and-drop, paste, path) and examples of prompts for describing UI elements, identifying issues in diagrams, and generating CSS/HTML from design mockups.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: AI Prompt
CODE:
```
> What does this image show?
```

LANGUAGE: AI Prompt
CODE:
```
> Describe the UI elements in this screenshot
```

LANGUAGE: AI Prompt
CODE:
```
> Are there any problematic elements in this diagram?
```

LANGUAGE: AI Prompt
CODE:
```
> Here's a screenshot of the error. What's causing it?
```

LANGUAGE: AI Prompt
CODE:
```
> This is our current database schema. How should we modify it for the new feature?
```

LANGUAGE: AI Prompt
CODE:
```
> Generate CSS to match this design mockup
```

LANGUAGE: AI Prompt
CODE:
```
> What HTML structure would recreate this component?
```

----------------------------------------

TITLE: File Protection Hook for Claude Code
DESCRIPTION: This hook prevents Claude from editing sensitive files by intercepting 'Edit', 'MultiEdit', or 'Write' operations. It executes a Python script that checks if the target file path contains restricted patterns like '.env', 'package-lock.json', or '.git/' directories, exiting with an error code if a match is found.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks-guide

LANGUAGE: JSON
CODE:
```
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); sys.exit(2 if any(p in path for p in ['.env', 'package-lock.json', '.git/']) else 0)\"
          }
        ]
      }
    ]
  }
}
```

----------------------------------------

TITLE: Example JSON Configuration for Claude Code Pre-Tool Use Hooks
DESCRIPTION: This JSON snippet illustrates how to define `PreToolUse` hooks within Claude Code's configuration. It shows two examples: one for logging memory operations and another for validating write operations, both executing external commands or scripts based on tool matcher patterns.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: JSON
CODE:
```
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

----------------------------------------

TITLE: Launch or Install Claude Code in IDE Terminal
DESCRIPTION: This command is used to initiate Claude Code within an integrated development environment's terminal. For VS Code users, running `claude` also triggers the automatic installation of the necessary extension, making it the primary entry point for using Claude Code features.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/ide-integrations

LANGUAGE: shell
CODE:
```
claude
```

----------------------------------------

TITLE: Invalid OTEL_RESOURCE_ATTRIBUTES Example (Contains Spaces)
DESCRIPTION: Highlights an incorrect usage of the `OTEL_RESOURCE_ATTRIBUTES` environment variable where the value contains spaces, which violates the W3C Baggage specification. This example shows what *not* to do.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: bash
CODE:
```
# ❌ Invalid - contains spaces
export OTEL_RESOURCE_ATTRIBUTES="org.name=John's Organization"
```

----------------------------------------

TITLE: Python Script for Claude Markdown Formatting Hook
DESCRIPTION: This Python script (`markdown_formatter.py`) is designed to be used as a Claude hook for markdown files. It detects programming languages within unlabeled code blocks, adds appropriate language tags for syntax highlighting, and fixes excessive blank lines. The script processes `.md` and `.mdx` files, ensuring consistent markdown formatting.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks-guide

LANGUAGE: python
CODE:
```
#!/usr/bin/env python3
"""
Markdown formatter for Claude Code output.
Fixes missing language tags and spacing issues while preserving code content.
"""
import json
import sys
import re
import os

def detect_language(code):
    """Best-effort language detection from code content."""
    s = code.strip()
    
    # JSON detection
    if re.search(r'^\s*[{\[]', s):
        try:
            json.loads(s)
            return 'json'
        except:
            pass
    
    # Python detection
    if re.search(r'^\s*def\s+\w+\s*\(', s, re.M) or \
       re.search(r'^\s*(import|from)\s+\w+', s, re.M):
        return 'python'
    
    # JavaScript detection  
    if re.search(r'\b(function\s+\w+\s*\(|const\s+\w+\s*=)', s) or \
       re.search(r'=>|console\.(log|error)', s):
        return 'javascript'
    
    # Bash detection
    if re.search(r'^#!.*\b(bash|sh)\b', s, re.M) or \
       re.search(r'\b(if|then|fi|for|in|do|done)\b', s):
        return 'bash'
    
    # SQL detection
    if re.search(r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE)\s+', s, re.I):
        return 'sql'
        
    return 'text'

def format_markdown(content):
    """Format markdown content with language detection."""
    # Fix unlabeled code fences
    def add_lang_to_fence(match):
        indent, info, body, closing = match.groups()
        if not info.strip():
            lang = detect_language(body)
            return f"{indent}``` {lang}\n{body}{closing}\n"
        return match.group(0)
    
    fence_pattern = r'(?ms)^([ \t]{0,3})```([^\n]*)\n(.*?)(\n\1```)\s*$'
    content = re.sub(fence_pattern, add_lang_to_fence, content)
    
    # Fix excessive blank lines (only outside code fences)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.rstrip() + '\n'

# Main execution
try:
    input_data = json.load(sys.stdin)
    file_path = input_data.get('tool_input', {}).get('file_path', '')
    
    if not file_path.endswith(('.md', '.mdx')):
        sys.exit(0)  # Not a markdown file
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        formatted = format_markdown(content)
        
        if formatted != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted)
            print(f"✓ Fixed markdown formatting in {file_path}")
    
except Exception as e:
    print(f"Error formatting markdown: {e}", file=sys.stderr)
    sys.exit(1)
```

----------------------------------------

TITLE: Execute MCP Slash Command With Arguments
DESCRIPTION: Illustrates how to pass arguments to an MCP prompt. Arguments are provided space-separated after the command. Examples include reviewing a GitHub pull request by ID and creating a Jira issue with a description and priority.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
> /mcp__github__pr_review 456
```

LANGUAGE: Shell
CODE:
```
> /mcp__jira__create_issue "Bug in login flow" high
```

----------------------------------------

TITLE: Implement SRE Incident Response Agent with Claude Code (TypeScript)
DESCRIPTION: This example demonstrates building an automated SRE incident response agent using the Claude Code SDK. The `investigateIncident` function takes an incident description and severity, then uses a system prompt to guide the agent in diagnosing issues and providing action items. It configures `maxTurns`, `allowedTools` (including custom MCP tools), and `mcpConfig` for advanced agent behavior and tool integration.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: TypeScript
CODE:
```
import { query } from "@anthropic-ai/claude-code";

// Automated incident response agent
async function investigateIncident(
  incidentDescription: string,
  severity = "medium"
) {
  const messages = [];

  for await (const message of query({
    prompt: `Incident: ${incidentDescription} (Severity: ${severity})`,
    options: {
      systemPrompt: "You are an SRE expert. Diagnose the issue, assess impact, and provide immediate action items.",
      maxTurns: 6,
      allowedTools: ["Bash", "Read", "WebSearch", "mcp__datadog"],
      mcpConfig: "monitoring-tools.json"
    }
  })) {
    messages.push(message);
  }

  return messages.find(m => m.type === "result");
}

// Usage
const result = await investigateIncident("Payment API returning 500 errors", "high");
console.log(result.result);
```

----------------------------------------

TITLE: Claude Code Bash Tool-Specific Permission Rules
DESCRIPTION: Examples of defining fine-grained permissions for specific Bash commands, supporting exact matches and prefix matching, while being aware of shell operators.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/iam

LANGUAGE: Configuration
CODE:
```
Bash(npm run build)
```

LANGUAGE: Configuration
CODE:
```
Bash(npm run test:*)
```

LANGUAGE: Configuration
CODE:
```
Bash(safe-cmd:*)
```

----------------------------------------

TITLE: Handle various input formats with Claude SDK
DESCRIPTION: This example illustrates how to send different types of inputs (text, image, multiple mixed inputs) to the Claude SDK and process the streaming responses. It shows basic text queries, image input using a filename, and iterating through multiple prompts for sequential processing.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: python
CODE:
```
import asyncio
from claude_code_sdk import ClaudeSDKClient

async def process_inputs():
    async with ClaudeSDKClient() as client:
        # Text input
        await client.query("Explain this code")
        async for message in client.receive_response():
            # Process streaming response
            pass

        # Image input (Claude will use Read tool automatically)
        await client.query("What's in this diagram? screenshot.png")
        async for message in client.receive_response():
            # Process image analysis
            pass

        # Multiple inputs with mixed content
        inputs = [
            "Analyze the architecture in diagram.png",
            "Compare it with best practices",
            "Generate improved version"
        ]

        for prompt in inputs:
            await client.query(prompt)
            async for message in client.receive_response():
                # Process each response
                pass

asyncio.run(process_inputs())
```

----------------------------------------

TITLE: Create Personal Custom Slash Command for Claude Code
DESCRIPTION: This example shows how to create a personal custom slash command. Personal commands are stored in the user's home directory at `~/.claude/commands/` and are available across all projects. The example creates a '/security-review' command.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/slash-commands

LANGUAGE: Shell
CODE:
```
mkdir -p ~/.claude/commands
echo "Review this code for security vulnerabilities:" > ~/.claude/commands/security-review.md
```

----------------------------------------

TITLE: Manage Multi-turn Conversations with Claude CLI Sessions
DESCRIPTION: This example shows how to use session management with the `claude` CLI to maintain context across multiple turns in a conversation. This feature is essential for complex, multi-step tasks like reviewing legal documents or conducting extended dialogues.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: bash
CODE:
```
# Legal document review with session persistence
session_id=$(claude -p "Start legal review session" --output-format json | jq -r '.session_id')

# Review contract in multiple steps
claude -p --resume "$session_id" "Review contract.pdf for liability clauses"
claude -p --resume "$session_id" "Check compliance with GDPR requirements"
claude -p --resume "$session_id" "Generate executive summary of risks"
```

----------------------------------------

TITLE: Update Claude Code to latest version
DESCRIPTION: Initiates an update process to fetch and install the newest version of Claude Code.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude update
```

----------------------------------------

TITLE: Use Extended Context Model in Claude Code
DESCRIPTION: Shows an example of using a full model name with the `[1m]` suffix to enable a 1 million token context window for Claude Code sessions.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/model-config

LANGUAGE: Shell
CODE:
```
# Example of using a full model name with the [1m] suffix
/model anthropic.claude-sonnet-4-20250514-v1:0[1m]
```

----------------------------------------

TITLE: Chain Subagents for Sequential Tasks (Claude Code)
DESCRIPTION: This example demonstrates how to chain multiple subagents in Claude Code to perform sequential tasks. It shows a command that first invokes a 'code-analyzer' subagent to identify performance issues, and then an 'optimizer' subagent to resolve them, illustrating a multi-step workflow.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sub-agents

LANGUAGE: Bash
CODE:
```
> First use the code-analyzer subagent to find performance issues, then use the optimizer subagent to fix them
```

----------------------------------------

TITLE: Passing Arguments to MCP Slash Commands
DESCRIPTION: Illustrates how to pass arguments to MCP prompts, which can be defined by the server. Examples show both commands without arguments and those accepting one or more arguments, demonstrating flexibility in command invocation.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/slash-commands

LANGUAGE: CLI
CODE:
```
# Without arguments
> /mcp__github__list_prs
```

LANGUAGE: CLI
CODE:
```
# With arguments
> /mcp__github__pr_review 456
> /mcp__jira__create_issue "Bug title" high
```

----------------------------------------

TITLE: Start Claude Code as an MCP Server
DESCRIPTION: Configure Claude Code to act as a stdio MCP server, allowing other applications to connect and utilize its integrated tools like View, Edit, and LS. This enables advanced interactions, such as asking Claude Desktop to read files or make edits, by exposing Claude Code's capabilities to an MCP client.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
# Start Claude as a stdio MCP server
claude mcp serve
```

----------------------------------------

TITLE: Provide Input to Claude Code Query via Direct Prompt or Variable (JavaScript)
DESCRIPTION: This section shows two ways to provide input to the Claude Code `query` function. The first example uses a direct string literal as the `prompt`, which is suitable for static queries. The second example demonstrates using a variable to hold the prompt string, offering flexibility for dynamic input based on user interaction or other program logic.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: JavaScript
CODE:
```
// Direct prompt
for await (const message of query({
  prompt: "Explain this code"
})) {
  if (message.type === "result") console.log(message.result);
}

// From variable
const userInput = "Explain this code";
for await (const message of query({ prompt: userInput })) {
  if (message.type === "result") console.log(message.result);
}
```

----------------------------------------

TITLE: Create SRE Incident Response Bot with Claude CLI
DESCRIPTION: This example illustrates how to build a bash script that leverages the `claude` CLI to act as an SRE expert agent. It automates incident diagnosis, impact assessment, and provides immediate action items by using system prompts and tool configurations.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: bash
CODE:
```
#!/bin/bash

# Automated incident response agent
investigate_incident() {
    local incident_description="$1"
    local severity="${2:-medium}"

    claude -p "Incident: $incident_description (Severity: $severity)" \
      --append-system-prompt "You are an SRE expert. Diagnose the issue, assess impact, and provide immediate action items." \
      --output-format json \
      --allowedTools "Bash,Read,WebSearch,mcp__datadog" \
      --mcp-config monitoring-tools.json
}

# Usage
investigate_incident "Payment API returning 500 errors" "high"
```

----------------------------------------

TITLE: Illustrate Markdown Code Block Tagging
DESCRIPTION: This snippet demonstrates the difference between untagged and properly language-tagged code blocks in Markdown, as generated by Claude Code. Untagged blocks lack syntax highlighting, while tagged blocks (e.g., 'javascript') ensure correct rendering and readability in various tools.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/troubleshooting

LANGUAGE: javascript
CODE:
```
function example() {
  return "hello";
}
```

LANGUAGE: javascript
CODE:
```
function example() {
  return "hello";
}
```

----------------------------------------

TITLE: Configure Git Bash path for Claude Code on Windows
DESCRIPTION: This command sets the `CLAUDE_CODE_GIT_BASH_PATH` environment variable for portable Git installations on Windows. It ensures Claude Code can locate the `bash.exe` executable when running within Git Bash.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/setup

LANGUAGE: Shell
CODE:
```
$env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
```

----------------------------------------

TITLE: Automate Security Reviews with Claude Code SDK (Python)
DESCRIPTION: This Python example demonstrates how to create an automated security audit agent for GitHub pull requests using the Claude Code SDK. It fetches PR diffs, streams security findings, and provides a structured report including cost and severity metadata.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: Python
CODE:
```
import subprocess
import asyncio
import json
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def audit_pr(pr_number: int):
    """Security audit agent for pull requests with streaming feedback"""
    # Get PR diff
    pr_diff = subprocess.check_output(
        ["gh", "pr", "diff", str(pr_number)],
        text=True
    )

    async with ClaudeSDKClient(
        options=ClaudeCodeOptions(
            system_prompt="You are a security engineer. Review this PR for vulnerabilities, insecure patterns, and compliance issues.",
            max_turns=3,
            allowed_tools=["Read", "Grep", "WebSearch"]
        )
    ) as client:
        print(f"🔍 Auditing PR #{pr_number}\n")
        await client.query(pr_diff)

        findings = []
        async for message in client.receive_response():
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'text'):
                        # Stream findings as they're discovered
                        print(block.text, end='', flush=True)
                        findings.append(block.text)

            if type(message).__name__ == "ResultMessage":
                return {
                    'pr_number': pr_number,
                    'findings': ''.join(findings),
                    'metadata': {
                        'cost': message.total_cost_usd,
                        'duration': message.duration_ms,
                        'severity': 'high' if 'vulnerability' in ''.join(findings).lower() else 'medium'
                    }
                }

# Usage
report = await audit_pr(123)
print(f"\n\nAudit complete. Severity: {report['metadata']['severity']}")
print(json.dumps(report, indent=2))
```

----------------------------------------

TITLE: JSON Schema for PreCompact Hook Input in Claude Code
DESCRIPTION: This JSON example shows the input structure for the `PreCompact` hook, which runs before a compact operation. It includes common session details, a `trigger` field (indicating 'manual' or 'auto' invocation), and `custom_instructions` which may be empty for auto-triggered compacts.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: json
CODE:
```
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

----------------------------------------

TITLE: Implement an SRE incident response agent with Claude SDK
DESCRIPTION: This advanced example showcases building an automated SRE incident response agent using the Claude SDK. It configures the client with a system prompt, sets allowed tools (Bash, Read, WebSearch, mcp__datadog), and streams the investigation process, capturing the final analysis and cost.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: python
CODE:
```
import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def investigate_incident(incident_description: str, severity: str = "medium"):
    """Automated incident response agent with real-time streaming"""

    # MCP server configuration for monitoring tools
    mcp_servers = {
        # Example configuration - uncomment and configure as needed:
        # "datadog": {
        #     "command": "npx",
        #     "args": ["-y", "@modelcontextprotocol/server-datadog"],
        #     "env": {"API_KEY": "your-datadog-key", "APP_KEY": "your-app-key"}
        # }
    }

    async with ClaudeSDKClient(
        options=ClaudeCodeOptions(
            system_prompt="You are an SRE expert. Diagnose issues systematically and provide actionable solutions.",
            max_turns=6,
            allowed_tools=["Bash", "Read", "WebSearch", "mcp__datadog"],
            mcp_servers=mcp_servers
        )
    ) as client:
        # Send the incident details
        prompt = f"Incident: {incident_description} (Severity: {severity})"
        print(f"🚨 Investigating: {prompt}\n")
        await client.query(prompt)

        # Stream the investigation process
        investigation_log = []
        async for message in client.receive_response():
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'type'):
                        if block.type == 'tool_use':
                            print(f"[{block.name}] ", end='')
                    if hasattr(block, 'text'):
                        text = block.text
                        print(text, end='', flush=True)
                        investigation_log.append(text)

            # Capture final result
            if type(message).__name__ == "ResultMessage":
                return {
                    'analysis': ''.join(investigation_log),
                    'cost': message.total_cost_usd,
                    'duration_ms': message.duration_ms
                }

# Usage
result = await investigate_incident("Payment API returning 500 errors", "high")
print(f"\n\nInvestigation complete. Cost: ${result['cost']:.4f}")
```

----------------------------------------

TITLE: Handle Errors and Exit Codes from Claude CLI
DESCRIPTION: This example provides a robust bash script for error handling when interacting with the `claude` CLI. It demonstrates how to check the command's exit code and redirect standard error to a log file, ensuring graceful failure and easier debugging.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: bash
CODE:
```
if ! claude -p "$prompt" 2>error.log; then
    echo "Error occurred:" >&2
    cat error.log >&2
    exit 1
fi
```

----------------------------------------

TITLE: Fix nvm Version Conflicts in WSL
DESCRIPTION: Provides solutions for `nvm` version conflicts in WSL. The primary solution ensures `nvm` is properly loaded in non-interactive shells by adding configuration to `.bashrc` or `.zshrc`. An alternative adjusts the PATH order.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/troubleshooting

LANGUAGE: bash
CODE:
```
# Load nvm if it exists
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

LANGUAGE: bash
CODE:
```
source ~/.nvm/nvm.sh
```

LANGUAGE: bash
CODE:
```
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

----------------------------------------

TITLE: Preventing import evaluation within markdown code spans and blocks in CLAUDE.md
DESCRIPTION: This example clarifies that the `@` import syntax is not evaluated when it appears inside markdown code spans or code blocks. This design choice helps avoid potential collisions and ensures that literal code examples are not misinterpreted as import directives.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/memory

LANGUAGE: CLAUDE.md Syntax
CODE:
```
This code span will not be treated as an import: `@anthropic-ai/claude-code`

```

----------------------------------------

TITLE: Example JSON Response Structure from Claude Code
DESCRIPTION: This JSON object illustrates the typical structure of a response received from Claude Code when the `--output-format json` flag is used. It includes various metadata fields such as type, subtype, cost, duration, error status, number of turns, the actual result text, and the session ID.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: json
CODE:
```
{
  "type": "result",
  "subtype": "success",
  "total_cost_usd": 0.003,
  "is_error": false,
  "duration_ms": 1234,
  "duration_api_ms": 800,
  "num_turns": 6,
  "result": "The response text here...",
  "session_id": "abc123"
}
```

----------------------------------------

TITLE: JSON Schema for UserPromptSubmit Hook Input in Claude Code
DESCRIPTION: This JSON example outlines the input structure for the `UserPromptSubmit` hook. It contains common session details and the `prompt` field, which holds the user's submitted prompt string.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: json
CODE:
```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

----------------------------------------

TITLE: Configure Claude Desktop for Claude Code MCP Server
DESCRIPTION: Add this JSON configuration to your `claude_desktop_config.json` file to enable Claude Desktop to connect to and interact with Claude Code running as an MCP server. This setup allows Claude Desktop to leverage Claude Code's tools for various tasks.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: JSON
CODE:
```
{
  "mcpServers": {
    "claude-code": {
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

----------------------------------------

TITLE: Add MCP Servers to Claude Code
DESCRIPTION: These commands demonstrate how to add various Model Context Protocol (MCP) servers to Claude Code using the `claude mcp add` command. Each command specifies the transport protocol (HTTP), the server name, and its corresponding MCP endpoint URL. Adding these servers allows Claude Code to interact with external tools like Sentry, Socket, Hugging Face, and Jam for enhanced capabilities. Users should exercise caution and verify the correctness and security of third-party MCP servers before installation.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: CLI
CODE:
```
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

LANGUAGE: CLI
CODE:
```
claude mcp add --transport http socket https://mcp.socket.dev/
```

LANGUAGE: CLI
CODE:
```
claude mcp add --transport http hugging-face https://huggingface.co/mcp
```

LANGUAGE: CLI
CODE:
```
claude mcp add --transport http jam https://mcp.jam.dev/mcp
```

----------------------------------------

TITLE: JSON Schema for Notification Hook Input in Claude Code
DESCRIPTION: This JSON example demonstrates the input structure for the `Notification` hook. It includes common session details and a `message` field, providing a notification string that can be displayed or logged.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: json
CODE:
```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Task completed successfully"
}
```

----------------------------------------

TITLE: JSON Schema for PostToolUse Hook Input in Claude Code
DESCRIPTION: This JSON example shows the input structure for the `PostToolUse` hook, which executes after a tool has been used. It contains common session details, `tool_name`, `tool_input`, and `tool_response`, with the latter two schemas depending on the specific tool and its output.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: json
CODE:
```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  }
}
```

----------------------------------------

TITLE: JSON Schema for PreToolUse Hook Input in Claude Code
DESCRIPTION: This JSON example illustrates the input structure for the `PreToolUse` hook, which runs before a tool is used. It includes common session details and specific fields like `tool_name` and `tool_input`, where the `tool_input` schema varies by the particular tool being invoked.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: json
CODE:
```
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

----------------------------------------

TITLE: Connect External Terminal to IDE for Claude Code
DESCRIPTION: Execute this command from any external terminal to establish a connection between Claude Code and your active IDE, thereby activating all integrated features. It is recommended to start Claude Code from the same directory as your IDE project root to ensure proper file access.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/ide-integrations

LANGUAGE: cli
CODE:
```
/ide
```

----------------------------------------

TITLE: Add MCP Server from JSON Configuration String
DESCRIPTION: Add an MCP server directly from a JSON configuration string using the `claude mcp add-json` command. This method allows for precise control over server settings, including type, command, arguments, and environment variables. After adding, verify the server's configuration with `claude mcp get`.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
# Basic syntax
claude mcp add-json <name> '<json>'

# Example: Adding a stdio server with JSON configuration
claude mcp add-json weather-api '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'

# Verify the server was added
claude mcp get weather-api
```

----------------------------------------

TITLE: Send Structured Messages and Image Inputs with Claude Code SDK
DESCRIPTION: This snippet demonstrates how to send various types of messages to Claude using the `claude_code_sdk`. It covers sending simple text queries, referencing image files (which Claude's Read tool processes), and sending a sequence of multiple text messages to guide a multi-step interaction. It highlights the SDK's ability to handle image inputs automatically.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: python
CODE:
```
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async with ClaudeSDKClient() as client:
    # Text message
    await client.query("Analyze this code for security issues")

    # Message with image reference (image will be read by Claude's Read tool)
    await client.query("Explain what's shown in screenshot.png")

    # Multiple messages in sequence
    messages = [
        "First, analyze the architecture diagram in diagram.png",
        "Now suggest improvements based on the diagram",
        "Finally, generate implementation code"
    ]

    for msg in messages:
        await client.query(msg)
        async for response in client.receive_response():
            # Process each response
            pass

# The SDK handles image files through Claude's built-in Read tool
# Supported formats: PNG, JPG, PDF, and other common formats
```

----------------------------------------

TITLE: Quickly adding a memory using the '#' shortcut in Claude Code
DESCRIPTION: This snippet demonstrates the fastest way to add a new memory to Claude Code. By starting an input with the '#' character, users are prompted to select which memory file to store the new instruction in, streamlining the process of adding preferences or guidelines.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/memory

LANGUAGE: Claude Code CLI
CODE:
```
# Always use descriptive variable names

```

----------------------------------------

TITLE: Explicitly Invoke Specific Subagents
DESCRIPTION: This snippet provides examples of how to explicitly invoke a specific subagent by mentioning its name within a command or request. This allows for direct control over which subagent handles a particular task.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sub-agents

LANGUAGE: Claude Code Command
CODE:
```
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my recent changes
> Ask the debugger subagent to investigate this error
```

----------------------------------------

TITLE: Define Claude Code Subagent Configuration File
DESCRIPTION: This Markdown file format, including YAML frontmatter, is used to define a Claude Code subagent. It specifies the subagent's name, a description of its purpose, optional tools it can access, and its core system prompt, which guides its behavior and capabilities.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sub-agents

LANGUAGE: Markdown
CODE:
```
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all tools if omitted
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow.
```

----------------------------------------

TITLE: Add Remote HTTP MCP Server with Claude CLI
DESCRIPTION: Shows how to add a remote HTTP server using `claude mcp add --transport http`. HTTP servers use standard request/response patterns, common for REST APIs and web services. Examples include basic syntax, connecting to Notion, and adding a Bearer token for authentication.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
# Basic syntax
claude mcp add --transport http <name> <url>

# Real example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Example with Bearer token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

----------------------------------------

TITLE: Define Custom Slash Command Syntax for Claude Code
DESCRIPTION: This snippet illustrates the basic syntax for defining custom slash commands in Claude Code. Commands start with a forward slash, followed by the command name, and can optionally include arguments.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/slash-commands

LANGUAGE: Shell
CODE:
```
/<command-name> [arguments]
```

----------------------------------------

TITLE: Migrating Claude Code GitHub Action Configuration from Beta to v1.0
DESCRIPTION: This snippet illustrates the breaking changes and updated configuration for the `anthropics/claude-code-action` from its beta version to the GA (v1.0) release. It highlights how parameters like `mode`, `direct_prompt`, `custom_instructions`, `max_turns`, and `model` have been consolidated into a unified `prompt` and `claude_args` structure in the v1.0 configuration.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/github-actions

LANGUAGE: YAML
CODE:
```
- uses: anthropics/claude-code-action@beta
  with:
    mode: "tag"
    direct_prompt: "Review this PR for security issues"
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    custom_instructions: "Follow our coding standards"
    max_turns: "10"
    model: "claude-3-5-sonnet-20241022"
```

LANGUAGE: YAML
CODE:
```
- uses: anthropics/claude-code-action@v1
  with:
    prompt: "Review this PR for security issues"
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    claude_args: |
      --system-prompt "Follow our coding standards"
      --max-turns 10
      --model claude-sonnet-4-20250514
```

----------------------------------------

TITLE: Add ClickUp Integration to Claude MCP
DESCRIPTION: Enable task management and project tracking capabilities through ClickUp.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add clickup --env CLICKUP_API_KEY=YOUR_KEY --env CLICKUP_TEAM_ID=YOUR_ID -- npx -y @hauptsache.net/clickup-mcp
```

----------------------------------------

TITLE: Get Text Output from Claude Code in Headless Mode
DESCRIPTION: This snippet shows how to obtain a simple text response from Claude Code when operating in headless mode. By default, the `-p` or `--print` flag will output the result as plain text directly to the console.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: bash
CODE:
```
claude -p "Explain file src/components/Header.tsx"
# Output: This is a React component showing...
```

----------------------------------------

TITLE: Manage Multi-Turn Conversations with Claude Code SDK
DESCRIPTION: This example illustrates two methods for maintaining conversation context with the `claude_code_sdk`. Method 1 uses `ClaudeSDKClient` for persistent sessions, allowing subsequent queries to build upon previous interactions. Method 2 shows how to use the `query` function with `continue_conversation` or `resume` options to manage session continuity or resume specific past conversations.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: python
CODE:
```
import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, query

# Method 1: Using ClaudeSDKClient for persistent conversations
async def multi_turn_conversation():
    async with ClaudeSDKClient() as client:
        # First query
        await client.query("Let's refactor the payment module")
        async for msg in client.receive_response():
            # Process first response
            pass

        # Continue in same session
        await client.query("Now add comprehensive error handling")
        async for msg in client.receive_response():
            # Process continuation
            pass

        # The conversation context is maintained throughout

# Method 2: Using query function with session management
async def resume_session():
    # Continue most recent conversation
    async for message in query(
        prompt="Now refactor this for better performance",
        options=ClaudeCodeOptions(continue_conversation=True)
    ):
        if type(message).__name__ == "ResultMessage":
            print(message.result)

    # Resume specific session
    async for message in query(
        prompt="Update the tests",
        options=ClaudeCodeOptions(
            resume="550e8400-e29b-41d4-a716-446655440000",
            max_turns=3
        )
    ):
        if type(message).__name__ == "ResultMessage":
            print(message.result)

# Run the examples
asyncio.run(multi_turn_conversation())
```

----------------------------------------

TITLE: Configure Claude Code basic proxy settings via environment variables
DESCRIPTION: Set `HTTPS_PROXY`, `HTTP_PROXY`, and `NO_PROXY` environment variables to route Claude Code traffic through a corporate proxy. Examples include bypassing the proxy for specific hosts using space-separated, comma-separated, or wildcard formats.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/corporate-proxy

LANGUAGE: Shell
CODE:
```
# HTTPS proxy (recommended)
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP proxy (if HTTPS not available)
export HTTP_PROXY=http://proxy.example.com:8080

# Bypass proxy for specific requests - space-separated format
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# Bypass proxy for specific requests - comma-separated format
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# Bypass proxy for all requests
export NO_PROXY="*"
```

----------------------------------------

TITLE: Centralized OpenTelemetry Configuration for Claude Code using Managed Settings File
DESCRIPTION: This example shows how administrators can configure OpenTelemetry settings for all users within an organization by using a managed settings JSON file. This method provides centralized control and ensures that specified environment variables have high precedence, preventing user overrides.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: json
CODE:
```
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.company.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer company-token"
  }
}
```

----------------------------------------

TITLE: Add Project-Scoped MCP Server and Configure via JSON
DESCRIPTION: Learn how to add a server that is specific to a single project using the `claude mcp add` command. This server's configuration is stored in a `.mcp.json` file, which follows a standardized format. Claude Code prompts for approval before using these servers, and approval choices can be reset with `claude mcp reset-project-choices`.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add shared-server --scope project /path/to/server
```

LANGUAGE: JSON
CODE:
```
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

----------------------------------------

TITLE: Configure Dynamic OpenTelemetry Headers Helper
DESCRIPTION: Illustrates how to configure the `otelHeadersHelper` in the `.claude/settings.json` file to specify a script that generates dynamic OpenTelemetry headers for authentication. This script is executed at startup to fetch headers.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: json
CODE:
```
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

----------------------------------------

TITLE: JSON Schema for SessionEnd Hook Input in Claude Code
DESCRIPTION: This JSON example outlines the input structure for the `SessionEnd` hook. It includes common session details, the current working directory, and a `reason` field, specifying why the session ended (e.g., 'clear', 'logout', 'prompt_input_exit', or 'other').

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: json
CODE:
```
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionEnd",
  "reason": "exit"
}
```

----------------------------------------

TITLE: Add Remote SSE MCP Server with Claude CLI
DESCRIPTION: Illustrates how to add a remote SSE (Server-Sent Events) server using `claude mcp add --transport sse`. SSE servers provide real-time streaming connections and are often used by cloud services for live updates. The examples include basic syntax, connecting to Linear, and adding an authentication header.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
# Basic syntax
claude mcp add --transport sse <name> <url>

# Real example: Connect to Linear
claude mcp add --transport sse linear https://mcp.linear.app/sse

# Example with authentication header
claude mcp add --transport sse private-api https://api.company.com/mcp \
  --header "X-API-Key: your-key-here"
```

----------------------------------------

TITLE: Switch WSL2 Networking Mode to Mirrored
DESCRIPTION: As an alternative to firewall configuration for WSL2 IDE detection issues, you can switch WSL2's networking mode to 'mirrored'. This is done by adding a specific configuration to your `.wslconfig` file in your Windows user directory. After modifying the file, you must restart WSL for the changes to take effect.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/troubleshooting

LANGUAGE: WSL Configuration
CODE:
```
[wsl2]
networkingMode=mirrored
```

----------------------------------------

TITLE: JSON Schema for Stop and SubagentStop Hook Input in Claude Code
DESCRIPTION: This JSON example illustrates the input structure for both `Stop` and `SubagentStop` hooks. It includes common session details and a `stop_hook_active` boolean, which indicates if a stop hook is already actively preventing Claude Code from running indefinitely.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: json
CODE:
```
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

----------------------------------------

TITLE: Initialize Project Memory with /init Command
DESCRIPTION: This command is used to bootstrap a CLAUDE.md file for a codebase. The CLAUDE.md file serves as a project-specific memory, storing important project information, conventions, and frequently used commands, helping Claude Code understand the project context.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/memory

LANGUAGE: Shell
CODE:
```
/init
```

----------------------------------------

TITLE: Utilize Claude's Plan Mode for Safe Code Analysis
DESCRIPTION: This section details Claude's Plan Mode, a read-only operation mode for safe codebase exploration, complex change planning, and interactive development. It explains how to activate Plan Mode during a session, start new sessions, run headless queries, and configure it as the default.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: CLI
CODE:
```
claude --permission-mode plan
```

LANGUAGE: CLI
CODE:
```
claude --permission-mode plan -p "Analyze the authentication system and suggest improvements"
```

LANGUAGE: CLI
CODE:
```
> I need to refactor our authentication system to use OAuth2. Create a detailed migration plan.
```

LANGUAGE: JSON
CODE:
```
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

----------------------------------------

TITLE: Define Claude Code Hooks for Global Events
DESCRIPTION: This example demonstrates how to configure hooks for events that do not require a specific tool matcher, such as "UserPromptSubmit". For these events, the "matcher" field can be omitted, allowing the hook to execute whenever the specified event occurs, enabling actions like prompt validation.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: json
CODE:
```
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/prompt-validator.py"
          }
        ]
      }
    ]
  }
}
```

----------------------------------------

TITLE: Configure Local MCP Servers with npx on Windows
DESCRIPTION: Explains the specific requirement for Windows users (not WSL) when configuring local MCP servers that utilize `npx`. It demonstrates how to wrap the `npx` command with `cmd /c` to ensure proper execution and prevent 'Connection closed' errors, which occur because Windows cannot directly execute `npx`.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
# This creates command="cmd" which Windows can execute
claude mcp add my-server -- cmd /c npx -y @some/package
```

----------------------------------------

TITLE: Create a Git-Aware Bash Status Line Script for Claude Code
DESCRIPTION: This Bash script extends the simple example by adding logic to detect if the current directory is a Git repository and, if so, display the current Git branch. It uses `git rev-parse` and `git branch` commands to retrieve Git information.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/statusline

LANGUAGE: Bash
CODE:
```
#!/bin/bash
# Read JSON input from stdin
input=$(cat)

# Extract values using jq
MODEL_DISPLAY=$(echo "$input" | jq -r '.model.display_name')
CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir')

# Show git branch if in a git repo
GIT_BRANCH=""
if git rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git branch --show-current 2>/dev/null)
    if [ -n "$BRANCH" ]; then
        GIT_BRANCH=" | 🌿 $BRANCH"
    fi
fi

echo "[$MODEL_DISPLAY] 📁 ${CURRENT_DIR##*/}$GIT_BRANCH"
```

----------------------------------------

TITLE: Configure Windows Firewall for WSL2 JetBrains IDE Detection
DESCRIPTION: When using Claude Code on WSL2 with JetBrains IDEs, 'No available IDEs detected' errors can occur due to WSL2's default NAT networking. This solution involves finding your WSL2 IP address and then creating a Windows Firewall rule to allow inbound TCP traffic from the WSL2 subnet, enabling proper IDE detection.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/troubleshooting

LANGUAGE: PowerShell
CODE:
```
wsl hostname -I
```

LANGUAGE: PowerShell
CODE:
```
New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
```

----------------------------------------

TITLE: Configure MCP Servers with Environment Variable Expansion in JSON
DESCRIPTION: Enable flexible and shareable MCP server configurations by utilizing environment variable expansion within `.mcp.json` files. This allows for machine-specific paths and sensitive values like API keys to be dynamically resolved at runtime. Supported syntax includes `${VAR}` and `${VAR:-default}`.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: JSON
CODE:
```
{
  "mcpServers": {
    "api-server": {
      "type": "sse",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

----------------------------------------

TITLE: Configure Claude Code for Terminal Bell Notifications
DESCRIPTION: This command sets Claude Code to use terminal bell notifications globally, providing sound alerts upon task completion. For macOS users, ensure notification permissions are enabled in System Settings for your terminal application.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/terminal-config

LANGUAGE: Shell
CODE:
```
claude config set --global preferredNotifChannel terminal_bell
```

----------------------------------------

TITLE: Utilize ClaudeSDKClient for streaming and multi-turn conversations in Python
DESCRIPTION: This snippet illustrates the recommended approach for interacting with the Claude Code SDK, leveraging the `ClaudeSDKClient` for streaming responses and managing multi-turn conversations. It demonstrates setting up an agent with a specific system prompt and allowed tools, then sending a query and processing the streamed output.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: Python
CODE:
```
import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def main():
    async with ClaudeSDKClient(
        options=ClaudeCodeOptions(
            system_prompt="You are a performance engineer",
            allowed_tools=["Bash", "Read", "WebSearch"],
            max_turns=5
        )
    ) as client:
        await client.query("Analyze system performance")

        # Stream responses
        async for message in client.receive_response():
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'text'):
                        print(block.text, end='', flush=True)

# Run as script
asyncio.run(main())

# Or in IPython/Jupyter: await main()
```

----------------------------------------

TITLE: Customize Claude Code Bedrock Model and Caching Settings
DESCRIPTION: This section provides examples for customizing the primary and small/fast Claude models used with Bedrock, either by their inference profile ID or application inference profile ARN. It also shows how to optionally disable prompt caching, which might be necessary in certain regions or scenarios.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock

LANGUAGE: bash
CODE:
```
# Using inference profile ID
export ANTHROPIC_MODEL='us.anthropic.claude-opus-4-1-20250805-v1:0'
export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-3-5-haiku-20241022-v1:0'

# Using application inference profile ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1
```

----------------------------------------

TITLE: Configure Claude Code for Amazon Bedrock with LLM Gateway
DESCRIPTION: This setup allows Claude Code to access Amazon Bedrock models via an LLM gateway service. The gateway handles the actual Bedrock endpoint and can optionally manage AWS authentication, allowing Claude Code to skip direct AWS authentication by setting CLAUDE_CODE_SKIP_BEDROCK_AUTH.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/bedrock-vertex-proxies

LANGUAGE: Shell
CODE:
```
export CLAUDE_CODE_USE_BEDROCK=1

export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # If gateway handles AWS auth
```

----------------------------------------

TITLE: Configure Claude Code for Google Vertex AI with LLM Gateway
DESCRIPTION: This setup allows Claude Code to access Google Vertex AI models via an LLM gateway service. The gateway handles the actual Vertex AI endpoint and can optionally manage GCP authentication, allowing Claude Code to skip direct GCP authentication by setting CLAUDE_CODE_SKIP_VERTEX_AUTH.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/bedrock-vertex-proxies

LANGUAGE: Shell
CODE:
```
export CLAUDE_CODE_USE_VERTEX=1

export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # If gateway handles GCP auth
```

----------------------------------------

TITLE: Add Monday.com Integration to Claude MCP
DESCRIPTION: Manage monday.com boards by creating items, updating columns, assigning owners, setting timelines, adding CRM activities, and writing summaries.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport sse monday https://mcp.monday.com/sse
```

----------------------------------------

TITLE: Implement Python Best Practices with Claude Code SDK
DESCRIPTION: This section showcases essential Python best practices when integrating with the Claude Code SDK. It covers using context managers for resource handling, running multiple agents concurrently, implementing robust error handling for common SDK exceptions, and collecting full responses with associated metadata.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: Python
CODE:
```
import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

# Always use context managers
async with ClaudeSDKClient() as client:
    await client.query("Analyze this code")
    async for msg in client.receive_response():
        # Process streaming messages
        pass

# Run multiple agents concurrently
async with ClaudeSDKClient() as reviewer, ClaudeSDKClient() as tester:
    await asyncio.gather(
        reviewer.query("Review main.py"),
        tester.query("Write tests for main.py")
    )

# Error handling
from claude_code_sdk import CLINotFoundError, ProcessError

try:
    async with ClaudeSDKClient() as client:
        # Your code here
        pass
except CLINotFoundError:
    print("Install CLI: npm install -g @anthropic-ai/claude-code")
except ProcessError as e:
    print(f"Process error: {e}")

# Collect full response with metadata
async def get_response(client, prompt):
    await client.query(prompt)
    text = []
    async for msg in client.receive_response():
        if hasattr(msg, 'content'):
            for block in msg.content:
                if hasattr(block, 'text'):
                    text.append(block.text)
        if type(msg).__name__ == "ResultMessage":
            return {'text': ''.join(text), 'cost': msg.total_cost_usd}
```

----------------------------------------

TITLE: Configure Claude Code SDK Options in Python
DESCRIPTION: This snippet demonstrates how to initialize and configure the `ClaudeCodeOptions` class from the `claude_code_sdk`. It covers various parameters for core configuration, tool management, session handling, environment settings, permissions, MCP integration, and advanced arguments, allowing fine-grained control over the Claude Code agent's behavior.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: Python
CODE:
```
from claude_code_sdk import ClaudeCodeOptions

options = ClaudeCodeOptions(
    # Core configuration
    system_prompt="You are a helpful assistant",
    append_system_prompt="Additional system instructions",
    max_turns=5,
    model="claude-3-5-sonnet-20241022",
    max_thinking_tokens=8000,
    
    # Tool management
    allowed_tools=["Bash", "Read", "Write"],
    disallowed_tools=["WebSearch"],
    
    # Session management
    continue_conversation=False,
    resume="session-uuid",
    
    # Environment
    cwd="/path/to/working/directory",
    add_dirs=["/additional/context/dir"],
    settings="/path/to/settings.json",
    
    # Permissions
    permission_mode="acceptEdits",  # "default", "acceptEdits", "plan", "bypassPermissions"
    permission_prompt_tool_name="mcp__approval_tool",
    
    # MCP integration
    mcp_servers={
        "my_server": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-example"],
            "env": {"API_KEY": "your-key"}
        }
    },
    
    # Advanced
    extra_args={
        "--verbose": None,
        "--custom-flag": "value"
    }
)
```

----------------------------------------

TITLE: Process Text Input with Claude CLI
DESCRIPTION: This snippet demonstrates the default method for providing text prompts to the `claude` CLI. You can pass the prompt directly as an argument or pipe it via standard input, making it flexible for various scripting scenarios.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: bash
CODE:
```
# Direct argument
claude -p "Explain this code"

# From stdin
echo "Explain this code" | claude -p
```

----------------------------------------

TITLE: Define Custom System Prompts for Specialized Claude Agents
DESCRIPTION: This snippet demonstrates how to customize the behavior and role of Claude agents using system prompts. It shows how to initialize `ClaudeSDKClient` with a `system_prompt` to define an agent's expertise (e.g., SRE expert) or `append_system_prompt` to add specific instructions (e.g., always include error handling). It also illustrates streaming responses.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: python
CODE:
```
import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def specialized_agents():
    # SRE incident response agent with streaming
    async with ClaudeSDKClient(
        options=ClaudeCodeOptions(
            system_prompt="You are an SRE expert. Diagnose issues systematically and provide actionable solutions.",
            max_turns=3
        )
    ) as sre_agent:
        await sre_agent.query("API is down, investigate")

        # Stream the diagnostic process
        async for message in sre_agent.receive_response():
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'text'):
                        print(block.text, end='', flush=True)

    # Legal review agent with custom prompt
    async with ClaudeSDKClient(
        options=ClaudeCodeOptions(
            append_system_prompt="Always include comprehensive error handling and unit tests.",
            max_turns=2
        )
    ) as dev_agent:
        await dev_agent.query("Refactor this function")

        # Collect full response
        full_response = []
        async for message in dev_agent.receive_response():
            if type(message).__name__ == "ResultMessage":
                print(message.result)

asyncio.run(specialized_agents())
```

----------------------------------------

TITLE: Configure Project-Scoped MCP Servers with Claude CLI
DESCRIPTION: Explains how to configure MCP servers with a 'project' scope. These servers store configurations in a `.mcp.json` file at the project's root directory, designed to be checked into version control for team collaboration. Claude Code automatically creates or updates this file when a project-scoped server is added.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --scope project my-shared-server /path/to/server
```

----------------------------------------

TITLE: Configure Claude Code Model Context Protocol (MCP) servers
DESCRIPTION: Accesses the configuration interface for setting up Model Context Protocol (MCP) servers.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude mcp
```

----------------------------------------

TITLE: Add Notion Integration to Claude MCP
DESCRIPTION: Read documents, update pages, and manage tasks within Notion.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

----------------------------------------

TITLE: Create and Refine Pull Requests with Claude
DESCRIPTION: This section outlines how to use Claude to summarize code changes, generate a pull request, and then review and refine its description, including adding testing details.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: CLI
CODE:
```
> summarize the changes I've made to the authentication module
```

LANGUAGE: CLI
CODE:
```
> create a pr
```

LANGUAGE: CLI
CODE:
```
> enhance the PR description with more context about the security improvements
```

LANGUAGE: CLI
CODE:
```
> add information about how these changes were tested
```

----------------------------------------

TITLE: Create Personal Custom Slash Commands for Claude
DESCRIPTION: Explains how to set up personal slash commands that are available across all projects for a single user. This involves creating a `~/.claude/commands` directory in the home folder and adding Markdown files for custom prompts, ensuring consistent workflows across different codebases.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: Shell
CODE:
```
mkdir -p ~/.claude/commands
```

LANGUAGE: Shell
CODE:
```
echo "Review this code for security vulnerabilities, focusing on:" >\n~/.claude/commands/security-review.md
```

LANGUAGE: Shell
CODE:
```
> /security-review
```

----------------------------------------

TITLE: Add Plaid Integration to Claude MCP
DESCRIPTION: Analyze, troubleshoot, and optimize Plaid integrations for banking data and financial account linking.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport sse plaid https://api.dashboard.plaid.com/mcp/sse
```

----------------------------------------

TITLE: Generate and Manage Tests with Claude
DESCRIPTION: This section provides commands for using Claude to identify untested code, generate test scaffolding, add meaningful test cases, and run/verify tests. It offers tips for effective test generation.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: CLI
CODE:
```
> find functions in NotificationsService.swift that are not covered by tests
```

LANGUAGE: CLI
CODE:
```
> add tests for the notification service
```

LANGUAGE: CLI
CODE:
```
> add test cases for edge conditions in the notification service
```

LANGUAGE: CLI
CODE:
```
> run the new tests and fix any failures
```

----------------------------------------

TITLE: Import Servers from Claude Desktop
DESCRIPTION: Learn how to import server configurations from Claude Desktop into Claude Code, including the interactive selection process and verification steps. This feature is supported on macOS and WSL, reading the Claude Desktop configuration from its standard location. Imported servers retain their original names, with numerical suffixes added for duplicates.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add-from-claude-desktop
```

LANGUAGE: Shell
CODE:
```
claude mcp list
```

----------------------------------------

TITLE: Importing user-specific instructions from home directory in CLAUDE.md
DESCRIPTION: This snippet illustrates how to import files from a user's home directory into a `CLAUDE.md` file. This is a convenient way for team members to include individual instructions that are not committed to the repository, replacing the deprecated `CLAUDE.local.md`.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/memory

LANGUAGE: CLAUDE.md Syntax
CODE:
```
# Individual Preferences
- @~/.claude/my-project-instructions.md

```

----------------------------------------

TITLE: Manually Update Claude Code
DESCRIPTION: Command to trigger a manual update for Claude Code, ensuring you have the latest features and security fixes.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/setup

LANGUAGE: Shell
CODE:
```
claude update
```

----------------------------------------

TITLE: Build Multi-Turn Legal Assistant with Claude Code SDK (Python)
DESCRIPTION: This Python snippet illustrates building a multi-turn legal document review assistant using the Claude Code SDK. It maintains a persistent session across multiple steps, streams analysis results, and calculates the total cost of the review process.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: Python
CODE:
```
import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def legal_review():
    """Legal document review with persistent session and streaming"""

    async with ClaudeSDKClient(
        options=ClaudeCodeOptions(
            system_prompt="You are a corporate lawyer. Provide detailed legal analysis.",
            max_turns=2
        )
    ) as client:
        # Multi-step review in same session
        steps = [
            "Review contract.pdf for liability clauses",
            "Check compliance with GDPR requirements",
            "Generate executive summary of risks"
        ]

        review_results = []

        for step in steps:
            print(f"\n📋 {step}\n")
            await client.query(step)

            step_result = []
            async for message in client.receive_response():
                if hasattr(message, 'content'):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            text = block.text
                            print(text, end='', flush=True)
                            step_result.append(text)

                if type(message).__name__ == "ResultMessage":
                    review_results.append({
                        'step': step,
                        'analysis': ''.join(step_result),
                        'cost': message.total_cost_usd
                    })

        # Summary
        total_cost = sum(r['cost'] for r in review_results)
        print(f"\n\n✅ Legal review complete. Total cost: ${total_cost:.4f}")
        return review_results

# Usage
results = await legal_review()
```

----------------------------------------

TITLE: Execute MCP Slash Command Without Arguments
DESCRIPTION: Demonstrates the basic syntax for executing an MCP prompt that does not require any additional parameters. Users can type `/` to discover available commands, which follow the `/mcp__servername__promptname` format.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
> /mcp__github__list_prs
```

----------------------------------------

TITLE: Add Atlassian Integration to Claude MCP
DESCRIPTION: Manage your Jira tickets and Confluence docs.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse
```

----------------------------------------

TITLE: Open Claude Code Subagents Interface
DESCRIPTION: Run this command within the Claude Code environment to access the subagents interface, which allows you to manage, create, and configure new AI subagents.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sub-agents

LANGUAGE: CLI
CODE:
```
/agents
```

----------------------------------------

TITLE: Add Canva Integration to Claude MCP
DESCRIPTION: Browse, summarize, autofill, and even generate new Canva designs directly from Claude.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http canva https://mcp.canva.com/mcp
```

----------------------------------------

TITLE: Add Asana Integration to Claude MCP
DESCRIPTION: Interact with your Asana workspace to keep projects on track.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

----------------------------------------

TITLE: Add Vercel Integration to Claude MCP
DESCRIPTION: Integrate with Vercel's official MCP server to search and navigate documentation, manage projects and deployments, and analyze deployment logs.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http vercel https://mcp.vercel.com/
```

----------------------------------------

TITLE: Add InVideo Integration to Claude MCP
DESCRIPTION: Build video creation capabilities into your applications using InVideo.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport sse invideo https://mcp.invideo.io/sse
```

----------------------------------------

TITLE: Configure Claude Code Model via CLI
DESCRIPTION: Demonstrates how to set the Claude Code model using command-line arguments at startup (`claude --model`) or by switching models mid-session (`/model`).

SOURCE: https://docs.anthropic.com/en/docs/claude-code/model-config

LANGUAGE: Shell
CODE:
```
# Start with Opus
claude --model opus

# Switch to Sonnet during session
/model sonnet
```

----------------------------------------

TITLE: Manage Subagents with the /agents Command
DESCRIPTION: This snippet demonstrates the use of the `/agents` command, which provides an interactive interface for comprehensive subagent management. Users can view, create, edit, delete, and manage tool permissions for subagents.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sub-agents

LANGUAGE: Claude Code Command
CODE:
```
/agents
```

----------------------------------------

TITLE: Add Stytch Integration to Claude MCP
DESCRIPTION: Configure and manage Stytch authentication services, redirect URLs, email templates, and workspace settings.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http stytch http://mcp.stytch.dev/mcp
```

----------------------------------------

TITLE: Manage Configured MCP Servers with Claude CLI
DESCRIPTION: Provides essential commands for managing already configured MCP servers. This includes listing all configured servers, retrieving detailed information for a specific server, removing a server, and checking the server status directly within Claude Code.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Remove a server
claude mcp remove github

# (within Claude Code) Check server status
/mcp
```

----------------------------------------

TITLE: Integrate Claude as a Unix-Style Utility for Code Verification
DESCRIPTION: This section demonstrates how to integrate Claude Code into your development workflow as a linter or code reviewer, specifically by adding it to your `package.json` scripts. This allows for automated code verification within your build process or CI/CD pipeline.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: JSON
CODE:
```
// package.json
{
    ...
    "scripts": {
        ...
        "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"
    }
}
```

----------------------------------------

TITLE: Enable Debug Logging for Claude Code
DESCRIPTION: To enable detailed logging for requests when debugging Claude Code deployments, set the `ANTHROPIC_LOG` environment variable to `debug`. This provides more verbose output for troubleshooting.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/bedrock-vertex-proxies

LANGUAGE: Shell
CODE:
```
export ANTHROPIC_LOG=debug
```

----------------------------------------

TITLE: Request JSON Output from Claude Code
DESCRIPTION: This command demonstrates how to instruct Claude Code to return its response in a structured JSON format. Using the `--output-format json` flag ensures that the output includes metadata alongside the primary result, making it suitable for programmatic parsing.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: bash
CODE:
```
claude -p "How does the data layer work?" --output-format json
```

----------------------------------------

TITLE: Reference MCP Resources in Claude Prompts
DESCRIPTION: Learn how to reference external MCP resources directly within your Claude prompts using a specific `@server:protocol://resource/path` format. This allows Claude to automatically fetch and include these resources as attachments, enabling analysis of diverse content like GitHub issues, API documentation, or database schemas.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
> Can you analyze @github:issue://123 and suggest a fix?
```

LANGUAGE: Shell
CODE:
```
> Please review the API documentation at @docs:file://api/authentication
```

LANGUAGE: Shell
CODE:
```
> Compare @postgres:schema://users with @docs:file://database/user-model
```

----------------------------------------

TITLE: Add Linear Integration to Claude MCP
DESCRIPTION: Integrate with Linear's issue tracking and project management system.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport sse linear https://mcp.linear.app/sse
```

----------------------------------------

TITLE: Add Square Integration to Claude MCP
DESCRIPTION: Use an agent to build on Square APIs for payments, inventory, orders, and more.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport sse square https://mcp.squareup.com/sse
```

----------------------------------------

TITLE: Direct Await Usage in Jupyter Cells with ClaudeSDKClient
DESCRIPTION: Demonstrates how to directly use `await` with the `ClaudeSDKClient` within Jupyter notebook cells for connecting, querying, receiving responses, and disconnecting. This pattern is suitable for interactive data analysis and immediate feedback.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: Python
CODE:
```
client = ClaudeSDKClient()
await client.connect()
await client.query("Analyze data.csv")
async for msg in client.receive_response():
    print(msg)
await client.disconnect()
```

----------------------------------------

TITLE: Implement Multi-turn Legal Assistant with Claude Code SDK
DESCRIPTION: This code snippet demonstrates how to build a multi-turn legal assistant using the Anthropic Claude Code SDK. It shows how to initiate a session, then conduct a series of steps (e.g., reviewing a contract, checking GDPR compliance) by resuming the same session, ensuring continuity in the conversation.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: TypeScript
CODE:
```
import { query } from "@anthropic-ai/claude-code";

async function legalReview() {
  // Start legal review session
  let sessionId: string;

  for await (const message of query({
    prompt: "Start legal review session",
    options: { maxTurns: 1 }
  })) {
    if (message.type === "system" && message.subtype === "init") {
      sessionId = message.session_id;
    }
  }

  // Multi-step review using same session
  const steps = [
    "Review contract.pdf for liability clauses",
    "Check compliance with GDPR requirements",
    "Generate executive summary of risks"
  ];

  for (const step of steps) {
    for await (const message of query({
      prompt: step,
      options: { resume: sessionId, maxTurns: 2 }
    })) {
      if (message.type === "result") {
        console.log(`Step: ${step}`);
        console.log(message.result);
      }
    }
  }
}
```

----------------------------------------

TITLE: Automate Claude AI Responses in GitHub with AWS Bedrock
DESCRIPTION: This GitHub Actions workflow enables Claude AI to respond to comments on issues and pull requests using AWS Bedrock. It requires configuring AWS Bedrock access, setting up GitHub as an OIDC provider in AWS, and defining specific GitHub secrets for AWS authentication and GitHub App credentials. The workflow checks out the repository, generates a GitHub App token, configures AWS credentials via OIDC, and then uses the `claude-code-action` to interact with Claude via Bedrock.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/github-actions

LANGUAGE: yaml
CODE:
```
name: Claude PR Action

permissions:
  contents: write
  pull-requests: write
  issues: write
  id-token: write

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]

jobs:
  claude-pr:
    if: |
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
    runs-on: ubuntu-latest
    env:
      AWS_REGION: us-west-2
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Configure AWS Credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
          aws-region: us-west-2

      - uses: anthropics/claude-code-action@v1
        with:
          github_token: ${{ steps.app-token.outputs.token }}
          use_bedrock: "true"
          claude_args: '--model us.anthropic.claude-sonnet-4-20250514-v1:0 --max-turns 10'
```

----------------------------------------

TITLE: Add Netlify Integration to Claude MCP
DESCRIPTION: Create, deploy, and manage websites on Netlify. Control all aspects of your site from creating secrets to enforcing access controls to aggregating form submissions.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http netlify https://netlify-mcp.netlify.app/mcp
```

----------------------------------------

TITLE: Manage Claude Code Configuration via CLI
DESCRIPTION: These commands allow users to interact with and manage Claude Code's configuration settings directly from the command line. Users can list all settings, retrieve specific values, set new values, or add/remove items from list-type settings. The `--global` flag can be used to modify global configurations instead of project-specific ones.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: Bash
CODE:
```
claude config list
```

LANGUAGE: Bash
CODE:
```
claude config get <key>
```

LANGUAGE: Bash
CODE:
```
claude config set <key> <value>
```

LANGUAGE: Bash
CODE:
```
claude config add <key> <value>
```

LANGUAGE: Bash
CODE:
```
claude config remove <key> <value>
```

----------------------------------------

TITLE: Configure Claude Code with Static API Key for LiteLLM
DESCRIPTION: This snippet demonstrates how to set a fixed API key for authentication with LiteLLM. The key can be configured either as an environment variable or directly within Claude Code's settings.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/llm-gateway

LANGUAGE: bash
CODE:
```
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

```

LANGUAGE: json
CODE:
```
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

----------------------------------------

TITLE: Integrate Custom Tools with Claude Code SDK via MCP
DESCRIPTION: This snippet demonstrates how to enable custom tools for a Claude agent using the Model Context Protocol (MCP). It shows configuring MCP servers, allowing specific tools, and setting a system prompt for a legal agent, then monitoring tool usage and responses.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: python
CODE:
```
import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def mcp_enabled_agent():
    # Legal agent with document access and streaming
    # Note: Configure your MCP servers as needed
    mcp_servers = {
        # Example configuration - uncomment and configure as needed:
        # "docusign": {
        #     "command": "npx",
        #     "args": ["-y", "@modelcontextprotocol/server-docusign"],
        #     "env": {"API_KEY": "your-key"}
        # }
    }

    async with ClaudeSDKClient(
        options=ClaudeCodeOptions(
            mcp_servers=mcp_servers,
            allowed_tools=["mcp__docusign", "mcp__compliance_db"],
            system_prompt="You are a corporate lawyer specializing in contract review.",
            max_turns=4
        )
    ) as client:
        await client.query("Review this contract for compliance risks")

        # Monitor tool usage and responses
        async for message in client.receive_response():
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'type'):
                        if block.type == 'tool_use':
                            print(f"\n[Using tool: {block.name}]\n")
                        elif hasattr(block, 'text'):
                            print(block.text, end='', flush=True)
                    elif hasattr(block, 'text'):
                        print(block.text, end='', flush=True)

            if type(message).__name__ == "ResultMessage":
                print(f"\n\nReview complete. Total cost: ${message.total_cost_usd:.4f}")

asyncio.run(mcp_enabled_agent())
```

----------------------------------------

TITLE: Find Relevant Code with Claude Code
DESCRIPTION: Leverage Claude Code to locate specific code related to a feature or functionality. Ask Claude to identify relevant files, explain how components interact, and trace execution flows like a login process, using specific domain language for better results.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: Claude Code CLI
CODE:
```
> find the files that handle user authentication
```

LANGUAGE: Claude Code CLI
CODE:
```
> how do these authentication files work together?
```

LANGUAGE: Claude Code CLI
CODE:
```
> trace the login process from front-end to database
```

----------------------------------------

TITLE: Automate Claude AI Responses in GitHub with Google Vertex AI
DESCRIPTION: This GitHub Actions workflow integrates Claude AI to respond to comments on issues and pull requests using Google Vertex AI. It necessitates enabling the Vertex AI API in GCP, configuring Workload Identity Federation for GitHub, and setting up a service account with Vertex AI permissions. The workflow handles repository checkout, GitHub App token generation, Google Cloud authentication via Workload Identity Federation, and then invokes the `claude-code-action` to interact with Claude via Vertex AI.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/github-actions

LANGUAGE: yaml
CODE:
```
name: Claude PR Action

permissions:
  contents: write
  pull-requests: write
  issues: write
  id-token: write

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]

jobs:
  claude-pr:
    if: |
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Authenticate to Google Cloud
        id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

      - uses: anthropics/claude-code-action@v1
        with:
          github_token: ${{ steps.app-token.outputs.token }}
          trigger_phrase: "@claude"
          use_vertex: "true"
          claude_args: '--model claude-sonnet-4@20250514 --max-turns 10'
        env:
          ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
          CLOUD_ML_REGION: us-east5
          VERTEX_REGION_CLAUDE_3_7_SONNET: us-east5
```

----------------------------------------

TITLE: Defining Command Metadata with Frontmatter
DESCRIPTION: Explains how to use YAML frontmatter at the beginning of command files to specify metadata such as allowed tools, argument hints, descriptions, and the specific model to use. This enhances command discoverability and behavior.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/slash-commands

LANGUAGE: YAML
CODE:
```
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: [message]
description: Create a git commit
model: claude-3-5-haiku-20241022
---

Create a git commit with message: $ARGUMENTS
```

LANGUAGE: YAML
CODE:
```
---
argument-hint: [pr-number] [priority] [assignee]
description: Review pull request
---

Review PR #$1 with priority $2 and assign to $3.
Focus on security, performance, and code style.
```

----------------------------------------

TITLE: Add Stripe Integration to Claude MCP
DESCRIPTION: Enable payment processing, subscription management, and financial transactions through Stripe.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http stripe https://mcp.stripe.com
```

----------------------------------------

TITLE: Enable Claude Code Telemetry with Multiple Exporters
DESCRIPTION: This configuration demonstrates how to enable multiple OpenTelemetry metrics exporters simultaneously. Here, metrics are exported to both the console and an OTLP endpoint using the HTTP/JSON protocol, providing flexibility for different monitoring needs.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: shell
CODE:
```
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json
```

----------------------------------------

TITLE: Create Project-Specific Custom Slash Commands for Claude
DESCRIPTION: Details the process of creating reusable slash commands specific to a project, making them available to all team members. This involves creating a `.claude/commands` directory and placing Markdown files within it, where the filename becomes the command name and the content serves as the prompt template.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: Shell
CODE:
```
mkdir -p .claude/commands
```

LANGUAGE: Shell
CODE:
```
echo "Analyze the performance of this code and suggest three specific optimizations:" > .claude/commands/optimize.md
```

LANGUAGE: Shell
CODE:
```
> /optimize
```

----------------------------------------

TITLE: Stream JSON Messages to Claude CLI
DESCRIPTION: Learn how to provide a stream of JSON messages to the `claude` CLI via standard input. This method is crucial for enabling multi-turn conversations and requires specifying both input and output formats as `stream-json`.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: bash
CODE:
```
echo '{"type":"user","message":{"role":"user","content":[{"type":"text","text":"Explain this code"}]}}' | claude -p --output-format=stream-json --input-format=stream-json --verbose
```

----------------------------------------

TITLE: Configure Claude Code CLI Arguments via `claude_args`
DESCRIPTION: Demonstrates how to use the `claude_args` parameter within a GitHub Action workflow to pass command-line arguments to the Claude Code CLI. This allows for fine-grained control over Claude's behavior, such as setting maximum conversation turns, specifying the model to use, or providing a path to an MCP configuration file.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/github-actions

LANGUAGE: YAML
CODE:
```
claude_args: "--max-turns 5 --model claude-sonnet-4-20250514 --mcp-config /path/to/config.json"
```

----------------------------------------

TITLE: Stream Text Output from Claude Code SDK
DESCRIPTION: This snippet shows how to retrieve and stream text output from the Claude Code SDK. It demonstrates querying the client and iterating through messages to print text content as it arrives, providing real-time feedback.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: python
CODE:
```
# Default text output with streaming
async with ClaudeSDKClient() as client:
    await client.query("Explain file src/components/Header.tsx")

    # Stream text as it arrives
    async for message in client.receive_response():
        if hasattr(message, 'content'):
            for block in message.content:
                if hasattr(block, 'text'):
                    print(block.text, end='', flush=True)
                    # Output streams in real-time: This is a React component showing...
```

----------------------------------------

TITLE: Access Claude Code Configuration Settings
DESCRIPTION: After launching Claude Code, use this command to enter its configuration interface. This allows users to adjust various preferences, such as setting the diff tool to `auto` for automatic IDE detection and seamless integration with the development environment.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/ide-integrations

LANGUAGE: cli
CODE:
```
/config
```

----------------------------------------

TITLE: Define a Code Reviewer Subagent
DESCRIPTION: This configuration defines a 'code-reviewer' subagent. It specifies the subagent's name, description, the tools it can access (Read, Grep, Glob, Bash), and detailed instructions for performing code reviews, including a checklist and feedback structure.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sub-agents

LANGUAGE: YAML
CODE:
```
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is simple and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

----------------------------------------

TITLE: Configure Claude Code with LiteLLM Unified Endpoint
DESCRIPTION: This configuration sets the `ANTHROPIC_BASE_URL` to LiteLLM's unified endpoint, which is recommended for benefits such as load balancing, fallbacks, and consistent support for cost and end-user tracking.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/llm-gateway

LANGUAGE: bash
CODE:
```
export ANTHROPIC_BASE_URL=https://litellm-server:4000

```

----------------------------------------

TITLE: Enable and Configure OpenTelemetry for Claude Code via Environment Variables
DESCRIPTION: This snippet demonstrates how to quickly enable OpenTelemetry for Claude Code and configure various aspects like metrics and logs exporters (OTLP, Prometheus, console), OTLP endpoint, authentication headers, and export intervals using shell environment variables. These settings are typically used for individual user configurations or quick testing.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: bash
CODE:
```
# 1. Enable telemetry
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Choose exporters (both are optional - configure only what you need)
export OTEL_METRICS_EXPORTER=otlp       # Options: otlp, prometheus, console
export OTEL_LOGS_EXPORTER=otlp          # Options: otlp, console

# 3. Configure OTLP endpoint (for OTLP exporter)
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. Set authentication (if required)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. For debugging: reduce export intervals
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 seconds (default: 60000ms)
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 seconds (default: 5000ms)

# 6. Run Claude Code
claude
```

----------------------------------------

TITLE: Add Daloopa Integration to Claude MCP
DESCRIPTION: Access high-quality fundamental financial data sourced from SEC Filings and investor presentations via Daloopa.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http daloopa https://mcp.daloopa.com/server/mcp
```

----------------------------------------

TITLE: Create a Simple Bash Status Line Script for Claude Code
DESCRIPTION: This Bash script demonstrates how to read the JSON input from stdin, parse it using `jq` to extract the model display name and current directory, and then print a formatted status line. It shows basic data extraction and output formatting.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/statusline

LANGUAGE: Bash
CODE:
```
#!/bin/bash
# Read JSON input from stdin
input=$(cat)

# Extract values using jq
MODEL_DISPLAY=$(echo "$input" | jq -r '.model.display_name')
CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir')

echo "[$MODEL_DISPLAY] 📁 ${CURRENT_DIR##*/}"
```

----------------------------------------

TITLE: Configure SessionStart Hook for Context Injection
DESCRIPTION: This JSON configuration demonstrates how to use the `SessionStart` hook to inject additional context at the beginning of a Claude session. The `additionalContext` field within `hookSpecificOutput` allows for custom string data to be loaded into the session's context, with multiple hooks' contexts being concatenated.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: json
CODE:
```
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

----------------------------------------

TITLE: Implement Custom Permission Handling Tool with MCP Server (JavaScript)
DESCRIPTION: This snippet demonstrates how to create a custom permission handling tool using an external MCP server in JavaScript. It defines an `McpServer` instance with a `tool` named `approval_prompt` that simulates a permission check, allowing or denying based on input. It also shows how to integrate this custom tool into an SDK query, specifying `permissionPromptTool`, `mcpConfig`, and `allowedTools` for advanced control.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: JavaScript
CODE:
```
const server = new McpServer({
  name: "Test permission prompt MCP Server",
  version: "0.0.1",
});

server.tool(
  "approval_prompt",
  'Simulate a permission check - approve if the input contains "allow", otherwise deny',
  {
    tool_name: z.string().describe("The name of the tool requesting permission"),
    input: z.object({}).passthrough().describe("The input for the tool"),
    tool_use_id: z.string().optional().describe("The unique tool use request ID"),
  },
  async ({ tool_name, input }) => {
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            JSON.stringify(input).includes("allow")
              ? {
                  behavior: "allow",
                  updatedInput: input,
                }
              : {
                  behavior: "deny",
                  message: "Permission denied by test approval_prompt tool",
                }
          ),
        },
      ],
    };
  }
);

// Use in SDK
import { query } from "@anthropic-ai/claude-code";

for await (const message of query({
  prompt: "Analyze the codebase",
  options: {
    permissionPromptTool: "mcp__test-server__approval_prompt",
    mcpConfig: "my-config.json",
    allowedTools: ["Read", "Grep"]
  }
})) {
  if (message.type === "result") console.log(message.result);
}
```

----------------------------------------

TITLE: Specify allowed tools for Claude Code
DESCRIPTION: Provides a list of tools that Claude Code is permitted to use without requiring explicit user permission, in addition to those defined in settings.json.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude --allowedTools "Bash(git log:*)" "Bash(git diff:*)" "Read"
```

----------------------------------------

TITLE: Define and Use Type-Safe Custom Tools with Claude SDK MCP Server
DESCRIPTION: This snippet demonstrates how to define multiple type-safe custom tools (e.g., calculate_compound_interest, fetch_user_data) using `createSdkMcpServer` and `tool` helper functions. It shows how to integrate these custom tools into a Claude `query` and highlights their ability to directly access application data layers.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: TypeScript
CODE:
```
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-code";
import { z } from "zod";

// Create an SDK MCP server with custom tools
const customServer = createSdkMcpServer({
  name: "my-custom-tools",
  version: "1.0.0",
  tools: [
    tool(
      "calculate_compound_interest",
      "Calculate compound interest for an investment",
      {
        principal: z.number().describe("Initial investment amount"),
        rate: z.number().describe("Annual interest rate (as decimal, e.g., 0.05 for 5%)"),
        time: z.number().describe("Investment period in years"),
        n: z.number().default(12).describe("Compounding frequency per year")
      },
      async (args) => {
        const amount = args.principal * Math.pow(1 + args.rate / args.n, args.n * args.time);
        const interest = amount - args.principal;
        
        return {
          content: [{
            type: "text",
            text: `Final amount: $${amount.toFixed(2)}\nInterest earned: $${interest.toFixed(2)}`
          }]
        };
      }
    ),
    tool(
      "fetch_user_data",
      "Fetch user data from your application database",
      {
        userId: z.string().describe("The user ID to fetch"),
        fields: z.array(z.string()).optional().describe("Specific fields to return")
      },
      async (args) => {
        // Direct access to your application's data layer
        const userData = await myDatabase.getUser(args.userId, args.fields);
        
        return {
          content: [{
            type: "text",
            text: JSON.stringify(userData, null, 2)
          }]
        };
      }
    )
  ]
});

// Use the custom tools in your query
for await (const message of query({
  prompt: "Calculate compound interest for $10,000 at 5% for 10 years",
  options: {
    mcpServers: {
      "my-custom-tools": customServer
    },
    maxTurns: 3
  }
})) {
  if (message.type === "result") {
    console.log(message.result);
  }
}
```

----------------------------------------

TITLE: Basic Claude Code GitHub Action Workflow for Comments
DESCRIPTION: Sets up a basic GitHub Actions workflow that triggers on `issue_comment` or `pull_request_review_comment` creation. It uses the `anthropics/claude-code-action@v1` to respond to `@claude` mentions, requiring an `ANTHROPIC_API_KEY` secret for authentication.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/github-actions

LANGUAGE: YAML
CODE:
```
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          # Responds to @claude mentions in comments
```

----------------------------------------

TITLE: Parse JSON Output from Claude CLI with jq
DESCRIPTION: This snippet demonstrates how to configure the `claude` CLI to output responses in JSON format for programmatic parsing. It then shows how to extract specific fields, such as the result and cost, from the JSON output using the `jq` command-line JSON processor.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: bash
CODE:
```
# Parse JSON response with jq
result=$(claude -p "Generate code" --output-format json)
code=$(echo "$result" | jq -r '.result')
cost=$(echo "$result" | jq -r '.cost_usd')
```

----------------------------------------

TITLE: Automate Security Review of Pull Requests with Claude CLI
DESCRIPTION: This snippet demonstrates a bash script for an automated security audit agent using the `claude` CLI. It pipes a GitHub pull request diff to Claude, which then acts as a security engineer to review for vulnerabilities, insecure patterns, and compliance issues.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: bash
CODE:
```
# Security audit agent for pull requests
audit_pr() {
    local pr_number="$1"

    gh pr diff "$pr_number" | claude -p \
      --append-system-prompt "You are a security engineer. Review this PR for vulnerabilities, insecure patterns, and compliance issues." \
      --output-format json \
      --allowedTools "Read,Grep,WebSearch"
}

# Usage and save to file
audit_pr 123 > security-report.json
```

----------------------------------------

TITLE: Resume Claude Code Sessions
DESCRIPTION: Demonstrates how to continue the most recent conversation or resume a specific session using the `query` function with `continue` or `resume` options. This allows for multi-turn interactions and maintaining context.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: TypeScript
CODE:
```
import { query } from "@anthropic-ai/claude-code";

// Continue most recent conversation
for await (const message of query({
  prompt: "Now refactor this for better performance",
  options: { continue: true }
})) {
  if (message.type === "result") console.log(message.result);
}

// Resume specific session
for await (const message of query({
  prompt: "Update the tests",
  options: {
    resume: "550e8400-e29b-41d4-a716-446655440000",
    maxTurns: 3
  }
})) {
  if (message.type === "result") console.log(message.result);
}
```

----------------------------------------

TITLE: Using $ARGUMENTS for All Command Arguments
DESCRIPTION: Demonstrates how the `$ARGUMENTS` placeholder captures all dynamic values passed to a Claude slash command, allowing for flexible input handling. This is useful when the exact number or structure of arguments is not fixed.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/slash-commands

LANGUAGE: Bash
CODE:
```
# Command definition
echo 'Fix issue #$ARGUMENTS following our coding standards' > .claude/commands/fix-issue.md
```

LANGUAGE: CLI
CODE:
```
# Usage
> /fix-issue 123 high-priority
# $ARGUMENTS becomes: "123 high-priority"
```

----------------------------------------

TITLE: Control Claude CLI Output Format (Text, JSON, Stream-JSON)
DESCRIPTION: Explains how to specify the output format for the `claude` CLI tool using the `--output-format` flag. It covers plain text (default), structured JSON, and real-time streaming JSON, which are useful for integrating Claude's responses into scripts or other tools.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: Shell
CODE:
```
cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt
```

LANGUAGE: Shell
CODE:
```
cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json
```

LANGUAGE: Shell
CODE:
```
cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
```

----------------------------------------

TITLE: Creating a Reusable Streaming Print Helper Function for Claude SDK
DESCRIPTION: Illustrates how to define an asynchronous helper function, `stream_print`, to handle streaming responses from the `ClaudeSDKClient`. This function queries the client with a given prompt and then iterates through the received messages to print text content incrementally, ensuring real-time output.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: Python
CODE:
```
async def stream_print(client, prompt):
    await client.query(prompt)
    async for msg in client.receive_response():
        if hasattr(msg, 'content'):
            for block in msg.content:
                if hasattr(block, 'text'):
                    print(block.text, end='', flush=True)
```

----------------------------------------

TITLE: Configure Custom Hooks for Claude Code Tool Execution
DESCRIPTION: Defines custom commands to run before or after tool executions, providing flexibility for integrating with external systems or logging.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: JSON
CODE:
```
{"PreToolUse": {"Bash": "echo 'Running command...'"}}
```

----------------------------------------

TITLE: Pipe Data into Claude CLI for Processing
DESCRIPTION: Demonstrates how to pipe content from a file into the `claude` command-line interface (CLI) tool and direct its output to another file. This enables integrating Claude into existing shell scripts for various tasks, such as concisely explaining build errors.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: Shell
CODE:
```
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

----------------------------------------

TITLE: Configure Local-Scoped MCP Servers with Claude CLI
DESCRIPTION: Details how to configure MCP servers with a 'local' scope. These servers are stored in project-specific user settings, remain private to the user, and are only accessible when working within the current project directory. This is the default configuration level and is ideal for personal development or sensitive credentials.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
# Add a local-scoped server (default)
claude mcp add my-private-server /path/to/server

# Explicitly specify local scope
claude mcp add my-private-server --scope local /path/to/server
```

----------------------------------------

TITLE: Specify Rejected MCP Servers for Claude Code
DESCRIPTION: Lists specific MCP servers from `.mcp.json` files that are explicitly rejected for use by Claude Code, preventing access to certain integrations.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: JSON
CODE:
```
["filesystem"]
```

----------------------------------------

TITLE: Fix Bugs Efficiently with Claude Code
DESCRIPTION: Utilize Claude Code to efficiently diagnose and resolve errors. Share error messages, ask for fix recommendations, and apply suggested changes. Providing context such as reproduction steps or stack traces helps Claude offer more accurate solutions.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: Claude Code CLI
CODE:
```
> I'm seeing an error when I run npm test
```

LANGUAGE: Claude Code CLI
CODE:
```
> suggest a few ways to fix the @ts-ignore in user.ts
```

LANGUAGE: Claude Code CLI
CODE:
```
> update user.ts to add the null check you suggested
```

----------------------------------------

TITLE: Integrate Custom Tools via Model Context Protocol (MCP) with Claude Code
DESCRIPTION: Demonstrates how to give Claude Code agents custom tools and capabilities using the Model Context Protocol (MCP). It shows configuring an agent with specific tools and a system prompt for SRE tasks.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: TypeScript
CODE:
```
import { query } from "@anthropic-ai/claude-code";

// SRE agent with monitoring tools
for await (const message of query({
  prompt: "Investigate the payment service outage",
  options: {
    mcpConfig: "sre-tools.json",
    allowedTools: ["mcp__datadog", "mcp__pagerduty", "mcp__kubernetes"],
    systemPrompt: "You are an SRE. Use monitoring data to diagnose issues.",
    maxTurns: 4
  }
})) {
  if (message.type === "result") console.log(message.result);
}
```

----------------------------------------

TITLE: Enable Claude Code Telemetry with OTLP/gRPC Exporter
DESCRIPTION: This configuration enables Claude Code telemetry and sets up the OpenTelemetry metrics exporter to use OTLP (OpenTelemetry Protocol) with gRPC. Metrics will be sent to the specified OTLP endpoint, typically a collector or backend.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: shell
CODE:
```
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

----------------------------------------

TITLE: Scheduled Claude Code GitHub Action for Daily Reports
DESCRIPTION: Defines a GitHub Actions workflow that runs on a daily schedule (9 AM UTC) to generate a report. It utilizes the `anthropics/claude-code-action@v1` with a custom prompt to summarize commits and open issues, specifying a particular Claude model for the task.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/github-actions

LANGUAGE: YAML
CODE:
```
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * *"
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Generate a summary of yesterday's commits and open issues"
          claude_args: "--model claude-opus-4-1-20250805"
```

----------------------------------------

TITLE: Configure Claude Code Hooks with Tool Matchers
DESCRIPTION: This configuration snippet illustrates the general structure for defining Claude Code hooks within your settings files. Hooks are organized by event name, and can include a "matcher" field to specify tool patterns (e.g., "Write", "Edit", or regex) that trigger the associated commands. The "hooks" array defines the commands to execute, supporting "command" types with optional "timeout".

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: json
CODE:
```
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

----------------------------------------

TITLE: Continue Claude Code conversation via SDK
DESCRIPTION: Continues the most recent conversation programmatically via the SDK, allowing for a new query.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude -c -p "Check for type errors"
```

----------------------------------------

TITLE: Add Arguments to Custom Claude Slash Commands
DESCRIPTION: Illustrates how to make custom slash commands more flexible by incorporating the `$ARGUMENTS` placeholder within the command's prompt template. This allows users to pass additional input directly to the command, which is then substituted into the prompt before sending it to Claude.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: Shell
CODE:
```
echo 'Find and fix issue #$ARGUMENTS. Follow these steps: 1.\nUnderstand the issue described in the ticket 2. Locate the relevant code in\nour codebase 3. Implement a solution that addresses the root cause 4. Add\nappropriate tests 5. Prepare a concise PR description' >\n.claude/commands/fix-issue.md
```

LANGUAGE: Shell
CODE:
```
> /fix-issue 123
```

----------------------------------------

TITLE: Claude Code WebFetch Tool-Specific Permission Rules
DESCRIPTION: Defines how to grant permissions for web fetch requests to specific domains, ensuring controlled external network access.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/iam

LANGUAGE: Configuration
CODE:
```
WebFetch(domain:example.com)
```

----------------------------------------

TITLE: Ask for Confirmation on Tool Use Permissions in Claude Code
DESCRIPTION: Defines an array of permission rules that require user confirmation before allowing specific tool uses within Claude Code, such as Git push operations.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: JSON
CODE:
```
[ "Bash(git push:*)" ]
```

----------------------------------------

TITLE: Add Airtable Integration to Claude MCP
DESCRIPTION: Read/write records and manage bases and tables within Airtable.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add airtable --env AIRTABLE_API_KEY=YOUR_KEY -- npx -y airtable-mcp-server
```

----------------------------------------

TITLE: Collect all messages with metadata using Claude SDK
DESCRIPTION: This snippet demonstrates how to query the Claude SDK, receive messages asynchronously, and extract metadata like cost, duration, and session ID from the `ResultMessage` once the final response is received.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python

LANGUAGE: python
CODE:
```
async with ClaudeSDKClient() as client:
    await client.query("How does the data layer work?")

    messages = []
    result_data = None

    async for message in client.receive_messages():
        messages.append(message)

        # Capture result message with metadata
        if type(message).__name__ == "ResultMessage":
            result_data = {
                "result": message.result,
                "cost": message.total_cost_usd,
                "duration": message.duration_ms,
                "num_turns": message.num_turns,
                "session_id": message.session_id
            }
            break

    print(result_data)
```

----------------------------------------

TITLE: Specify Approved MCP Servers for Claude Code
DESCRIPTION: Lists specific MCP servers from `.mcp.json` files that are explicitly approved for use by Claude Code, enabling access to defined integrations.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: JSON
CODE:
```
["memory", "github"]
```

----------------------------------------

TITLE: Configure OpenTelemetry Resource Attributes for Claude Code
DESCRIPTION: This snippet demonstrates how to set the OTEL_RESOURCE_ATTRIBUTES environment variable to include custom resource attributes for OpenTelemetry. It highlights the importance of percent-encoding special characters in attribute values and warns against quoting the entire key-value pair.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: shell
CODE:
```
export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
```

----------------------------------------

TITLE: Leverage Extended Thinking for Complex Tasks with Claude
DESCRIPTION: Discover how to prompt Claude Code for 'extended thinking' to tackle complex architectural decisions, challenging bugs, or multi-step implementations that require deep reasoning. This involves providing initial context and refining the thinking process with follow-up prompts to achieve deeper insights and comprehensive solutions.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: AI Prompt
CODE:
```
> I need to implement a new authentication system using OAuth2 for our API. Think deeply about the best approach for implementing this in our codebase.
```

LANGUAGE: AI Prompt
CODE:
```
> think about potential security vulnerabilities in this approach
```

LANGUAGE: AI Prompt
CODE:
```
> keep thinking about edge cases we should handle
```

----------------------------------------

TITLE: Integrate and Authenticate with Remote MCP Servers (e.g., Sentry)
DESCRIPTION: Demonstrates how to add a remote MCP server using an HTTP transport and authenticate with it, typically via OAuth 2.0. This process involves adding the server with `claude mcp add` and then using the `/mcp` command within Claude Code to initiate the authentication flow. This enables interaction with cloud-based services like Sentry for tasks such as error monitoring.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Use /mcp to authenticate with your Sentry account
> /mcp

# Debug production issues
> "What are the most common errors in the last 24 hours?"
> "Show me the stack trace for error ID abc123"
> "Which deployment introduced these new errors?"
```

----------------------------------------

TITLE: Configure Separate Endpoints for Claude Code Metrics and Logs
DESCRIPTION: This advanced configuration allows for distinct OpenTelemetry exporters and endpoints for metrics and logs. Metrics are sent via OTLP HTTP/protobuf to one endpoint, while logs are sent via OTLP gRPC to another, enabling specialized handling of different telemetry signals.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: shell
CODE:
```
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.company.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.company.com:4317
```

----------------------------------------

TITLE: Claude Code GitHub Action for Pull Request Review with Slash Commands
DESCRIPTION: Configures a GitHub Actions workflow to automatically trigger a code review when a pull request is opened or synchronized. It uses the `anthropics/claude-code-action@v1` with a `/review` prompt and limits the number of turns to 5, requiring an `ANTHROPIC_API_KEY` secret for authentication.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/github-actions

LANGUAGE: YAML
CODE:
```
name: Code Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "/review"
          claude_args: "--max-turns 5"
```

----------------------------------------

TITLE: Enable verbose logging for Claude Code
DESCRIPTION: Activates detailed logging, showing full turn-by-turn output for debugging purposes in both print and interactive modes.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude --verbose
```

----------------------------------------

TITLE: Allow Specific Tool Use Permissions in Claude Code
DESCRIPTION: Defines an array of permission rules that explicitly allow certain tool uses within Claude Code, such as specific Git commands.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: JSON
CODE:
```
[ "Bash(git diff:*)" ]
```

----------------------------------------

TITLE: Executing Bash Commands with '!' Prefix in Claude
DESCRIPTION: Illustrates how to execute bash commands before a Claude slash command runs by using the `!` prefix. The output of these bash commands is included in the command context, enabling dynamic information retrieval. Requires `allowed-tools` configuration for `Bash`.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/slash-commands

LANGUAGE: YAML
CODE:
```
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
```

----------------------------------------

TITLE: Add Fireflies Integration to Claude MCP
DESCRIPTION: Extract valuable insights from meeting transcripts and summaries using Fireflies.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http fireflies https://api.fireflies.ai/mcp
```

----------------------------------------

TITLE: Specify MCP tool for permission prompts
DESCRIPTION: Designates a Model Context Protocol (MCP) tool to manage and handle permission prompts when Claude Code is in non-interactive mode.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude -p --permission-prompt-tool mcp_auth_tool "query"
```

----------------------------------------

TITLE: Add Figma Integration to Claude MCP
DESCRIPTION: Access designs and export assets from Figma. Requires the latest Figma Desktop with Dev Mode MCP Server. If an existing server is present at http://127.0.0.1:3845/sse, delete it before adding this new one.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http figma-dev-mode-mcp-server http://127.0.0.1:3845/mcp
```

----------------------------------------

TITLE: Set Custom Attributes for Multi-Team Support
DESCRIPTION: Demonstrates how to use the `OTEL_RESOURCE_ATTRIBUTES` environment variable to add custom attributes like department, team ID, and cost center. These attributes are included in all metrics and events for filtering and analysis.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: bash
CODE:
```
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

----------------------------------------

TITLE: Reference Files and Directories in Claude Conversations
DESCRIPTION: This section explains how to use the `@` symbol to quickly include file or directory content in your conversations with Claude Code. It covers referencing single files for content inclusion, directories for structure listing, and MCP resources for fetching data from connected servers.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: AI Prompt
CODE:
```
> Explain the logic in @src/utils/auth.js
```

LANGUAGE: AI Prompt
CODE:
```
> What's the structure of @src/components?
```

LANGUAGE: AI Prompt
CODE:
```
> Show me the data from @github:repos/owner/repo/issues
```

----------------------------------------

TITLE: Generate and Manage Code Documentation with Claude
DESCRIPTION: This section demonstrates how to use Claude Code to identify undocumented functions, generate JSDoc comments, and review/verify documentation quality. It provides a step-by-step process for integrating AI assistance into documentation workflows, ensuring adherence to project standards.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: AI Prompt
CODE:
```
> find functions without proper JSDoc comments in the auth module
```

LANGUAGE: AI Prompt
CODE:
```
> add JSDoc comments to the undocumented functions in auth.js
```

LANGUAGE: AI Prompt
CODE:
```
> improve the generated documentation with more context and examples
```

LANGUAGE: AI Prompt
CODE:
```
> check if the documentation follows our project standards
```

----------------------------------------

TITLE: Extending Claude Code Working Directory Access
DESCRIPTION: Commands and configuration options to grant Claude Code access to additional directories beyond its launch location, either during startup, session, or persistently.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/iam

LANGUAGE: CLI
CODE:
```
--add-dir <path>
```

LANGUAGE: CLI
CODE:
```
/add-dir
```

----------------------------------------

TITLE: Continue most recent Claude Code conversation
DESCRIPTION: Loads and continues the most recently active conversation in the current directory.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude -c
```

----------------------------------------

TITLE: Custom Claude Code Output Style Markdown Template
DESCRIPTION: This snippet provides the standard Markdown file structure for defining a custom output style for Claude Code. It includes a YAML front matter for metadata like the style's name and description, followed by sections for custom instructions and specific behavioral definitions for the AI assistant.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/output-styles

LANGUAGE: Markdown
CODE:
```
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

----------------------------------------

TITLE: Configure Claude Code Status Line in settings.json
DESCRIPTION: This JSON snippet shows how to add a custom status line command to your `.claude/settings.json` file. The `type` should be `command`, and `command` specifies the path to your executable script. `padding` is an optional setting to control spacing.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/statusline

LANGUAGE: JSON
CODE:
```
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0 
  }
}
```

----------------------------------------

TITLE: Set Token Refresh Interval for Dynamic API Key Helper
DESCRIPTION: This environment variable sets the refresh interval (in milliseconds) for the dynamic API key helper, controlling how often Claude Code will re-run the helper script to obtain a new key.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/llm-gateway

LANGUAGE: bash
CODE:
```
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000

```

----------------------------------------

TITLE: View Claude Hook Debug Output
DESCRIPTION: This snippet demonstrates how to use the `claude --debug` command to view detailed execution information for hooks. The output provides insights into hook matching, command execution, and status, aiding in debugging.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: Shell
CODE:
```
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 60000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

----------------------------------------

TITLE: Configure Claude Code with LiteLLM Google Vertex AI Pass-Through Endpoint
DESCRIPTION: This snippet demonstrates how to configure Claude Code to route Google Vertex AI requests through LiteLLM, specifying the project ID, region, and options to skip Vertex AI's native authentication.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/llm-gateway

LANGUAGE: bash
CODE:
```
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5

```

----------------------------------------

TITLE: Claude Code Default Permission Modes
DESCRIPTION: Defines the standard behavior for Claude Code's interaction with tools and file permissions, configurable via the `defaultMode` setting in settings files.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/iam

LANGUAGE: Configuration
CODE:
```
default
```

LANGUAGE: Configuration
CODE:
```
acceptEdits
```

LANGUAGE: Configuration
CODE:
```
plan
```

LANGUAGE: Configuration
CODE:
```
bypassPermissions
```

----------------------------------------

TITLE: Claude Code Read & Edit File Permission Pattern Types
DESCRIPTION: Describes the four distinct pattern types used for defining file read and edit permissions, which follow the gitignore specification for path interpretation.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/iam

LANGUAGE: Configuration
CODE:
```
//path
```

LANGUAGE: Configuration
CODE:
```
~/path
```

LANGUAGE: Configuration
CODE:
```
/path
```

LANGUAGE: Configuration
CODE:
```
path
```

LANGUAGE: Configuration
CODE:
```
./path
```

----------------------------------------

TITLE: Automate Security Review of Pull Requests with Claude Code (TypeScript)
DESCRIPTION: This snippet illustrates how to create an automated security review agent for pull requests using Claude Code. The `auditPR` function fetches a PR diff using `execSync` and then feeds it as a prompt to the Claude Code `query` function. It uses a system prompt to instruct the agent to identify vulnerabilities and insecure patterns, leveraging tools like `Read`, `Grep`, and `WebSearch` for comprehensive analysis.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: TypeScript
CODE:
```
import { query } from "@anthropic-ai/claude-code";
import { execSync } from "child_process";

async function auditPR(prNumber: number) {
  // Get PR diff
  const prDiff = execSync(`gh pr diff ${prNumber}`, { encoding: 'utf8' });

  const messages = [];
  for await (const message of query({
    prompt: prDiff,
    options: {
      systemPrompt: "You are a security engineer. Review this PR for vulnerabilities, insecure patterns, and compliance issues.",
      maxTurns: 3,
      allowedTools: ["Read", "Grep", "WebSearch"]
    }
  })) {
    messages.push(message);
  }

  return messages.find(m => m.type === "result");
}

// Usage
const report = await auditPR(123);
console.log(JSON.stringify(report, null, 2));
```

----------------------------------------

TITLE: Extract JSON Data and Format Status Line with Bash and JQ
DESCRIPTION: This Bash script demonstrates how to parse JSON input from stdin using `jq` and define helper functions for common data extractions. It then uses these functions to retrieve model and directory information, outputting a concise status line. This approach promotes reusability and readability for complex Bash scripts.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/statusline

LANGUAGE: Bash
CODE:
```
#!/bin/bash
# Read JSON input once
input=$(cat)

# Helper functions for common extractions
get_model_name() { echo "$input" | jq -r '.model.display_name'; }
get_current_dir() { echo "$input" | jq -r '.workspace.current_dir'; }
get_project_dir() { echo "$input" | jq -r '.workspace.project_dir'; }
get_version() { echo "$input" | jq -r '.version'; }
get_cost() { echo "$input" | jq -r '.cost.total_cost_usd'; }
get_duration() { echo "$input" | jq -r '.cost.total_duration_ms'; }
get_lines_added() { echo "$input" | jq -r '.cost.total_lines_added'; }
get_lines_removed() { echo "$input" | jq -r '.cost.total_lines_removed'; }

# Use the helpers
MODEL=$(get_model_name)
DIR=$(get_current_dir)
echo "[$MODEL] 📁 ${DIR##*/}"
```

----------------------------------------

TITLE: Enable Claude Code Telemetry for Console Debugging
DESCRIPTION: This configuration enables Claude Code telemetry and sets the OpenTelemetry metrics exporter to 'console', with an export interval of 1 second (1000 milliseconds). This is useful for local debugging and immediate feedback on collected metrics.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: shell
CODE:
```
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000
```

----------------------------------------

TITLE: Understand JSON Input Structure for Claude Code Status Line Commands
DESCRIPTION: This JSON snippet illustrates the data structure passed via stdin to your custom status line script. It includes session details, model information, workspace paths, version, output style, and cost metrics, allowing scripts to display contextual information.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/statusline

LANGUAGE: JSON
CODE:
```
{
  "hook_event_name": "Status",
  "session_id": "abc123...",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/current/working/directory",
  "model": {
    "id": "claude-opus-4-1",
    "display_name": "Opus"
  },
  "workspace": {
    "current_dir": "/current/working/directory",
    "project_dir": "/original/project/directory"
  },
  "version": "1.0.80",
  "output_style": {
    "name": "default"
  },
  "cost": {
    "total_cost_usd": 0.01234,
    "total_duration_ms": 45000,
    "total_api_duration_ms": 2300,
    "total_lines_added": 156,
    "total_lines_removed": 23
  }
}
```

----------------------------------------

TITLE: Configure Claude Code with LiteLLM Amazon Bedrock Pass-Through Endpoint
DESCRIPTION: This configuration enables Claude Code to use LiteLLM as a pass-through for Amazon Bedrock, including settings to skip Bedrock's native authentication.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/llm-gateway

LANGUAGE: bash
CODE:
```
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1

```

----------------------------------------

TITLE: Define a Debugger Subagent
DESCRIPTION: This configuration defines a 'debugger' subagent, specializing in root cause analysis for errors, test failures, and unexpected behavior. It outlines the subagent's name, description, available tools (Read, Edit, Bash, Grep, Glob), and a structured debugging process.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sub-agents

LANGUAGE: YAML
CODE:
```
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not just symptoms.
```

----------------------------------------

TITLE: Query Claude Code via SDK and exit
DESCRIPTION: Sends a query to Claude Code programmatically via the SDK and exits after receiving the response, without entering interactive mode.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude -p "explain this function"
```

----------------------------------------

TITLE: Disable Claude Code Auto-updates
DESCRIPTION: Shows how to disable automatic updates for Claude Code by setting the `DISABLE_AUTOUPDATER` environment variable in your shell or settings file.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/setup

LANGUAGE: Shell
CODE:
```
export DISABLE_AUTOUPDATER=1
```

----------------------------------------

TITLE: Create a Python Status Line Script for Claude Code
DESCRIPTION: This Python script provides an alternative to Bash for creating a custom status line. It reads JSON input, extracts model and directory information, and attempts to find the Git branch by inspecting the `.git/HEAD` file. It demonstrates Python's `json` and `os` modules for data processing.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/statusline

LANGUAGE: Python
CODE:
```
#!/usr/bin/env python3
import json
import sys
import os

# Read JSON from stdin
data = json.load(sys.stdin)

# Extract values
model = data['model']['display_name']
current_dir = os.path.basename(data['workspace']['current_dir'])

# Check for git branch
git_branch = ""
if os.path.exists('.git'):
    try:
        with open('.git/HEAD', 'r') as f:
            ref = f.read().strip()
            if ref.startswith('ref: refs/heads/'):
                git_branch = f" | 🌿 {ref.replace('ref: refs/heads/', '')}"
    except:
        pass

print(f"[{model}] 📁 {current_dir}{git_branch}")
```

----------------------------------------

TITLE: Append to Claude Code system prompt
DESCRIPTION: Adds custom instructions or context to the system prompt, which influences Claude Code's behavior (only applicable with `--print` mode).

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude --append-system-prompt "Custom instruction"
```

----------------------------------------

TITLE: Manage Claude Subagents
DESCRIPTION: This section explains how to view, use, and create specialized AI subagents within Claude to handle specific coding tasks. It covers automatic delegation, explicit requests, and custom subagent creation.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: CLI
CODE:
```
> /agents
```

LANGUAGE: CLI
CODE:
```
> review my recent code changes for security issues
```

LANGUAGE: CLI
CODE:
```
> run all tests and fix any failures
```

LANGUAGE: CLI
CODE:
```
> use the code-reviewer subagent to check the auth module
```

LANGUAGE: CLI
CODE:
```
> have the debugger subagent investigate why users can't log in
```

----------------------------------------

TITLE: Configure Claude Code API Key Helper Script
DESCRIPTION: Defines a custom shell script to be executed to generate an authentication value. This value will be sent as `X-Api-Key` and `Authorization: Bearer` headers for model requests.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: Shell
CODE:
```
/bin/generate_temp_api_key.sh
```

----------------------------------------

TITLE: Claude Code MCP Tool-Specific Permission Rules
DESCRIPTION: Rules for Managed Code Provider (MCP) tools, allowing approval of all tools from a server or specific tools, with the limitation that wildcards are not supported.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/iam

LANGUAGE: Configuration
CODE:
```
mcp__puppeteer
```

LANGUAGE: Configuration
CODE:
```
mcp__puppeteer__puppeteer_navigate
```

LANGUAGE: Configuration
CODE:
```
mcp__github
```

LANGUAGE: Configuration
CODE:
```
mcp__github__get_issue
```

LANGUAGE: Configuration
CODE:
```
mcp__github__list_issues
```

----------------------------------------

TITLE: Manage Multi-Turn Conversations in Headless Mode
DESCRIPTION: These commands illustrate how to handle multi-turn conversations when running Claude Code in headless mode. You can continue the most recent session using `--continue` or resume a specific conversation by its session ID with `--resume`, including an option for non-interactive resume.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: bash
CODE:
```
# Continue the most recent conversation
claude --continue "Now refactor this for better performance"

# Resume a specific conversation by session ID
claude --resume 550e8400-e29b-41d4-a716-446655440000 "Update the tests"

# Resume in non-interactive mode
claude --resume 550e8400-e29b-41d4-a716-446655440000 "Fix all linting issues" --no-interactive
```

----------------------------------------

TITLE: Enable Claude Code Telemetry with Prometheus Exporter
DESCRIPTION: This configuration enables Claude Code telemetry and sets the OpenTelemetry metrics exporter to 'prometheus'. This allows Prometheus to scrape metrics directly from Claude Code for monitoring and alerting purposes.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: shell
CODE:
```
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus
```

----------------------------------------

TITLE: Stream JSON Output from Claude Code
DESCRIPTION: This command shows how to receive a continuous stream of JSON messages from Claude Code. The `--output-format stream-json` flag is useful for real-time processing, where each conversation turn or system message is emitted as a separate JSON object.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: bash
CODE:
```
claude -p "Build an application" --output-format stream-json
```

----------------------------------------

TITLE: Configure Claude Code to Deny Access to Sensitive Files
DESCRIPTION: This configuration snippet for `.claude/settings.json` demonstrates how to use the `permissions.deny` setting to prevent Claude Code from accessing specified sensitive files and directories. This mechanism ensures that files like environment variables, API keys, or build outputs are completely invisible to Claude Code, enhancing data security. It replaces the deprecated `ignorePatterns` configuration.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: json
CODE:
```
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

----------------------------------------

TITLE: Set Recommended Output Token Limits for Claude Code Bedrock
DESCRIPTION: This snippet outlines the recommended environment variable settings for CLAUDE_CODE_MAX_OUTPUT_TOKENS and MAX_THINKING_TOKENS when using Claude Code with Amazon Bedrock. These values are optimized to prevent premature truncation of tool uses and maintain focused reasoning chains, aligning with Bedrock's burndown throttling logic.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock

LANGUAGE: bash
CODE:
```
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=4096
export MAX_THINKING_TOKENS=1024
```

----------------------------------------

TITLE: Add User-Scoped MCP Server
DESCRIPTION: Add a server that is accessible across all projects on your machine, private to your user account. This scope is ideal for personal utility servers, development tools, or services frequently used across different projects.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add my-user-server --scope user /path/to/server
```

----------------------------------------

TITLE: Provide Post-Tool Execution Feedback with PostToolUse Hook
DESCRIPTION: The `PostToolUse` hook enables providing feedback to Claude after a tool has executed. Setting `decision` to `block` automatically prompts Claude with a specified `reason`. Additionally, `hookSpecificOutput.additionalContext` can be used to add more information for Claude to consider.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: JSON
CODE:
```
{
  "decision": "block" | undefined,
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

----------------------------------------

TITLE: Resume a specific Claude Code session by ID
DESCRIPTION: Loads a particular Claude Code session using its unique identifier, or allows selection in interactive mode.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude --resume abc123 "query"
```

----------------------------------------

TITLE: Configure AWS CLI for Claude Code Bedrock Access
DESCRIPTION: Details how to set up AWS credentials using the AWS CLI's `aws configure` command. This command is part of the default AWS SDK credential chain used by Claude Code for authentication with Bedrock.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock

LANGUAGE: Shell
CODE:
```
aws configure
```

----------------------------------------

TITLE: Stream Input with Images to Claude Code
DESCRIPTION: Shows how to attach images to messages when using streaming input mode. It demonstrates sending an image along with text content by reading a file and encoding it in base64.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: TypeScript
CODE:
```
import { query } from "@anthropic-ai/claude-code";
import { readFileSync } from "fs";

async function* messagesWithImage() {
  // Send an image with text
  yield {
    type: "user" as const,
    message: {
      role: "user" as const,
      content: [
        {
          type: "text",
          text: "Analyze this screenshot and suggest improvements"
        },
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/png",
            data: readFileSync("screenshot.png", "base64")
          }
        }
      ]
    }
  };
}

for await (const message of query({
  prompt: messagesWithImage()
})) {
  if (message.type === "result") console.log(message.result);
}
```

----------------------------------------

TITLE: Implement Fine-Grained Permission Control for Claude Tools
DESCRIPTION: This snippet demonstrates how to use the `canUseTool` callback within a Claude `query` to implement fine-grained permission control for custom tools. It allows developers to define custom logic, such as checking user permissions, to dynamically allow or deny tool execution.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: TypeScript
CODE:
```
for await (const message of query({
  prompt: "Analyze user behavior and calculate metrics",
  options: {
    mcpServers: {
      "analytics": analyticsServer
    },
    canUseTool: async (toolName, input) => {
      // Control which tools can be used
      if (toolName.startsWith("mcp__analytics__")) {
        // Check permissions for analytics tools
        const hasPermission = await checkUserPermissions(toolName);
        
        return hasPermission
          ? { behavior: "allow", updatedInput: input }
          : { behavior: "deny", message: "Insufficient permissions" };
      }
      
      // Allow other tools by default
      return { behavior: "allow", updatedInput: input };
    }
  }
})) {
  if (message.type === "result") console.log(message.result);
}
```

----------------------------------------

TITLE: Add PayPal Integration to Claude MCP
DESCRIPTION: Integrate PayPal commerce capabilities, including payment processing and transaction management.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http paypal https://mcp.paypal.com/mcp
```

----------------------------------------

TITLE: Enable Claude Code Telemetry for Metrics Only
DESCRIPTION: This configuration enables Claude Code telemetry specifically for metrics, disabling event/log export. Metrics are sent using OTLP over gRPC to a specified endpoint, focusing solely on performance and usage data.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: shell
CODE:
```
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

----------------------------------------

TITLE: Claude Code Enterprise Managed Policy File Locations
DESCRIPTION: Standard file paths for deploying enterprise-managed policy settings across different operating systems, which take precedence over user and project settings.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/iam

LANGUAGE: File Path
CODE:
```
/Library/Application Support/ClaudeCode/managed-settings.json
```

LANGUAGE: File Path
CODE:
```
/etc/claude-code/managed-settings.json
```

LANGUAGE: File Path
CODE:
```
C:\ProgramData\ClaudeCode\managed-settings.json
```

----------------------------------------

TITLE: Use Project-Relative Paths in Claude Code Hooks
DESCRIPTION: This configuration shows how to leverage the "CLAUDE_PROJECT_DIR" environment variable within hook commands. This variable, available when Claude Code spawns the hook, allows you to reference scripts or files located within your project directory, ensuring that your hooks are portable and function correctly regardless of the current working directory.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: json
CODE:
```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/check-style.sh"
          }
        ]
      }
    ]
  }
}
```

----------------------------------------

TITLE: Specify Additional Accessible Directories for Claude Code
DESCRIPTION: Defines an array of additional working directories that Claude Code has permission to access, extending its operational scope.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: JSON
CODE:
```
[ "../docs/" ]
```

----------------------------------------

TITLE: Inject Context and Validate User Prompts with UserPromptSubmit Hook
DESCRIPTION: This Python script demonstrates a `UserPromptSubmit` hook that can both inject additional context and perform validation on user prompts. It checks for sensitive patterns like 'password' or 'token' and, if found, blocks the prompt using a JSON output with a 'block' decision. Otherwise, it adds the current timestamp as context to the prompt, allowing it to proceed.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: python
CODE:
```
#!/usr/bin/env python3
import json
import sys
import re
import datetime

# Load input from stdin
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

prompt = input_data.get("prompt", "")

# Check for sensitive patterns
sensitive_patterns = [
    (r"(?i)\b(password|secret|key|token)\s*[:=]", "Prompt contains potential secrets"),
]

for pattern, message in sensitive_patterns:
    if re.search(pattern, prompt):
        # Use JSON output to block with a specific reason
        output = {
            "decision": "block",
            "reason": f"Security policy violation: {message}. Please rephrase your request without sensitive information."
        }
        print(json.dumps(output))
        sys.exit(0)

# Add current time to context
context = f"Current time: {datetime.datetime.now()}"
print(context)

"""
The following is also equivalent:
print(json.dumps({
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": context,
  },
}))
"""

# Allow the prompt to proceed with the additional context
sys.exit(0)
```

----------------------------------------

TITLE: Add Intercom Integration to Claude MCP
DESCRIPTION: Access real-time customer conversations, tickets, and user data from Intercom.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http intercom https://mcp.intercom.com/mcp
```

----------------------------------------

TITLE: Enable Claude Code Bedrock Integration and AWS Region
DESCRIPTION: Presents the essential environment variables required to enable Claude Code's integration with Amazon Bedrock. Setting `CLAUDE_CODE_USE_BEDROCK` to `1` and specifying the `AWS_REGION` ensures Claude Code communicates with the correct Bedrock endpoint.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock

LANGUAGE: Shell
CODE:
```
# Enable Bedrock integration
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # or your preferred region
```

----------------------------------------

TITLE: Enable Vertex AI API for Claude Code on GCP
DESCRIPTION: This command enables the Vertex AI API in your Google Cloud Platform project, which is a prerequisite for using Claude Code with Vertex AI. It also sets the default project ID for `gcloud` commands, ensuring subsequent operations target the correct project.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai

LANGUAGE: Bash
CODE:
```
# Set your project ID
gcloud config set project YOUR-PROJECT-ID

# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

----------------------------------------

TITLE: Auto-Approve Tool Calls with PreToolUse Hook
DESCRIPTION: This Python script implements a `PreToolUse` hook to automatically approve specific tool calls based on predefined criteria. It checks if the tool is 'Read' and if the `file_path` ends with common documentation extensions. If conditions are met, it outputs JSON with a 'decision' of 'approve' and `suppressOutput` set to true, allowing the tool call to proceed without user intervention or transcript display.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: python
CODE:
```
#!/usr/bin/env python3
import json
import sys

# Load input from stdin
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

# Example: Auto-approve file reads for documentation files
if tool_name == "Read":
    file_path = tool_input.get("file_path", "")
    if file_path.endswith((".md", ".mdx", ".txt", ".json")):
        # Use JSON output to auto-approve the tool call
        output = {
            "decision": "approve",
            "reason": "Documentation file auto-approved",
            "suppressOutput": True  # Don't show in transcript mode
        }
        print(json.dumps(output))
        sys.exit(0)

# For other cases, let the normal permission flow proceed
sys.exit(0)
```

----------------------------------------

TITLE: Configure Claude Code proxy with basic authentication credentials
DESCRIPTION: Include username and password directly in the `HTTPS_PROXY` URL for basic authentication with a corporate proxy. It is recommended to avoid hardcoding passwords in scripts for security.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/corporate-proxy

LANGUAGE: Shell
CODE:
```
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

----------------------------------------

TITLE: Configure Claude Code with LiteLLM Anthropic Pass-Through Endpoint
DESCRIPTION: This snippet shows how to configure Claude Code to route Anthropic API requests through a specific LiteLLM pass-through endpoint.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/llm-gateway

LANGUAGE: bash
CODE:
```
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic

```

----------------------------------------

TITLE: Configure Custom Status Line Command in Claude Code
DESCRIPTION: Sets up a custom status line to display context, executing a specified command to generate the status text.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: JSON
CODE:
```
{"type": "command", "command": "~/.claude/statusline.sh"}
```

----------------------------------------

TITLE: Specify disallowed tools for Claude Code
DESCRIPTION: Provides a list of tools that Claude Code is explicitly forbidden from using, overriding any permissions from settings.json.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude --disallowedTools "Bash(git log:*)" "Bash(git diff:*)" "Edit"
```

----------------------------------------

TITLE: Referencing Files in Claude Commands with '@'
DESCRIPTION: Shows how to include the contents of local files directly within Claude commands using the `@` prefix. This allows commands to operate on specific file content, facilitating tasks like code review or comparison.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/slash-commands

LANGUAGE: Claude Command Syntax
CODE:
```
# Reference a specific file

Review the implementation in @src/utils/helpers.js
```

LANGUAGE: Claude Command Syntax
CODE:
```
# Reference multiple files

Compare @src/old-version.js with @src/new-version.js
```

----------------------------------------

TITLE: MCP Slash Command Format
DESCRIPTION: Describes the standard format for MCP (Multi-Cloud Platform) slash commands, which are dynamically discovered from connected MCP servers. These commands follow a specific naming convention to identify the server and prompt.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/slash-commands

LANGUAGE: CLI
CODE:
```
/mcp__<server-name>__<prompt-name> [arguments]
```

----------------------------------------

TITLE: Add additional working directories to Claude Code
DESCRIPTION: Allows specifying extra directories that Claude Code can access during its operations, validating each path.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude --add-dir ../apps ../lib
```

----------------------------------------

TITLE: Process piped content with Claude Code
DESCRIPTION: Feeds content from standard input (e.g., a file) to Claude Code for processing, typically used with the print mode.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
cat logs.txt | claude -p "explain"
```

----------------------------------------

TITLE: Set Environment Variables in Claude Code Sessions
DESCRIPTION: Specifies environment variables that will be applied to every Claude Code session, allowing for custom configurations.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: JSON
CODE:
```
{"FOO": "bar"}
```

----------------------------------------

TITLE: Deny Specific Tool Use Permissions in Claude Code
DESCRIPTION: Defines an array of permission rules that explicitly deny certain tool uses, including excluding sensitive files or commands from Claude Code access.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: JSON
CODE:
```
[ "WebFetch", "Bash(curl:*)", "Read(./.env)", "Read(./secrets/**)" ]
```

----------------------------------------

TITLE: Invoke a Specific Claude Code Subagent
DESCRIPTION: Explicitly direct Claude Code to use a predefined subagent for a particular task. This command delegates the current interaction to the specified subagent, leveraging its specialized configuration and context.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sub-agents

LANGUAGE: Natural Language
CODE:
```
> Use the code-reviewer subagent to check my recent changes
```

----------------------------------------

TITLE: Resume Claude Code session by ID
DESCRIPTION: Resumes a specific Claude Code session using its unique session ID, allowing continuation of a past conversation.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude -r "abc123" "Finish this PR"
```

----------------------------------------

TITLE: Configure Claude Code for custom SSL/TLS certificates with proxy
DESCRIPTION: Resolve SSL certificate errors when using a corporate proxy by specifying the path to a custom certificate bundle. Use `SSL_CERT_FILE` and `NODE_EXTRA_CA_CERTS` environment variables.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/corporate-proxy

LANGUAGE: Shell
CODE:
```
export SSL_CERT_FILE=/path/to/certificate-bundle.crt
export NODE_EXTRA_CA_CERTS=/path/to/certificate-bundle.crt
```

----------------------------------------

TITLE: Enable Claude Code Telemetry for Events/Logs Only
DESCRIPTION: This configuration enables Claude Code telemetry specifically for events and logs, disabling metrics export. Logs are sent using OTLP over gRPC to a specified endpoint, focusing on operational insights and debugging information.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/monitoring-usage

LANGUAGE: shell
CODE:
```
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

----------------------------------------

TITLE: Stream Input to Claude Code
DESCRIPTION: Illustrates how to provide messages as an async iterable for streaming input, enabling multi-turn conversations and dynamic message generation. It uses an async generator to yield user messages over time.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: TypeScript
CODE:
```
import { query } from "@anthropic-ai/claude-code";

// Create an async generator for streaming messages
async function* generateMessages() {
  yield {
    type: "user" as const,
    message: {
      role: "user" as const,
      content: "Start analyzing this codebase"
    }
  };
  
  // Wait for some condition or user input
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  yield {
    type: "user" as const,
    message: {
      role: "user" as const,
      content: "Now focus on the authentication module"
    }
  };
}

// Use streaming input
for await (const message of query({
  prompt: generateMessages(),
  options: {
    maxTurns: 5,
    allowedTools: ["Read", "Grep", "Bash"]
  }
})) {
  if (message.type === "result") {
    console.log(message.result);
  }
}
```

----------------------------------------

TITLE: Configure Custom Claude Command for Execution
DESCRIPTION: Users can define a custom command to invoke Claude from the terminal or IDE. This allows for flexibility, supporting direct executables, package manager calls, or specific configurations like those for Windows Subsystem for Linux (WSL). Ensure the specified command is accessible in your system's PATH.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/ide-integrations

LANGUAGE: Shell
CODE:
```
claude
```

LANGUAGE: Shell
CODE:
```
/usr/local/bin/claude
```

LANGUAGE: Shell
CODE:
```
npx @anthropic/claude
```

LANGUAGE: Shell
CODE:
```
wsl -d Ubuntu -- bash -lic "claude"
```

----------------------------------------

TITLE: Skip Claude Code permission prompts
DESCRIPTION: Disables all permission prompts, allowing Claude Code to execute actions without user confirmation (use with caution).

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude --dangerously-skip-permissions
```

----------------------------------------

TITLE: Generate CLI Status Line with Node.js
DESCRIPTION: This Node.js script reads JSON input from stdin, extracts relevant information like the model display name and current directory, and optionally checks for the current Git branch. It then outputs a formatted status line to the console, useful for displaying contextual information in a terminal.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/statusline

LANGUAGE: Node.js
CODE:
```
#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Read JSON from stdin
let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
    const data = JSON.parse(input);
    
    // Extract values
    const model = data.model.display_name;
    const currentDir = path.basename(data.workspace.current_dir);
    
    // Check for git branch
    let gitBranch = '';
    try {
        const headContent = fs.readFileSync('.git/HEAD', 'utf8').trim();
        if (headContent.startsWith('ref: refs/heads/')) {
            gitBranch = ` | 🌿 ${headContent.replace('ref: refs/heads/', '')}`;
        }
    } catch (e) {
        // Not a git repo or can't read HEAD
    }
    
    console.log(`[${model}] 📁 ${currentDir}${gitBranch}`);
});
```

----------------------------------------

TITLE: Configure Claude Code for Google Vertex AI with Corporate Proxy
DESCRIPTION: This configuration enables Claude Code to use Google Vertex AI models, routing all traffic through a specified corporate HTTP/HTTPS proxy. It requires setting the Vertex AI region and project ID, along with the proxy address via environment variables.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/bedrock-vertex-proxies

LANGUAGE: Shell
CODE:
```
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

export HTTPS_PROXY='https://proxy.example.com:8080'
```

----------------------------------------

TITLE: Control Tool Execution with PreToolUse Hook Decisions
DESCRIPTION: The `PreToolUse` hook allows controlling whether a tool call proceeds using the `permissionDecision` field within `hookSpecificOutput`. Options include `allow` (bypasses permission system), `deny` (prevents execution), or `ask` (prompts user for confirmation). A `permissionDecisionReason` can be provided to explain the decision.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: JSON
CODE:
```
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow" | "deny" | "ask",
    "permissionDecisionReason": "My reason here"
  }
}
```

----------------------------------------

TITLE: Set Timeouts for Claude CLI Operations
DESCRIPTION: This snippet shows how to use the `timeout` command to limit the execution time of `claude` CLI operations. This is useful for preventing long-running processes and providing immediate feedback if a complex prompt takes too long to process.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless

LANGUAGE: bash
CODE:
```
timeout 300 claude -p "$complex_prompt" || echo "Timed out after 5 minutes"
```

----------------------------------------

TITLE: Configure AWS Credential Export Script for Claude Code
DESCRIPTION: Defines a custom script that outputs AWS credentials in JSON format, used for advanced credential configuration.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: Shell
CODE:
```
/bin/generate_aws_grant.sh
```

----------------------------------------

TITLE: Configure Claude Code Environment Variables for Vertex AI Integration
DESCRIPTION: These environment variables configure Claude Code to use Vertex AI, specify the Vertex AI project ID, and optionally disable prompt caching. It also allows overriding default regions for specific Claude models when using Vertex AI, which is crucial for models not supported globally or in certain regions.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai

LANGUAGE: Bash
CODE:
```
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1

# When CLOUD_ML_REGION=global, override region for unsupported models
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5

# Optional: Override regions for other specific models
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1
export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west1
```

----------------------------------------

TITLE: Configure Claude Code Model in Settings File
DESCRIPTION: Illustrates how to permanently configure the Claude Code model by specifying the `model` field in the settings JSON file.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/model-config

LANGUAGE: JSON
CODE:
```
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

----------------------------------------

TITLE: Common JSON Fields for Claude Code Hook Input
DESCRIPTION: This JSON structure defines the common fields available to all Claude Code hooks, including session ID, transcript path, current working directory, and the specific hook event name. These fields provide context about the current Claude Code session.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: json
CODE:
```
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "hook_event_name": "string",
  "...": ""
}
```

----------------------------------------

TITLE: Refactor Code with Claude Code
DESCRIPTION: Employ Claude Code to update legacy code to modern patterns and practices. Identify deprecated API usage, request refactoring recommendations, and apply changes safely while maintaining behavior. It's recommended to perform refactoring in small, testable increments and verify changes.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: Claude Code CLI
CODE:
```
> find deprecated API usage in our codebase
```

LANGUAGE: Claude Code CLI
CODE:
```
> suggest how to refactor utils.js to use modern JavaScript features
```

LANGUAGE: Claude Code CLI
CODE:
```
> refactor utils.js to use ES2024 features while maintaining the same behavior
```

LANGUAGE: Claude Code CLI
CODE:
```
> run tests for the refactored code
```

----------------------------------------

TITLE: Add HubSpot Integration to Claude MCP
DESCRIPTION: Access and manage HubSpot CRM data by fetching contacts, companies, and deals, and creating and updating records.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
claude mcp add --transport http hubspot https://mcp.hubspot.com/anthropic
```

----------------------------------------

TITLE: Using Positional Arguments ($1, $2, etc.) in Commands
DESCRIPTION: Explains how to access specific arguments individually using positional parameters like `$1`, `$2`, etc., similar to shell scripts. This method is ideal for structured commands where arguments have specific roles or when providing defaults for missing parameters.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/slash-commands

LANGUAGE: Bash
CODE:
```
# Command definition  
echo 'Review PR #$1 with priority $2 and assign to $3' > .claude/commands/review-pr.md
```

LANGUAGE: CLI
CODE:
```
# Usage
> /review-pr 456 high alice
# $1 becomes "456", $2 becomes "high", $3 becomes "alice"
```

----------------------------------------

TITLE: Resume Claude Code Conversations
DESCRIPTION: This section details how to resume previous Claude Code conversations using the CLI. It covers options for automatically continuing the most recent conversation or interactively selecting a past conversation from a list, and also demonstrates non-interactive mode for scripting.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: Shell
CODE:
```
claude --continue
```

LANGUAGE: Shell
CODE:
```
claude --continue --print "Continue with my task"
```

LANGUAGE: Shell
CODE:
```
claude --resume
```

LANGUAGE: Shell
CODE:
```
# Continue most recent conversation
claude --continue

# Continue most recent conversation with a specific prompt
claude --continue --print "Show me our progress"

# Show conversation picker
claude --resume

# Continue most recent conversation in non-interactive mode
claude --continue --print "Run the tests again"
```

----------------------------------------

TITLE: Set AWS Credentials via Environment Variables for Claude Code
DESCRIPTION: Illustrates how to provide AWS access keys and session tokens directly through environment variables. These variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`) are recognized by Claude Code for authenticating with Amazon Bedrock.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock

LANGUAGE: Shell
CODE:
```
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

----------------------------------------

TITLE: Manage Parallel Claude Code Sessions with Git Worktrees
DESCRIPTION: Learn how to leverage Git worktrees to create isolated development environments, enabling you to run multiple Claude Code instances simultaneously without interference. This is ideal for working on different tasks or branches concurrently while sharing the same Git history.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/common-workflows

LANGUAGE: Shell
CODE:
```
# Create a new worktree with a new branch 
git worktree add ../project-feature-a -b feature-a

# Or create a worktree with an existing branch
git worktree add ../project-bugfix bugfix-123
```

LANGUAGE: Shell
CODE:
```
# Navigate to your worktree 
cd ../project-feature-a

# Run Claude Code in this isolated environment
claude
```

LANGUAGE: Shell
CODE:
```
cd ../project-bugfix
claude
```

LANGUAGE: Shell
CODE:
```
# List all worktrees
git worktree list

# Remove a worktree when done
git worktree remove ../project-feature-a
```

----------------------------------------

TITLE: Ensure Type Safety for Custom Tools using Zod Schemas in Claude
DESCRIPTION: This snippet illustrates how the `tool` helper function leverages Zod schemas to provide full TypeScript type inference for tool arguments. It ensures both runtime validation and compile-time type safety when processing structured data, making tool development more robust.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: TypeScript
CODE:
```
tool(
  "process_data",
  "Process structured data with type safety",
  {
    // Zod schema defines both runtime validation and TypeScript types
    data: z.object({
      name: z.string(),
      age: z.number().min(0).max(150),
      email: z.string().email(),
      preferences: z.array(z.string()).optional()
    }),
    format: z.enum(["json", "csv", "xml"]).default("json")
  },
  async (args) => {
    // args is fully typed based on the schema
    // TypeScript knows: args.data.name is string, args.data.age is number, etc.
    console.log(`Processing ${args.data.name}'s data as ${args.format}`);
    
    // Your processing logic here
    return {
      content: [{
        type: "text",
        text: `Processed data for ${args.data.name}`
      }]
    };
  }
)
```

----------------------------------------

TITLE: Access Structured JSON Output from Claude Code Query (JavaScript)
DESCRIPTION: This snippet demonstrates how to collect all messages from a Claude Code query and access specific metadata like cost and duration from the result message. It shows how to iterate through the query messages, store them in an array, and then find the "result" message to extract its content along with `total_cost_usd` and `duration_ms` for programmatic use.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: JavaScript
CODE:
```
// Collect all messages for JSON-like access
const messages = [];
for await (const message of query({
  prompt: "How does the data layer work?"
})) {
  messages.push(message);
}

// Access result message with metadata
const result = messages.find(m => m.type === "result");
console.log({
  result: result.result,
  cost: result.total_cost_usd,
  duration: result.duration_ms
});
```

----------------------------------------

TITLE: Load most recent Claude Code conversation
DESCRIPTION: Automatically loads the most recently active conversation associated with the current working directory.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude --continue
```

----------------------------------------

TITLE: Adjust Claude MCP Output Token Limit
DESCRIPTION: Control the maximum allowed output tokens for MCP tools to prevent overwhelming your conversation context. This snippet demonstrates how to increase the `MAX_MCP_OUTPUT_TOKENS` environment variable, which is useful for servers producing large datasets, reports, or log files.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/mcp

LANGUAGE: Shell
CODE:
```
# Set a higher limit for MCP tool outputs
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

----------------------------------------

TITLE: Set Claude Code model for current session
DESCRIPTION: Specifies the AI model to be used for the current session, either by an alias (e.g., `sonnet`, `opus`) or its full name.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude --model claude-sonnet-4-20250514
```

----------------------------------------

TITLE: Define Claude Code SDK Message Schema
DESCRIPTION: This TypeScript type definition outlines the structure of messages returned from the Anthropic Claude Code JSON API. It details various message types such as 'assistant', 'user', 'result' (for success or error), and 'system' (for initialization), providing a comprehensive schema for API response parsing.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript

LANGUAGE: TypeScript
CODE:
```
type SDKMessage =
  // An assistant message
  | {
      type: "assistant";
      uuid: string;
      session_id: string;
      message: Message; // from Anthropic SDK
      parent_tool_use_id: string | null;
    }

  // A user message (input)
  | {
      type: "user";
      uuid?: string;
      session_id: string;
      message: MessageParam; // from Anthropic SDK
      parent_tool_use_id: string | null;
    }

  // A user message (output/replay with required UUID)
  | {
      type: "user";
      uuid: string;
      session_id: string;
      message: MessageParam; // from Anthropic SDK
      parent_tool_use_id: string | null;
    }

  // Emitted as the last message on success
  | {
      type: "result";
      subtype: "success";
      uuid: UUID;
      session_id: string;
      duration_ms: number;
      duration_api_ms: number;
      is_error: boolean;
      num_turns: number;
      result: string;
      total_cost_usd: number;
      usage: Usage;
      permission_denials: SDKPermissionDenial[];
    }

  // Emitted as the last message on error or max turns
  | {
      type: "result";
      subtype: "error_max_turns" | "error_during_execution";
      uuid: UUID;
      session_id: string;
      duration_ms: number;
      duration_api_ms: number;
      is_error: boolean;
      num_turns: number;
      total_cost_usd: number;
      usage: Usage;
      permission_denials: SDKPermissionDenial[];
    }

  // Emitted as the first message at the start of a conversation
  | {
      type: "system";
      subtype: "init";
      uuid: UUID;
      session_id: string;
      apiKeySource: "user" | "project" | "org" | "temporary";
      cwd: string;
      tools: string[];
      mcp_servers: {
        name: string;
        status: string;
      }[];
      model: string;
      permissionMode: "default" | "acceptEdits" | "bypassPermissions" | "plan";
      slash_commands: string[];
      output_style: string;
    };

  type SDKPermissionDenial = {
    tool_name: string;
    tool_use_id: string;
    tool_input: Record<string, unknown>;
  }
```

----------------------------------------

TITLE: Manage User Prompt Processing with UserPromptSubmit Hook
DESCRIPTION: The `UserPromptSubmit` hook controls whether a user's prompt is processed. Setting `decision` to `block` prevents processing and erases the prompt, showing the `reason` to the user. Alternatively, `hookSpecificOutput.additionalContext` can inject a string into Claude's context if the prompt is not blocked.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: JSON
CODE:
```
{
  "decision": "block" | undefined,
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

----------------------------------------

TITLE: Specify Claude Code input format for print mode
DESCRIPTION: Defines the expected format of the input when using print mode, with options like `text` or `stream-json`.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude -p --output-format json --input-format stream-json
```

----------------------------------------

TITLE: Print Claude Code response without interactive mode
DESCRIPTION: Outputs Claude Code's response directly to the console without entering an interactive session, useful for scripting.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude -p "query"
```

----------------------------------------

TITLE: Configure AWS SSO Profile for Claude Code Bedrock Authentication
DESCRIPTION: Demonstrates how to log in using an AWS SSO profile and then set the `AWS_PROFILE` environment variable. This configuration allows Claude Code to utilize the SSO-managed credentials for Bedrock access.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock

LANGUAGE: Shell
CODE:
```
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

----------------------------------------

TITLE: Authenticate Claude Code with Bedrock API Key
DESCRIPTION: Shows a simpler authentication method for Claude Code by setting the `AWS_BEARER_TOKEN_BEDROCK` environment variable. This variable should contain your Bedrock API key, bypassing the need for full AWS credentials.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock

LANGUAGE: Shell
CODE:
```
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

----------------------------------------

TITLE: Configure Claude Code for Amazon Bedrock with Corporate Proxy
DESCRIPTION: This configuration enables Claude Code to use Amazon Bedrock models, routing all traffic through a specified corporate HTTP/HTTPS proxy. It requires setting the AWS region and the proxy address via environment variables.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/bedrock-vertex-proxies

LANGUAGE: Shell
CODE:
```
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

export HTTPS_PROXY='https://proxy.example.com:8080'
```

----------------------------------------

TITLE: Configure AWS Authentication Refresh Script for Claude Code
DESCRIPTION: Defines a custom script that modifies the `.aws` directory, used for advanced credential configuration such as AWS SSO login.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/settings

LANGUAGE: Shell
CODE:
```
aws sso login --profile myprofile
```

----------------------------------------

TITLE: Specify Claude Code output format for print mode
DESCRIPTION: Defines the format of the output when using print mode, with options like `text`, `json`, or `stream-json`.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude -p "query" --output-format json
```

----------------------------------------

TITLE: Customize Default Claude Models for Vertex AI
DESCRIPTION: These environment variables allow you to override the default primary and small/fast Claude models used by Claude Code when integrated with Vertex AI. This enables the use of specific model versions or different models based on your application's requirements, such as a newer opus model or a specific haiku version.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai

LANGUAGE: Bash
CODE:
```
export ANTHROPIC_MODEL='claude-opus-4-1@20250805'
export ANTHROPIC_SMALL_FAST_MODEL='claude-3-5-haiku@20241022'
```

----------------------------------------

TITLE: Configure AWS Region for Claude Code Haiku Model
DESCRIPTION: This snippet demonstrates how to explicitly set the AWS region for the small and fast Claude model (Haiku) used by Claude Code. It uses an environment variable to override the default region, ensuring the model operates from a specified AWS location.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock

LANGUAGE: bash
CODE:
```
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2
```

----------------------------------------

TITLE: Control Claude's Stopping Behavior with Stop/SubagentStop Hooks
DESCRIPTION: The `Stop` and `SubagentStop` hooks allow preventing Claude from stopping. By setting `decision` to `block`, Claude is forced to continue, and a `reason` must be provided to inform Claude how to proceed. If `decision` is `undefined`, Claude is allowed to stop.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: JSON
CODE:
```
{
  "decision": "block" | undefined,
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

----------------------------------------

TITLE: Define IAM Policy for Claude Code Bedrock API Access
DESCRIPTION: This JSON snippet provides a standard IAM policy required for Claude Code to interact with Amazon Bedrock. It grants permissions to invoke models and list inference profiles, ensuring Claude Code has the necessary access to Bedrock services.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock

LANGUAGE: json
CODE:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*"
      ]
    }
  ]
}
```

----------------------------------------

TITLE: Define Custom AWS Credential Export Command for Claude Code
DESCRIPTION: Outlines the required JSON format for the output of a custom `awsCredentialExport` command. Claude Code uses this command to silently capture and refresh AWS credentials when direct modification of the `.aws` directory is not possible.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock

LANGUAGE: JSON
CODE:
```
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

----------------------------------------

TITLE: Configure Claude Hook Behavior with Common JSON Fields
DESCRIPTION: This JSON structure defines optional fields that can be included in the stdout of any Claude hook to control its subsequent behavior. It allows specifying whether Claude should continue processing, providing a reason for stopping, suppressing output from the transcript, and including a system message for the user.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: JSON
CODE:
```
{
  "continue": true, // Whether Claude should continue after hook execution (default: true)
  "stopReason": "string", // Message shown when continue is false

  "suppressOutput": true, // Hide stdout from transcript mode (default: false)
  "systemMessage": "string" // Optional warning message shown to the user
}
```

----------------------------------------

TITLE: Troubleshoot Bedrock Region Issues by Switching AWS Region
DESCRIPTION: This command demonstrates how to temporarily switch the active AWS region using an environment variable. It is a useful step for troubleshooting connectivity or model availability issues when working with Amazon Bedrock services.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock

LANGUAGE: bash
CODE:
```
export AWS_REGION=us-east-1
```

----------------------------------------

TITLE: Validate Bash Commands with Python Exit Code Hook
DESCRIPTION: This Python script acts as a hook to validate Bash commands before execution. It defines a set of regular expression rules to identify and flag problematic commands, such as using `grep` instead of `rg` or `find -name` instead of `rg --files`. If validation issues are found, the script exits with code 2, blocking the tool call and displaying the error messages to Claude.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/hooks

LANGUAGE: python
CODE:
```
#!/usr/bin/env python3
import json
import re
import sys

# Define validation rules as a list of (regex pattern, message) tuples
VALIDATION_RULES = [
    (
        r"\bgrep\b(?!.*\|)",
        "Use 'rg' (ripgrep) instead of 'grep' for better performance and features",
    ),
    (
        r"\bfind\s+\S+\s+-name\b",
        "Use 'rg --files | rg pattern' or 'rg --files -g pattern' instead of 'find -name' for better performance",
    ),
]


def validate_command(command: str) -> list[str]:
    issues = []
    for pattern, message in VALIDATION_RULES:
        if re.search(pattern, command):
            issues.append(message)
    return issues


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
command = tool_input.get("command", "")

if tool_name != "Bash" or not command:
    sys.exit(1)

# Validate the command
issues = validate_command(command)

if issues:
    for message in issues:
        print(f"\u2022 {message}", file=sys.stderr)
    # Exit code 2 blocks tool call and shows stderr to Claude
    sys.exit(2)
```

----------------------------------------

TITLE: Define Data Scientist Subagent in YAML
DESCRIPTION: This snippet defines a 'data-scientist' subagent, an AI expert specializing in SQL and BigQuery analysis. It outlines the subagent's capabilities, including writing efficient SQL queries, using BigQuery tools, analyzing results, and presenting findings, along with key practices for optimized data analysis.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/sub-agents

LANGUAGE: YAML
CODE:
```
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

----------------------------------------

TITLE: Limit agentic turns in non-interactive mode
DESCRIPTION: Sets a maximum number of agentic turns Claude Code can take when operating in non-interactive (print) mode.

SOURCE: https://docs.anthropic.com/en/docs/claude-code/cli-reference

LANGUAGE: Shell
CODE:
```
claude -p --max-turns 3 "query"
```