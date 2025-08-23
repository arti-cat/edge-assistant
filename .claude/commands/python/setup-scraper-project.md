# Setup Product Price Monitoring Project

Initialize the multi-site product price monitoring system for Tony McDonald and Carhartt WIP with modern Python tooling

## Instructions

1. **First, Think About the Multi-Scraper Architecture**

Before starting, ask Claude to think through the requirements:

```
Think about our product price monitoring system:
1. Two-scraper architecture: Tony McDonald (existing) + Carhartt WIP (new)
2. How Carhartt WIP's data-driven approach differs from Tony McDonald's defensive parsing
3. Database schema needs for multi-source support (sku, source) composite keys
4. CLI integration for running specific scrapers or all scrapers
```

**Project Analysis and Requirements**
   - Target websites: Tony McDonald (climbing gear) and Carhartt WIP (workwear/streetwear)
   - Product categories: Sale items, Carhartt WIP size filters (XS, S, M)
   - Tony McDonald: Single page with complex parsing (already implemented)
   - Carhartt WIP: Multi-page (14+) with excellent data attributes
   - Validate that scraping approaches respect site policies and rate limits

2. **Verify Existing Project Structure**
   - Check that project already has proper structure (initialized with uv)
   - Verify existing directories match our needs:
     ```
     product-prices/
     ├── src/
     │   └── product_prices/
     │       ├── __init__.py
     │       ├── cli.py (existing)
     │       └── scrapers/
     │           ├── __init__.py
     │           └── tony_mcdonald.py (existing)
     ├── tests/
     │   ├── __init__.py
     │   ├── conftest.py
     │   └── test_tony_mcdonald.py (existing)
     ├── docs/ (existing with PRD.md and API_SPEC.md)
     └── pyproject.toml (existing)
     ```
   - Create missing directories for multi-scraper architecture:
     ```bash
     mkdir -p src/product_prices/models
     mkdir -p src/product_prices/database
     mkdir -p src/product_prices/utils
     mkdir -p tests/test_scrapers
     mkdir -p config
     ```
   - Ensure .gitignore includes: `*.db`, `logs/`, `htmlcov/`, `.coverage`

3. **Verify and Add Dependencies**
   - Check existing dependencies in pyproject.toml
   - Core dependencies already installed: `requests`, `beautifulsoup4`
   - Add missing dependencies if needed: `uv add lxml python-dateutil`
   - Verify type checking support: `types-requests` should be installed

4. **Development Dependencies Check**
   - Verify testing framework: `pytest`, `pytest-cov` should be installed
   - Check code quality tools: `ruff`, `mypy` should be installed
   - Add any missing dev dependencies:
     ```bash
     uv add --dev pytest-mock responses
     ```
   - Ensure pre-commit hooks are configured (if desired)

5. **Data Models Setup (API_SPEC.md Compliance)**
   - Create `src/product_prices/models/product.py` with exact Product dataclass:
     ```python
     @dataclass
     class Product:
         sku: str                    # Unique identifier within source
         source: str                 # Source identifier (tony_mcdonald, carhartt_wip)
         name: str                   # Product display name
         url: str | None             # Direct product URL
         current_price: str | None   # Current/sale price as string (e.g., "22.50")
         original_price: str | None  # Original/MSRP price as string (e.g., "45.00")
         currency: str              # Currency code (GBP)
         in_stock: bool             # Availability status
         last_seen: datetime        # When product was last observed
         metadata: dict[str, Any]   # Source-specific additional data
     ```
   - Create PriceChange and ScrapingResult dataclasses per API spec
   - Add ChangeType enum: NEW, REMOVED, PRICE_DROP, PRICE_INCREASE
   - Include JSON serialization methods

6. **Database Schema Implementation (Multi-Source)**
   - Create `src/product_prices/database/schema.py` with exact schema from API_SPEC.md:
     - products table with (sku, source) composite unique key
     - price_history table for tracking changes over time
     - scraping_runs table for monitoring and debugging
   - Implement database connection management with context managers
   - Add indexes: idx_products_source_sku, idx_products_last_seen, etc.
   - Create database initialization functions

7. **Base Scraper Architecture**
   - Create abstract BaseScraper class with methods: scrape(), parse_product(), save_results(), handle_errors()
   - Implement rate limiting with configurable delays between requests
   - Add request retry logic with exponential backoff
   - Create user-agent rotation system for respectful scraping
   - Implement session management with cookie persistence
   - Add proxy support configuration (optional)

8. **Site-Specific Scrapers (Focus on Carhartt WIP)**
   - TonyMcDonaldScraper (already implemented):
     - Complex defensive parsing with fallbacks
     - Single page with size filters
   - CarharttWipScraper (new implementation):
     - Data-driven parsing with clean selectors: `article.product-grid-item`
     - Size filtering for XS, S, M: `?filter_size=XS&filter_size=S&filter_size=M`
     - Pagination handling for 14+ pages: `?page=1` through `?page=14`
     - Price extraction: `span.strikeout.country_gbp` (original), `span.sale.country_gbp` (current)
   - Add configuration with Carhartt-specific selectors and URL patterns

**Verification Step**: Ask Claude to verify the Carhartt scraper works with carhartt_sample.html before proceeding.

9. **Configuration System**
   - Create TOML configuration files for:
     - Scraper settings (delays, retries, user agents)
     - Database connection parameters
     - Logging levels and output formats
     - Rate limiting rules per site
   - Implement environment-specific configurations (dev, staging, prod)
   - Add configuration validation with Pydantic models
   - Create configuration hot-reloading capability

