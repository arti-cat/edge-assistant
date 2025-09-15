# Python Mutation Testing

Implement comprehensive mutation testing to assess test suite quality and effectiveness in Python projects using modern mutation testing tools

## Instructions

1. **Project Analysis and Setup Assessment**
   - Analyze current Python project structure and existing test suite
   - Parse target modules or packages from arguments: `$ARGUMENTS`
   - If no target specified, analyze entire project for mutation testing scope
   - Examine testing framework in use (pytest preferred) and test coverage
   - Assess code complexity, test patterns, and mutation testing feasibility
   - Identify critical code paths that require high-quality test validation

2. **Mutation Testing Framework Installation**
   - Install comprehensive mutation testing stack with uv:
   ```bash
   uv add --dev mutmut cosmic-ray pytest-mutagen
   uv add --dev mutpy pytest-cov coverage
   uv add --dev pytest-html pytest-json-report
   ```
   - Configure mutation testing tools for optimal performance
   - Set up mutation testing environment and workspace
   - Install additional analysis and reporting tools

3. **Mutmut Configuration and Setup**
   - Configure mutmut as primary mutation testing tool:
   ```toml
   # pyproject.toml
   [tool.mutmut]
   paths_to_mutate = "src/"
   backup = false
   runner = "python -m pytest"
   tests_dir = "tests/"
   cache_only = false

   [tool.mutmut.coverage]
   percentage_threshold = 80

   [tool.mutmut.exclude]
   line_patterns = [
       "pragma: no mutate",
       "# pragma: no mutate",
       "raise NotImplementedError",
       "pass",
   ]
   ```
   - Set up mutmut exclusion patterns for non-testable code
   - Configure mutation operators and strategies

4. **Cosmic Ray Advanced Configuration**
   - Configure cosmic-ray for advanced mutation strategies:
   ```toml
   # cosmic-ray.toml
   [cosmic-ray]
   module-path = "src"
   python-path = ["."]
   test-command = "python -m pytest tests/"
   timeout = 30.0
   exclude-modules = []

   [cosmic-ray.execution-engine]
   name = "local"

   [cosmic-ray.operators]
   standard = [
       "cosmic_ray.operators.boolean_replacer",
       "cosmic_ray.operators.break_continue_replacer",
       "cosmic_ray.operators.comparison_operator_replacer",
       "cosmic_ray.operators.logical_connector_replacer",
       "cosmic_ray.operators.number_replacer",
   ]
   ```

5. **Mutation Operator Configuration**
   - Configure comprehensive mutation operators:
   ```python
   # Custom mutation operators configuration
   MUTATION_OPERATORS = {
       'arithmetic': {
           '+': ['-', '*', '/', '%'],
           '-': ['+', '*', '/', '%'],
           '*': ['+', '-', '/', '%'],
           '/': ['+', '-', '*', '%'],
       },
       'comparison': {
           '<': ['<=', '>', '>=', '==', '!='],
           '<=': ['<', '>', '>=', '==', '!='],
           '>': ['<', '<=', '>=', '==', '!='],
           '>=': ['<', '<=', '>', '==', '!='],
           '==': ['!=', '<', '<=', '>', '>='],
           '!=': ['==', '<', '<=', '>', '>='],
       },
       'logical': {
           'and': ['or'],
           'or': ['and'],
           'not': [''],
       },
       'constants': {
           'True': ['False'],
           'False': ['True'],
           '0': ['1', '-1'],
           '1': ['0', '2'],
           '[]': ['[None]'],
           '{}': ['{None: None}'],
       }
   }
   ```

6. **Test Quality Assessment Pre-Mutation**
   - Analyze existing test suite quality before mutation testing:
   ```python
   # test_quality_analyzer.py
   import ast
   import coverage
   from pathlib import Path

   class TestQualityAnalyzer:
       def __init__(self, src_path, test_path):
           self.src_path = Path(src_path)
           self.test_path = Path(test_path)

       def analyze_test_coverage(self):
           """Analyze code coverage of test suite"""
           cov = coverage.Coverage()
           cov.start()
           # Run tests
           cov.stop()
           return cov.get_percent()

       def analyze_assertion_patterns(self):
           """Analyze assertion complexity and patterns"""
           assertions = []
           for test_file in self.test_path.glob("**/*.py"):
               tree = ast.parse(test_file.read_text())
               for node in ast.walk(tree):
                   if isinstance(node, ast.Assert):
                       assertions.append(node)
           return len(assertions)

       def identify_weak_test_patterns(self):
           """Identify potentially weak test patterns"""
           weak_patterns = []
           # Analyze for common weak patterns
           return weak_patterns
   ```

