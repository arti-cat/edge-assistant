# Setup Python Environment

Setup complete Python development environment optimized for uv and modern Python workflows

## Instructions

1. **Environment Analysis and Requirements**
   - Analyze current project structure and Python requirements
   - Identify required Python version and dependencies
   - Check existing Python environment configuration
   - Determine team size and collaboration requirements
   - Assess platform requirements (Windows, macOS, Linux)

2. **Python Runtime and Package Manager Setup**
   - Install or verify Python installation (3.8+ recommended)
   - Install uv package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Configure uv settings and global configuration
   - Set up Python version management with uv
   - Configure virtual environment settings
   - Verify uv installation: `uv --version`

3. **Project Environment Configuration**
   - Initialize uv project if not exists: `uv init`
   - Create or update pyproject.toml with project metadata
   - Set up Python version pinning with .python-version
   - Configure dependency groups (dev, test, docs, etc.)
   - Set up virtual environment: `uv venv`
   - Install project dependencies: `uv sync`

4. **Development Tools Installation**
   - Install ruff for linting and formatting: `uv add --dev ruff`
   - Set up type checking with mypy: `uv add --dev mypy`
   - Install pytest for testing: `uv add --dev pytest`
   - Add debugging tools: `uv add --dev ipdb pdb++`
   - Configure IDE extensions and Python language server
   - Set up import sorting and organization tools

5. **Code Quality and Standards**
   - Configure ruff linting rules in pyproject.toml
   - Set up ruff formatting configuration
   - Configure mypy type checking rules
   - Set up pre-commit hooks with pre-commit: `uv add --dev pre-commit`
   - Configure code coverage tools: `uv add --dev pytest-cov`
   - Set up security scanning: `uv add --dev bandit`

6. **Development Server and Database**
   - Set up local development server configuration
   - Configure database connections and ORM setup
   - Set up containerized development environment with Docker
   - Configure API testing tools: `uv add --dev httpx pytest-httpx`
   - Set up environment variable management with python-dotenv
   - Configure logging and debugging tools

7. **IDE and Editor Configuration**
   - Configure VSCode settings for Python development
   - Set up Python interpreter path for IDE
   - Configure IntelliSense and auto-completion
   - Set up debugging configurations and breakpoints
   - Configure integrated terminal with uv commands
   - Set up code snippets and templates for Python

8. **Environment Variables and Secrets**
   - Create .env template files for different environments
   - Set up local environment variable management
   - Configure secrets management for development
   - Set up API keys and service credentials securely
   - Configure environment-specific configuration files
   - Document required environment variables in README

9. **Documentation and Knowledge Base**
   - Create comprehensive setup documentation
   - Document common Python development workflows
   - Set up project documentation with mkdocs or sphinx
   - Create troubleshooting guides for common Python issues
   - Document coding standards and Python best practices
   - Set up onboarding checklist for new Python developers

10. **Validation and Testing**
    - Verify Python version and uv installation
    - Test virtual environment activation and deactivation
    - Validate dependency installation and resolution
    - Test development server startup and hot reloading
    - Verify code quality tools are working correctly
    - Test import resolution and package discovery
    - Create Python environment health check script: `uv run python -c "import sys; print(f'Python {sys.version} ready!')"`