10. **Logging and Monitoring**
    - Set up structured logging with JSON format
    - Create log rotation and archival system
    - Implement different log levels for debugging vs production
    - Add performance metrics logging (response times, success rates)
    - Create error tracking and alerting system
    - Set up scraping statistics dashboard preparation

11. **CLI Interface Development**
    - Create main CLI entry point with Click
    - Implement commands: scrape, init-db, list-products, check-prices, export-data
    - Add command options for: --site, --category, --output-format, --verbose
    - Create interactive mode for configuration setup
    - Implement progress bars and status reporting with Rich
    - Add dry-run capability for testing scrapers

12. **Error Handling and Resilience**
    - Implement comprehensive exception handling for network errors
    - Add HTML parsing error recovery
    - Create database transaction rollback mechanisms
    - Implement graceful shutdown handling
    - Add data validation and sanitization
    - Create error notification system (optional email/webhook alerts)

13. **Testing Infrastructure**
    - Set up pytest with fixtures for scrapers and database
    - Create mock HTTP responses for scraper testing
    - Implement database testing with temporary SQLite instances
    - Add integration tests for end-to-end scraping workflows
    - Create performance tests for database operations
    - Set up test data fixtures and factories

14. **Ethical Scraping Configuration**
    - Create robots.txt compliance checker
    - Implement respectful rate limiting (default 1-2 second delays)
    - Add terms of service awareness documentation
    - Create scraping ethics guidelines in README
    - Implement request caching to minimize server load
    - Add optional CDN/cache detection to avoid unnecessary requests

15. **Development Scripts and Automation**
    - Create database initialization script with sample data
    - Build automated scraper execution script with scheduling
    - Implement data export utilities (JSON, CSV, Excel)
    - Create database cleanup and maintenance scripts
    - Add development server for API preview (optional)
    - Set up automated backup procedures

16. **API Foundation Setup**
    - Create FastAPI app structure for future API endpoints
    - Implement basic REST endpoints: GET /products, GET /price-changes
    - Add API response models matching CLI output
    - Set up API documentation with OpenAPI/Swagger
    - Implement API authentication preparation (tokens, keys)
    - Create API rate limiting and usage monitoring

17. **CI/CD Pipeline Configuration**
    - Create GitHub Actions workflow for Python testing
    - Set up automated testing across Python versions (3.9+)
    - Configure automated dependency security scanning
    - Add linting and code quality checks
    - Set up database migration testing
    - Create deployment preparation for cloud hosting

18. **Documentation Generation**
    - Generate comprehensive README with setup instructions
    - Create API documentation with example requests/responses
    - Document scraper configuration and customization
    - Add troubleshooting guide for common scraping issues
    - Create developer onboarding guide
    - Document ethical scraping practices and legal considerations

19. **Security and Best Practices**
    - Implement secure credential management for API keys
    - Add SQL injection prevention measures
    - Set up input validation and sanitization
    - Configure secure HTTP headers for API endpoints
    - Implement audit logging for data access
    - Add GDPR compliance considerations documentation

20. **Project Validation and Initial Setup**
    - Verify uv installation and dependency resolution
    - Test database schema creation and migration
    - Validate scraper base classes and inheritance
    - Test CLI commands and option parsing
    - Verify logging configuration and output
    - Run initial scraper test with sample data
    - Create initial git commit with complete project structure

21. **Example Configuration Templates**

    **Scraper Configuration (config/scraper_config.toml):**
    ```toml
    [global]
    default_delay = 2.0
    max_retries = 3
    timeout = 30
    user_agents = [
        "Mozilla/5.0 (compatible; PriceMonitor/1.0; +https://example.com/bot)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    ]

    [tony_mcdonald]
    base_url = "https://tonymcdonald.com"
    product_list_url = "/collections/all"
    delay = 2.5
    respect_robots_txt = true
    categories = ["clothing", "accessories", "footwear"]

    [carhartt_wip]
    base_url = "https://www.carhartt-wip.com"
    product_list_url = "/en/men"
    delay = 3.0
    respect_robots_txt = true
    categories = ["workwear", "streetwear", "accessories"]
    ```

    **Database Schema (src/database/schema.py):**
    ```python
    CREATE_TABLES = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        brand TEXT NOT NULL,
        category TEXT,
        current_price REAL,
        original_price REAL,
        discount_percentage REAL,
        availability BOOLEAN,
        product_url TEXT UNIQUE NOT NULL,
        image_url TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS price_changes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        old_price REAL,
        new_price REAL,
        change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        change_percentage REAL,
        FOREIGN KEY (product_id) REFERENCES products (id)
    );

    CREATE TABLE IF NOT EXISTS scraping_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scraper_name TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        products_found INTEGER,
        errors_encountered INTEGER,
        execution_time REAL
    );
    """
    ```

22. **CLI Command Examples**
    ```bash
    # Initialize database
    uv run python -m src.cli.main init-db

    # Run specific scraper
    uv run python -m src.cli.main scrape --site tony_mcdonald --category clothing

    # Check for price changes
    uv run python -m src.cli.main check-prices --since "2024-01-01"

    # Export data
    uv run python -m src.cli.main export --format json --output products.json

    # Run all scrapers
    uv run python scripts/run_scrapers.py
    ```