7. **Mutation Testing Execution Strategy**
   - Implement comprehensive mutation testing workflow:
   ```bash
   # Basic mutation testing execution
   uv run mutmut run --paths-to-mutate src/

   # Advanced mutation testing with cosmic-ray
   uv run cosmic-ray init cosmic-ray.toml session.sqlite
   uv run cosmic-ray exec session.sqlite

   # Parallel mutation testing for faster execution
   uv run mutmut run --paths-to-mutate src/ --runner "python -m pytest -x"

   # Focused mutation testing on specific modules
   uv run mutmut run --paths-to-mutate src/core/ --tests-dir tests/unit/
   ```

8. **Mutation Score Analysis and Reporting**
   - Generate comprehensive mutation testing reports:
   ```python
   # mutation_reporter.py
   import json
   from pathlib import Path
   from dataclasses import dataclass
   from typing import Dict, List, Optional

   @dataclass
   class MutationResult:
       file_path: str
       line_number: int
       mutation_type: str
       original_code: str
       mutated_code: str
       status: str  # 'killed', 'survived', 'timeout', 'error'
       test_output: Optional[str] = None

   class MutationReporter:
       def __init__(self, results_file: Path):
           self.results_file = results_file
           self.results = []

       def parse_mutmut_results(self) -> List[MutationResult]:
           """Parse mutmut results into structured format"""
           # Implementation for parsing mutmut JSON output
           pass

       def calculate_mutation_score(self) -> float:
           """Calculate mutation score (killed mutations / total mutations)"""
           total = len(self.results)
           killed = sum(1 for r in self.results if r.status == 'killed')
           return (killed / total * 100) if total > 0 else 0

       def generate_html_report(self, output_path: Path):
           """Generate comprehensive HTML mutation report"""
           pass

       def identify_survived_mutations(self) -> List[MutationResult]:
           """Identify mutations that survived (indicate weak tests)"""
           return [r for r in self.results if r.status == 'survived']
   ```

9. **Weak Test Detection and Analysis**
   - Implement systematic weak test detection:
   ```python
   # weak_test_detector.py
   from typing import List, Dict, Tuple

   class WeakTestDetector:
       def __init__(self, mutation_results: List[MutationResult]):
           self.mutation_results = mutation_results

       def detect_weak_assertions(self) -> List[str]:
           """Detect tests with weak or missing assertions"""
           weak_tests = []
           survived_mutations = [r for r in self.mutation_results if r.status == 'survived']

           for mutation in survived_mutations:
               if self._is_assertion_weakness(mutation):
                   weak_tests.append(mutation.file_path)

           return list(set(weak_tests))

       def detect_insufficient_edge_cases(self) -> Dict[str, List[str]]:
           """Detect areas lacking edge case testing"""
           edge_case_gaps = {}

           for mutation in self.mutation_results:
               if mutation.status == 'survived' and self._is_edge_case_mutation(mutation):
                   if mutation.file_path not in edge_case_gaps:
                       edge_case_gaps[mutation.file_path] = []
                   edge_case_gaps[mutation.file_path].append(mutation.mutation_type)

           return edge_case_gaps

       def suggest_test_improvements(self) -> List[str]:
           """Suggest specific test improvements based on survived mutations"""
           suggestions = []

           for mutation in self.mutation_results:
               if mutation.status == 'survived':
                   suggestion = self._generate_improvement_suggestion(mutation)
                   if suggestion:
                       suggestions.append(suggestion)

           return suggestions

       def _is_assertion_weakness(self, mutation: MutationResult) -> bool:
           """Check if mutation indicates weak assertions"""
           return mutation.mutation_type in ['comparison_operator', 'logical_connector']

       def _is_edge_case_mutation(self, mutation: MutationResult) -> bool:
           """Check if mutation indicates missing edge case tests"""
           return mutation.mutation_type in ['boundary_value', 'null_check', 'arithmetic_operator']

       def _generate_improvement_suggestion(self, mutation: MutationResult) -> str:
           """Generate specific improvement suggestion for survived mutation"""
           suggestions_map = {
               'comparison_operator': f"Add assertion to verify comparison logic at {mutation.file_path}:{mutation.line_number}",
               'logical_connector': f"Test both branches of logical operation at {mutation.file_path}:{mutation.line_number}",
               'arithmetic_operator': f"Verify arithmetic operation results at {mutation.file_path}:{mutation.line_number}",
               'boundary_value': f"Add boundary value tests for {mutation.file_path}:{mutation.line_number}",
           }
           return suggestions_map.get(mutation.mutation_type, "")
   ```

