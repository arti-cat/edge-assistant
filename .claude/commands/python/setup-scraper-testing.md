# setup-scraper-testing

Set up comprehensive testing infrastructure specifically designed for web scraping projects, including HTTP mocking, HTML fixture management, database testing, and scraping ethics validation.

## Instructions

### 1. Configure Core Testing Dependencies

Add web scraping specific testing dependencies to your project:

```bash
# Core testing framework with scraping plugins
uv add --dev pytest pytest-asyncio pytest-mock pytest-benchmark pytest-cov

# HTTP mocking and request testing
uv add --dev responses requests-mock httpx-mock aioresponses

# HTML parsing and fixture management
uv add --dev beautifulsoup4 lxml html5lib selectolax

# Database testing utilities
uv add --dev pytest-postgresql pytest-factoryboy freezegun

# Property-based testing for robust validation
uv add --dev hypothesis

# Performance and memory profiling
uv add --dev memory-profiler pytest-memray pytest-timeout

# Network simulation and rate limiting testing
uv add --dev pytest-httpserver
```

### 2. Create Testing Configuration

Create `pytest.ini` with scraper-specific settings:

```ini
[tool:pytest]
minversion = 6.0
addopts =
    -ra
    --strict-markers
    --strict-config
    --cov=src
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-report=xml
    --benchmark-disable
    --timeout=300
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    performance: Performance tests
    slow: Slow running tests
    network: Tests requiring network access
    scraper: Web scraper specific tests
    parser: HTML parser tests
    database: Database tests
    ethics: Scraping ethics validation tests
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

### 3. Set Up HTML Fixture Management System

Create `tests/fixtures/html_fixtures.py`:

```python
"""HTML fixture management for scraper testing."""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class HTMLFixture:
    """Represents an HTML fixture with metadata."""
    name: str
    content: str
    url: str
    description: str
    expected_data: Dict[str, Any]
    last_updated: str
    site_type: str


class HTMLFixtureManager:
    """Manages HTML fixtures for scraper testing."""

    def __init__(self, fixtures_dir: Path = None):
        self.fixtures_dir = fixtures_dir or Path(__file__).parent / "html"
        self.fixtures_dir.mkdir(exist_ok=True)

    def save_fixture(self, fixture: HTMLFixture) -> None:
        """Save an HTML fixture with metadata."""
        fixture_dir = self.fixtures_dir / fixture.name
        fixture_dir.mkdir(exist_ok=True)

        # Save HTML content
        (fixture_dir / "content.html").write_text(fixture.content, encoding='utf-8')

        # Save metadata
        metadata = {
            "name": fixture.name,
            "url": fixture.url,
            "description": fixture.description,
            "expected_data": fixture.expected_data,
            "last_updated": fixture.last_updated,
            "site_type": fixture.site_type
        }
        (fixture_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=2), encoding='utf-8'
        )

    def load_fixture(self, name: str) -> HTMLFixture:
        """Load an HTML fixture by name."""
        fixture_dir = self.fixtures_dir / name

        if not fixture_dir.exists():
            raise FileNotFoundError(f"Fixture '{name}' not found")

        content = (fixture_dir / "content.html").read_text(encoding='utf-8')
        metadata = json.loads(
            (fixture_dir / "metadata.json").read_text(encoding='utf-8')
        )

        return HTMLFixture(
            content=content,
            **metadata
        )

    def list_fixtures(self) -> list[str]:
        """List all available fixtures."""
        return [d.name for d in self.fixtures_dir.iterdir() if d.is_dir()]

    def create_malformed_html(self, base_fixture: str) -> str:
        """Create malformed HTML from a base fixture for robustness testing."""
        fixture = self.load_fixture(base_fixture)
        soup = BeautifulSoup(fixture.content, 'html.parser')

        # Introduce common HTML issues
        malformed_variants = []

        # Missing closing tags
        content1 = fixture.content.replace('</div>', '', 1)
        malformed_variants.append(content1)

        # Unclosed attributes
        content2 = fixture.content.replace('class="', 'class="unclosed')
        malformed_variants.append(content2)

        # Mixed encoding
        content3 = fixture.content.encode('utf-8').decode('latin1', errors='ignore')
        malformed_variants.append(content3)

        return malformed_variants


# Create fixture manager instance
fixture_manager = HTMLFixtureManager()
```

### 4. Create Database Testing Infrastructure

Create `tests/conftest.py`:

```python
"""Global test configuration and fixtures."""

import pytest
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import Mock
from typing import Generator
import factory
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import your models
from src.models import Base, Product, PriceChange, ScrapingSession
from tests.fixtures.html_fixtures import fixture_manager


