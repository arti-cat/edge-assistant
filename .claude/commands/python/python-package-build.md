# Python Package Build and Distribution

Build and distribute Python packages using modern packaging tools and workflows

## Instructions

1. **Package Analysis and Configuration**
   - Parse package name and version from arguments: `$ARGUMENTS`
   - If no arguments provided, analyze current project and prompt for package details
   - Validate existing pyproject.toml configuration for packaging requirements
   - Check for proper package structure and required metadata
   - Verify package name availability on PyPI if needed

2. **Modern Packaging Setup**
   - Ensure uv is installed and updated: `uv --version`
   - Configure pyproject.toml with complete package metadata:
     - Package name, version, description, authors
     - License, homepage, repository URLs
     - Keywords, classifiers, and Python version requirements
     - Entry points, console scripts, and GUI scripts
     - Dependencies and optional dependency groups
   - Set up proper package structure with src-layout
   - Configure build system using modern build backends (hatchling, setuptools, pdm-backend)

3. **Build Environment Configuration**
   - Install modern build tools: `uv add --dev build twine`
   - Set up isolated build environment with uv
   - Configure build dependencies and build-system requirements
   - Install package validation tools: `uv add --dev check-manifest twine`
   - Set up wheel and sdist build configuration
   - Configure cross-platform build settings

4. **Package Content Validation**
   - Verify package imports and module structure
   - Check for proper __init__.py files and package discovery
   - Validate entry points and console scripts functionality
   - Review package data and resource files inclusion
   - Test package installation in clean environment
   - Run package integrity checks with check-manifest

5. **Version Management and Tagging**
   - Implement semantic versioning strategy
   - Set up version management with bump2version or hatch
   - Configure dynamic versioning from git tags or VCS
   - Create version bump commands and scripts
   - Set up changelog generation for releases
   - Tag releases with proper version format

6. **Build Process Execution**
   - Clean previous build artifacts: `rm -rf dist/ build/ *.egg-info/`
   - Build source distribution: `uv run python -m build --sdist`
   - Build wheel distribution: `uv run python -m build --wheel`
   - Build both distributions: `uv run python -m build`
   - Verify build artifacts in dist/ directory
   - Check wheel contents and metadata

7. **Package Testing and Validation**
   - Test package installation from wheel: `uv pip install dist/*.whl`
   - Test package installation from sdist: `uv pip install dist/*.tar.gz`
   - Run import tests in fresh environment
   - Validate entry points and console scripts
   - Test package functionality and API compatibility
   - Run security scanning on built packages

8. **Package Metadata Validation**
   - Check package metadata: `uv run twine check dist/*`
   - Validate long description rendering for PyPI
   - Verify license file inclusion and format
   - Check package classifiers and keywords
   - Validate dependency specifications
   - Test package discovery and import paths

9. **Test PyPI Upload (Staging)**
   - Configure TestPyPI credentials securely
   - Upload to TestPyPI: `uv run twine upload --repository testpypi dist/*`
   - Test installation from TestPyPI in clean environment
   - Verify package page rendering and metadata display
   - Test dependency resolution from TestPyPI
   - Validate download and installation process

10. **Production PyPI Publishing**
    - Configure PyPI credentials using API tokens
    - Set up secure credential storage (keyring, environment variables)
    - Upload to PyPI: `uv run twine upload dist/*`
    - Verify package publication and availability
    - Test installation from PyPI
    - Monitor package statistics and downloads

11. **Automated Publishing Workflows**
    - Set up GitHub Actions for automated publishing
    - Configure release triggers (tags, manual dispatch)
    - Implement multi-platform builds (Linux, macOS, Windows)
    - Set up matrix builds for multiple Python versions
    - Configure trusted publisher authentication for PyPI
    - Add deployment protection rules and approvals

12. **Security and Best Practices**
    - Enable two-factor authentication for PyPI
    - Use API tokens instead of username/password
    - Configure trusted publishers for GitHub Actions
    - Set up vulnerability scanning for dependencies
    - Implement supply chain security measures
    - Configure package signing and verification

13. **Distribution Strategy Configuration**
    - Set up multiple distribution channels (PyPI, conda, etc.)
    - Configure package mirrors and alternative indices
    - Set up enterprise/private package repositories
    - Implement package dependency management
    - Configure platform-specific builds and wheels
    - Set up binary distribution for compiled extensions

