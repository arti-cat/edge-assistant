# Claude Code Project Configuration Guide

This project uses a `.claude/` directory to configure Claude Code for repeatable, safe, and team-friendly workflows.

Use this guide as a quick reference for what lives where and how to get started.

## Directory layout

```
.claude/
  agents/             # Subagent definitions (Markdown with YAML frontmatter)
  commands/           # Reusable custom commands (Markdown with YAML frontmatter)
  output-styles/      # Output style definitions (Markdown with YAML frontmatter)
  settings.json       # Project-wide hook configuration (Claude Code hooks)
  hooks/              # Optional: scripts or utilities invoked by hooks
  scripts/            # Optional: helper scripts referenced by commands/hooks
```

- Project-level config (`.claude/*`) overrides user-level config (`~/.claude/*`).
- Prefer project-level config for team consistency; reserve user-level config for personal defaults.

## Quickstart

1) Create structure

```bash
mkdir -p .claude/{agents,commands,output-styles,hooks,scripts}
: > .claude/settings.json
```

2) Add a subagent

Create `.claude/agents/reviewer.md` (see best practices in `docs/claude/agents.md`).

3) Add a command

Create `.claude/commands/commit.md` (see `docs/claude/commands.md`).

4) Enable hooks

Edit `.claude/settings.json` (see `docs/claude/hooks.md`).

5) Choose an output style

Add a file in `.claude/output-styles/` (see `docs/claude/output-styles.md`).

## Naming conventions

- Agents: `role-scope.md` (e.g., `reviewer-auth.md`, `coder-refactor.md`)
- Commands: `verb-target.md` (e.g., `commit.md`, `review-pr.md`)
- Output styles: `purpose.md` (e.g., `explanatory.md`, `learning.md`)
- Hook scripts: `action-purpose.ext` (e.g., `format-on-write.py`, `log-bash.sh`)

## Safety and governance

- Apply least-privilege: restrict tool permissions in agents and commands.
- Protect sensitive files via PreToolUse hooks (.env, secrets, .git/).
- Prefer JSON output (`--output-format json`) for steps that need machine parsing.
- Store deterministic artifacts: prompts, outputs, diffs under a `/artifacts` directory if automating workflows.

## Best-practices docs

- Agents: `docs/claude/agents.md`
- Commands: `docs/claude/commands.md`
- Hooks: `docs/claude/hooks.md`
- Output styles: `docs/claude/output-styles.md`
