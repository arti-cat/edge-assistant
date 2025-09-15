# Python Commands

Python-specific commands optimized for modern Python development using uv for dependency management.

## Overview

This directory contains commands specifically designed for Python development workflows, leveraging:

- **uv** - Modern Python package manager and project manager
- **pyproject.toml** - Standard Python project configuration
- **ruff** - Fast Python linter and formatter
- **pytest** - Testing framework
- **Modern Python tooling** - Type checking, documentation, and more

## Available Commands

### Project Setup
- `init-python-project` - Initialize new Python project with uv and best practices
- `setup-python-environment` - Configure Python development environment
- `setup-python-monorepo` - Set up Python monorepo with uv workspaces

### Code Quality
- `setup-python-linting` - Configure ruff linting and code quality tools
- `setup-python-formatting` - Set up ruff format and code formatting
- `python-code-review` - Python-specific code review workflow

### Testing
- `setup-python-testing` - Configure pytest and testing infrastructure

### Development & Debugging
- `python-debug-setup` - Setup comprehensive debugging and development tools for Python projects

### Package Distribution
- `python-package-build` - Build and distribute Python packages using modern packaging tools

### Web Scraping & Data Collection
- `setup-scraper-project` - Initialize complete web scraping project for multi-site product monitoring
- `implement-base-scraper` - Implement core scraper architecture with BaseScraper abstract class
- `add-site-scraper` - Template and workflow for adding new site-specific scrapers
- `setup-scraper-testing` - Comprehensive testing infrastructure for web scraping projects
- `scraper-monitoring-setup` - Production monitoring for web scraping operations
- `optimize-scraper-performance` - Performance optimization for large-scale web scraping

### Security & Performance
- `python-security-hardening` - Comprehensive security hardening for Python applications
- `python-dependency-audit` - Comprehensive dependency security audit with vulnerability scanning
- `python-performance-audit` - Performance analysis for Python applications

## Key Features

### uv Integration
All commands are designed to work with uv's modern Python workflow:
- `uv add` for dependency management
- `uv run` for script execution
- `uv sync` for environment synchronization
- `uv workspace` for monorepo management

### Modern Python Tooling
Commands leverage the latest Python development tools:
- **ruff** for linting and formatting (replaces multiple tools)
- **mypy/pyright** for type checking
- **pytest** with modern plugin ecosystem
- **mkdocs/sphinx** for documentation

### Best Practices
Each command includes:
- Virtual environment management
- Proper dependency isolation
- Security considerations
- Performance optimizations
- Type safety recommendations

## Usage

Commands are used with the `/project:` prefix:

```bash
# Initialize new Python project
/project:init-python-project my-app

# Set up development environment
/project:setup-python-environment

# Configure debugging tools
/project:python-debug-setup

# Configure linting
/project:setup-python-linting

# Review Python code
/project:python-code-review

# Build and distribute Python package
/project:python-package-build my-package
```

## Configuration Files

Python commands work with these configuration files:
- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Dependency lock file
- `.python-version` - Python version specification
- `ruff.toml` - Linting and formatting configuration
- `pytest.ini` or `pyproject.toml` - Testing configuration

## Compatibility

These commands are designed for:
- Python 3.8+
- uv 0.1.0+
- Linux/macOS/Windows
- Modern Python development workflows

## Contributing

When adding new Python commands:
1. Follow the established command structure
2. Use uv for all dependency management
3. Include proper error handling
4. Test across different Python versions
5. Include security and performance considerations