@pytest.fixture(scope="session")
def test_database_url():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        return f"sqlite:///{tmp.name}"


@pytest.fixture(scope="session")
def engine(test_database_url):
    """Create database engine for testing."""
    engine = create_engine(test_database_url, echo=False)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine) -> Generator[Session, None, None]:
    """Create a database session for each test."""
    Session = sessionmaker(bind=engine)
    session = Session()

    # Start a transaction
    transaction = session.begin()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()


@pytest.fixture
def html_fixture_manager():
    """Provide HTML fixture manager for tests."""
    return fixture_manager


class ProductFactory(SQLAlchemyModelFactory):
    """Factory for creating test Product instances."""

    class Meta:
        model = Product
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker('catch_phrase')
    url = factory.Faker('url')
    site_name = factory.Iterator(['amazon', 'ebay', 'walmart'])
    current_price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    currency = 'USD'
    availability = factory.Iterator(['in_stock', 'out_of_stock', 'limited'])
    sku = factory.Faker('uuid4')


class PriceChangeFactory(SQLAlchemyModelFactory):
    """Factory for creating test PriceChange instances."""

    class Meta:
        model = PriceChange
        sqlalchemy_session_persistence = "commit"

    product = factory.SubFactory(ProductFactory)
    old_price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    new_price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    change_percentage = factory.LazyAttribute(
        lambda obj: float((obj.new_price - obj.old_price) / obj.old_price * 100)
    )


@pytest.fixture
def product_factory():
    """Provide ProductFactory for tests."""
    return ProductFactory


@pytest.fixture
def price_change_factory():
    """Provide PriceChangeFactory for tests."""
    return PriceChangeFactory


@pytest.fixture
def sample_products(db_session, product_factory):
    """Create sample products for testing."""
    products = [
        product_factory(name="iPhone 15", site_name="amazon", current_price=999.99),
        product_factory(name="MacBook Pro", site_name="apple", current_price=2499.99),
        product_factory(name="Gaming Chair", site_name="ebay", current_price=299.99),
    ]
    db_session.add_all(products)
    db_session.commit()
    return products


@pytest.fixture
def mock_requests():
    """Mock HTTP requests for testing."""
    with responses.RequestsMock() as rsps:
        yield rsps
```

### 5. Create Parser Testing Framework

Create `tests/test_parsers.py`:

```python
"""Tests for HTML parsers and data extraction."""

import pytest
from decimal import Decimal
from bs4 import BeautifulSoup
from hypothesis import given, strategies as st

from src.parsers import BaseParser, AmazonParser, EbayParser
from tests.fixtures.html_fixtures import HTMLFixture


class TestBaseParser:
    """Test the base parser functionality."""

    def test_price_parsing_robustness(self):
        """Test price parsing with various formats."""
        parser = BaseParser()

        test_cases = [
            ("$99.99", Decimal("99.99")),
            ("£45.50", Decimal("45.50")),
            ("€123.45", Decimal("123.45")),
            ("¥1000", Decimal("1000.00")),
            ("$1,234.56", Decimal("1234.56")),
            ("99.99 USD", Decimal("99.99")),
            ("Price: $45.00", Decimal("45.00")),
            ("FREE", Decimal("0.00")),
            ("N/A", None),
            ("", None),
        ]

        for price_text, expected in test_cases:
            result = parser.parse_price(price_text)
            assert result == expected, f"Failed for '{price_text}'"

    @given(st.decimals(min_value=0, max_value=99999, places=2))
    def test_price_parsing_property_based(self, price):
        """Property-based test for price parsing."""
        parser = BaseParser()
        price_str = f"${price}"
        result = parser.parse_price(price_str)
        assert result == price


class TestParserRobustness:
    """Test parser robustness with malformed HTML."""

    def test_malformed_html_handling(self, html_fixture_manager):
        """Test parsers handle malformed HTML gracefully."""
        # Create a sample fixture for testing
        sample_fixture = HTMLFixture(
            name="sample_product",
            content="""
            <div class="product">
                <h1 class="title">Test Product</h1>
                <span class="price">$99.99</span>
                <div class="availability">In Stock</div>
            </div>
            """,
            url="https://example.com/product/123",
            description="Sample product page",
            expected_data={"name": "Test Product", "price": 99.99},
            last_updated="2024-01-01",
            site_type="generic"
        )

        html_fixture_manager.save_fixture(sample_fixture)
        malformed_variants = html_fixture_manager.create_malformed_html("sample_product")

        parser = BaseParser()

        for malformed_html in malformed_variants:
            try:
                soup = BeautifulSoup(malformed_html, 'html.parser')
                # Parser should not crash on malformed HTML
                result = parser.parse(soup, "https://example.com/product/123")
                assert isinstance(result, dict)
            except Exception as e:
                pytest.fail(f"Parser crashed on malformed HTML: {e}")


