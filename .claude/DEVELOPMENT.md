# Development Guide

Guide for contributing to claude-rules, testing commands, and following best practices.

## Contributing

### Getting Started

1. **Fork and Clone:**
   ```bash
   git fork https://github.com/qdhenry/Claude-Command-Suite.git
   git clone <your-fork-url>
   cd Claude-Command-Suite
   ```

2. **Set Up Development Environment:**
   ```bash
   # Install using symlink for development
   ./install.sh --symlink

   # This creates a symbolic link so changes are immediately available
   ```

3. **Create a Feature Branch:**
   ```bash
   git checkout -b feature/new-command-name
   ```

### Development Workflow

1. **Create or Modify Commands:**
   - Add new `.md` files to `.claude/commands/`
   - Follow the established naming convention
   - Use the standard command structure

2. **Test Your Changes:**
   ```bash
   # Test command recognition
   claude code
   # Type / to see if your command appears

   # Test command execution
   /project:your-new-command
   ```

3. **Validate Command Format:**
   ```bash
   # Check markdown syntax
   markdownlint .claude/commands/your-command.md

   # Verify file structure
   head -n 10 .claude/commands/your-command.md
   ```

## Testing Commands

### Manual Testing

1. **Test Command Recognition:**
   ```bash
   # Start Claude Code
   claude code

   # Verify command appears in slash command list
   # Type / and look for /project:your-command
   ```

2. **Test Command Execution:**
   ```bash
   # Test with different argument types
   /project:your-command
   /project:your-command simple-argument
   /project:your-command "complex argument with spaces"
   ```

3. **Test Different Project Types:**
   ```bash
   # Test in various project structures
   cd javascript-project && claude code
   cd python-project && claude code
   cd rust-project && claude code
   ```

### Testing Checklist

For each command, verify:

- [ ] Command appears in slash command autocomplete
- [ ] Command executes without errors
- [ ] Command produces expected output
- [ ] Command handles arguments correctly
- [ ] Command works across different project types
- [ ] Command follows established patterns
- [ ] Command includes appropriate error handling

### Integration Testing

1. **Test Command Sequences:**
   ```bash
   # Test typical workflows
   /project:code-review
   /project:create-feature test-feature
   /project:security-audit
   ```

2. **Test with Real Projects:**
   ```bash
   # Test on actual codebases
   cd ~/real-project
   /project:your-command
   ```

3. **Test Error Conditions:**
   ```bash
   # Test with invalid arguments
   /project:your-command invalid-arg-format

   # Test in empty directories
   mkdir empty-dir && cd empty-dir
   /project:your-command
   ```

## Command Development Best Practices

### 1. Follow Naming Conventions

```bash
# Good command names
architecture-review.md
create-feature.md
security-audit.md

# Avoid
arch_review.md
CreateFeature.md
security_and_performance_audit.md
```

### 2. Use Standard Structure

```markdown
# Command Name

Brief, clear description of what the command does.

## Instructions

1. **Descriptive Step Category**
   - Specific, actionable items
   - Use tools and best practices
   - Include quality checkpoints

2. **Next Logical Step**
   - Continue the workflow
   - Validate previous steps
   - Prepare for next phase
```

### 3. Make Commands Robust

```markdown
## Instructions

1. **Environment Validation**
   - Check that required tools are available
   - Verify project structure is appropriate
   - Validate any prerequisites

2. **Error Handling**
   - Provide clear error messages
   - Suggest fixes for common issues
   - Gracefully handle edge cases
```

### 4. Include Context

```markdown
1. **Project Analysis**
   - Examine project structure and technology stack
   - Review existing documentation
   - Understand project goals and constraints
   - Adapt approach based on project characteristics
```

### 5. Be Language Agnostic

```markdown
# Good: Adaptable approach
1. **Code Quality Analysis**
   - Use appropriate linting tools for the project language
   - Check for language-specific best practices
   - Review dependency management

# Avoid: Language-specific assumptions
1. **JavaScript Analysis**
   - Run ESLint on all files
   - Check package.json dependencies
```

## Quality Standards

### Command Quality Checklist

