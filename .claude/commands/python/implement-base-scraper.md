# Implement Base Scraper Architecture

Implement the core scraper architecture for multi-site price monitoring system with exact API specification compliance

## Instructions

Follow these steps to implement the complete base scraper architecture according to the API_SPEC.md requirements:

1. **Project Structure Verification**
   - Verify the project has been initialized with proper directory structure
   - Check for uv configuration and dependency management setup
   - Ensure database, models, and scraper directories exist
   - Validate that all required dependencies are installed
   - Create missing directories if needed following the established structure

2. **Data Models Implementation**
   - Create `src/models/product.py` with exact Product dataclass from API spec:
     ```python
     @dataclass
     class Product:
         sku: str                    # Unique identifier within source
         source: str                 # Source identifier
         name: str                   # Product display name
         url: str | None             # Direct product URL
         current_price: str | None   # Current/sale price as string
         original_price: str | None  # Original/MSRP price as string
         currency: str              # Currency code (e.g., "GBP", "USD")
         in_stock: bool             # Availability status
         last_seen: datetime        # When product was last observed
         metadata: dict[str, Any]   # Source-specific additional data
     ```
   - Create `src/models/price_change.py` with PriceChange dataclass:
     ```python
     @dataclass
     class PriceChange:
         sku: str
         source: str
         old_price: str | None
         new_price: str | None
         old_original_price: str | None
         new_original_price: str | None
         change_type: ChangeType     # NEW, REMOVED, PRICE_DROP, PRICE_INCREASE
         detected_at: datetime
     ```
   - Create `src/models/scraping_result.py` with ScrapingResult dataclass
   - Add ChangeType enum with values: NEW, REMOVED, PRICE_DROP, PRICE_INCREASE, STOCK_CHANGE
   - Implement proper datetime handling with timezone awareness
   - Add JSON serialization methods using dataclasses.asdict() and custom datetime encoder
   - Include validation methods for price string formats and currency codes

3. **Database Schema Implementation**
   - Create `src/database/schema.py` with exact SQLite schema from API spec:
     ```sql
     CREATE TABLE products (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         sku TEXT NOT NULL,
         source TEXT NOT NULL,
         name TEXT NOT NULL,
         url TEXT,
         current_price TEXT,
         original_price TEXT,
         currency TEXT DEFAULT 'GBP',
         in_stock BOOLEAN DEFAULT TRUE,
         metadata JSON,
         first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
         last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
         UNIQUE(sku, source)
     );
     ```
   - Include price_history and scraping_runs tables with proper foreign keys
   - Add all performance indexes: idx_products_source_sku, idx_products_last_seen, etc.
   - Create database initialization functions with proper error handling
   - Implement database migration system for schema updates
   - Add database connection context manager for transaction safety

4. **Error Handling System**
   - Create `src/utils/exceptions.py` with exact exception hierarchy from API spec:
     ```python
     class ScrapingError(Exception):
         """Base exception for scraping errors."""
         pass

     class NetworkError(ScrapingError):
         """Network-related errors (timeouts, connection issues)."""
         pass

     class ParseError(ScrapingError):
         """HTML parsing errors (selectors not found, unexpected structure)."""
         pass

     class RateLimitError(ScrapingError):
         """Rate limiting or anti-bot detection."""
         pass

     class ConfigurationError(ScrapingError):
         """Configuration or setup errors."""
         pass
     ```
   - Add detailed error context with URL, source, and operation information
   - Implement error recovery strategies for each exception type
   - Create error aggregation for batch operations
   - Add structured logging integration with error details

5. **BaseScraper Abstract Class Implementation**
   - Create `src/scrapers/base_scraper.py` with exact interface from API spec:
     ```python
     from abc import ABC, abstractmethod

     class BaseScraper(ABC):
         def __init__(self, source_name: str, base_url: str, db_path: Path) -> None:
             self.source_name = source_name
             self.base_url = base_url
             self.db_path = db_path
             self.session = requests.Session()
             self._setup_session()

         @abstractmethod
         def get_urls(self) -> list[str]:
             """Return list of URLs to scrape."""
             pass

         @abstractmethod
         def parse_product_page(self, url: str, content: str) -> list[Product]:
             """Parse products from a single page."""
             pass

         @abstractmethod
         def get_product_selector(self) -> str:
             """Return CSS selector for product containers."""
             pass
     ```
   - Implement all concrete methods: fetch_current_products(), detect_changes(), save_products(), run()
   - Add proper type hints throughout the class
   - Include comprehensive docstrings for all methods

