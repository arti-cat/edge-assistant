# Python Coverage Analysis

Advanced test coverage analysis and improvement for Python projects using coverage.py with comprehensive visualization and quality enforcement

## Instructions

Follow this systematic approach to perform advanced Python test coverage analysis and improvement: **$ARGUMENTS**

1. **Coverage Environment Setup**
   - Install coverage.py and advanced tools:
   ```bash
   uv add --dev coverage[toml] pytest-cov coverage-badge
   uv add --dev pytest-html pytest-json-report
   uv add --dev coverage-conditional-plugin diff-cover
   ```
   - Configure coverage.py with advanced options in pyproject.toml:
   ```toml
   [tool.coverage.run]
   source = ["src", "."]
   omit = [
       "tests/*",
       "*/migrations/*",
       "*/venv/*",
       "*/__pycache__/*",
       "*/site-packages/*",
       "setup.py",
       "conftest.py"
   ]
   branch = true
   data_file = ".coverage"
   parallel = true
   context = "${COVERAGE_CONTEXT}"
   dynamic_context = "test_function"

   [tool.coverage.report]
   precision = 2
   show_missing = true
   skip_covered = false
   skip_empty = false
   exclude_lines = [
       "pragma: no cover",
       "def __repr__",
       "if self.debug:",
       "if settings.DEBUG",
       "raise AssertionError",
       "raise NotImplementedError",
       "if 0:",
       "if __name__ __ == .__main__.:",
       "class .*\\bProtocol\\):",
       "@(abc\\.)?abstractmethod"
   ]
   fail_under = 85

   [tool.coverage.html]
   directory = "htmlcov"
   show_contexts = true

   [tool.coverage.xml]
   output = "coverage.xml"

   [tool.coverage.json]
   output = "coverage.json"
   show_contexts = true
   ```

2. **Advanced Coverage Configuration**
   - Set up conditional coverage exclusions:
   ```toml
   [tool.coverage.run]
   plugins = ["coverage_conditional_plugin"]

   [tool.coverage.coverage_conditional_plugin]
   rules = [
       "sys_platform == 'win32'",
       "python_version < '3.9'",
       "not TYPE_CHECKING"
   ]
   ```
   - Configure branch coverage with detailed context tracking
   - Set up parallel coverage collection for multi-process testing
   - Enable dynamic context tracking for pytest integration

3. **Baseline Coverage Analysis**
   - Run comprehensive coverage analysis:
   ```bash
   # Clean previous coverage data
   uv run coverage erase

   # Run tests with detailed coverage tracking
   uv run coverage run -m pytest tests/ --tb=short

   # Generate multiple report formats
   uv run coverage report --show-missing
   uv run coverage html --show-contexts
   uv run coverage xml
   uv run coverage json

   # Generate coverage badge
   uv run coverage-badge -o coverage.svg
   ```
   - Document baseline metrics for all coverage types
   - Identify critical coverage gaps in business logic
   - Analyze coverage distribution across modules

4. **Multi-Dimensional Coverage Analysis**
   - **Line Coverage Analysis:**
     ```bash
     uv run coverage report --show-missing --sort=cover
     ```
   - **Branch Coverage Deep Dive:**
     ```bash
     uv run coverage report --show-missing --include="**/branches.py"
     ```
   - **Function Coverage Assessment:**
     ```bash
     uv run coverage report --show-missing --skip-covered
     ```
   - **Condition Coverage Evaluation:**
     - Analyze conditional statements and boolean expressions
     - Identify uncovered truth table combinations
     - Test all logical operators and short-circuit evaluations

5. **Visual Coverage Dashboard Creation**
   - Generate enhanced HTML reports with coverage.py:
   ```bash
   uv run coverage html --show-contexts --title="Project Coverage Analysis"
   ```
   - Create coverage heatmaps and trend analysis
   - Set up interactive coverage exploration
   - Generate diff coverage for code changes:
   ```bash
   uv run diff-cover coverage.xml --compare-branch=main --html-report diff-cover.html
   ```

6. **Critical Path Coverage Assessment**
   - Identify and prioritize uncovered code paths:
     - Business-critical functions and classes
     - Error handling and exception paths
     - Security-sensitive operations
     - Public API endpoints and interfaces
     - Database operations and transactions
   - Create coverage heat map for risk assessment
   - Analyze cyclomatic complexity vs coverage correlation

