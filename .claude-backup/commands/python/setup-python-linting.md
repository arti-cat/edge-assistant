# Setup Python Linting

Setup modern Python linting with ruff and code quality tools

## Instructions

Follow this systematic approach to setup Python linting: **$ARGUMENTS**

1. **Project Analysis**
   - Identify Python version and framework requirements
   - Check existing linting configuration in pyproject.toml
   - Review current code style and patterns
   - Assess team preferences and coding standards
   - Analyze codebase size and complexity

2. **Ruff Installation and Configuration**
   - Install ruff as development dependency: `uv add --dev ruff`
   - Verify installation: `uv run ruff --version`
   - Create ruff configuration in pyproject.toml
   - Configure target Python version and line length
   - Set up include/exclude patterns for files

3. **Core Linting Configuration**
   ```toml
   [tool.ruff]
   target-version = "py38"
   line-length = 88
   select = [
       "E",  # pycodestyle errors
       "W",  # pycodestyle warnings
       "F",  # pyflakes
       "I",  # isort
       "B",  # flake8-bugbear
       "C4", # flake8-comprehensions
       "UP", # pyupgrade
   ]
   ignore = [
       "E501", # line too long, handled by formatter
       "B008", # do not perform function calls in argument defaults
   ]
   ```

4. **Advanced Linting Rules**
   - Enable security rules: `uv add --dev bandit`
   - Configure import sorting and organization
   - Set up docstring conventions (D rules)
   - Enable type checking hints (ANN rules)
   - Configure complexity and maintainability rules (C90, PLR)
   - Set up naming conventions (N rules)

5. **Type Checking Setup**
   - Install mypy: `uv add --dev mypy`
   - Configure mypy in pyproject.toml:
   ```toml
   [tool.mypy]
   python_version = "3.8"
   warn_return_any = true
   warn_unused_configs = true
   disallow_untyped_defs = true
   ```
   - Set up type checking for dependencies
   - Configure stub packages for third-party libraries

6. **IDE Integration**
   - Configure VS Code settings for ruff
   - Set up auto-fix on save
   - Install Python and ruff extensions
   - Configure IntelliSense and error highlighting
   - Set up keyboard shortcuts for linting commands

7. **Pre-commit Hook Setup**
   - Install pre-commit: `uv add --dev pre-commit`
   - Create .pre-commit-config.yaml:
   ```yaml
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.1.0
       hooks:
         - id: ruff
           args: [--fix, --exit-non-zero-on-fix]
         - id: ruff-format
     - repo: https://github.com/pre-commit/mirrors-mypy
       rev: v1.5.1
       hooks:
         - id: mypy
   ```

8. **CI/CD Integration**
   ```yaml
   - name: Lint Python code
     run: |
       uv run ruff check .
       uv run ruff format --check .
       uv run mypy src/
   ```

9. **Scripts and Commands**
   - Add linting scripts to pyproject.toml:
   ```toml
   [tool.uv.scripts]
   lint = "ruff check ."
   lint-fix = "ruff check --fix ."
   format = "ruff format ."
   format-check = "ruff format --check ."
   type-check = "mypy src/"
   ```

10. **Quality Gates and Enforcement**
    - Set up ruff configuration for different environments
    - Configure error vs warning thresholds
    - Set up code quality metrics and monitoring
    - Create linting reports and dashboards
    - Document coding standards and exceptions
    - Set up automated code quality checks

Remember to start with basic rules and gradually introduce stricter standards to avoid overwhelming the team.
