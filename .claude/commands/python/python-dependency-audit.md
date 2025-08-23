# Python Dependency Security Audit

Comprehensive security audit for Python dependencies with vulnerability scanning, license checking, and dependency analysis using modern Python tooling

## Instructions

Follow these steps to conduct a thorough Python dependency security audit:

1. **Environment and Project Analysis**
   - Examine the Python project structure and configuration files
   - Check for pyproject.toml, requirements.txt, setup.py, or Poetry files
   - Identify package manager (pip, uv, poetry, pipenv) and lock files
   - Review Python version requirements and compatibility
   - Analyze virtual environment setup and dependency isolation
   - Document current dependency management approach

2. **Install Security Audit Tools**
   - Install pip-audit for vulnerability scanning: `uv add --dev pip-audit`
   - Install safety for security database checks: `uv add --dev safety`
   - Install bandit for code security analysis: `uv add --dev bandit`
   - Install semgrep for advanced security patterns: `uv add --dev semgrep`
   - Install cyclonedx-bom for SBOM generation: `uv add --dev cyclonedx-bom`
   - Install pip-licenses for license analysis: `uv add --dev pip-licenses`

3. **Dependency Inventory and Lock File Analysis**
   - Generate comprehensive dependency list: `uv pip list --format=json > dependencies.json`
   - Analyze uv.lock or requirements.lock for pinned versions
   - Check for dependency version conflicts: `uv pip check`
   - Identify direct vs transitive dependencies
   - Review dependency tree structure: `uv pip show --verbose <package>`
   - Document critical dependencies and their purposes

4. **Vulnerability Scanning**
   - Run pip-audit on current environment: `uv run pip-audit --format=json --output=vulnerabilities.json`
   - Run safety check against PyUp database: `uv run safety check --json --output=safety-report.json`
   - Scan requirements files: `uv run pip-audit -r requirements.txt`
   - Check for known CVEs and security advisories
   - Analyze vulnerability severity levels (critical, high, medium, low)
   - Cross-reference findings between multiple security databases

5. **Python-Specific Security Analysis**
   - Scan for pickle/dill deserialization vulnerabilities
   - Check for eval(), exec(), and code injection risks
   - Review subprocess usage for command injection vulnerabilities
   - Analyze file operations for path traversal issues
   - Check for insecure random number generation
   - Review cryptographic implementations and key management
   - Identify potential dependency confusion attacks

6. **License Compliance Audit**
   - Generate license report: `uv run pip-licenses --format=json --output-file=licenses.json`
   - Identify GPL, AGPL, and other copyleft licenses
   - Check for license compatibility issues
   - Review commercial license requirements
   - Document license obligations and restrictions
   - Flag packages with unclear or missing licenses

7. **Dependency Risk Assessment**
   - Analyze package maintenance status and last update dates
   - Check for deprecated or unmaintained packages
   - Review package download statistics and community adoption
   - Assess maintainer reputation and security practices
   - Identify packages with multiple security vulnerabilities
   - Check for typosquatting and malicious package indicators

8. **Code Quality and Security Scanning**
   - Run bandit security linter: `uv run bandit -r . -f json -o bandit-report.json`
   - Scan for hardcoded secrets and API keys
   - Check for insecure function usage patterns
   - Analyze import statements for malicious packages
   - Review setup.py and pyproject.toml for security issues
   - Scan for shell injection and path manipulation vulnerabilities

9. **Supply Chain Security Analysis**
   - Generate Software Bill of Materials (SBOM): `uv run cyclonedx-py -o sbom.json`
   - Analyze package origins and download sources
   - Check for packages with suspicious install scripts
   - Review package signatures and integrity verification
   - Assess dependency update frequency and security patching
   - Identify packages from untrusted or unknown sources

10. **Dependency Update and Remediation Planning**
    - Identify available security updates: `uv tree --outdated`
    - Prioritize updates based on vulnerability severity
    - Test dependency updates in isolated environment
    - Check for breaking changes in dependency updates
    - Create dependency update plan with rollback strategy
    - Document required code changes for major version updates

11. **pyproject.toml Security Configuration**
    - Configure dependency security scanning in pyproject.toml:
    ```toml
    [tool.bandit]
    exclude_dirs = ["tests", "venv", ".venv"]
    severity = ["medium", "high"]
    confidence = ["medium", "high"]

    [tool.pip-audit]
    require-hashes = true
    vulnerability-service = ["pypi", "osv"]

    [tool.safety]
    ignore = []  # Add CVE IDs to ignore specific vulnerabilities
    ```

12. **Automated Security Monitoring Setup**
    - Configure dependabot or renovate for automated updates
    - Set up GitHub/GitLab security advisories
    - Configure pre-commit hooks for security scanning:
    ```yaml
    # .pre-commit-config.yaml
    repos:
    - repo: https://github.com/PyCQA/bandit
      rev: '1.7.5'
      hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']
    - repo: https://github.com/gitguardian/ggshield
      rev: v1.25.0
      hooks:
      - id: ggshield
        language: python
        stages: [commit]
    ```

13. **CI/CD Security Integration**
    - Add security scanning to GitHub Actions workflow:
    ```yaml
    name: Security Audit
    on: [push, pull_request]
    jobs:
      security:
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@v4
        - uses: astral-sh/setup-uv@v1
        - run: uv sync
        - run: uv run pip-audit --format=sarif --output=pip-audit.sarif
        - run: uv run bandit -r . -f json -o bandit-report.json
        - run: uv run safety check --json --output=safety-report.json
        - uses: github/codeql-action/upload-sarif@v2
          with:
            sarif_file: pip-audit.sarif
    ```

14. **Security Monitoring and Alerting**
    - Set up vulnerability monitoring dashboards
    - Configure security alert notifications
    - Implement security metrics tracking
    - Set up automated security report generation
    - Create security incident response procedures
    - Document security audit schedule and responsibilities

15. **Security Documentation and Training**
    - Create security guidelines for Python dependencies
    - Document approved and blocked package lists
    - Establish dependency approval process
    - Create security awareness training materials
    - Document vulnerability response procedures
    - Maintain security audit history and lessons learned

16. **Reporting and Recommendations**
    - Generate comprehensive security audit report
    - Prioritize findings by risk level and impact
    - Create actionable remediation plan with timelines
    - Provide specific upgrade recommendations with testing notes
    - Document security best practices for future development
    - Schedule regular dependency security audits

Remember to regularly update security tools and databases, test all dependency updates in staging environments, and maintain comprehensive documentation of security findings and remediation efforts. Focus on creating a sustainable security practice that integrates with the development workflow.