7. **Advanced Testing Integration**
   - Configure pytest with coverage integration:
   ```bash
   uv run pytest --cov=src --cov-report=html --cov-report=term-missing --cov-report=xml --cov-branch
   ```
   - Set up coverage collection for:
     - Unit tests with isolation
     - Integration tests with realistic scenarios
     - End-to-end tests with full workflow coverage
     - Property-based testing with hypothesis
     - Async/await code coverage

8. **Edge Case and Boundary Testing**
   - Identify untested edge cases:
     ```python
     # Example coverage-driven edge case identification
     import coverage

     cov = coverage.Coverage()
     cov.load()

     # Analyze uncovered lines for edge cases
     for filename in cov.get_data().measured_files():
         missing_lines = cov.analysis2(filename)[3]
         # Analyze patterns in missing lines
     ```
   - Test boundary conditions:
     - Input validation limits
     - Resource exhaustion scenarios
     - Concurrent access patterns
     - Network failure conditions
     - File system edge cases

9. **Coverage Quality Gates and Enforcement**
   - Set up coverage enforcement in CI/CD:
   ```yaml
   # GitHub Actions example
   - name: Test with coverage
     run: |
       uv run coverage run -m pytest
       uv run coverage report --fail-under=85
       uv run coverage xml

   - name: Upload coverage to Codecov
     uses: codecov/codecov-action@v3
     with:
       file: ./coverage.xml
   ```
   - Configure pre-commit hooks for coverage:
   ```yaml
   # .pre-commit-config.yaml
   - repo: local
     hooks:
       - id: coverage-check
         name: Coverage check
         entry: uv run coverage report --fail-under=80
         language: system
         pass_filenames: false
   ```

10. **Mutation Testing Integration**
    - Install and configure mutation testing:
    ```bash
    uv add --dev mutmut cosmic-ray
    ```
    - Run mutation testing to validate test quality:
    ```bash
    # Using mutmut
    uv run mutmut run --paths-to-mutate=src/
    uv run mutmut results
    uv run mutmut html

    # Using cosmic-ray
    uv run cosmic-ray init cosmic-ray.toml src/ -- pytest tests/
    uv run cosmic-ray exec cosmic-ray.toml
    ```
    - Analyze mutation test results to improve test assertions

11. **Coverage Analysis Automation**
    - Create coverage analysis scripts:
    ```python
    # scripts/coverage_analysis.py
    import coverage
    import json
    from pathlib import Path

    def analyze_coverage_gaps():
        cov = coverage.Coverage()
        cov.load()

        gaps = {}
        for filename in cov.get_data().measured_files():
            _, missing_lines, _, missing_branches = cov.analysis2(filename)
            if missing_lines or missing_branches:
                gaps[filename] = {
                    'missing_lines': missing_lines,
                    'missing_branches': missing_branches
                }

        return gaps

    def generate_coverage_report():
        gaps = analyze_coverage_gaps()
        with open('coverage_analysis.json', 'w') as f:
            json.dump(gaps, f, indent=2)
    ```

12. **Framework-Specific Coverage Strategies**
    - **Django Applications:**
    ```bash
    uv run coverage run --source='.' manage.py test
    uv run coverage run --append --source='.' -m pytest tests/
    ```
    - **FastAPI Applications:**
    ```python
    # Test async endpoints with coverage
    import pytest
    from httpx import AsyncClient

    @pytest.mark.asyncio
    async def test_async_endpoint():
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/api/endpoint")
        assert response.status_code == 200
    ```
    - **Flask Applications:**
    ```python
    # Test with application context
    with app.test_client() as client:
        with app.app_context():
            response = client.get('/api/endpoint')
    ```

13. **Performance Impact Analysis**
    - Measure coverage collection overhead:
    ```bash
    # Baseline test execution time
    time uv run pytest tests/

    # Coverage-enabled execution time
    time uv run pytest --cov=src tests/
    ```
    - Optimize coverage collection:
      - Use parallel coverage collection
      - Exclude non-critical files from coverage
      - Use coverage contexts for targeted analysis
      - Implement coverage sampling for large codebases

