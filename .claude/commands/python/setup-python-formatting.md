# Setup Python Formatting

Configure modern Python code formatting with ruff format and additional tools

## Instructions

Setup Python code formatting following these steps: **$ARGUMENTS**

1. **Ruff Format Configuration**
   - Install ruff (if not already installed): `uv add --dev ruff`
   - Configure ruff formatting in pyproject.toml:
   ```toml
   [tool.ruff.format]
   quote-style = "double"
   line-ending = "auto"
   indent-style = "space"
   skip-magic-trailing-comma = false
   ```
   - Set target Python version and line length
   - Test formatting: `uv run ruff format --check .`

2. **Import Sorting and Organization**
   - Configure import sorting in ruff (replaces isort):
   ```toml
   [tool.ruff.lint.isort]
   known-first-party = ["your_package"]
   known-third-party = ["fastapi", "pydantic", "requests"]
   split-on-trailing-comma = true
   ```
   - Set up import grouping and ordering
   - Configure relative import preferences

3. **Docstring Formatting**
   - Install docformatter: `uv add --dev docformatter`
   - Configure docstring style in pyproject.toml:
   ```toml
   [tool.docformatter]
   black = true
   summary-wrap-length = 88
   description-wrap-length = 88
   ```
   - Set up numpy/google/sphinx docstring conventions

4. **Alternative Formatting Tools (Optional)**
   - Install black as alternative: `uv add --dev black`
   - Configure black in pyproject.toml:
   ```toml
   [tool.black]
   line-length = 88
   target-version = ["py38", "py39", "py310", "py311"]
   include = '\.pyi?$'
   extend-exclude = '''
   /(
     \.eggs
     | \.git
     | \.mypy_cache
     | \.tox
     | \.venv
     | _build
     | buck-out
     | build
     | dist
   )/
   '''
   ```

5. **IDE Integration**
   - Configure VS Code settings for Python formatting
   - Set up format on save functionality
   - Install Python and ruff extensions
   - Configure keyboard shortcuts for formatting commands
   - Set up auto-import organization

6. **Pre-commit Hook Setup**
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
     - repo: https://github.com/PyCQA/docformatter
       rev: v1.7.5
       hooks:
         - id: docformatter
           args: [--in-place, --black]
   ```

7. **Scripts and Commands**
   - Add formatting scripts to pyproject.toml:
   ```toml
   [tool.uv.scripts]
   format = "ruff format ."
   format-check = "ruff format --check ."
   format-imports = "ruff check --select I --fix ."
   format-docstrings = "docformatter --in-place --black ."
   format-all = ["ruff format .", "ruff check --select I --fix .", "docformatter --in-place --black ."]
   ```

8. **CI/CD Integration**
   ```yaml
   - name: Check Python formatting
     run: |
       uv run ruff format --check .
       uv run ruff check --select I .
       uv run docformatter --check --black .
   ```

9. **Team Configuration**
   - Create .editorconfig file for consistent formatting:
   ```ini
   root = true

   [*.py]
   charset = utf-8
   end_of_line = lf
   insert_final_newline = true
   trim_trailing_whitespace = true
   indent_style = space
   indent_size = 4
   max_line_length = 88
   ```

10. **Initial Codebase Formatting**
    - Run initial formatting on entire codebase: `uv run ruff format .`
    - Fix import organization: `uv run ruff check --select I --fix .`
    - Format docstrings: `uv run docformatter --in-place --black .`
    - Commit formatted code with clear message
    - Configure team IDE settings consistently
    - Create formatting guidelines documentation

Remember to run formatting on the entire codebase initially and ensure all team members have consistent IDE settings configured.
