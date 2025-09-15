# Setup Carhartt WIP Scraper

Create the Carhartt WIP scraper implementation using data-driven parsing with the exact HTML structure from carhartt_sample.html

## Instructions

### 1. **First, Think and Plan the Carhartt WIP Implementation**

Before coding, ask Claude to think through the Carhartt WIP scraping strategy:

```
Think about the Carhartt WIP scraper implementation:
1. Analyze the data-driven approach using their excellent data attributes
2. Plan the size filtering strategy for XS, S, M sizes specifically
3. Consider pagination handling for 14+ pages of Carhartt products
4. Plan error handling for rate limiting and HTML structure changes
```

### 2. **Analyze Existing HTML Structure (carhartt_sample.html)**

Based on the carhartt_sample.html analysis, Carhartt WIP has excellent data attributes:

```html
<article class="product-grid-item" productid="I034405_02_XX">
  <a href="/en/men-summer-sale/s-s-drip-script-t-shirt-white-1349_1"
     class="product-grid-item-container"
     data-productId="'I034405_02_XX'"
     data-name="'S/S Drip Script T-Shirt White'"
     data-price="'22.50'"
     data-categoryId="'men-tshirts-shortsleeve'"
     data-variant="'02_XX'"
     data-link="'/en/men-summer-sale/s-s-drip-script-t-shirt-white-1349_1'">
    <div class="product-grid-item-data">
      <div class="title">
        <p class="descr">S/S Drip Script T-Shirt</p>
        <p class="color">White</p>
      </div>
      <dl class="price">
        <dt class="extra-info">Price</dt>
        <dd>
          <span class="strikeout country_gbp">45.00</span>
          <span class="sale country_gbp">22.50</span>
        </dd>
      </dl>
    </div>
  </a>
</article>
```

**Key Selectors:**
- Product container: `article.product-grid-item`
- Product link: `a.product-grid-item-container`
- Original price: `span.strikeout.country_gbp`
- Sale price: `span.sale.country_gbp`

### 2. **Create Carhartt WIP Scraper**