14. **Coverage Trend Analysis and Monitoring**
    - Set up coverage tracking over time:
    ```python
    # scripts/coverage_tracking.py
    import json
    import datetime
    from coverage import Coverage

    def track_coverage_metrics():
        cov = Coverage()
        cov.load()

        total_lines = sum(cov.get_data().line_counts().values())
        covered_lines = total_lines - len(cov.get_data().missing_lines())
        coverage_percent = (covered_lines / total_lines) * 100

        metrics = {
            'timestamp': datetime.datetime.now().isoformat(),
            'total_lines': total_lines,
            'covered_lines': covered_lines,
            'coverage_percent': coverage_percent
        }

        # Append to historical data
        with open('coverage_history.json', 'a') as f:
            f.write(json.dumps(metrics) + '\n')
    ```

15. **Coverage Improvement Strategies**
    - **Systematic Gap Filling:**
      - Prioritize high-value, low-coverage areas
      - Focus on public API coverage first
      - Target error handling and edge cases
      - Address security-critical code paths
    - **Test Quality Enhancement:**
      - Ensure meaningful assertions in tests
      - Test behavior, not implementation
      - Use property-based testing for comprehensive coverage
      - Implement parameterized tests for edge cases
    - **Refactoring for Testability:**
      - Extract complex functions into testable units
      - Use dependency injection for better isolation
      - Separate side effects from pure logic
      - Create seams for testing legacy code

16. **Coverage Reporting and Visualization**
    - Generate comprehensive coverage dashboard:
    ```bash
    # Create detailed HTML report
    uv run coverage html --show-contexts --title="Python Project Coverage"

    # Generate summary report
    uv run coverage report --format=markdown > coverage_summary.md

    # Create coverage badge
    uv run coverage-badge -o coverage.svg -f
    ```
    - Set up coverage visualization with tools like:
      - Codecov for cloud-based coverage tracking
      - SonarQube for enterprise coverage analysis
      - Custom dashboards with coverage.py API

17. **Coverage Scripts and Automation**
    - Add coverage scripts to pyproject.toml:
    ```toml
    [tool.uv.scripts]
    coverage = "coverage run -m pytest"
    coverage-report = "coverage report --show-missing"
    coverage-html = "coverage html --show-contexts"
    coverage-check = "coverage report --fail-under=85"
    coverage-clean = "coverage erase"
    coverage-diff = "diff-cover coverage.xml --compare-branch=main"
    coverage-full = [
        "coverage erase",
        "coverage run -m pytest",
        "coverage report --show-missing",
        "coverage html",
        "coverage xml"
    ]
    ```

18. **Advanced Coverage Techniques**
    - **Context-aware coverage:**
    ```python
    # Use coverage contexts for detailed analysis
    import coverage

    cov = coverage.Coverage(context="unit_tests")
    cov.start()
    # Run unit tests
    cov.stop()
    cov.save()

    cov = coverage.Coverage(context="integration_tests")
    cov.start()
    # Run integration tests
    cov.stop()
    cov.save()
    ```
    - **Selective coverage measurement:**
    ```python
    # Measure coverage for specific modules
    cov = coverage.Coverage(source=["src/core", "src/api"])
    ```

19. **Coverage Quality Assessment**
    - Validate test quality beyond coverage metrics:
      - Check for proper assertions in tests
      - Ensure tests fail when they should
      - Verify test isolation and independence
      - Assess test maintainability and readability
    - Use mutation testing to identify weak tests
    - Implement coverage quality scoring system

20. **Team Coverage Collaboration**
    - Set up coverage review process:
      - Include coverage analysis in code reviews
      - Set coverage targets for new features
      - Track coverage improvements over sprints
      - Celebrate coverage milestones
    - Create coverage improvement guidelines:
      - When to write tests vs refactor for testability
      - How to handle hard-to-test legacy code
      - Strategies for testing external dependencies
      - Best practices for async and concurrent code testing

Remember: The goal is not just high coverage percentages, but meaningful coverage that catches real bugs and improves code quality. Focus on testing critical business logic, error conditions, and edge cases rather than pursuing 100% coverage for its own sake.