10. **Test Suite Enhancement Based on Mutation Results**
    - Generate improved tests based on mutation analysis:
    ```python
    # test_enhancer.py
    import ast
    from pathlib import Path
    from typing import List, Dict

    class TestSuiteEnhancer:
        def __init__(self, mutation_results: List[MutationResult], test_dir: Path):
            self.mutation_results = mutation_results
            self.test_dir = test_dir

        def generate_missing_tests(self) -> Dict[str, str]:
            """Generate tests for survived mutations"""
            new_tests = {}

            survived_mutations = [r for r in self.mutation_results if r.status == 'survived']

            for mutation in survived_mutations:
                test_code = self._generate_test_for_mutation(mutation)
                if test_code:
                    test_file = self._get_test_file_for_mutation(mutation)
                    if test_file not in new_tests:
                        new_tests[test_file] = ""
                    new_tests[test_file] += test_code + "\n\n"

            return new_tests

        def enhance_existing_tests(self) -> Dict[str, str]:
            """Enhance existing tests based on mutation analysis"""
            enhanced_tests = {}

            for test_file in self.test_dir.glob("**/*.py"):
                if self._needs_enhancement(test_file):
                    enhanced_code = self._enhance_test_file(test_file)
                    enhanced_tests[str(test_file)] = enhanced_code

            return enhanced_tests

        def _generate_test_for_mutation(self, mutation: MutationResult) -> str:
            """Generate specific test for a survived mutation"""
            templates = {
                'comparison_operator': '''
    def test_{function_name}_comparison_edge_case(self):
        """Test comparison operator at line {line_number}"""
        # Test the specific comparison that was mutated
        result = {function_call}
        assert result == expected_value  # Verify exact comparison
    ''',
                'arithmetic_operator': '''
    def test_{function_name}_arithmetic_precision(self):
        """Test arithmetic operation at line {line_number}"""
        # Test the specific arithmetic operation that was mutated
        result = {function_call}
        assert result == expected_result  # Verify exact arithmetic result
    ''',
                'logical_connector': '''
    def test_{function_name}_logical_branches(self):
        """Test logical operation branches at line {line_number}"""
        # Test both True and False branches of logical operation
        assert {function_call}(True, False) == expected_true_false
        assert {function_call}(False, True) == expected_false_true
    '''
            }

            template = templates.get(mutation.mutation_type, "")
            if template:
                return template.format(
                    function_name=self._extract_function_name(mutation),
                    line_number=mutation.line_number,
                    function_call=self._generate_function_call(mutation)
                )
            return ""
    ```

11. **Advanced Mutation Strategies and Custom Operators**
    - Implement domain-specific mutation operators:
    ```python
    # custom_mutators.py
    import ast
    from typing import List, Any

    class PythonSpecificMutator(ast.NodeTransformer):
        """Custom mutation operators for Python-specific patterns"""

        def visit_ListComp(self, node: ast.ListComp) -> Any:
            """Mutate list comprehensions"""
            # Mutate comprehension logic
            mutated = ast.GeneratorExp(
                elt=node.elt,
                generators=node.generators
            )
            return mutated

        def visit_DictComp(self, node: ast.DictComp) -> Any:
            """Mutate dictionary comprehensions"""
            # Mutate dict comprehension to set comprehension
            mutated = ast.SetComp(
                elt=node.key,
                generators=node.generators
            )
            return mutated

        def visit_With(self, node: ast.With) -> Any:
            """Mutate context managers"""
            # Remove context manager (dangerous mutation)
            return ast.Module(body=node.body, type_ignores=[])

        def visit_Try(self, node: ast.Try) -> Any:
            """Mutate exception handling"""
            # Remove exception handling
            return ast.Module(body=node.body, type_ignores=[])

    class DomainSpecificMutator:
        """Domain-specific mutation operators"""

        def __init__(self, domain: str):
            self.domain = domain

        def get_mutations_for_domain(self) -> List[str]:
            """Get domain-specific mutations"""
            domain_mutations = {
                'web': ['request_method', 'http_status', 'url_parameter'],
                'data_science': ['aggregation_function', 'statistical_operator'],
                'machine_learning': ['activation_function', 'loss_function'],
                'database': ['sql_operator', 'join_type', 'index_hint'],
            }
            return domain_mutations.get(self.domain, [])
    ```