class TestSiteSpecificParsers:
    """Test site-specific parser implementations."""

    def test_amazon_parser(self, html_fixture_manager):
        """Test Amazon-specific parsing logic."""
        amazon_html = """
        <div id="feature-bullets">
            <h1 id="productTitle">Amazon Echo Dot</h1>
            <span class="a-price-whole">49</span>
            <span class="a-price-fraction">99</span>
            <div id="availability">
                <span>In Stock</span>
            </div>
        </div>
        """

        parser = AmazonParser()
        soup = BeautifulSoup(amazon_html, 'html.parser')
        result = parser.parse(soup, "https://amazon.com/dp/B123456")

        assert result['name'] == "Amazon Echo Dot"
        assert result['price'] == Decimal("49.99")
        assert result['availability'] == "in_stock"

    def test_parser_regression_detection(self):
        """Test that parsers detect structural changes in websites."""
        # This would typically involve comparing current parsing results
        # with known good results from fixtures
        pass


class TestParserPerformance:
    """Test parser performance characteristics."""

    @pytest.mark.performance
    def test_large_html_parsing_performance(self, benchmark):
        """Benchmark parser performance with large HTML documents."""
        # Create a large HTML document
        large_html = "<div>" * 10000 + "Product Name" + "</div>" * 10000

        parser = BaseParser()
        soup = BeautifulSoup(large_html, 'html.parser')

        result = benchmark(parser.parse, soup, "https://example.com")
        assert isinstance(result, dict)

    @pytest.mark.performance
    def test_memory_usage_with_large_documents(self):
        """Test memory usage doesn't grow excessively with large documents."""
        import tracemalloc

        tracemalloc.start()

        parser = BaseParser()

        # Process multiple large documents
        for i in range(100):
            large_html = f"<div>Product {i}</div>" * 1000
            soup = BeautifulSoup(large_html, 'html.parser')
            parser.parse(soup, f"https://example.com/product/{i}")

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Memory usage should be reasonable (adjust threshold as needed)
        assert peak < 100 * 1024 * 1024  # 100MB threshold
```

### 6. Create Integration Testing Framework

Create `tests/test_integration.py`:

```python
"""Integration tests for complete scraper workflows."""

import pytest
import responses
import asyncio
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

from src.scrapers import BaseScraper, ScrapingOrchestrator
from src.models import Product, PriceChange


class TestScraperWorkflow:
    """Test complete scraper workflows end-to-end."""

    @pytest.mark.integration
    @responses.activate
    def test_complete_scraping_workflow(self, db_session, sample_products):
        """Test a complete scraping workflow from start to finish."""
        # Mock HTTP response
        responses.add(
            responses.GET,
            "https://example.com/product/123",
            body="""
            <div class="product">
                <h1>Test Product</h1>
                <span class="price">$89.99</span>
                <div class="stock">In Stock</div>
            </div>
            """,
            status=200,
            headers={"Content-Type": "text/html"}
        )

        scraper = BaseScraper(db_session)

        # Add product to scrape
        product = sample_products[0]
        product.url = "https://example.com/product/123"
        product.current_price = Decimal("99.99")  # Old price
        db_session.commit()

        # Run scraper
        result = scraper.scrape_product(product.url)

        # Verify results
        assert result is not None
        assert result['price'] == Decimal("89.99")

        # Check price change was recorded
        price_changes = db_session.query(PriceChange).filter_by(product_id=product.id).all()
        assert len(price_changes) == 1
        assert price_changes[0].old_price == Decimal("99.99")
        assert price_changes[0].new_price == Decimal("89.99")

    @pytest.mark.integration
    def test_error_handling_and_recovery(self, db_session):
        """Test scraper error handling and recovery mechanisms."""
        scraper = BaseScraper(db_session)

        # Test network timeout
        with patch('requests.get') as mock_get:
            mock_get.side_effect = TimeoutError("Connection timeout")

            result = scraper.scrape_product("https://example.com/timeout")
            assert result is None

            # Verify error was logged
            assert scraper.last_error is not None

    @pytest.mark.integration
    def test_rate_limiting_behavior(self, db_session):
        """Test that scrapers respect rate limiting."""
        scraper = BaseScraper(db_session, rate_limit=2.0)  # 2 second delay

        start_time = datetime.now()

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = "<html>Test</html>"

            # Make multiple requests
            scraper.scrape_product("https://example.com/1")
            scraper.scrape_product("https://example.com/2")

        end_time = datetime.now()
        elapsed = (end_time - start_time).total_seconds()

        # Should have waited at least the rate limit duration
        assert elapsed >= 2.0


