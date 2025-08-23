# Python Generate API Documentation - Product Prices

Generate comprehensive API documentation for the product-prices CLI tool with MkDocs and Material theme.

## Instructions

Follow these steps to create focused API documentation for the product-prices monitoring system:

1. **Project Documentation Analysis**
   - Analyze current product-prices structure: CLI tool with scrapers for Tony McDonald and Carhartt WIP
   - Review existing docstrings in src/product_prices/ modules
   - Identify 6 core modules: cli.py, monitoring.py, scrapers/carhartt_wip.py, scrapers/tony_mcdonald.py
   - Focus on CLI usage patterns and scraper API documentation

2. **MkDocs Setup for CLI Tool Documentation**
   - Add MkDocs dependencies to existing dev dependencies:
   ```bash
   uv add --dev mkdocs mkdocs-material mkdocstrings[python]
   ```
   - Skip complex Sphinx setup - use MkDocs for simplicity and clarity
   - Configure for Python CLI tool with web scraping components

3. **MkDocs Configuration for Product-Prices**
   - Create mkdocs.yml with Material theme focused on CLI documentation:
   ```yaml
   site_name: Product Prices API Documentation
   site_description: Multi-site product price monitoring CLI tool
   theme:
     name: material
     features:
       - navigation.tabs
       - navigation.sections
       - toc.integrate
       - search.suggest
       - content.code.annotate

   plugins:
     - search
     - mkdocstrings:
         handlers:
           python:
             options:
               docstring_style: google
               show_source: true
               show_root_heading: true
               show_submodules: true

   nav:
     - Home: index.md
     - CLI Usage: cli-usage.md
     - API Reference:
       - CLI Module: api-reference/cli.md
       - Monitoring: api-reference/monitoring.md
       - Scrapers: api-reference/scrapers.md
     - Database Schema: database-schema.md
     - Development: development.md

   markdown_extensions:
     - pymdownx.highlight:
         anchor_linenums: true
     - pymdownx.superfences
     - pymdownx.tabbed:
         alternate_style: true
     - admonition
     - pymdownx.details
   ```

4. **API Reference Documentation Structure**
   - Create docs/ directory structure for product-prices:
   ```
   docs/
   ├── index.md (Project overview and quick start)
   ├── cli-usage.md (Command examples: tony-mcdonald, carhartt-wip, all)
   ├── api-reference/
   │   ├── cli.md (CLI module documentation)
   │   ├── monitoring.md (HealthChecker, MonitoringQueries)
   │   └── scrapers.md (CarharttWIPScraper, TonyMcdonald functions)
   ├── database-schema.md (SQLite schema, price_history, scraping_runs)
   └── development.md (Development setup, testing, code quality)
   ```

5. **Generate API Reference Pages**
   - Create api-reference/cli.md with mkdocstrings:
   ```markdown
   # CLI Module

   Command-line interface for product price monitoring.

   ::: product_prices.cli
   ```
   - Create api-reference/monitoring.md:
   ```markdown
   # Monitoring Module

   Database monitoring and health checking functionality.

   ::: product_prices.monitoring
   ```
   - Create api-reference/scrapers.md:
   ```markdown
   # Scrapers Module

   Web scrapers for Tony McDonald and Carhartt WIP.

   ## Carhartt WIP Scraper
   ::: product_prices.scrapers.carhartt_wip

   ## Tony McDonald Scraper
   ::: product_prices.scrapers.tony_mcdonald
   ```

6. **CLI Usage Documentation**
   - Create cli-usage.md with practical examples:
   ```markdown
   # CLI Usage

   ## Basic Commands

   ```bash
   # Run specific scrapers
   uv run python -m product_prices.cli tony-mcdonald
   uv run python -m product_prices.cli carhartt-wip
   uv run python -m product_prices.cli all

   # Monitor scraper health
   uv run python -c "from product_prices.monitoring import HealthChecker; HealthChecker('products.db').check_all()"
   ```

   ## Configuration

   Default database: `products.db`
   Supported sizes: XS, S, M (Carhartt WIP)
   Rate limiting: 5-15 second delays
   ```

7. **Database Schema Documentation**
   - Create database-schema.md from the existing products.db
   ```markdown
   # Database Schema

   ## Products Table
   Multi-source product tracking with composite keys.

   ## Price History Table
   Enhanced change tracking with specific change types.

   ## Scraping Runs Table
   Operational monitoring for scraper health.
   ```

8. **Development Documentation Integration**
   - Create development.md incorporating CLAUDE.md content:
   ```markdown
   # Development Guide

   ## Setup
   ```bash
   uv install --dev
   ```

   ## Testing
   ```bash
   uv run pytest
   uv run ruff check .
   uv run mypy src/
   ```

   ## Implementation Patterns
   Defensive parsing for Tony McDonald, data-driven for Carhartt WIP.
   ```

9. **Documentation Build Scripts**
   - Add documentation scripts to pyproject.toml:
   ```toml
   [tool.uv.scripts]
   docs-build = "mkdocs build"
   docs-serve = "mkdocs serve"
   docs-clean = "rm -rf site/"
   ```

10. **Documentation Quality for Product-Prices**
    - Use existing pydocstyle configuration from pyproject.toml
    - Focus on documenting CLI patterns and scraper APIs
    - Ensure examples work with actual product-prices commands
    - Validate that all 6 Python modules are properly documented

11. **Local Documentation Testing**
    - Build and serve documentation locally:
    ```bash
    uv run docs-build
    uv run docs-serve
    ```
    - Verify API reference generation from docstrings
    - Test navigation between CLI usage and API reference
    - Ensure database schema documentation is accurate

12. **Documentation Maintenance**
    - Keep focused on actual CLI usage patterns
    - Update when new scrapers are added
    - Maintain alignment with CLAUDE.md development guidelines
    - Skip complex deployment automation - focus on local development use

Remember: This is a CLI tool documentation, not a web API. Focus on command usage, scraper configuration, and development patterns rather than REST endpoints or complex deployment scenarios.