12. **CI/CD Integration and Automation**
    - Configure mutation testing in CI/CD pipelines:
    ```yaml
    # .github/workflows/mutation-testing.yml
    name: Mutation Testing

    on:
      pull_request:
        branches: [main]
      schedule:
        - cron: '0 2 * * 0'  # Weekly mutation testing

    jobs:
      mutation-testing:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3

          - name: Set up Python
            uses: actions/setup-python@v4
            with:
              python-version: '3.11'

          - name: Install uv
            run: pip install uv

          - name: Install dependencies
            run: uv sync --dev

          - name: Run baseline tests
            run: uv run pytest --cov=src --cov-report=xml

          - name: Run mutation testing
            run: |
              uv run mutmut run --paths-to-mutate src/
              uv run mutmut results

          - name: Generate mutation report
            run: |
              uv run python scripts/generate_mutation_report.py

          - name: Upload mutation results
            uses: actions/upload-artifact@v3
            with:
              name: mutation-results
              path: mutation-report.html

          - name: Comment PR with results
            if: github.event_name == 'pull_request'
            run: |
              python scripts/comment_mutation_results.py
    ```

13. **Mutation Testing Scripts and Automation**
    - Create comprehensive mutation testing scripts:
    ```bash
    # Add to pyproject.toml
    [tool.uv.scripts]
    mutate = "mutmut run --paths-to-mutate src/"
    mutate-fast = "mutmut run --paths-to-mutate src/ --runner 'python -m pytest -x'"
    mutate-report = "python scripts/generate_mutation_report.py"
    mutate-analyze = "python scripts/analyze_mutations.py"
    mutate-enhance = "python scripts/enhance_tests.py"
    mutate-ci = "python scripts/mutation_ci_check.py"

    # Targeted mutation testing
    mutate-core = "mutmut run --paths-to-mutate src/core/"
    mutate-api = "mutmut run --paths-to-mutate src/api/"
    mutate-models = "mutmut run --paths-to-mutate src/models/"

    # Mutation testing with different strategies
    mutate-comprehensive = "cosmic-ray exec session.sqlite"
    mutate-selective = "python scripts/selective_mutation.py"
    ```

14. **Performance Optimization and Scalability**
    - Optimize mutation testing performance:
    ```python
    # performance_optimizer.py
    import multiprocessing
    from concurrent.futures import ProcessPoolExecutor
    from pathlib import Path
    from typing import List

    class MutationTestingOptimizer:
        def __init__(self, src_path: Path, test_path: Path):
            self.src_path = src_path
            self.test_path = test_path
            self.cpu_count = multiprocessing.cpu_count()

        def optimize_test_execution(self) -> dict:
            """Optimize test execution for mutation testing"""
            optimizations = {
                'parallel_execution': True,
                'fast_fail': True,
                'test_selection': self._select_relevant_tests(),
                'caching': True,
                'incremental': True,
            }
            return optimizations

        def _select_relevant_tests(self) -> List[str]:
            """Select only tests relevant to mutated code"""
            # Implementation for intelligent test selection
            pass

        def configure_parallel_execution(self) -> dict:
            """Configure optimal parallel execution"""
            return {
                'workers': min(self.cpu_count - 1, 8),
                'chunk_size': 10,
                'timeout': 30,
                'memory_limit': '2GB',
            }
    ```