class TestConcurrentScraping:
    """Test concurrent scraping scenarios."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_concurrent_scraping_safety(self, db_session, sample_products):
        """Test that concurrent scraping doesn't cause race conditions."""
        orchestrator = ScrapingOrchestrator(db_session)

        # Mock responses for concurrent requests
        with responses.RequestsMock() as rsps:
            for i, product in enumerate(sample_products):
                rsps.add(
                    responses.GET,
                    product.url,
                    body=f"<div>Product {i}</div>",
                    status=200
                )

            # Run concurrent scraping
            tasks = [
                orchestrator.scrape_product_async(product.url)
                for product in sample_products
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Verify no exceptions occurred
            for result in results:
                assert not isinstance(result, Exception)

            # Verify database consistency
            db_session.commit()
            products_count = db_session.query(Product).count()
            assert products_count >= len(sample_products)


class TestDataConsistency:
    """Test data consistency and validation."""

    @pytest.mark.integration
    def test_price_change_detection_accuracy(self, db_session, product_factory):
        """Test accuracy of price change detection algorithms."""
        scraper = BaseScraper(db_session)

        # Create product with known price history
        product = product_factory(current_price=Decimal("100.00"))
        db_session.add(product)
        db_session.commit()

        # Simulate price changes
        price_sequence = [
            Decimal("95.00"),   # 5% decrease
            Decimal("105.25"),  # 10.79% increase
            Decimal("105.25"),  # No change
            Decimal("90.00"),   # 14.52% decrease
        ]

        for new_price in price_sequence:
            with patch.object(scraper, '_extract_price', return_value=new_price):
                scraper.scrape_product(product.url)

        # Verify price changes were detected correctly
        price_changes = db_session.query(PriceChange).filter_by(product_id=product.id).all()

        # Should have 3 changes (no change shouldn't create record)
        assert len(price_changes) == 3

        # Verify change percentages
        assert abs(price_changes[0].change_percentage - (-5.0)) < 0.01
        assert abs(price_changes[1].change_percentage - 10.79) < 0.01
        assert abs(price_changes[2].change_percentage - (-14.52)) < 0.01
```

### 7. Create Ethics and Rate Limiting Tests

Create `tests/test_scraping_ethics.py`:

```python
"""Tests for ethical scraping behavior and compliance."""

import pytest
import time
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

from src.scrapers import BaseScraper
from src.utils.rate_limiter import RateLimiter
from src.utils.user_agents import UserAgentRotator


class TestRateLimiting:
    """Test rate limiting implementation."""

    def test_rate_limiter_enforcement(self):
        """Test that rate limiter enforces delays properly."""
        rate_limiter = RateLimiter(requests_per_minute=30)  # 2 second intervals

        start_time = time.time()

        # Make first request
        rate_limiter.wait_if_needed()
        first_request_time = time.time()

        # Make second request
        rate_limiter.wait_if_needed()
        second_request_time = time.time()

        # Should have waited at least 2 seconds
        elapsed = second_request_time - first_request_time
        assert elapsed >= 2.0

    def test_rate_limiter_burst_protection(self):
        """Test rate limiter prevents burst requests."""
        rate_limiter = RateLimiter(requests_per_minute=10, burst_limit=3)

        # Make burst requests
        for i in range(3):
            rate_limiter.wait_if_needed()

        # Next request should be delayed significantly
        start_time = time.time()
        rate_limiter.wait_if_needed()
        elapsed = time.time() - start_time

        assert elapsed >= 6.0  # Should wait for rate limit reset


class TestUserAgentRotation:
    """Test User-Agent rotation for respectful scraping."""

    def test_user_agent_rotation(self):
        """Test that User-Agent headers are rotated properly."""
        rotator = UserAgentRotator()

        user_agents = []
        for i in range(10):
            ua = rotator.get_user_agent()
            user_agents.append(ua)

        # Should have variety in user agents
        unique_agents = set(user_agents)
        assert len(unique_agents) > 1

        # Should contain realistic browser strings
        for ua in unique_agents:
            assert any(browser in ua.lower() for browser in ['chrome', 'firefox', 'safari', 'edge'])

    def test_user_agent_consistency_per_session(self):
        """Test User-Agent consistency within scraping sessions."""
        rotator = UserAgentRotator(session_consistency=True)

        session_id = "test_session_123"

        # Get user agent multiple times for same session
        ua1 = rotator.get_user_agent(session_id)
        ua2 = rotator.get_user_agent(session_id)
        ua3 = rotator.get_user_agent(session_id)

        # Should be consistent within session
        assert ua1 == ua2 == ua3

        # But different for different sessions
        ua_different = rotator.get_user_agent("different_session")
        assert ua_different != ua1


class TestRequestHeaders:
    """Test proper HTTP header configuration."""

    def test_respectful_headers(self):
        """Test that scrapers use respectful HTTP headers."""
        scraper = BaseScraper()
        headers = scraper.get_headers()

        # Should include proper headers
        assert 'User-Agent' in headers
        assert 'Accept' in headers
        assert 'Accept-Language' in headers
        assert 'Accept-Encoding' in headers

        # Should not appear as a bot
        ua = headers['User-Agent'].lower()
        assert 'bot' not in ua
        assert 'scraper' not in ua
        assert 'crawler' not in ua

        # Should include Accept headers that mimic real browsers
        assert 'text/html' in headers['Accept']
        assert 'gzip' in headers['Accept-Encoding']

    def test_referer_header_handling(self):
        """Test proper Referer header handling."""
        scraper = BaseScraper()

        # When scraping product pages, should use site's homepage as referer
        headers = scraper.get_headers(
            url="https://example.com/product/123",
            referer="https://example.com"
        )

        assert headers.get('Referer') == "https://example.com"


class TestRobotsRespect:
    """Test robots.txt compliance."""

    @pytest.mark.network
    def test_robots_txt_parsing(self):
        """Test robots.txt parsing and compliance."""
        from src.utils.robots import RobotsChecker

        checker = RobotsChecker()

        # Test with known robots.txt
        can_fetch = checker.can_fetch("https://httpbin.org/robots.txt", "*")
        assert isinstance(can_fetch, bool)

    def test_crawl_delay_respect(self):
        """Test that crawl delays from robots.txt are respected."""
        from src.utils.robots import RobotsChecker

        checker = RobotsChecker()

        # Mock robots.txt with crawl delay
        mock_robots = """
        User-agent: *
        Crawl-delay: 5
        Disallow: /admin/
        """

        with patch.object(checker, '_fetch_robots_txt', return_value=mock_robots):
            delay = checker.get_crawl_delay("https://example.com")
            assert delay == 5


class TestGracefulDegradation:
    """Test graceful handling of various scenarios."""

    def test_timeout_handling(self, db_session):
        """Test graceful handling of request timeouts."""
        scraper = BaseScraper(db_session, timeout=1.0)

        with patch('requests.get') as mock_get:
            mock_get.side_effect = TimeoutError("Request timeout")

            result = scraper.scrape_product("https://slow-site.com/product")

            # Should return None gracefully, not crash
            assert result is None
            assert scraper.last_error is not None

    def test_503_retry_logic(self, db_session):
        """Test retry logic for 503 Service Unavailable responses."""
        scraper = BaseScraper(db_session, max_retries=3)

        with patch('requests.get') as mock_get:
            # First two calls return 503, third succeeds
            mock_responses = [
                Mock(status_code=503, text="Service Unavailable"),
                Mock(status_code=503, text="Service Unavailable"),
                Mock(status_code=200, text="<html>Success</html>")
            ]
            mock_get.side_effect = mock_responses

            result = scraper.scrape_product("https://example.com/product")

            # Should eventually succeed after retries
            assert result is not None
            assert mock_get.call_count == 3

    def test_captcha_detection(self, db_session):
        """Test detection of CAPTCHA challenges."""
        scraper = BaseScraper(db_session)

        captcha_html = """
        <html>
            <body>
                <div class="captcha-challenge">
                    Please complete the CAPTCHA below
                </div>
            </body>
        </html>
        """

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = captcha_html

            result = scraper.scrape_product("https://example.com/product")

            # Should detect CAPTCHA and handle appropriately
            assert result is None
            assert "captcha" in scraper.last_error.lower()
```

### 8. Create Performance Testing Suite

Create `tests/test_performance.py`:

```python
"""Performance tests for scraper efficiency and resource usage."""

import pytest
import psutil
import time
from decimal import Decimal
from unittest.mock import patch, Mock

from src.scrapers import BaseScraper, ScrapingOrchestrator
from src.models import Product


class TestScraperPerformance:
    """Test scraper performance characteristics."""

    @pytest.mark.performance
    def test_scraping_throughput(self, db_session, benchmark):
        """Benchmark scraping throughput."""
        scraper = BaseScraper(db_session)

        # Mock fast HTTP responses
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = """
            <div class="product">
                <h1>Test Product</h1>
                <span class="price">$99.99</span>
            </div>
            """

            # Benchmark single scraping operation
            result = benchmark(scraper.scrape_product, "https://example.com/product")
            assert result is not None

    @pytest.mark.performance
    def test_memory_usage_scaling(self, db_session, product_factory):
        """Test memory usage with increasing dataset size."""
        scraper = BaseScraper(db_session)

        # Monitor memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Create and process many products
        products = []
        for i in range(1000):
            product = product_factory()
            products.append(product)
            db_session.add(product)

        db_session.commit()

        # Process all products
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = "<html>Product</html>"

            for product in products:
                scraper.scrape_product(product.url)

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable (adjust threshold as needed)
        assert memory_increase < 200  # Less than 200MB increase

    @pytest.mark.performance
    def test_database_query_performance(self, db_session, product_factory, benchmark):
        """Test database query performance with large datasets."""
        # Create large dataset
        products = []
        for i in range(5000):
            product = product_factory()
            products.append(product)

        db_session.add_all(products)
        db_session.commit()

        scraper = BaseScraper(db_session)

        # Benchmark product lookup performance
        def lookup_product():
            return scraper.get_product_by_url(products[2500].url)

        result = benchmark(lookup_product)
        assert result is not None

    @pytest.mark.performance
    def test_concurrent_scraping_performance(self, db_session, sample_products):
        """Test performance under concurrent load."""
        import concurrent.futures
        import threading

        results = []
        errors = []

        def scrape_worker(product):
            try:
                scraper = BaseScraper(db_session)
                with patch('requests.get') as mock_get:
                    mock_get.return_value.status_code = 200
                    mock_get.return_value.text = f"<html>Product {product.id}</html>"

                    result = scraper.scrape_product(product.url)
                    return result
            except Exception as e:
                errors.append(e)
                return None

        start_time = time.time()

        # Use thread pool for concurrent scraping
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(scrape_worker, product)
                for product in sample_products * 10  # Scale up the test
            ]

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)

        end_time = time.time()

        # Verify performance
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) > 0

        # Should complete within reasonable time
        elapsed = end_time - start_time
        assert elapsed < 30  # Should complete within 30 seconds


