# Setup Python Testing

Setup comprehensive Python testing infrastructure with pytest and modern testing tools

## Instructions

1. **Testing Strategy Analysis**
   - Analyze current project structure and identify testing needs
   - Determine appropriate testing frameworks for Python ecosystem
   - Define testing pyramid strategy (unit, integration, e2e)
   - Plan test coverage goals and quality metrics
   - Assess existing testing infrastructure and gaps

2. **Core Testing Framework Setup**
   - Install pytest and essential plugins: `uv add --dev pytest pytest-cov pytest-asyncio`
   - Configure pytest in pyproject.toml:
   ```toml
   [tool.pytest.ini_options]
   testpaths = ["tests"]
   python_files = ["test_*.py", "*_test.py"]
   python_classes = ["Test*"]
   python_functions = ["test_*"]
   addopts = "-v --tb=short --strict-markers"
   markers = [
       "slow: marks tests as slow",
       "integration: marks tests as integration tests",
       "unit: marks tests as unit tests",
   ]
   ```

3. **Test Directory Structure**
   - Create comprehensive test directory structure:
   ```
   tests/
   ├── conftest.py
   ├── unit/
   │   ├── __init__.py
   │   └── test_core.py
   ├── integration/
   │   ├── __init__.py
   │   └── test_api.py
   └── fixtures/
       ├── __init__.py
       └── sample_data.py
   ```

4. **Advanced Testing Plugins**
   - Install pytest plugins for enhanced functionality:
   ```bash
   uv add --dev pytest-mock pytest-django pytest-asyncio pytest-xdist
   uv add --dev pytest-benchmark pytest-timeout pytest-sugar
   ```
   - Configure parallel test execution
   - Set up test mocking and fixtures
   - Configure async testing support

5. **Test Coverage Configuration**
   - Configure coverage reporting in pyproject.toml:
   ```toml
   [tool.coverage.run]
   source = ["src"]
   omit = ["tests/*", "*/migrations/*", "*/venv/*"]
   branch = true

   [tool.coverage.report]
   exclude_lines = [
       "pragma: no cover",
       "def __repr__",
       "raise AssertionError",
       "raise NotImplementedError",
   ]
   show_missing = true
   skip_covered = false
   ```

6. **Property-Based Testing**
   - Install hypothesis for property-based testing: `uv add --dev hypothesis`
   - Configure hypothesis settings:
   ```toml
   [tool.hypothesis]
   max_examples = 1000
   deadline = 5000
   derandomize = true
   ```
   - Set up property-based test examples

7. **Database and API Testing**
   - Install testing dependencies for databases:
   ```bash
   uv add --dev pytest-postgresql pytest-redis
   uv add --dev requests-mock httpx
   ```
   - Configure test database setup
   - Set up API testing with httpx/requests-mock
   - Configure test data factories

8. **Performance and Load Testing**
   - Install performance testing tools: `uv add --dev pytest-benchmark locust`
   - Configure benchmark testing
   - Set up load testing scenarios
   - Configure performance regression detection

9. **Test Data Management**
   - Set up test data factories and fixtures
   - Configure database seeding and cleanup
   - Set up test data isolation
   - Configure test environment data management
   - Set up API mocking and service virtualization

10. **CI/CD Integration**
    - Configure automated test execution:
    ```yaml
    - name: Run Python tests
      run: |
        uv run pytest --cov=src --cov-report=xml
        uv run pytest tests/integration --maxfail=1
    ```
    - Set up parallel test execution
    - Configure test result reporting
    - Set up coverage reporting to services like Codecov

11. **Testing Scripts and Commands**
    - Add testing scripts to pyproject.toml:
    ```toml
    [tool.uv.scripts]
    test = "pytest"
    test-unit = "pytest tests/unit"
    test-integration = "pytest tests/integration"
    test-cov = "pytest --cov=src --cov-report=html"
    test-benchmark = "pytest --benchmark-only"
    test-watch = "pytest-watch"
    ```

12. **Quality Gates and Reporting**
    - Set up test coverage thresholds
    - Configure test result visualization
    - Set up test performance monitoring
    - Configure test report generation
    - Set up automated test quality checks
    - Create testing metrics dashboard