- [ ] **Clear Purpose**: Command has a single, well-defined purpose
- [ ] **Comprehensive Instructions**: Step-by-step workflow is complete
- [ ] **Proper Structure**: Follows standard markdown format
- [ ] **Error Handling**: Includes validation and error recovery
- [ ] **Documentation**: Instructions are clear and actionable
- [ ] **Flexibility**: Works across different project types
- [ ] **Consistency**: Matches patterns from other commands

### Documentation Standards

1. **Command Descriptions:**
   - One clear sentence explaining the purpose
   - Avoid jargon and technical complexity
   - Focus on the outcome, not the process

2. **Instruction Steps:**
   - Use action verbs (analyze, create, verify, etc.)
   - Include expected outcomes
   - Provide context for decision-making

3. **Examples:**
   - Include concrete examples where helpful
   - Show both simple and complex usage
   - Demonstrate error handling

## Release Process

### 1. Code Review

1. **Self Review:**
   ```bash
   # Check your changes
   git diff main...your-branch

   # Test thoroughly
   ./test-commands.sh  # If available
   ```

2. **Peer Review:**
   - Submit pull request with clear description
   - Include testing steps and examples
   - Address all feedback

### 2. Documentation Updates

1. **Update README.md:**
   - Add new commands to the list
   - Update examples if needed
   - Maintain consistency with existing docs

2. **Update Installation Guide:**
   - Note any new requirements
   - Update troubleshooting if needed

### 3. Version Management

```bash
# Tag releases
git tag -a v1.2.0 -m "Add new debugging commands"
git push origin v1.2.0
```

## Advanced Development

### Creating Command Categories

When adding many related commands:

```bash
# Group related commands
.claude/commands/
├── analysis/
│   ├── architecture-review.md
│   ├── code-review.md
│   └── security-audit.md
├── development/
│   ├── create-feature.md
│   ├── fix-issue.md
│   └── refactor-code.md
```

### Template Commands

Create templates for common patterns:

```bash
# Create template for new analysis commands
cp .claude/commands/code-review.md .claude/commands/_analysis-template.md
# Edit to create generic analysis pattern
```

### Automated Testing

```bash
#!/bin/bash
# test-commands.sh - Basic command validation

echo "Testing command file formats..."
for cmd in .claude/commands/*.md; do
    # Check file starts with proper header
    if ! head -n 1 "$cmd" | grep -q "^# "; then
        echo "ERROR: $cmd doesn't start with proper header"
        exit 1
    fi

    # Check for Instructions section
    if ! grep -q "^## Instructions" "$cmd"; then
        echo "ERROR: $cmd missing Instructions section"
        exit 1
    fi
done

echo "All command files validated successfully!"
```

## Debugging Commands

### Common Issues

1. **Command Not Recognized:**
   ```bash
   # Check file permissions
   ls -la .claude/commands/

   # Verify markdown format
   head -n 5 .claude/commands/problematic-command.md
   ```

2. **Command Execution Errors:**
   ```bash
   # Enable Claude Code debug mode
   export CLAUDE_DEBUG=1
   claude code
   ```

3. **Argument Processing Issues:**
   ```markdown
   # Debug argument handling
   ## Instructions

   1. **Debug Arguments**
      - Print received arguments: "$ARGUMENTS"
      - Validate argument format
      - Handle empty or malformed arguments
   ```

### Logging and Debugging

```markdown
## Instructions

1. **Debug Information**
   - Current working directory: `pwd`
   - Git status: `git status --porcelain`
   - Available tools: Check for required dependencies
   - Environment: List relevant environment variables

2. **Execution Logging**
   - Log each major step completion
   - Save intermediate results
   - Record any errors or warnings encountered
```

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and improve
- Follow established patterns and conventions

### Contribution Types

1. **New Commands**: Add workflows for common development tasks
2. **Command Improvements**: Enhance existing commands with better practices
3. **Documentation**: Improve guides and examples
4. **Testing**: Add test cases and validation tools
5. **Bug Fixes**: Resolve issues with existing commands

### Getting Help

- Review existing commands for patterns
- Check GitHub issues for known problems
- Ask questions in discussions
- Provide detailed context when reporting issues

---

This development guide ensures consistent, high-quality contributions to the claude-rules project while maintaining the usability and reliability that users expect.