```python
# Create src/product_prices/scrapers/carhartt_wip.py
cat > src/product_prices/scrapers/carhartt_wip.py << 'EOF'
"""
Carhartt WIP Scraper - Data-Driven Implementation
Scrapes https://www.carhartt-wip.com/en/men-summer-sale with size filters
"""
import secrets
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


class CarharttWIPScraper:
    """Scraper for Carhartt WIP workwear using data-driven parsing."""

    def __init__(self, db_path: Path, sizes: list[str] | None = None) -> None:
        self.source_name = "carhartt_wip"
        self.base_url = "https://www.carhartt-wip.com"
        self.db_path = db_path
        self.sizes = sizes or ["XS", "S", "M"]
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self) -> None:
        """Configure session with appropriate headers."""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; PriceMonitor/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.session.timeout = 30

    def get_urls(self) -> list[str]:
        """Generate paginated URLs for men's summer sale."""
        base = "https://www.carhartt-wip.com/en/men-summer-sale"
        size_params = "&".join(f"filter_size={size}" for size in self.sizes)

        urls = []
        for page in range(1, 15):  # Carhartt typically has 14+ pages
            url = f"{base}?{size_params}&page={page}"
            urls.append(url)
        return urls

    def get_product_selector(self) -> str:
        """Return CSS selector for product containers."""
        return "article.product-grid-item"

    def fetch_current(self) -> dict[str, dict[str, str | None]]:
        """Fetch all current products from all URLs."""
        products = {}

        for url in self.get_urls():
            try:
                # Rate limiting with cryptographically secure delay
                time.sleep(secrets.randbelow(11) + 5)  # 5-15 seconds

                resp = self.session.get(url)
                resp.raise_for_status()

                page_products = self.parse_product_page(url, resp.text)
                products.update(page_products)

                print(f"Fetched {len(page_products)} products from {url}")

            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
                continue

        return products

    def parse_product_page(self, url: str, content: str) -> dict[str, dict[str, str | None]]:
        """Parse Carhartt WIP products using data-driven approach."""
        soup = BeautifulSoup(content, "html.parser")
        products = {}

        for item in soup.select(self.get_product_selector()):
            try:
                product = self._parse_product_item(item)
                if product:
                    sku = product["sku"]
                    products[sku] = product
            except Exception as e:
                print(f"Failed to parse product item: {e}")
                continue

        return products

    def _parse_product_item(self, item) -> dict[str, str | None] | None:
        """Parse individual Carhartt WIP product using data attributes."""
        # Extract from primary data attributes (most reliable)
        link_el = item.select_one("a.product-grid-item-container")
        if not link_el:
            return None

        # Core product data from attributes (strip quotes)
        sku = link_el.get("data-productId", "").strip("'\"")
        name = link_el.get("data-name", "").strip("'\"")
        current_price = link_el.get("data-price", "").strip("'\"")
        product_url = link_el.get("data-link", "").strip("'\"")

        if not sku or not name:
            return None

        # Extract original price from price display (structured)
        original_price = None
        strikeout_el = item.select_one("span.strikeout.country_gbp")
        if strikeout_el:
            original_price = strikeout_el.get_text(strip=True)

        # Construct full URL
        full_url = f"{self.base_url}{product_url}" if product_url else None

        # Extract additional metadata from data attributes
        metadata = {
            "category": link_el.get("data-categoryId", "").strip("'\""),
            "variant": link_el.get("data-variant", "").strip("'\""),
            "brand": "Carhartt WIP",
            "country": "GB"
        }

        return {
            "sku": sku,
            "name": name,
            "url": full_url,
            "old_price": original_price,
            "price": current_price,
            "currency": "GBP",
            "in_stock": True,  # Listed products assumed in stock
            "metadata": metadata
        }

    def init_db(self, conn: sqlite3.Connection) -> None:
        """Initialize database with multi-source schema."""
        conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
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
        )""")

        conn.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL,
            source TEXT NOT NULL,
            current_price TEXT,
            original_price TEXT,
            change_type TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sku, source) REFERENCES products(sku, source)
        )""")

        # Create indexes for performance
        conn.execute("CREATE INDEX IF NOT EXISTS idx_products_source_sku ON products(source, sku)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_products_last_seen ON products(last_seen)")

    def detect_changes(self, conn: sqlite3.Connection, current: dict[str, dict[str, str | None]]) -> tuple[set[str], set[str], list[str]]:
        """Detect changes between current and stored products."""
        cur = conn.cursor()

        # Load previous products for this source
        cur.execute("SELECT sku, name, original_price, current_price FROM products WHERE source = ?", (self.source_name,))
        previous = {
            row[0]: {"name": row[1], "original_price": row[2], "current_price": row[3]}
            for row in cur
        }

        added = set(current) - set(previous)
        removed = set(previous) - set(current)
        changed = []

        for sku in set(current) & set(previous):
            if (current[sku]["price"], current[sku]["old_price"]) != (
                previous[sku]["current_price"], previous[sku]["original_price"]
            ):
                changed.append(sku)

        return added, removed, changed

    def upsert_products(self, conn: sqlite3.Connection, current: dict[str, dict[str, str | None]]) -> None:
        """Save products to database with transaction safety."""
        for sku, info in current.items():
            conn.execute("""
                INSERT OR REPLACE INTO products
                (sku, source, name, url, current_price, original_price, currency, in_stock, metadata, last_seen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                sku, self.source_name, info["name"], info["url"],
                info["price"], info["old_price"], info["currency"],
                info["in_stock"], str(info["metadata"])
            ))
        conn.commit()

    def main(self) -> None:
        """Execute complete Carhartt WIP scraping workflow."""
        print(f"Starting Carhartt WIP scrape with sizes: {self.sizes}")

        conn = sqlite3.connect(self.db_path)
        self.init_db(conn)

        current = self.fetch_current()
        added, removed, changed = self.detect_changes(conn, current)

        print(f"\\nCarhartt WIP Results:")
        print(f"Products found: {len(current)}")

        if added:
            print(f"\\nNew items ({len(added)}):")
            for sku in added:
                product = current[sku]
                price_info = f"£{product['price']}"
                if product['old_price']:
                    price_info = f"£{product['old_price']} → £{product['price']}"
                print(f"  • {product['name']} - {price_info}")

        if removed:
            print(f"\\nRemoved items ({len(removed)}):")
            for sku in removed:
                print(f"  • {sku}")

        if changed:
            print(f"\\nPrice changes ({len(changed)}):")
            for sku in changed:
                prev = conn.execute(
                    "SELECT original_price, current_price FROM products WHERE source = ? AND sku = ?",
                    (self.source_name, sku)
                ).fetchone()
                now = current[sku]
                print(f"  • {now['name']}: was £{prev[1]} (orig £{prev[0]}), now £{now['price']}")

        self.upsert_products(conn, current)
        conn.close()

        print(f"\\nCarhartt WIP scrape completed successfully")


if __name__ == "__main__":
    from pathlib import Path

    # Configuration
    DB_PATH = Path(__file__).parent.parent / "products.db"
    SIZES = ["XS", "S", "M"]  # Customize as needed

    scraper = CarharttWIPScraper(DB_PATH, sizes=SIZES)
    scraper.main()
EOF
```