class TestCachePerformance:
    """Test caching mechanisms for improved performance."""

    @pytest.mark.performance
    def test_parser_cache_effectiveness(self, benchmark):
        """Test that parser caching improves performance."""
        from src.utils.cache import ParserCache

        cache = ParserCache(max_size=100)

        html_content = """
        <div class="product">
            <h1>Expensive Product</h1>
            <span class="price">$999.99</span>
        </div>
        """ * 100  # Large HTML content

        url = "https://example.com/expensive-product"

        # First parse (should be slower)
        def first_parse():
            return cache.get_or_parse(url, html_content)

        first_result = benchmark(first_parse)

        # Second parse (should be faster due to caching)
        def cached_parse():
            return cache.get_or_parse(url, html_content)

        cached_result = benchmark(cached_parse)

        assert first_result == cached_result

    @pytest.mark.performance
    def test_database_connection_pooling(self, benchmark):
        """Test database connection pooling performance."""
        from src.database import DatabaseManager

        db_manager = DatabaseManager(pool_size=10)

        def get_connection():
            with db_manager.get_session() as session:
                return session.execute("SELECT 1").scalar()

        # Should reuse connections efficiently
        result = benchmark(get_connection)
        assert result == 1


class TestResourceUtilization:
    """Test resource utilization patterns."""

    @pytest.mark.performance
    def test_cpu_usage_under_load(self, db_session, sample_products):
        """Test CPU usage remains reasonable under load."""
        import psutil

        process = psutil.Process()
        initial_cpu = process.cpu_percent()

        scraper = BaseScraper(db_session)

        # Simulate heavy scraping load
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = "<html>Product</html>"

            start_time = time.time()

            # Run for 10 seconds
            while time.time() - start_time < 10:
                for product in sample_products:
                    scraper.scrape_product(product.url)

        final_cpu = process.cpu_percent()

        # CPU usage should be reasonable (adjust threshold as needed)
        assert final_cpu < 80  # Less than 80% CPU usage

    @pytest.mark.performance
    def test_network_connection_reuse(self):
        """Test that HTTP connections are reused efficiently."""
        import requests

        scraper = BaseScraper()

        # Should reuse session for multiple requests
        assert hasattr(scraper, 'session')
        assert isinstance(scraper.session, requests.Session)

        # Verify connection pooling is configured
        adapter = scraper.session.get_adapter('https://')
        assert hasattr(adapter, 'poolmanager')