6. **Session Management and HTTP Handling**
   - Implement `_setup_session()` method with proper User-Agent headers:
     ```python
     def _setup_session(self) -> None:
         self.session.headers.update({
             'User-Agent': 'Mozilla/5.0 (compatible; PriceMonitor/1.0; +https://example.com/bot)',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Language': 'en-US,en;q=0.5',
             'Accept-Encoding': 'gzip, deflate',
             'Connection': 'keep-alive',
             'Upgrade-Insecure-Requests': '1',
         })
         self.session.timeout = 30
     ```
   - Add configurable timeout handling (default 30 seconds)
   - Implement connection pooling with proper session management
   - Add SSL verification and certificate handling
   - Create request wrapper with automatic retries

7. **Rate Limiting Implementation**
   - Create `src/utils/rate_limiter.py` with configurable delays:
     ```python
     class RateLimiter:
         def __init__(self, min_delay: float = 5.0, max_delay: float = 15.0):
             self.min_delay = min_delay
             self.max_delay = max_delay
             self.last_request_time = 0.0

         def wait(self) -> None:
             """Wait appropriate time before next request."""
             current_time = time.time()
             elapsed = current_time - self.last_request_time
             delay = random.uniform(self.min_delay, self.max_delay)
             if elapsed < delay:
                 time.sleep(delay - elapsed)
             self.last_request_time = time.time()
     ```
   - Integrate rate limiter into BaseScraper with configurable delays (5-15 seconds)
   - Add per-domain rate limiting support
   - Implement exponential backoff for failed requests
   - Add burst protection and request queuing

8. **Retry Logic with Exponential Backoff**
   - Create `src/utils/retry.py` with configurable retry strategies:
     ```python
     def retry_with_backoff(
         func: Callable,
         max_retries: int = 3,
         base_delay: float = 1.0,
         max_delay: float = 60.0,
         backoff_factor: float = 2.0,
         exceptions: tuple[Exception, ...] = (NetworkError, requests.RequestException)
     ) -> Any:
         """Retry function with exponential backoff."""
     ```
   - Integrate retry logic into HTTP requests
   - Add jitter to prevent thundering herd
   - Implement different retry strategies for different error types
   - Add retry statistics and logging

9. **Product Fetching Implementation**
   - Implement `fetch_current_products()` method in BaseScraper:
     ```python
     def fetch_current_products(self) -> dict[str, Product]:
         """Fetch all current products from all URLs."""
         products = {}
         for url in self.get_urls():
             try:
                 self.rate_limiter.wait()
                 response = self.session.get(url)
                 response.raise_for_status()

                 page_products = self.parse_product_page(url, response.text)
                 for product in page_products:
                     products[f"{product.source}:{product.sku}"] = product

             except Exception as e:
                 logger.error(f"Failed to fetch {url}: {e}")

         return products
     ```
   - Add progress tracking with rich progress bars
   - Implement concurrent fetching with asyncio (optional)
   - Add response caching to minimize server load
   - Include content validation and encoding detection

10. **Change Detection Algorithm**
    - Implement `detect_changes()` method with comprehensive comparison:
      ```python
      def detect_changes(self, current: dict[str, Product]) -> list[PriceChange]:
          """Compare current products with database and detect changes."""
          changes = []
          stored_products = self._load_stored_products()

          # Detect new products
          for key, product in current.items():
              if key not in stored_products:
                  changes.append(PriceChange(
                      sku=product.sku,
                      source=product.source,
                      old_price=None,
                      new_price=product.current_price,
                      old_original_price=None,
                      new_original_price=product.original_price,
                      change_type=ChangeType.NEW,
                      detected_at=datetime.now()
                  ))

          # Detect removed products
          for key, stored_product in stored_products.items():
              if key not in current:
                  changes.append(PriceChange(
                      sku=stored_product.sku,
                      source=stored_product.source,
                      old_price=stored_product.current_price,
                      new_price=None,
                      old_original_price=stored_product.original_price,
                      new_original_price=None,
                      change_type=ChangeType.REMOVED,
                      detected_at=datetime.now()
                  ))

          # Detect price changes
          for key, product in current.items():
              if key in stored_products:
                  stored = stored_products[key]
                  if stored.current_price != product.current_price:
                      change_type = ChangeType.PRICE_DROP if self._is_price_decrease(
                          stored.current_price, product.current_price
                      ) else ChangeType.PRICE_INCREASE

                      changes.append(PriceChange(
                          sku=product.sku,
                          source=product.source,
                          old_price=stored.current_price,
                          new_price=product.current_price,
                          old_original_price=stored.original_price,
                          new_original_price=product.original_price,
                          change_type=change_type,
                          detected_at=datetime.now()
                      ))

          return changes
      ```
    - Add price comparison logic with currency handling
    - Implement stock status change detection
    - Add metadata comparison for detecting product updates
    - Include change significance filtering (minimum change thresholds)