14. **Continuous Integration Setup**
    ```yaml
    # .github/workflows/build-and-publish.yml
    name: Build and Publish Python Package

    on:
      push:
        tags:
          - 'v*'
      workflow_dispatch:
        inputs:
          publish:
            description: 'Publish to PyPI'
            required: true
            default: 'false'

    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: astral-sh/setup-uv@v4
          - name: Build package
            run: |
              uv sync
              uv run python -m build
          - name: Check package
            run: uv run twine check dist/*
          - name: Test install
            run: |
              uv venv test-env
              uv pip install dist/*.whl
              uv run python -c "import package_name"

      publish:
        needs: build
        runs-on: ubuntu-latest
        if: startsWith(github.ref, 'refs/tags/')
        environment:
          name: pypi
          url: https://pypi.org/p/package-name
        permissions:
          id-token: write
        steps:
          - uses: actions/checkout@v4
          - uses: astral-sh/setup-uv@v4
          - name: Build package
            run: |
              uv sync
              uv run python -m build
          - name: Publish to PyPI
            uses: pypa/gh-action-pypi-publish@release/v1
    ```

15. **Package Documentation and Marketing**
    - Generate comprehensive package documentation
    - Create usage examples and tutorials
    - Set up documentation hosting (Read the Docs, GitHub Pages)
    - Write package announcement and release notes
    - Configure package discovery metadata
    - Set up community and support channels

16. **Post-Release Monitoring**
    - Monitor package download statistics
    - Set up error tracking and issue reporting
    - Monitor dependency vulnerability alerts
    - Track package compatibility across Python versions
    - Set up automated dependency updates
    - Monitor package performance and usage patterns

17. **Release Automation Scripts**
    - Create release preparation scripts
    - Set up automated changelog generation
    - Configure version bumping automation
    - Implement rollback procedures for failed releases
    - Set up notification systems for releases
    - Create release validation checklists

18. **Advanced Build Configuration**

    **Complete pyproject.toml example:**
    ```toml
    [build-system]
    requires = ["hatchling>=1.10.0"]
    build-backend = "hatchling.build"

    [project]
    name = "my-package"
    dynamic = ["version"]
    description = "Modern Python package"
    readme = "README.md"
    license = {file = "LICENSE"}
    authors = [
        {name = "Author Name", email = "author@example.com"},
    ]
    maintainers = [
        {name = "Maintainer Name", email = "maintainer@example.com"},
    ]
    keywords = ["python", "package", "modern"]
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ]
    requires-python = ">=3.8"
    dependencies = [
        "click>=8.0.0",
        "requests>=2.25.0",
    ]

    [project.optional-dependencies]
    dev = [
        "build>=0.10.0",
        "twine>=4.0.0",
        "check-manifest>=0.49",
        "ruff>=0.1.0",
        "mypy>=1.0.0",
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ]
    docs = [
        "mkdocs>=1.5.0",
        "mkdocs-material>=9.0.0",
        "mkdocstrings[python]>=0.20.0",
    ]
    test = [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "pytest-mock>=3.10.0",
    ]

    [project.urls]
    Homepage = "https://github.com/username/my-package"
    Documentation = "https://my-package.readthedocs.io"
    Repository = "https://github.com/username/my-package.git"
    Issues = "https://github.com/username/my-package/issues"
    Changelog = "https://github.com/username/my-package/blob/main/CHANGELOG.md"

    [project.scripts]
    my-cli = "my_package.cli:main"

    [project.gui-scripts]
    my-gui = "my_package.gui:main"

    [project.entry-points."my_package.plugins"]
    plugin1 = "my_package.plugins:plugin1"

    [tool.hatch.version]
    path = "src/my_package/__about__.py"

    [tool.hatch.build.targets.wheel]
    packages = ["src/my_package"]

    [tool.hatch.build.targets.sdist]
    exclude = [
        "/.github",
        "/docs",
        "/.gitignore",
        "/.pre-commit-config.yaml",
    ]
    ```

19. **Package Structure Validation**
    - Verify src-layout package structure:
      ```
      project-root/
      ├── src/
      │   └── package_name/
      │       ├── __init__.py
      │       ├── __about__.py
      │       ├── core.py
      │       └── cli.py
      ├── tests/
      │   ├── __init__.py
      │   └── test_core.py
      ├── docs/
      │   └── index.md
      ├── pyproject.toml
      ├── README.md
      ├── LICENSE
      └── CHANGELOG.md
      ```
    - Validate package discovery and import resolution
    - Check for proper namespace package configuration
    - Verify data files and resource inclusion

20. **Distribution Testing Matrix**
    - Test installation across Python versions (3.8-3.12)
    - Validate cross-platform compatibility (Linux, macOS, Windows)
    - Test installation methods (pip, uv, conda)
    - Verify dependency resolution in different environments
    - Test package functionality in various deployment scenarios
    - Validate package uninstallation and cleanup

21. **Quality Assurance Checklist**
    - [ ] Package builds successfully with modern tools
    - [ ] All tests pass in clean environment
    - [ ] Package installs and imports correctly
    - [ ] Console scripts and entry points work
    - [ ] Documentation builds and renders properly
    - [ ] License and copyright information included
    - [ ] Security scanning passes without critical issues
    - [ ] Version numbering follows semantic versioning
    - [ ] Package metadata is complete and accurate
    - [ ] Distribution files are properly signed/verified
