# Setup Python Monorepo

Configure Python monorepo project structure with uv workspaces

## Instructions

1. **Monorepo Strategy Analysis**
   - Parse monorepo configuration from arguments: `$ARGUMENTS`
   - Analyze project structure and determine if monorepo is appropriate
   - Assess team size, project complexity, and shared library needs
   - Validate uv workspace compatibility with existing codebase
   - Determine workspace organization strategy

2. **Workspace Structure Setup**
   - Create standard Python monorepo directory structure:
     ```
     workspace/
     ├── pyproject.toml          # Root workspace configuration
     ├── uv.lock                 # Unified lock file
     ├── packages/
     │   ├── app-api/            # FastAPI application
     │   ├── app-cli/            # CLI application
     │   └── app-web/            # Web application
     ├── libs/
     │   ├── shared-core/        # Core shared library
     │   ├── shared-utils/       # Utility functions
     │   └── shared-models/      # Data models
     ├── tools/
     │   ├── scripts/            # Build and deployment scripts
     │   └── dev-tools/          # Development utilities
     └── docs/                   # Documentation
     ```

3. **uv Workspace Configuration**
   - Configure root pyproject.toml with workspace definition:
   ```toml
   [tool.uv.workspace]
   members = [
       "packages/*",
       "libs/*",
       "tools/*"
   ]

   [tool.uv.sources]
   shared-core = { workspace = true }
   shared-utils = { workspace = true }
   shared-models = { workspace = true }
   ```
   - Set up unified dependency management
   - Configure workspace-wide Python version: `.python-version`

4. **Package Structure Templates**
   - Create standardized package structure for each workspace member:
   ```
   packages/app-api/
   ├── pyproject.toml
   ├── src/
   │   └── app_api/
   │       ├── __init__.py
   │       └── main.py
   ├── tests/
   │   └── test_main.py
   └── README.md
   ```

5. **Dependency Management**
   - Configure shared dependencies in root pyproject.toml:
   ```toml
   [dependency-groups]
   dev = [
       "ruff",
       "mypy",
       "pytest",
       "pre-commit",
   ]
   test = [
       "pytest-cov",
       "pytest-asyncio",
       "httpx",
   ]
   docs = [
       "mkdocs",
       "mkdocs-material",
   ]
   ```
   - Set up cross-package dependency management
   - Configure private package references

6. **Build System Integration**
   - Set up workspace-wide build commands:
   ```toml
   [tool.uv.scripts]
   build-all = ["uv run --package app-api python -m build", "uv run --package app-cli python -m build"]
   test-all = "uv run pytest packages/*/tests libs/*/tests"
   lint-all = "uv run ruff check packages/ libs/ tools/"
   format-all = "uv run ruff format packages/ libs/ tools/"
   ```
   - Configure parallel builds and task execution
   - Set up incremental builds for changed packages

7. **Development Workflow**
   - Set up workspace-wide development scripts
   - Configure hot reloading for development packages
   - Set up workspace-wide linting and formatting
   - Configure debugging across multiple packages
   - Set up workspace-wide testing and coverage reporting

8. **Version Management**
   - Configure versioning strategy for workspace packages
   - Set up changelog generation for workspace packages
   - Configure release workflow and package publishing
   - Set up semantic versioning with conventional commits
   - Configure workspace-wide dependency updates

9. **Testing and Quality Assurance**
   - Configure workspace-wide testing:
   ```toml
   [tool.pytest.ini_options]
   testpaths = ["packages/*/tests", "libs/*/tests"]
   pythonpath = ["packages/*/src", "libs/*/src"]
   ```
   - Set up integration testing between packages
   - Configure test coverage across workspace
   - Set up workspace-wide code quality checks

10. **CI/CD Pipeline Integration**
    - Configure CI to detect affected packages:
    ```yaml
    - name: Test affected packages
      run: |
        uv run pytest --cov=packages --cov=libs
        uv run ruff check packages/ libs/ tools/
    ```
    - Set up build matrix for different package combinations
    - Configure deployment pipeline for multiple packages
    - Set up workspace-wide quality gates

11. **Documentation and Standards**
    - Create workspace-wide development guidelines
    - Document package creation and management procedures
    - Set up workspace-wide code standards and conventions
    - Create architectural decision records for monorepo patterns
    - Document deployment and release procedures

12. **Validation and Testing**
    - Verify workspace configuration with: `uv workspace list`
    - Test package creation and cross-package dependencies
    - Validate build pipeline and task execution
    - Test development workflow and hot reloading
    - Verify CI/CD integration and affected package detection
    - Create example packages to demonstrate workspace functionality

13. **Advanced Features**
    - Set up workspace-wide pre-commit hooks
    - Configure workspace-wide security scanning
    - Set up workspace-wide performance monitoring
    - Configure workspace-wide documentation generation
    - Set up workspace-wide deployment orchestration