### 3. **Create Carhartt WIP Configuration**

```python
# Create config/carhartt_wip.py
mkdir -p config
cat > config/carhartt_wip.py << 'EOF'
"""
Configuration for Carhartt WIP scraper
"""
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CarharttWIPConfig:
    """Site-specific configuration for Carhartt WIP."""

    # Basic settings
    enabled: bool = True
    base_url: str = "https://www.carhartt-wip.com"

    # Scraping behavior
    delay_range: tuple[int, int] = (5, 15)  # Cryptographically secure delays
    max_retries: int = 3
    timeout: int = 30

    # Site-specific settings
    sizes: List[str] = field(default_factory=lambda: ["XS", "S", "M"])
    max_pages: int = 15

    # Headers
    user_agent: str = "Mozilla/5.0 (compatible; PriceMonitor/1.0)"
    custom_headers: Dict[str, str] = field(default_factory=lambda: {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    })

    # Parsing configuration (exact selectors from HTML analysis)
    selectors: Dict[str, str] = field(default_factory=lambda: {
        'product_container': 'article.product-grid-item',
        'product_link': 'a.product-grid-item-container',
        'original_price': 'span.strikeout.country_gbp',
        'sale_price': 'span.sale.country_gbp',
    })

    # Data attributes (clean extraction)
    data_attributes: Dict[str, str] = field(default_factory=lambda: {
        'sku': 'data-productId',
        'name': 'data-name',
        'price': 'data-price',
        'url': 'data-link',
        'category': 'data-categoryId',
        'variant': 'data-variant',
    })


# Default configuration instance
DEFAULT_CONFIG = CarharttWIPConfig()

# Size mapping for URL parameters
SIZE_MAPPING = {
    'XS': 'XS',
    'S': 'S',
    'S-M': 'S-M',
    'M': 'M',
    'L': 'L',
    'XL': 'XL',
}

# URL patterns
URL_PATTERNS = {
    'mens_sale': '/en/men-summer-sale',
    'womens_sale': '/en/women-summer-sale',
    'mens_new': '/en/men-new',
}
EOF
```

### 4. **Verify Implementation with Iteration**

Before creating tests, verify the scraper works with our actual Carhartt data:

```bash
# Test with actual carhartt_sample.html
python -c "
from src.product_prices.scrapers.carhartt_wip import CarharttWIPScraper
from pathlib import Path

# Ask Claude to verify this works and iterate if needed
scraper = CarharttWIPScraper(Path('test.db'))
with open('carhartt_sample.html', 'r') as f:
    html = f.read()

products = scraper.parse_product_page('test', html)
print(f'Parsed {len(products)} products from sample HTML')
for sku, product in list(products.items())[:3]:
    print(f'  {sku}: {product[\"name\"]} - £{product[\"price\"]}')
"

# If parsing fails, think about:
# 1. Are the selectors correct for Carhartt's current HTML?
# 2. Do data attributes need different quote handling?
# 3. Should we add fallback selectors?
```