11. **Database Operations Implementation**
    - Implement `save_products()` method with proper transaction handling:
      ```python
      def save_products(self, products: dict[str, Product]) -> None:
          """Save products to database with transaction safety."""
          with sqlite3.connect(self.db_path) as conn:
              conn.execute("BEGIN TRANSACTION")
              try:
                  for product in products.values():
                      conn.execute("""
                          INSERT OR REPLACE INTO products
                          (sku, source, name, url, current_price, original_price,
                           currency, in_stock, metadata, last_seen)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                      """, (
                          product.sku, product.source, product.name, product.url,
                          product.current_price, product.original_price,
                          product.currency, product.in_stock,
                          json.dumps(product.metadata), product.last_seen
                      ))
                  conn.execute("COMMIT")
              except Exception as e:
                  conn.execute("ROLLBACK")
                  raise DatabaseError(f"Failed to save products: {e}")
      ```
    - Add batch insert operations for performance
    - Implement database connection pooling
    - Add data validation before database operations
    - Include database backup before major operations

12. **Complete Scraping Workflow**
    - Implement the main `run()` method that orchestrates the entire process:
      ```python
      def run(self) -> ScrapingResult:
          """Execute complete scraping workflow."""
          start_time = time.time()
          errors = []

          try:
              # Fetch current products
              logger.info(f"Starting scrape for {self.source_name}")
              current_products = self.fetch_current_products()

              # Detect changes
              changes = self.detect_changes(current_products)

              # Save products and changes
              self.save_products(current_products)
              self._save_price_changes(changes)

              # Calculate statistics
              result = ScrapingResult(
                  source=self.source_name,
                  url=self.base_url,
                  products_found=len(current_products),
                  products_added=sum(1 for c in changes if c.change_type == ChangeType.NEW),
                  products_removed=sum(1 for c in changes if c.change_type == ChangeType.REMOVED),
                  products_changed=sum(1 for c in changes if c.change_type in [ChangeType.PRICE_DROP, ChangeType.PRICE_INCREASE]),
                  duration_seconds=time.time() - start_time,
                  errors=errors,
                  timestamp=datetime.now()
              )

              # Save scraping run record
              self._save_scraping_result(result)

              logger.info(f"Completed scrape for {self.source_name}: {result}")
              return result

          except Exception as e:
              logger.error(f"Scraping failed for {self.source_name}: {e}")
              errors.append(str(e))
              raise
      ```
    - Add comprehensive error handling throughout the workflow
    - Implement graceful degradation for partial failures
    - Add performance metrics collection
    - Include memory usage monitoring

13. **Logging and Monitoring Integration**
    - Create `src/utils/logger.py` with structured logging:
      ```python
      import structlog

      def setup_logging(level: str = "INFO") -> None:
          structlog.configure(
              processors=[
                  structlog.stdlib.filter_by_level,
                  structlog.stdlib.add_logger_name,
                  structlog.stdlib.add_log_level,
                  structlog.stdlib.PositionalArgumentsFormatter(),
                  structlog.processors.TimeStamper(fmt="iso"),
                  structlog.processors.StackInfoRenderer(),
                  structlog.processors.format_exc_info,
                  structlog.processors.UnicodeDecoder(),
                  structlog.processors.JSONRenderer()
              ],
              context_class=dict,
              logger_factory=structlog.stdlib.LoggerFactory(),
              wrapper_class=structlog.stdlib.BoundLogger,
              cache_logger_on_first_use=True,
          )
      ```
    - Integrate structured logging throughout BaseScraper
    - Add performance metrics logging (response times, success rates)
    - Implement log rotation and archival
    - Add monitoring hooks for external systems