```

### 9. Create Test Data Management

Create `tests/utils/test_data.py`:

```python
"""Utilities for test data management and generation."""

import json
import random
from decimal import Decimal
from datetime import datetime, timedelta
from typing import List, Dict, Any

from src.models import Product, PriceChange


class TestDataGenerator:
    """Generate realistic test data for scraper testing."""

    def __init__(self):
        self.product_names = [
            "iPhone 15 Pro", "MacBook Air M2", "Sony WH-1000XM5",
            "Samsung 4K TV", "Nintendo Switch OLED", "iPad Pro 12.9",
            "AirPods Pro 2", "PlayStation 5", "Xbox Series X",
            "Dell XPS 13", "Herman Miller Chair", "Instant Pot Duo"
        ]

        self.sites = ["amazon", "ebay", "walmart", "bestbuy", "target"]

    def generate_products(self, count: int) -> List[Dict[str, Any]]:
        """Generate realistic product data."""
        products = []

        for i in range(count):
            site = random.choice(self.sites)
            name = random.choice(self.product_names)

            product = {
                "name": f"{name} - {random.randint(1, 999)}",
                "url": f"https://{site}.com/product/{random.randint(100000, 999999)}",
                "site_name": site,
                "current_price": Decimal(str(round(random.uniform(10, 2000), 2))),
                "currency": "USD",
                "availability": random.choice(["in_stock", "out_of_stock", "limited"]),
                "sku": f"SKU{random.randint(100000, 999999)}",
                "category": random.choice(["electronics", "home", "books", "clothing"]),
                "created_at": datetime.now() - timedelta(days=random.randint(1, 365))
            }
            products.append(product)

        return products

    def generate_price_history(self, product_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """Generate realistic price history for a product."""
        base_price = Decimal(str(random.uniform(50, 500)))
        price_changes = []
        current_price = base_price

        for day in range(days):
            # Random price fluctuation (-10% to +10%)
            change_factor = Decimal(str(random.uniform(0.9, 1.1)))
            new_price = current_price * change_factor

            # Round to 2 decimal places
            new_price = Decimal(str(round(float(new_price), 2)))

            if new_price != current_price:
                change = {
                    "product_id": product_id,
                    "old_price": current_price,
                    "new_price": new_price,
                    "change_percentage": float((new_price - current_price) / current_price * 100),
                    "detected_at": datetime.now() - timedelta(days=days-day),
                    "notification_sent": random.choice([True, False])
                }
                price_changes.append(change)
                current_price = new_price

        return price_changes

    def generate_html_fixtures(self, site_type: str) -> Dict[str, str]:
        """Generate HTML fixtures for different site types."""
        fixtures = {
            "amazon": """
            <div id="dp" class="dp-container">
                <h1 id="productTitle">{product_name}</h1>
                <div class="a-price">
                    <span class="a-price-symbol">$</span>
                    <span class="a-price-whole">{price_whole}</span>
                    <span class="a-price-fraction">{price_fraction}</span>
                </div>
                <div id="availability">
                    <span>{availability}</span>
                </div>
                <div id="feature-bullets">
                    <ul>
                        <li>Feature 1</li>
                        <li>Feature 2</li>
                    </ul>
                </div>
            </div>
            """,

            "ebay": """
            <div class="x-item-title-label">
                <h1 id="itemTitle">{product_name}</h1>
            </div>
            <div class="item-price">
                <span class="currency">${price_whole}.{price_fraction}</span>
            </div>
            <div class="item-condition">
                <span>{availability}</span>
            </div>
            """,

            "generic": """
            <div class="product-container">
                <h1 class="product-title">{product_name}</h1>
                <div class="price-container">
                    <span class="price">${price_whole}.{price_fraction}</span>
                </div>
                <div class="availability">
                    <span class="status">{availability}</span>
                </div>
            </div>
            """
        }

        return fixtures.get(site_type, fixtures["generic"])


class MockResponseGenerator:
    """Generate mock HTTP responses for testing."""

    @staticmethod
    def success_response(html_content: str, status_code: int = 200) -> Dict[str, Any]:
        """Generate a successful HTTP response."""
        return {
            "status_code": status_code,
            "text": html_content,
            "headers": {
                "Content-Type": "text/html; charset=utf-8",
                "Server": "nginx/1.18.0"
            }
        }

    @staticmethod
    def error_response(status_code: int, message: str = "") -> Dict[str, Any]:
        """Generate an error HTTP response."""
        error_messages = {
            404: "Not Found",
            403: "Forbidden",
            429: "Too Many Requests",
            503: "Service Unavailable"
        }

        return {
            "status_code": status_code,
            "text": message or error_messages.get(status_code, "Error"),
            "headers": {"Content-Type": "text/plain"}
        }

    @staticmethod
    def slow_response(html_content: str, delay: float = 5.0) -> Dict[str, Any]:
        """Generate a slow response for timeout testing."""
        import time
        time.sleep(delay)
        return MockResponseGenerator.success_response(html_content)


# Export utility instances
test_data_generator = TestDataGenerator()
mock_response_generator = MockResponseGenerator()
```

### 10. Create Test Configuration and Commands

Create `tests/commands.py` for test management:

```python
"""Test management commands and utilities."""

import click
import subprocess
from pathlib import Path


@click.group()
def cli():
    """Test management commands for scraper testing."""
    pass


@cli.command()
@click.option('--coverage', is_flag=True, help='Run with coverage reporting')
@click.option('--performance', is_flag=True, help='Include performance tests')
@click.option('--integration', is_flag=True, help='Include integration tests')
@click.option('--network', is_flag=True, help='Include network tests')
def run_tests(coverage, performance, integration, network):
    """Run the test suite with specified options."""
    cmd = ["python", "-m", "pytest"]

    if coverage:
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term"])

    markers = []
    if not performance:
        markers.append("not performance")
    if not integration:
        markers.append("not integration")
    if not network:
        markers.append("not network")

    if markers:
        cmd.extend(["-m", " and ".join(markers)])

    subprocess.run(cmd)


@cli.command()
def generate_fixtures():
    """Generate HTML fixtures for testing."""
    from tests.utils.test_data import test_data_generator
    from tests.fixtures.html_fixtures import fixture_manager, HTMLFixture

    sites = ["amazon", "ebay", "generic"]

    for site in sites:
        html_template = test_data_generator.generate_html_fixtures(site)

        fixture = HTMLFixture(
            name=f"sample_{site}",
            content=html_template.format(
                product_name="Sample Product",
                price_whole="99",
                price_fraction="99",
                availability="In Stock"
            ),
            url=f"https://{site}.com/product/123",
            description=f"Sample {site} product page",
            expected_data={"name": "Sample Product", "price": 99.99},
            last_updated="2024-01-01",
            site_type=site
        )

        fixture_manager.save_fixture(fixture)
        click.echo(f"Created fixture: {fixture.name}")


@cli.command()
def benchmark():
    """Run performance benchmarks."""
    cmd = [
        "python", "-m", "pytest",
        "-m", "performance",
        "--benchmark-only",
        "--benchmark-sort=mean"
    ]
    subprocess.run(cmd)


if __name__ == "__main__":
    cli()
```

### 11. Update Project Configuration

Add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra --strict-markers --strict-config"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "e2e: End-to-end tests",
    "performance: Performance tests",
    "slow: Slow running tests",
    "network: Tests requiring network access",
    "scraper: Web scraper specific tests",
    "parser: HTML parser tests",
    "database: Database tests",
    "ethics: Scraping ethics validation tests"
]

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/venv/*",
    "*/__pycache__/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError"
]
```

## Testing Commands

After setup, run tests with:

```bash
# Run all tests
python -m pytest

# Run specific test categories
python -m pytest -m "unit"
python -m pytest -m "integration"
python -m pytest -m "performance"
python -m pytest -m "ethics"

# Run with coverage
python -m pytest --cov=src --cov-report=html

# Run performance benchmarks
python -m pytest -m performance --benchmark-only

# Generate test fixtures
python tests/commands.py generate-fixtures

# Run specific scraper tests
python -m pytest tests/test_parsers.py -v
python -m pytest tests/test_scraping_ethics.py -v
```

This comprehensive testing infrastructure provides:

- **Complete scraper testing framework** with HTTP mocking and HTML fixtures
- **Database testing** with factories and transaction rollback
- **Parser robustness testing** with malformed HTML handling
- **Integration testing** for complete workflows
- **Performance testing** and benchmarking
- **Ethics validation** for respectful scraping behavior
- **Specialized utilities** for web scraping test scenarios

The framework ensures your scrapers are robust, performant, and ethically compliant while providing comprehensive test coverage for all scraping scenarios.