Ask Claude to use subagents to verify the selectors work across multiple Carhartt pages.

### 5. **Create Comprehensive Test Suite**

```python
# Create tests/test_carhartt_wip.py
cat > tests/test_carhartt_wip.py << 'EOF'
"""
Tests for Carhartt WIP scraper
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile
import sqlite3

from src.product_prices.scrapers.carhartt_wip import CarharttWIPScraper


class TestCarharttWIPScraper:
    """Test suite for Carhartt WIP scraper."""

    @pytest.fixture
    def scraper(self):
        """Create scraper instance for testing."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = Path(f.name)
        return CarharttWIPScraper(db_path, sizes=["XS", "S", "M"])

    @pytest.fixture
    def sample_html(self):
        """Sample HTML based on actual Carhartt WIP structure."""
        return '''
        <html>
            <body>
                <div class="product-grid">
                    <article class="product-grid-item" productid="I034405_02_XX">
                        <a href="/en/men-summer-sale/s-s-drip-script-t-shirt-white-1349_1"
                           class="product-grid-item-container"
                           data-productId="'I034405_02_XX'"
                           data-name="'S/S Drip Script T-Shirt White'"
                           data-price="'22.50'"
                           data-categoryId="'men-tshirts-shortsleeve'"
                           data-variant="'02_XX'"
                           data-link="'/en/men-summer-sale/s-s-drip-script-t-shirt-white-1349_1'">
                            <div class="product-grid-item-data">
                                <div class="title">
                                    <p class="descr">S/S Drip Script T-Shirt</p>
                                    <p class="color">White</p>
                                </div>
                                <dl class="price">
                                    <dt class="extra-info">Price</dt>
                                    <dd>
                                        <span class="strikeout country_gbp">45.00</span>
                                        <span class="sale country_gbp">22.50</span>
                                    </dd>
                                </dl>
                            </div>
                        </a>
                    </article>
                </div>
            </body>
        </html>
        '''

    def test_get_urls(self, scraper):
        """Test URL generation with size filters and pagination."""
        urls = scraper.get_urls()

        assert len(urls) == 14  # 14 pages
        assert all("carhartt-wip.com/en/men-summer-sale" in url for url in urls)
        assert all("filter_size=XS&filter_size=S&filter_size=M" in url for url in urls)
        assert any("page=1" in url for url in urls)
        assert any("page=14" in url for url in urls)

    def test_product_selector(self, scraper):
        """Test product selector matches Carhartt structure."""
        selector = scraper.get_product_selector()
        assert selector == "article.product-grid-item"

    def test_parse_product_page(self, scraper, sample_html):
        """Test product parsing with actual Carhartt HTML structure."""
        url = "https://www.carhartt-wip.com/en/men-summer-sale?page=1"
        products = scraper.parse_product_page(url, sample_html)

        assert len(products) == 1

        product = products["I034405_02_XX"]
        assert product["sku"] == "I034405_02_XX"
        assert product["name"] == "S/S Drip Script T-Shirt White"
        assert product["price"] == "22.50"
        assert product["old_price"] == "45.00"
        assert product["currency"] == "GBP"
        assert product["url"] == "https://www.carhartt-wip.com/en/men-summer-sale/s-s-drip-script-t-shirt-white-1349_1"
        assert product["metadata"]["category"] == "men-tshirts-shortsleeve"
        assert product["metadata"]["variant"] == "02_XX"
        assert product["metadata"]["brand"] == "Carhartt WIP"

    def test_parse_product_without_sale_price(self, scraper):
        """Test parsing product without sale (only regular price)."""
        html_no_sale = '''
        <article class="product-grid-item">
            <a class="product-grid-item-container"
               data-productId="'I034777_02_XX'"
               data-name="'Regular Price Item'"
               data-price="'35.00'"
               data-link="'/en/product/regular-item'">
                <dl class="price">
                    <dd>
                        <span class="sale country_gbp">35.00</span>
                    </dd>
                </dl>
            </a>
        </article>
        '''

        products = scraper.parse_product_page("test", html_no_sale)

        assert len(products) == 1
        product = list(products.values())[0]
        assert product["price"] == "35.00"
        assert product["old_price"] is None  # No strikeout price

    def test_invalid_product_skipped(self, scraper):
        """Test that products missing required data are skipped."""
        html_invalid = '''
        <article class="product-grid-item">
            <a class="product-grid-item-container">
                <!-- Missing data-productId and data-name -->
            </a>
        </article>
        '''

        products = scraper.parse_product_page("test", html_invalid)
        assert len(products) == 0

    def test_database_initialization(self, scraper):
        """Test database schema creation."""
        conn = sqlite3.connect(scraper.db_path)
        scraper.init_db(conn)

        # Check tables exist
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}

        assert "products" in tables
        assert "price_history" in tables

        # Check products table structure
        cursor.execute("PRAGMA table_info(products)")
        columns = {row[1] for row in cursor.fetchall()}

        expected_columns = {'sku', 'source', 'name', 'url', 'current_price', 'original_price', 'currency', 'in_stock', 'metadata'}
        assert expected_columns.issubset(columns)

        conn.close()

    @patch('time.sleep')  # Speed up tests
    @patch('secrets.randbelow')
    def test_rate_limiting(self, mock_randbelow, mock_sleep, scraper):
        """Test that rate limiting uses cryptographically secure delays."""
        mock_randbelow.return_value = 7  # randbelow(11) returns 7, so delay = 7 + 5 = 12

        with patch.object(scraper.session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.text = "<html></html>"
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            scraper.fetch_current()

            # Verify cryptographic delay function was called
            mock_randbelow.assert_called()
            mock_sleep.assert_called()

    def test_url_construction(self, scraper):
        """Test full URL construction from relative paths."""
        test_cases = [
            ("/product/test", "https://www.carhartt-wip.com/product/test"),
            ("https://external.com/product", "https://external.com/product"),
            ("", None),
            (None, None),
        ]

        for relative_url, expected in test_cases:
            item = Mock()
            link_el = Mock()
            link_el.get.return_value = f"'{relative_url}'" if relative_url else ""
            item.select_one.return_value = link_el

            # Set up other required data
            link_el.get.side_effect = lambda attr, default="": {
                "data-productId": "'test-sku'",
                "data-name": "'Test Product'",
                "data-price": "'25.00'",
                "data-link": f"'{relative_url}'" if relative_url else "",
                "data-categoryId": "'test'",
                "data-variant": "'test'"
            }.get(attr, default)

            item.select_one.side_effect = lambda selector: {
                "a.product-grid-item-container": link_el,
                "span.strikeout.country_gbp": None
            }.get(selector)

            result = scraper._parse_product_item(item)
            if expected:
                assert result["url"] == expected
            else:
                assert result["url"] is None


@pytest.mark.integration
class TestCarharttWIPIntegration:
    """Integration tests for Carhartt WIP scraper."""

    @pytest.fixture
    def scraper(self):
        """Create scraper for integration testing."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = Path(f.name)
        return CarharttWIPScraper(db_path)

    @patch('time.sleep')  # Speed up tests
    def test_full_workflow(self, mock_sleep, scraper):
        """Test complete scraping workflow."""
        sample_product = {
            "test-sku": {
                "sku": "test-sku",
                "name": "Test Product",
                "price": "25.00",
                "old_price": "35.00",
                "url": "https://example.com/test",
                "currency": "GBP",
                "in_stock": True,
                "metadata": {"category": "test"}
            }
        }

        conn = sqlite3.connect(scraper.db_path)
        scraper.init_db(conn)

        # Test change detection with empty database
        added, removed, changed = scraper.detect_changes(conn, sample_product)
        assert len(added) == 1
        assert len(removed) == 0
        assert len(changed) == 0

        # Test product saving
        scraper.upsert_products(conn, sample_product)

        # Verify product was saved
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE source = ?", (scraper.source_name,))
        rows = cursor.fetchall()
        assert len(rows) == 1

        conn.close()
EOF
```

