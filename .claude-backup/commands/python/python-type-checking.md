# Python Type Checking

Setup and manage comprehensive type checking for Python projects with modern tooling

## Instructions

Follow this systematic approach to implement comprehensive Python type checking: **$ARGUMENTS**

1. **Project Analysis and Assessment**
   - Analyze codebase size, complexity, and existing type annotations
   - Review Python version requirements and compatibility needs
   - Identify critical modules and high-priority areas for type safety
   - Assess team experience with type hints and gradual adoption strategy
   - Check for existing type checking configuration and tools
   - Document current type coverage baseline for improvement tracking

2. **Type Checker Installation and Setup**
   - Install mypy as primary type checker: `uv add --dev mypy`
   - Install pyright for additional validation: `uv add --dev pyright`
   - Install typing-extensions for compatibility: `uv add typing-extensions`
   - Verify installations: `uv run mypy --version && uv run pyright --version`
   - Create initial mypy.ini or configure in pyproject.toml
   - Set up pyright configuration in pyrightconfig.json

3. **Core Type Checking Configuration**
   ```toml
   [tool.mypy]
   python_version = "3.8"
   warn_return_any = true
   warn_unused_configs = true
   warn_unused_ignores = true
   warn_redundant_casts = true
   warn_unreachable = true
   check_untyped_defs = true
   disallow_any_generics = true
   disallow_incomplete_defs = true
   disallow_subclassing_any = true
   disallow_untyped_calls = true
   disallow_untyped_decorators = true
   disallow_untyped_defs = true
   no_implicit_optional = true
   strict_optional = true
   show_error_codes = true
   show_column_numbers = true
   ```

4. **Pyright Configuration Setup**
   ```json
   {
     "include": ["src"],
     "exclude": ["**/__pycache__", "**/node_modules"],
     "pythonVersion": "3.8",
     "typeCheckingMode": "basic",
     "reportMissingImports": true,
     "reportMissingTypeStubs": false,
     "reportImportCycles": true,
     "reportUnusedImport": true,
     "reportUnusedClass": "warning",
     "reportUnusedFunction": "warning",
     "reportDuplicateImport": true,
     "reportIncompatibleMethodOverride": true,
     "reportIncompatibleVariableOverride": true
   }
   ```

5. **Gradual Type Adoption Strategy**
   - Start with entry points and public APIs
   - Implement per-module type checking exclusions:
   ```toml
   [[tool.mypy.overrides]]
   module = "legacy.*"
   ignore_errors = true
   ```
   - Use `# type: ignore` comments strategically for temporary exceptions
   - Create typed versions of critical functions first
   - Set up module-specific strictness levels
   - Document migration path and timeline

6. **Stub File Generation and Management**
   - Install stubgen for automatic stub generation: `uv add --dev mypy`
   - Generate stubs for untyped modules: `uv run stubgen -p untyped_package -o stubs/`
   - Install type stubs for third-party packages:
   ```bash
   uv add --dev types-requests types-redis types-pyyaml
   uv add --dev types-setuptools types-six types-dateutil
   ```
   - Create custom stub files for internal untyped modules
   - Set up stub file organization in typings/ directory
   - Configure mypy_path to include custom stubs

7. **Advanced Type Checking Features**
   - Configure plugins for frameworks (Django, SQLAlchemy, etc.):
   ```toml
   [tool.mypy]
   plugins = ["mypy_django_plugin.main", "sqlalchemy.ext.mypy.plugin"]
   ```
   - Set up type checking for tests with pytest-mypy
   - Configure strict mode for new modules
   - Enable experimental features for latest Python versions
   - Set up custom type checking rules and validators

8. **Type Hint Generation and Enhancement**
   - Install MonkeyType for runtime type collection: `uv add --dev monkeytype`
   - Set up automatic type hint generation:
   ```bash
   # Collect types during test runs
   uv run monkeytype run pytest
   # Generate type hints
   uv run monkeytype apply module_name
   ```
   - Install pytype for type inference: `uv add --dev pytype`
   - Use autotyping for automated type annotation: `uv add --dev libcst`
   - Create scripts for batch type hint generation

9. **Type Coverage and Quality Metrics**
   - Install type coverage tools: `uv add --dev mypy-stat`
   - Generate type coverage reports:
   ```bash
   uv run mypy --html-report mypy-report src/
   uv run mypy --txt-report mypy-coverage src/
   ```
   - Set up coverage thresholds and quality gates
   - Create type coverage dashboard and tracking
   - Monitor type safety improvements over time
   - Document type coverage goals and milestones

10. **CI/CD Pipeline Integration**
    ```yaml
    - name: Type Check with mypy
      run: |
        uv run mypy src/ --strict
        uv run mypy tests/ --ignore-missing-imports

    - name: Type Check with pyright
      run: uv run pyright src/

    - name: Generate Type Coverage Report
      run: |
        uv run mypy --html-report type-coverage src/
        uv run mypy --cobertura-xml-report type-coverage src/
    ```

11. **IDE Integration and Developer Experience**
    - Configure VS Code Python extension for type checking
    - Set up real-time type checking in editor
    - Configure auto-imports for typing modules
    - Set up type checking shortcuts and commands
    - Install Pylance for enhanced type checking experience
    - Configure type checking on save and file change

12. **Advanced Typing Patterns and Best Practices**
    - Implement Protocol classes for structural typing
    - Use TypeVar and Generic for type-safe generics
    - Set up Literal types for enumerated values
    - Configure Union and Optional type usage
    - Implement TypedDict for structured dictionaries
    - Use NewType for type safety with primitives
    - Set up overload decorators for function polymorphism

13. **Type Checking Scripts and Automation**
    - Add comprehensive type checking scripts to pyproject.toml:
    ```toml
    [tool.uv.scripts]
    type-check = "mypy src/"
    type-check-strict = "mypy src/ --strict"
    type-check-pyright = "pyright src/"
    type-coverage = "mypy --html-report type-coverage src/"
    stub-gen = "stubgen -p src -o stubs/"
    type-stats = "mypy --txt-report type-stats src/"
    ```

14. **Progressive Type Safety Enhancement**
    - Create per-module strictness configuration
    - Set up automated type hint suggestions
    - Implement type checking quality gates
    - Configure incremental type checking for large codebases
    - Set up type checking performance optimization
    - Create type safety improvement roadmap

15. **Documentation and Team Onboarding**
    - Document type checking standards and conventions
    - Create type annotation style guide
    - Set up type checking troubleshooting guide
    - Document common type checking patterns
    - Create training materials for team adoption
    - Set up type checking best practices documentation

16. **Monitoring and Maintenance**
    - Set up automated type checking health reports
    - Monitor type coverage regression prevention
    - Create alerts for type checking failures
    - Set up periodic stub file updates
    - Monitor type checking performance impact
    - Track type safety improvement metrics

Remember to start with basic type checking and gradually increase strictness to ensure smooth team adoption and minimal disruption to existing workflows.
