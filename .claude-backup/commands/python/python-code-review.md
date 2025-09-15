# Python Code Quality Review

Perform comprehensive Python code quality review with focus on modern Python practices

## Instructions

Follow these steps to conduct a thorough Python code review:

1. **Python Project Analysis**
   - Examine the repository structure and identify Python version and framework
   - Check for configuration files (pyproject.toml, requirements.txt, setup.py, etc.)
   - Review README and documentation for context
   - Identify package manager (pip, poetry, uv, pipenv)
   - Check for virtual environment setup and dependency management

2. **Code Quality Assessment**
   - Scan for Python-specific code smells and anti-patterns
   - Check PEP 8 compliance and consistent coding style
   - Identify unused imports, variables, or dead code
   - Review error handling and exception management
   - Check for proper use of Python idioms and best practices
   - Verify proper use of type hints and annotations

3. **Security Review**
   - Look for common Python security vulnerabilities
   - Check for hardcoded secrets, API keys, or passwords
   - Review authentication and authorization logic
   - Examine input validation and sanitization
   - Check for SQL injection vulnerabilities in database queries
   - Review pickle usage and deserialization security
   - Analyze dependency vulnerabilities with security scanning

4. **Performance Analysis**
   - Identify potential performance bottlenecks in Python code
   - Check for inefficient algorithms or database queries
   - Review memory usage patterns and potential leaks
   - Analyze import performance and module loading
   - Check for proper use of generators and iterators
   - Review async/await usage and coroutine performance

5. **Architecture & Design**
   - Evaluate code organization and module structure
   - Check for proper abstraction and modularity
   - Review dependency management and coupling
   - Assess scalability and maintainability
   - Check for proper use of design patterns
   - Review package and module organization

6. **Python-Specific Best Practices**
   - Check for proper use of context managers (with statements)
   - Review string formatting and f-string usage
   - Verify proper use of list/dict comprehensions
   - Check for appropriate use of built-in functions
   - Review exception handling patterns
   - Assess logging configuration and usage

7. **Testing Coverage**
   - Check existing test coverage with pytest
   - Identify areas lacking proper testing
   - Review test structure and organization
   - Suggest additional test scenarios
   - Check for proper use of fixtures and mocking
   - Review integration and unit test balance

8. **Documentation Review**
   - Evaluate docstrings and inline documentation
   - Check API documentation completeness
   - Review README and setup instructions
   - Identify areas needing better documentation
   - Check for proper type annotations
   - Review code comments for clarity

9. **Dependency Management**
   - Review dependency versions and compatibility
   - Check for outdated or vulnerable dependencies
   - Assess dependency tree and potential conflicts
   - Review dev vs production dependency separation
   - Check for proper virtual environment usage

10. **Tool Integration**
    - Check for linting tool configuration (ruff, flake8, pylint)
    - Review formatting tool setup (black, autopep8)
    - Verify type checking configuration (mypy, pyright)
    - Check for pre-commit hooks and CI/CD integration
    - Review code quality metrics and reporting

11. **Framework-Specific Review**
    - **Django**: Check models, views, templates, and settings
    - **Flask**: Review blueprints, routes, and middleware
    - **FastAPI**: Check endpoints, models, and async patterns
    - **CLI Tools**: Review argument parsing and error handling
    - **Data Science**: Check pandas usage, numpy operations, and visualization

12. **Recommendations**
    - Prioritize issues by severity (critical, high, medium, low)
    - Provide specific, actionable recommendations with Python examples
    - Suggest modern Python tools and practices for improvement
    - Create a summary report with next steps
    - Include refactoring suggestions with code examples

Remember to be constructive and provide specific examples with file paths and line numbers where applicable. Focus on modern Python practices and tools like uv, ruff, and pytest.
