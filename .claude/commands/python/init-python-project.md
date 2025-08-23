# Initialize Python Project

Initialize new Python project with uv and modern best practices

## Instructions

1. **Project Analysis and Setup**
   - Parse the project type and framework from arguments: `$ARGUMENTS`
   - If no arguments provided, analyze current directory and ask user for project type and framework
   - Create project directory structure if needed
   - Validate that the chosen framework is appropriate for the project type

2. **Base Project Structure**
   - Initialize uv project: `uv init`
   - Create essential directories (src/, tests/, docs/, scripts/)
   - Initialize git repository with Python .gitignore
   - Create README.md with project description and setup instructions
   - Set up proper Python package structure with __init__.py files

3. **Framework-Specific Configuration**
   - **Web/FastAPI**: Set up FastAPI with async support, Pydantic models, and middleware
   - **Web/Django**: Configure Django project with proper settings and app structure
   - **Web/Flask**: Set up Flask with blueprints, extensions, and configuration
   - **CLI/Click**: Create CLI application with Click and proper command structure
   - **API/GraphQL**: Set up GraphQL with Strawberry or Ariadne
   - **Data/Jupyter**: Configure Jupyter notebooks with data science dependencies
   - **Library/Package**: Set up Python package with proper module structure for PyPI

4. **Development Environment Setup**
   - Configure pyproject.toml with project metadata and dependencies
   - Set up Python version with .python-version file
   - Configure uv dependency groups (dev, test, docs, optional)
   - Set up virtual environment: `uv venv`
   - Install development dependencies: `uv sync`

5. **Code Quality Tools**
   - Install and configure ruff for linting and formatting: `uv add --dev ruff`
   - Set up mypy for type checking: `uv add --dev mypy`
   - Configure pre-commit hooks: `uv add --dev pre-commit`
   - Add security scanning: `uv add --dev bandit`
   - Configure code coverage: `uv add --dev coverage`

6. **Testing Infrastructure**
   - Install pytest and plugins: `uv add --dev pytest pytest-cov pytest-asyncio`
   - Set up test directory structure with conftest.py
   - Configure pytest in pyproject.toml
   - Add example tests and test utilities
   - Set up test coverage reporting

7. **Build and Development Tools**
   - Configure uv scripts for common tasks
   - Set up environment variable management with python-dotenv
   - Add development server configuration
   - Configure logging and debugging tools
   - Set up hot reloading for development

8. **CI/CD Pipeline**
   - Create GitHub Actions workflow for Python testing
   - Set up automated testing across Python versions
   - Configure automated dependency updates with Dependabot
   - Add status badges to README
   - Set up automated PyPI publishing

9. **Documentation Setup**
   - Generate comprehensive README with uv installation instructions
   - Create CONTRIBUTING.md with development guidelines
   - Set up documentation with mkdocs or sphinx: `uv add --dev mkdocs`
   - Configure API documentation generation
   - Add code quality badges and shields

10. **Security and Best Practices**
    - Configure security scanning with bandit
    - Set up dependency vulnerability checking
    - Add security-focused linting rules
    - Configure environment-specific security settings
    - Set up secrets management for development

11. **Project Validation**
    - Verify uv installation and dependency resolution
    - Run initial tests to ensure testing setup works
    - Execute linting and formatting checks
    - Validate that development environment starts successfully
    - Test import resolution and package discovery
    - Create initial commit with proper project structure

12. **Project Templates by Type**

    **Web API Template:**
    ```
    src/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── api/
    │   ├── models/
    │   └── services/
    tests/
    ├── test_api.py
    └── conftest.py
    ```

    **CLI Application Template:**
    ```
    src/
    ├── cli_app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── commands/
    │   └── utils/
    tests/
    ├── test_cli.py
    └── conftest.py
    ```

    **Library Template:**
    ```
    src/
    ├── my_library/
    │   ├── __init__.py
    │   ├── core.py
    │   └── utils.py
    tests/
    ├── test_core.py
    └── conftest.py
    ```