15. **Mutation Testing Quality Gates and Thresholds**
    - Implement quality gates based on mutation scores:
    ```python
    # quality_gates.py
    from dataclasses import dataclass
    from typing import Dict, List, Optional

    @dataclass
    class MutationQualityGate:
        minimum_mutation_score: float = 80.0
        critical_path_score: float = 95.0
        new_code_score: float = 90.0
        regression_threshold: float = 5.0

    class MutationQualityChecker:
        def __init__(self, quality_gate: MutationQualityGate):
            self.quality_gate = quality_gate

        def check_quality_gates(self, current_score: float,
                              previous_score: Optional[float] = None) -> Dict[str, bool]:
            """Check if mutation testing meets quality gates"""
            results = {
                'minimum_score_met': current_score >= self.quality_gate.minimum_mutation_score,
                'no_regression': True,
                'critical_paths_covered': True,  # Would need implementation
            }

            if previous_score:
                regression = previous_score - current_score
                results['no_regression'] = regression <= self.quality_gate.regression_threshold

            return results

        def generate_quality_report(self, results: Dict[str, bool]) -> str:
            """Generate quality gate report"""
            passed = all(results.values())
            status = "PASSED" if passed else "FAILED"

            report = f"Mutation Testing Quality Gate: {status}\n"
            for check, result in results.items():
                status_icon = "✅" if result else "❌"
                report += f"{status_icon} {check.replace('_', ' ').title()}: {'PASS' if result else 'FAIL'}\n"

            return report
    ```

16. **Integration with Test Quality Metrics**
    - Integrate mutation testing with broader test quality assessment:
    ```python
    # test_quality_metrics.py
    from dataclasses import dataclass
    from typing import Dict, List, Optional

    @dataclass
    class TestQualityMetrics:
        code_coverage: float
        mutation_score: float
        test_count: int
        assertion_count: int
        test_complexity: float
        test_maintainability: float

    class ComprehensiveTestQualityAssessment:
        def __init__(self):
            self.metrics = {}

        def assess_overall_quality(self, mutation_score: float,
                                 coverage_score: float) -> Dict[str, str]:
            """Assess overall test suite quality"""
            quality_matrix = {
                (True, True): "Excellent - High coverage and high mutation score",
                (True, False): "Good - High coverage but low mutation score (weak tests)",
                (False, True): "Concerning - Low coverage but high mutation score (missing tests)",
                (False, False): "Poor - Low coverage and low mutation score",
            }

            high_coverage = coverage_score >= 80
            high_mutation = mutation_score >= 80

            return {
                'overall_quality': quality_matrix[(high_coverage, high_mutation)],
                'recommendations': self._generate_recommendations(high_coverage, high_mutation),
                'priority_actions': self._prioritize_improvements(high_coverage, high_mutation),
            }

        def _generate_recommendations(self, high_coverage: bool, high_mutation: bool) -> List[str]:
            """Generate specific recommendations for improvement"""
            recommendations = []

            if not high_coverage:
                recommendations.append("Increase test coverage by adding tests for uncovered code")

            if not high_mutation:
                recommendations.append("Improve test assertions and edge case coverage")
                recommendations.append("Add more specific and targeted test cases")

            if high_coverage and not high_mutation:
                recommendations.append("Focus on test quality rather than quantity")
                recommendations.append("Review and strengthen existing test assertions")

            return recommendations
    ```

17. **Documentation and Training Materials**
    - Generate mutation testing documentation and guidelines:
    ```markdown
    # Mutation Testing Guidelines

    ## What is Mutation Testing?
    Mutation testing introduces small changes (mutations) to your code to verify
    that your tests can detect these changes. A good test suite should "kill"
    most mutations by failing when the code is altered.

    ## Key Metrics
    - **Mutation Score**: Percentage of mutations killed by tests
    - **Survived Mutations**: Mutations not detected by tests (indicates weak tests)
    - **Test Effectiveness**: How well tests detect bugs

    ## Best Practices
    1. Aim for mutation scores above 80%
    2. Focus on critical code paths first
    3. Use mutation testing to guide test improvement
    4. Run mutation testing regularly in CI/CD
    5. Balance coverage and mutation score

    ## Common Issues and Solutions
    - **Low Mutation Score**: Add more specific assertions
    - **Slow Execution**: Use parallel testing and selective mutation
    - **False Positives**: Configure appropriate exclusions
    ```

18. **Mutation Testing Validation and Quality Assurance**
    - Validate mutation testing setup and results:
    - Ensure mutation operators are working correctly
    - Verify test execution environment consistency
    - Validate mutation score calculations and reporting accuracy
    - Check for proper exclusion of non-testable code patterns
    - Ensure integration with existing testing infrastructure
    - Validate CI/CD integration and automated reporting
    - Generate comprehensive mutation testing metrics and analytics