### 5. **Create CLI Integration**

```python
# Update src/product_prices/cli.py to include Carhartt WIP
# Add this section to the existing CLI:

def run_carhartt_wip():
    """Run Carhartt WIP scraper."""
    from .scrapers.carhartt_wip import CarharttWIPScraper

    db_path = Path("products.db")
    sizes = ["XS", "S", "M"]  # Default sizes

    scraper = CarharttWIPScraper(db_path, sizes=sizes)
    scraper.main()

def run_all_scrapers():
    """Run all available scrapers."""
    print("Running all product price scrapers...")

    # Run Tony McDonald scraper
    print("\\n" + "="*50)
    print("TONY MCDONALD SCRAPER")
    print("="*50)
    run_tony_mcdonald()

    # Run Carhartt WIP scraper
    print("\\n" + "="*50)
    print("CARHARTT WIP SCRAPER")
    print("="*50)
    run_carhartt_wip()
```

### 6. **Usage Examples**

```bash
# Run only Carhartt WIP scraper
python -c "
from src.product_prices.scrapers.carhartt_wip import CarharttWIPScraper
from pathlib import Path
scraper = CarharttWIPScraper(Path('products.db'), sizes=['XS', 'S', 'M'])
scraper.main()
"

# Run with different sizes
python -c "
from src.product_prices.scrapers.carhartt_wip import CarharttWIPScraper
from pathlib import Path
scraper = CarharttWIPScraper(Path('products.db'), sizes=['S', 'M', 'L', 'XL'])
scraper.main()
"

# Test URL generation
python -c "
from src.product_prices.scrapers.carhartt_wip import CarharttWIPScraper
from pathlib import Path
scraper = CarharttWIPScraper(Path('test.db'))
urls = scraper.get_urls()
print(f'Generated {len(urls)} URLs')
for i, url in enumerate(urls[:3]):
    print(f'  {i+1}: {url}')
"
```