14. **Configuration Management**
    - Create `src/utils/config.py` with Pydantic models for configuration:
      ```python
      from pydantic import BaseSettings

      class ScraperConfig(BaseSettings):
          enabled: bool = True
          delay_range: tuple[int, int] = (5, 15)
          max_retries: int = 3
          timeout: int = 30
          custom_settings: dict[str, Any] = {}

      class GlobalConfig(BaseSettings):
          database_path: Path
          log_level: str = "INFO"
          scrapers: dict[str, ScraperConfig] = {}

          class Config:
              env_file = ".env"
              env_prefix = "SCRAPER_"
      ```
    - Add environment variable support
    - Implement configuration validation
    - Add hot-reloading capability for development
    - Create configuration file templates

15. **Testing Infrastructure Setup**
    - Create `tests/test_base_scraper.py` with comprehensive test coverage:
      ```python
      import pytest
      from unittest.mock import Mock, patch
      from src.scrapers.base_scraper import BaseScraper
      from src.models.product import Product

      class TestBaseScraper:
          def test_session_setup(self):
              """Test session configuration."""
              pass

          def test_rate_limiting(self):
              """Test rate limiting functionality."""
              pass

          def test_change_detection(self):
              """Test change detection algorithm."""
              pass

          def test_error_handling(self):
              """Test error handling and recovery."""
              pass
      ```
    - Add fixtures for database testing with temporary SQLite
    - Create mock HTTP responses for scraper testing
    - Implement integration tests for complete workflows
    - Add performance tests for database operations

16. **Example Site-Specific Implementation**
    - Create example implementation showing how to extend BaseScraper:
      ```python
      class ExampleScraper(BaseScraper):
          def __init__(self, db_path: Path) -> None:
              super().__init__(
                  source_name="example_site",
                  base_url="https://example.com",
                  db_path=db_path
              )

          def get_urls(self) -> list[str]:
              return ["https://example.com/products"]

          def get_product_selector(self) -> str:
              return "div.product-item"

          def parse_product_page(self, url: str, content: str) -> list[Product]:
              soup = BeautifulSoup(content, "html.parser")
              products = []

              for item in soup.select(self.get_product_selector()):
                  # Example parsing logic
                  sku = item.get("data-sku")
                  name = item.select_one("h3.product-name").get_text(strip=True)
                  price = item.select_one("span.price").get_text(strip=True)

                  product = Product(
                      sku=sku,
                      source=self.source_name,
                      name=name,
                      url=f"{self.base_url}/product/{sku}",
                      current_price=price,
                      original_price=None,
                      currency="GBP",
                      in_stock=True,
                      last_seen=datetime.now(),
                      metadata={}
                  )
                  products.append(product)

              return products
      ```
    - Include detailed comments explaining the implementation
    - Add error handling examples for common parsing issues
    - Show how to handle different product page structures

17. **Performance Optimization**
    - Add database query optimization with proper indexing
    - Implement connection pooling for concurrent operations
    - Add memory-efficient product processing for large catalogs
    - Optimize string operations and price parsing
    - Add caching strategies for repeated operations

18. **Documentation and Examples**
    - Create comprehensive docstrings for all classes and methods
    - Add inline comments explaining complex logic
    - Include usage examples in class docstrings
    - Document error handling strategies
    - Add troubleshooting guide for common issues

19. **Integration with uv and Modern Python Tools**
    - Ensure compatibility with uv package management
    - Add proper type hints throughout the codebase
    - Use modern Python features (3.9+ syntax)
    - Integrate with ruff for linting and formatting
    - Add mypy configuration for type checking

20. **Validation and Testing**
    - Verify all abstract methods are properly implemented
    - Test database schema creation and migration
    - Validate error handling with various failure scenarios
    - Test rate limiting and retry logic
    - Verify proper resource cleanup and memory management
    - Test complete workflow with mock data
    - Ensure proper logging output and structure

The implementation should exactly match the API_SPEC.md requirements while providing a robust, scalable foundation for the multi-site price monitoring system. All classes, methods, and data structures must follow the exact specifications provided in the API documentation.