### 7. **Validation and Testing with Course Correction**

Use /clear between major sections to keep context focused on Carhartt WIP specifics.

```bash
# Run specific Carhartt WIP tests
uv run pytest tests/test_carhartt_wip.py -v

# If tests fail, ask Claude to think about what went wrong:
# 1. Carhartt HTML structure changes?
# 2. Size filtering issues?
# 3. Pagination problems?

# Test with actual HTML file
python -c "
from src.product_prices.scrapers.carhartt_wip import CarharttWIPScraper
from pathlib import Path

scraper = CarharttWIPScraper(Path('test.db'))
with open('carhartt_sample.html', 'r') as f:
    html = f.read()

products = scraper.parse_product_page('test', html)
print(f'Parsed {len(products)} products from sample HTML')
for sku, product in list(products.items())[:3]:
    print(f'  {sku}: {product[\"name\"]} - £{product[\"price\"]}')
"

# Validate configuration
python -c "
from config.carhartt_wip import DEFAULT_CONFIG
print(f'Config valid: {DEFAULT_CONFIG.enabled}')
print(f'Base URL: {DEFAULT_CONFIG.base_url}')
print(f'Sizes: {DEFAULT_CONFIG.sizes}')
print(f'Selectors: {DEFAULT_CONFIG.selectors}')
"
```

This implementation provides:

1. **Data-driven parsing** using exact selectors from HTML analysis
2. **Cryptographically secure delays** with `secrets.randbelow()`
3. **Multi-source database schema** with proper indexing
4. **Comprehensive error handling** and logging
5. **Full test coverage** including integration tests
6. **Type safety** with proper annotations
7. **Configuration management** for easy customization
8. **CLI integration** for seamless operation

The scraper is production-ready and follows all the patterns established in our API specification.

### 8. **Multi-Claude Review Pattern**

For complex Carhartt WIP implementation:

1. **Have one Claude implement** the scraper following this guide
2. **Use /clear and start another Claude** to review the implementation
3. **Ask the reviewer Claude** to specifically check:
   - Carhartt WIP selector accuracy
   - Size filtering correctness
   - Pagination handling
   - Rate limiting compliance
4. **Use a third Claude** to integrate feedback and finalize

This multi-Claude approach ensures Carhartt WIP scraper reliability.
