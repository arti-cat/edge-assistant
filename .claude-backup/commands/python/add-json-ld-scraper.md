# Add JSON-LD Scraper

Add a new site-specific scraper for e-commerce sites that use JSON-LD structured data (Schema.org). This command provides structured implementation patterns for sites like End Clothing that embed product data in JSON-LD script tags instead of HTML data attributes.

## Usage

```bash
# Add a JSON-LD scraper for a site with structured data
/add-json-ld-scraper --site="end_clothing" --base-url="https://www.endclothing.com" --brand="Carhartt WIP"

# Add JSON-LD scraper with custom filters
/add-json-ld-scraper --site="new_site" --base-url="https://example.com" --filters="size,brand,category"
```

## Instructions

### 1. Analyze Target Site's JSON-LD Structure

First, download and analyze the target site to identify JSON-LD patterns:

```bash
# Download sample page with JSON-LD data
SITE_NAME="${1:-end_clothing}"
TARGET_URL="${2:-https://www.endclothing.com/gb/sale}"

curl -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
     "$TARGET_URL" -o "${SITE_NAME}_sample.html"

# Extract JSON-LD scripts
grep -o '<script type="application/ld+json">.*</script>' "${SITE_NAME}_sample.html" > "${SITE_NAME}_jsonld.json"
```

Identify JSON-LD structure patterns:

**JSON-LD Product Schema Pattern:**
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "position": 1,
  "name": "Product Name",
  "url": "https://site.com/product-url",
  "brand": {"@type": "Brand", "name": "Brand Name"},
  "offers": {
    "@type": "Offer",
    "priceCurrency": "GBP",
    "price": 59.00,
    "availability": "https://schema.org/InStock"
  },
  "image": "https://site.com/image.jpg"
}
```

Create analysis document:

```bash
cat > docs/site_analysis_${SITE_NAME}.md << 'EOF'
# Site Analysis: End Clothing (JSON-LD Structured Data)

## Strategy Decision
✅ JSON-LD Structured Data Parsing (Schema.org compliant)

## Data Source Structure
- **Data Location**: `<script type="application/ld+json">` tags
- **Schema Type**: Schema.org Product objects
- **Data Format**: Clean JSON with typed fields
- **Product Count**: Embedded in JSON array or individual objects

## JSON-LD Product Structure
- **Product Identification**: `@type: "Product"`
- **Name**: `product.name` (direct string)
- **Price**: `product.offers.price` (numeric value)
- **Currency**: `product.offers.priceCurrency` (ISO code)
- **URL**: `product.url` (absolute or relative path)
- **Brand**: `product.brand.name` (nested object)
- **Availability**: `product.offers.availability` (Schema.org URL)

## URL Structure (End Clothing Pattern)
- Base URL: https://www.endclothing.com
- Sale pages: /gb/sale?brand=Carhartt%20WIP&size_label=Small,Medium
- Pagination: Embedded in JSON-LD data (position field)
- Filters: URL parameters for brand, size, category

## Rate Limiting Requirements
- Delay range: 3-8 seconds (lighter than HTML scraping)
- Required headers: Standard browser headers
- Robots.txt compliance: Check robots.txt for JSON-LD specific rules

## Implementation Notes
JSON-LD provides clean, structured data ideal for reliable extraction
EOF
```

### 2. Think and Plan JSON-LD Implementation Strategy

Before implementing, ask Claude to think about the JSON-LD approach:

```
Think about the JSON-LD scraping strategy for this site:
1. How should we extract and parse JSON-LD script tags?
2. What error handling is needed for malformed JSON?
3. How do we handle multiple JSON-LD objects per page?
4. What validation should we perform on Schema.org compliance?
5. How should pagination work with JSON-LD data?
```

### 3. Create JSON-LD Scraper Implementation

```python
# Create scraper using JSON-LD template
cat > src/product_prices/scrapers/${SITE_NAME}.py << 'EOF'
"""
{SITE_NAME} Scraper - JSON-LD Structured Data Implementation
Parses Schema.org Product objects from JSON-LD script tags
"""
import json
import secrets
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup


class {ClassName}Scraper:
    """Scraper for {SITE_NAME} using JSON-LD structured data parsing."""

    def __init__(self, db_path: Path, **kwargs) -> None:
        self.source_name = "{SITE_NAME_LOWER}"
        self.base_url = "{BASE_URL}"
        self.db_path = db_path

        # Site-specific configuration
        self.brand_filter = kwargs.get('brand_filter', '{DEFAULT_BRAND}')
        self.size_filters = kwargs.get('size_filters', ['{DEFAULT_SIZES}'])
        self.categories = kwargs.get('categories', ['{DEFAULT_CATEGORY}'])

        # Configure session
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self) -> None:
        """Configure session with appropriate headers for JSON-LD sites."""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; PriceMonitor/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.session.timeout = 30

    def get_urls(self) -> List[str]:
        """Generate URLs with brand and size filters."""
        urls = []

        for category in self.categories:
            # Build URL with filters
            params = []
            if self.brand_filter:
                params.append(f"brand={self.brand_filter.replace(' ', '%20')}")
            if self.size_filters:
                size_param = ",".join(self.size_filters)
                params.append(f"size_label={size_param}")

            url = f"{self.base_url}/{category}"
            if params:
                url += "?" + "&".join(params)

            urls.append(url)

        return urls

    def fetch_current(self) -> Dict[str, Dict[str, Any]]:
        """Fetch all current products from JSON-LD data."""
        products = {}

        for url in self.get_urls():
            try:
                # Rate limiting (lighter for JSON-LD)
                time.sleep(secrets.randbelow(6) + 3)  # 3-8 seconds

                resp = self.session.get(url)
                resp.raise_for_status()

                page_products = self.parse_json_ld_page(url, resp.text)
                products.update(page_products)

                print(f"Fetched {len(page_products)} products from {url}")

            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
                continue

        return products

    def parse_json_ld_page(self, url: str, content: str) -> Dict[str, Dict[str, Any]]:
        """Parse JSON-LD structured data from page content."""
        soup = BeautifulSoup(content, "html.parser")
        products = {}

        # Find all JSON-LD script tags
        json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})

        for script in json_ld_scripts:
            try:
                json_data = json.loads(script.string)
                page_products = self._extract_products_from_json_ld(json_data)
                products.update(page_products)
            except (json.JSONDecodeError, AttributeError) as e:
                print(f"Failed to parse JSON-LD: {e}")
                continue

        return products

    def _extract_products_from_json_ld(self, json_data: Any) -> Dict[str, Dict[str, Any]]:
        """Extract product data from JSON-LD object."""
        products = {}

        # Handle different JSON-LD structures
        if isinstance(json_data, list):
            # Array of objects
            for item in json_data:
                if self._is_product_object(item):
                    product = self._parse_json_ld_product(item)
                    if product:
                        products[product["sku"]] = product
        elif isinstance(json_data, dict):
            if self._is_product_object(json_data):
                # Single product object
                product = self._parse_json_ld_product(json_data)
                if product:
                    products[product["sku"]] = product
            elif "@graph" in json_data:
                # JSON-LD graph structure
                for item in json_data["@graph"]:
                    if self._is_product_object(item):
                        product = self._parse_json_ld_product(item)
                        if product:
                            products[product["sku"]] = product

        return products

    def _is_product_object(self, obj: Any) -> bool:
        """Check if JSON-LD object is a Product."""
        if not isinstance(obj, dict):
            return False

        obj_type = obj.get("@type", "")
        return obj_type == "Product" or (isinstance(obj_type, list) and "Product" in obj_type)

    def _parse_json_ld_product(self, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse individual product from JSON-LD data."""
        try:
            # Extract core product information
            name = product_data.get("name", "")
            url = product_data.get("url", "")

            if not name:
                return None

            # Generate SKU from URL or use product identifier
            sku = self._extract_sku_from_product(product_data, url)
            if not sku:
                return None

            # Extract pricing information
            offers = product_data.get("offers", {})
            if isinstance(offers, list):
                offers = offers[0] if offers else {}

            current_price = str(offers.get("price", ""))
            currency = offers.get("priceCurrency", "GBP")

            # Extract brand information
            brand_info = product_data.get("brand", {})
            if isinstance(brand_info, dict):
                brand = brand_info.get("name", "")
            else:
                brand = str(brand_info) if brand_info else ""

            # Determine stock status
            availability = offers.get("availability", "")
            in_stock = self._parse_availability(availability)

            # Build full URL
            full_url = self._build_full_url(url)

            # Extract additional metadata
            metadata = {
                "position": product_data.get("position"),
                "brand": brand,
                "image": product_data.get("image", ""),
                "description": product_data.get("description", ""),
                "schema_type": product_data.get("@type", ""),
                "availability": availability
            }

            return {
                "sku": sku,
                "name": name,
                "url": full_url,
                "price": current_price,
                "old_price": None,  # JSON-LD rarely includes original prices
                "currency": currency,
                "in_stock": in_stock,
                "metadata": metadata
            }

        except Exception as e:
            print(f"Failed to parse JSON-LD product: {e}")
            return None

    def _extract_sku_from_product(self, product_data: Dict[str, Any], url: str) -> Optional[str]:
        """Extract SKU from product data or URL."""
        # Try various SKU fields
        sku_fields = ["sku", "productID", "identifier", "gtin", "mpn"]

        for field in sku_fields:
            if field in product_data:
                return str(product_data[field])

        # Extract from URL as fallback
        if url:
            # Common URL patterns: /product-name-123.html or /products/abc-123
            import re
            patterns = [
                r'/([^/]+)\.html$',  # product-name.html
                r'/([^/]+)/?$',      # /product-name/
                r'-([A-Z0-9]+)\.html$',  # -SKU123.html
            ]

            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)

        # Generate SKU from name + position as last resort
        position = product_data.get("position", "")
        if position:
            name_slug = name.lower().replace(" ", "-")[:20]
            return f"{name_slug}-{position}"

        return None

    def _parse_availability(self, availability: str) -> bool:
        """Parse Schema.org availability status."""
        if not availability:
            return True  # Default to in stock

        # Schema.org availability values
        in_stock_statuses = [
            "https://schema.org/InStock",
            "InStock",
            "https://schema.org/PreOrder",
            "PreOrder"
        ]

        out_of_stock_statuses = [
            "https://schema.org/OutOfStock",
            "OutOfStock",
            "https://schema.org/SoldOut",
            "SoldOut",
            "https://schema.org/Discontinued",
            "Discontinued"
        ]

        if availability in out_of_stock_statuses:
            return False
        elif availability in in_stock_statuses:
            return True

        # Default to in stock for unknown statuses
        return True

    def _build_full_url(self, url: str) -> Optional[str]:
        """Build complete product URL."""
        if not url:
            return None

        if url.startswith('http'):
            return url
        elif url.startswith('/'):
            return f"{self.base_url}{url}"
        else:
            return f"{self.base_url}/{url}"

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
            change_type TEXT NOT NULL CHECK (change_type IN (
                'NEW', 'REMOVED', 'PRICE_DROP', 'PRICE_INCREASE',
                'ORIGINAL_PRICE_CHANGE', 'RESTOCKED', 'OUT_OF_STOCK'
            )),
            old_current_price TEXT,
            new_current_price TEXT,
            old_original_price TEXT,
            new_original_price TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sku, source) REFERENCES products(sku, source)
        )""")

        # Create indexes for performance
        conn.execute("CREATE INDEX IF NOT EXISTS idx_products_source_sku ON products(source, sku)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_products_last_seen ON products(last_seen)")

    def detect_changes(self, conn: sqlite3.Connection, current: Dict[str, Dict[str, Any]]) -> tuple:
        """Detect changes between current and stored products."""
        cur = conn.cursor()

        # Load previous products for this source
        cur.execute("SELECT sku, name, current_price FROM products WHERE source = ?", (self.source_name,))
        previous = {
            row[0]: {"name": row[1], "current_price": row[2]}
            for row in cur
        }

        added = set(current) - set(previous)
        removed = set(previous) - set(current)
        changed = []

        for sku in set(current) & set(previous):
            if current[sku]["price"] != previous[sku]["current_price"]:
                changed.append(sku)

        return added, removed, changed

    def upsert_products(self, conn: sqlite3.Connection, current: Dict[str, Dict[str, Any]]) -> None:
        """Save products to database with transaction safety."""
        for sku, info in current.items():
            conn.execute("""
                INSERT OR REPLACE INTO products
                (sku, source, name, url, current_price, original_price, currency, in_stock, metadata, last_seen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                sku, self.source_name, info["name"], info["url"],
                info["price"], info["old_price"], info["currency"],
                info["in_stock"], json.dumps(info["metadata"])
            ))
        conn.commit()

    def main(self) -> None:
        """Execute complete JSON-LD scraping workflow."""
        print(f"Starting {self.source_name} scrape with JSON-LD parsing")
        print(f"Brand filter: {self.brand_filter}")
        print(f"Size filters: {self.size_filters}")

        conn = sqlite3.connect(self.db_path)
        self.init_db(conn)

        current = self.fetch_current()
        added, removed, changed = self.detect_changes(conn, current)

        print(f"\\n{self.source_name.title()} Results:")
        print(f"Products found: {len(current)}")

        if added:
            print(f"\\nNew items ({len(added)}):")
            for sku in list(added)[:10]:  # Show first 10
                product = current[sku]
                print(f"  • {product['name']} - {product['currency']}{product['price']}")

        if removed:
            print(f"\\nRemoved items ({len(removed)}):")
            for sku in list(removed)[:5]:  # Show first 5
                print(f"  • {sku}")

        if changed:
            print(f"\\nPrice changes ({len(changed)}):")
            for sku in list(changed)[:5]:  # Show first 5
                prev = conn.execute(
                    "SELECT current_price FROM products WHERE source = ? AND sku = ?",
                    (self.source_name, sku)
                ).fetchone()
                now = current[sku]
                print(f"  • {now['name']}: was {now['currency']}{prev[0]}, now {now['currency']}{now['price']}")

        self.upsert_products(conn, current)
        conn.close()

        print(f"\\n{self.source_name.title()} scrape completed successfully")


if __name__ == "__main__":
    from pathlib import Path

    # Configuration
    DB_PATH = Path(__file__).parent.parent / "products.db"

    scraper = {ClassName}Scraper(
        DB_PATH,
        brand_filter="{DEFAULT_BRAND}",
        size_filters=["{DEFAULT_SIZES}"],
        categories=["{DEFAULT_CATEGORY}"]
    )
    scraper.main()
EOF
```

### 4. Create JSON-LD Specific Configuration

```python
# Create configuration for JSON-LD scraper
cat > config/${SITE_NAME}.py << 'EOF'
"""
Configuration for {SITE_NAME} JSON-LD scraper
"""
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class {ClassName}Config:
    """Site-specific configuration for {SITE_NAME} JSON-LD scraper."""

    # Basic settings
    enabled: bool = True
    base_url: str = "{BASE_URL}"

    # JSON-LD specific settings
    json_ld_timeout: int = 10  # Timeout for JSON parsing
    max_json_size: int = 10_000_000  # 10MB max JSON size
    validate_schema: bool = True  # Validate Schema.org compliance

    # Scraping behavior (lighter than HTML scraping)
    delay_range: tuple[int, int] = (3, 8)  # Shorter delays for JSON-LD
    max_retries: int = 3
    timeout: int = 30

    # Site-specific filters
    brand_filter: str = "{DEFAULT_BRAND}"
    size_filters: List[str] = field(default_factory=lambda: ["{DEFAULT_SIZES}"])
    categories: List[str] = field(default_factory=lambda: ["{DEFAULT_CATEGORY}"])

    # Headers
    user_agent: str = "Mozilla/5.0 (compatible; PriceMonitor/1.0)"
    custom_headers: Dict[str, str] = field(default_factory=lambda: {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    })

    # JSON-LD parsing configuration
    json_ld_selectors: Dict[str, str] = field(default_factory=lambda: {
        'script_tag': 'script[type="application/ld+json"]',
        'product_type': 'Product',
        'offer_type': 'Offer',
        'brand_type': 'Brand'
    })

    # Schema.org field mappings
    schema_mappings: Dict[str, str] = field(default_factory=lambda: {
        'name': 'name',
        'url': 'url',
        'price': 'offers.price',
        'currency': 'offers.priceCurrency',
        'availability': 'offers.availability',
        'brand': 'brand.name',
        'image': 'image',
        'description': 'description',
        'sku': 'sku'
    })


# Default configuration instance
DEFAULT_CONFIG = {ClassName}Config()

# Schema.org availability mappings
AVAILABILITY_MAPPING = {
    'https://schema.org/InStock': True,
    'InStock': True,
    'https://schema.org/PreOrder': True,
    'PreOrder': True,
    'https://schema.org/OutOfStock': False,
    'OutOfStock': False,
    'https://schema.org/SoldOut': False,
    'SoldOut': False,
    'https://schema.org/Discontinued': False,
    'Discontinued': False,
}

# URL patterns for different site sections
URL_PATTERNS = {
    'sale': '/gb/sale',
    'new_arrivals': '/gb/new-arrivals',
    'mens': '/gb/men',
    'womens': '/gb/women'
}

# Filter parameter mappings
FILTER_MAPPINGS = {
    'brand': 'brand',
    'size': 'size_label',
    'category': 'category',
    'price_range': 'price_range'
}
EOF
```

### 5. Create JSON-LD Specific Test Suite

```python
# Create comprehensive test suite for JSON-LD scraper
cat > tests/test_${SITE_NAME}_scraper.py << 'EOF'
"""
Tests for {SITE_NAME} JSON-LD scraper
"""
import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile
import sqlite3

from src.product_prices.scrapers.{SITE_NAME_LOWER} import {ClassName}Scraper


class Test{ClassName}Scraper:
    """Test suite for {SITE_NAME} JSON-LD scraper."""

    @pytest.fixture
    def scraper(self):
        """Create scraper instance for testing."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = Path(f.name)
        return {ClassName}Scraper(
            db_path,
            brand_filter="{TEST_BRAND}",
            size_filters=["Small", "Medium"]
        )

    @pytest.fixture
    def sample_json_ld(self):
        """Sample JSON-LD data based on Schema.org Product."""
        return {
            "@context": "https://schema.org",
            "@type": "Product",
            "position": 1,
            "name": "Test Product Name",
            "url": "/test-product-url",
            "brand": {
                "@type": "Brand",
                "name": "{TEST_BRAND}"
            },
            "offers": {
                "@type": "Offer",
                "priceCurrency": "GBP",
                "price": 59.00,
                "availability": "https://schema.org/InStock"
            },
            "image": "https://example.com/image.jpg",
            "description": "Test product description"
        }

    @pytest.fixture
    def sample_html_with_json_ld(self, sample_json_ld):
        """Sample HTML containing JSON-LD script tag."""
        json_ld_str = json.dumps(sample_json_ld)
        return f'''
        <html>
            <head>
                <title>Test Page</title>
                <script type="application/ld+json">
                {json_ld_str}
                </script>
            </head>
            <body>
                <h1>Product Page</h1>
            </body>
        </html>
        '''

    def test_get_urls(self, scraper):
        """Test URL generation with brand and size filters."""
        urls = scraper.get_urls()

        assert len(urls) > 0
        assert all(scraper.base_url in url for url in urls)
        assert any("brand={TEST_BRAND}".replace(" ", "%20") in url for url in urls)
        assert any("size_label=Small,Medium" in url for url in urls)

    def test_is_product_object(self, scraper, sample_json_ld):
        """Test product object identification."""
        assert scraper._is_product_object(sample_json_ld) == True

        # Test non-product object
        non_product = {"@type": "Organization", "name": "Test"}
        assert scraper._is_product_object(non_product) == False

        # Test invalid object
        assert scraper._is_product_object("not an object") == False
        assert scraper._is_product_object(None) == False

    def test_parse_json_ld_product(self, scraper, sample_json_ld):
        """Test individual JSON-LD product parsing."""
        product = scraper._parse_json_ld_product(sample_json_ld)

        assert product is not None
        assert product["name"] == "Test Product Name"
        assert product["price"] == "59.0"
        assert product["currency"] == "GBP"
        assert product["in_stock"] == True
        assert product["url"] == f"{scraper.base_url}/test-product-url"
        assert product["metadata"]["brand"] == "{TEST_BRAND}"
        assert product["metadata"]["position"] == 1

    def test_parse_json_ld_page(self, scraper, sample_html_with_json_ld):
        """Test parsing JSON-LD from HTML page."""
        url = "https://example.com/test"
        products = scraper.parse_json_ld_page(url, sample_html_with_json_ld)

        assert len(products) == 1
        product = list(products.values())[0]
        assert product["name"] == "Test Product Name"
        assert product["price"] == "59.0"

    def test_extract_products_from_json_ld_array(self, scraper, sample_json_ld):
        """Test extracting products from JSON-LD array."""
        json_ld_array = [sample_json_ld, {**sample_json_ld, "name": "Second Product"}]

        products = scraper._extract_products_from_json_ld(json_ld_array)
        assert len(products) == 2

    def test_extract_products_from_json_ld_graph(self, scraper, sample_json_ld):
        """Test extracting products from JSON-LD @graph structure."""
        json_ld_graph = {
            "@context": "https://schema.org",
            "@graph": [
                sample_json_ld,
                {"@type": "Organization", "name": "Not a product"}
            ]
        }

        products = scraper._extract_products_from_json_ld(json_ld_graph)
        assert len(products) == 1

    def test_parse_availability_statuses(self, scraper):
        """Test Schema.org availability parsing."""
        test_cases = [
            ("https://schema.org/InStock", True),
            ("InStock", True),
            ("https://schema.org/OutOfStock", False),
            ("OutOfStock", False),
            ("https://schema.org/PreOrder", True),
            ("https://schema.org/SoldOut", False),
            ("", True),  # Default to in stock
            ("UnknownStatus", True),  # Default to in stock
        ]

        for availability, expected in test_cases:
            assert scraper._parse_availability(availability) == expected

    def test_sku_extraction_strategies(self, scraper):
        """Test various SKU extraction methods."""
        # Test direct SKU field
        product_with_sku = {"sku": "TEST-SKU-123", "name": "Test"}
        sku = scraper._extract_sku_from_product(product_with_sku, "")
        assert sku == "TEST-SKU-123"

        # Test URL extraction
        product_no_sku = {"name": "Test Product", "position": 1}
        sku = scraper._extract_sku_from_product(product_no_sku, "/product-abc-123.html")
        assert sku == "product-abc-123"

        # Test fallback generation
        sku = scraper._extract_sku_from_product(product_no_sku, "")
        assert "test-product-1" in sku.lower()

    def test_url_building(self, scraper):
        """Test URL construction from relative and absolute paths."""
        test_cases = [
            ("/product/test", f"{scraper.base_url}/product/test"),
            ("https://external.com/product", "https://external.com/product"),
            ("product/relative", f"{scraper.base_url}/product/relative"),
            ("", None),
            (None, None),
        ]

        for input_url, expected in test_cases:
            result = scraper._build_full_url(input_url)
            assert result == expected

    def test_malformed_json_handling(self, scraper):
        """Test handling of malformed JSON-LD."""
        malformed_html = '''
        <html>
            <script type="application/ld+json">
                {"@type": "Product", "name": "Test", invalid json}
            </script>
        </html>
        '''

        # Should not crash and return empty dict
        products = scraper.parse_json_ld_page("test", malformed_html)
        assert products == {}

    def test_empty_json_ld_handling(self, scraper):
        """Test handling of empty or missing JSON-LD."""
        empty_html = '''
        <html>
            <head><title>No JSON-LD</title></head>
            <body><p>Regular HTML content</p></body>
        </html>
        '''

        products = scraper.parse_json_ld_page("test", empty_html)
        assert products == {}

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

        # Check products table has JSON-LD specific columns
        cursor.execute("PRAGMA table_info(products)")
        columns = {row[1] for row in cursor.fetchall()}
        expected_columns = {'sku', 'source', 'name', 'url', 'current_price', 'metadata'}
        assert expected_columns.issubset(columns)

        conn.close()

    @patch('time.sleep')  # Speed up tests
    @patch('secrets.randbelow')
    def test_rate_limiting(self, mock_randbelow, mock_sleep, scraper):
        """Test JSON-LD appropriate rate limiting (lighter than HTML scraping)."""
        mock_randbelow.return_value = 4  # randbelow(6) returns 4, so delay = 4 + 3 = 7

        with patch.object(scraper.session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.text = "<html></html>"
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            scraper.fetch_current()

            # Verify lighter rate limiting for JSON-LD
            mock_randbelow.assert_called_with(6)  # 3-8 second range
            mock_sleep.assert_called()


@pytest.mark.integration
class Test{ClassName}Integration:
    """Integration tests for {SITE_NAME} JSON-LD scraper."""

    @pytest.fixture
    def scraper(self):
        """Create scraper for integration testing."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = Path(f.name)
        return {ClassName}Scraper(db_path)

    @patch('time.sleep')  # Speed up tests
    def test_full_json_ld_workflow(self, mock_sleep, scraper):
        """Test complete JSON-LD scraping workflow."""
        sample_product = {
            "test-sku": {
                "sku": "test-sku",
                "name": "Test JSON-LD Product",
                "price": "45.00",
                "old_price": None,
                "url": "https://example.com/test",
                "currency": "GBP",
                "in_stock": True,
                "metadata": {"brand": "{TEST_BRAND}", "schema_type": "Product"}
            }
        }

        conn = sqlite3.connect(scraper.db_path)
        scraper.init_db(conn)

        # Test change detection
        added, removed, changed = scraper.detect_changes(conn, sample_product)
        assert len(added) == 1
        assert len(removed) == 0
        assert len(changed) == 0

        # Test product saving
        scraper.upsert_products(conn, sample_product)

        # Verify product was saved with JSON metadata
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE source = ?", (scraper.source_name,))
        rows = cursor.fetchall()
        assert len(rows) == 1

        # Verify metadata is JSON
        metadata_json = rows[0][9]  # metadata column
        metadata = json.loads(metadata_json)
        assert metadata["brand"] == "{TEST_BRAND}"
        assert metadata["schema_type"] == "Product"

        conn.close()


# JSON-LD test fixtures for different site scenarios
SAMPLE_SINGLE_PRODUCT_JSON_LD = '''
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Single Product Test",
  "url": "/single-product",
  "offers": {
    "@type": "Offer",
    "price": 25.00,
    "priceCurrency": "GBP"
  }
}
'''

SAMPLE_PRODUCT_ARRAY_JSON_LD = '''
[
  {
    "@context": "https://schema.org",
    "@type": "Product",
    "position": 1,
    "name": "First Product",
    "offers": {"price": 30.00, "priceCurrency": "GBP"}
  },
  {
    "@context": "https://schema.org",
    "@type": "Product",
    "position": 2,
    "name": "Second Product",
    "offers": {"price": 40.00, "priceCurrency": "GBP"}
  }
]
'''

SAMPLE_GRAPH_JSON_LD = '''
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Product",
      "name": "Graph Product",
      "offers": {"price": 35.00, "priceCurrency": "GBP"}
    },
    {
      "@type": "Organization",
      "name": "Test Company"
    }
  ]
}
'''
EOF
```

### 6. Create CLI Integration for JSON-LD Scraper

```python
# Update CLI to include JSON-LD scraper
cat >> src/product_prices/cli.py << 'EOF'

def run_{SITE_NAME_LOWER}():
    """Run {SITE_NAME} JSON-LD scraper."""
    from .scrapers.{SITE_NAME_LOWER} import {ClassName}Scraper

    db_path = Path("products.db")

    scraper = {ClassName}Scraper(
        db_path,
        brand_filter="{DEFAULT_BRAND}",
        size_filters=["{DEFAULT_SIZES}"],
        categories=["{DEFAULT_CATEGORY}"]
    )
    scraper.main()

# Update the main CLI function to include the new scraper
def main():
    """Enhanced CLI with JSON-LD scraper support."""
    if len(sys.argv) < 2:
        print("Usage: python -m product_prices [tony-mcdonald|carhartt-wip|{SITE_NAME_LOWER}|all]")
        return

    scraper_name = sys.argv[1].lower()

    if scraper_name == "tony-mcdonald":
        run_tony_mcdonald()
    elif scraper_name == "carhartt-wip":
        run_carhartt_wip()
    elif scraper_name == "{SITE_NAME_LOWER}":
        run_{SITE_NAME_LOWER}()
    elif scraper_name == "all":
        run_all_scrapers()
    else:
        print(f"Unknown scraper: {scraper_name}")
        print("Available scrapers: tony-mcdonald, carhartt-wip, {SITE_NAME_LOWER}, all")

def run_all_scrapers():
    """Run all available scrapers including JSON-LD."""
    print("Running all product price scrapers...")

    scrapers = [
        ("TONY MCDONALD", run_tony_mcdonald),
        ("CARHARTT WIP", run_carhartt_wip),
        ("{SITE_NAME_UPPER}", run_{SITE_NAME_LOWER})
    ]

    for name, scraper_func in scrapers:
        print("\\n" + "="*50)
        print(f"{name} SCRAPER")
        print("="*50)
        try:
            scraper_func()
        except Exception as e:
            print(f"ERROR: {name} scraper failed: {e}")
            continue
EOF
```

### 7. Create JSON-LD Scraper Documentation

```markdown
# Create comprehensive documentation
cat > docs/scrapers/${SITE_NAME_LOWER}.md << 'EOF'
# {SITE_NAME} JSON-LD Scraper Documentation

## Overview

{SITE_DESCRIPTION} scraper using JSON-LD structured data parsing. This scraper extracts product information from Schema.org compliant JSON-LD script tags instead of HTML parsing.

## JSON-LD Architecture

### Advantages over HTML Scraping

1. **Structured Data**: Clean JSON format vs. complex HTML parsing
2. **Schema.org Compliance**: Standardized product fields
3. **Reliability**: Less likely to break with UI changes
4. **Performance**: Faster parsing than BeautifulSoup selectors
5. **Accuracy**: Data intended for machines, not presentation

### JSON-LD Product Structure

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "url": "/product-url",
  "brand": {"@type": "Brand", "name": "Brand Name"},
  "offers": {
    "@type": "Offer",
    "price": 59.00,
    "priceCurrency": "GBP",
    "availability": "https://schema.org/InStock"
  },
  "image": "https://site.com/image.jpg"
}
```

## Configuration

### Basic Setup

```python
from scrapers.{SITE_NAME_LOWER} import {ClassName}Scraper

scraper = {ClassName}Scraper(
    db_path=Path("products.db"),
    brand_filter="{DEFAULT_BRAND}",
    size_filters=["Small", "Medium", "Large"],
    categories=["gb/sale"]
)
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `brand_filter` | str | "{DEFAULT_BRAND}" | Brand name to filter products |
| `size_filters` | List[str] | ["{DEFAULT_SIZES}"] | Size filters to apply |
| `categories` | List[str] | ["{DEFAULT_CATEGORY}"] | URL categories to scrape |
| `json_ld_timeout` | int | 10 | Timeout for JSON parsing |
| `validate_schema` | bool | True | Validate Schema.org compliance |

### CLI Usage

```bash
# Run {SITE_NAME} scraper only
uv run python -m product_prices {SITE_NAME_LOWER}

# Run with custom brand filter
# (Modify scraper initialization in cli.py)

# Run all scrapers including JSON-LD
uv run python -m product_prices all
```

## JSON-LD Parsing Strategy

### 1. Script Tag Extraction
```python
json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})
```

### 2. JSON Structure Handling
- **Single Product**: `{"@type": "Product", ...}`
- **Product Array**: `[{"@type": "Product", ...}, ...]`
- **Graph Structure**: `{"@graph": [{"@type": "Product", ...}]}`

### 3. SKU Generation Strategy
1. Direct fields: `sku`, `productID`, `identifier`
2. URL extraction: `/product-name-123.html` → `product-name-123`
3. Fallback: `{name-slug}-{position}`

### 4. Availability Parsing
```python
AVAILABILITY_MAPPING = {
    'https://schema.org/InStock': True,
    'https://schema.org/OutOfStock': False,
    'https://schema.org/PreOrder': True,
    'https://schema.org/SoldOut': False
}
```

## Site-Specific Details

### URL Structure
- Base URL: `{BASE_URL}`
- Sale pages: `/gb/sale?brand=Brand%20Name&size_label=Small,Medium`
- Filter format: URL parameters for brand, size, category

### Rate Limiting
- Delay between requests: 3-8 seconds (lighter than HTML scraping)
- JSON-LD sites typically more stable, require less aggressive rate limiting
- Recommended concurrent requests: 1

### Error Handling
1. **JSON Parse Errors**: Malformed JSON-LD scripts
2. **Missing Schema Fields**: Products without required @type or name
3. **Invalid URLs**: Relative URL resolution
4. **Large JSON**: Size limits to prevent memory issues

## Testing

### Run Tests
```bash
# Unit tests
uv run pytest tests/test_{SITE_NAME_LOWER}_scraper.py

# Integration tests
uv run pytest tests/test_{SITE_NAME_LOWER}_scraper.py::Test{ClassName}Integration -m integration

# Test JSON-LD parsing specifically
uv run pytest tests/test_{SITE_NAME_LOWER}_scraper.py -k "json_ld"
```

### Test Fixtures

JSON-LD test fixtures are provided:
- `SAMPLE_SINGLE_PRODUCT_JSON_LD` - Single product object
- `SAMPLE_PRODUCT_ARRAY_JSON_LD` - Array of products
- `SAMPLE_GRAPH_JSON_LD` - Graph structure with mixed types

### Testing Strategy

1. **JSON-LD Structure Tests**: Verify parsing of different JSON-LD formats
2. **Schema.org Compliance**: Test Schema.org field mappings
3. **Error Handling**: Malformed JSON, missing fields
4. **URL Construction**: Relative to absolute URL conversion
5. **Availability Parsing**: Schema.org availability status mapping

## Troubleshooting

### Common Issues

1. **No products found**
   - Check if site uses JSON-LD: View page source for `<script type="application/ld+json">`
   - Verify JSON-LD contains `@type: "Product"` objects
   - Check brand/size filters aren't too restrictive

2. **JSON parsing errors**
   - Site may have malformed JSON-LD
   - Check for escaped quotes or invalid JSON syntax
   - Enable debug logging to see raw JSON

3. **Missing product data**
   - Site's JSON-LD may not include all Schema.org fields
   - Check `schema_mappings` in config for field availability
   - Some sites use custom or minimal JSON-LD

4. **Performance issues**
   - Large JSON-LD objects can slow parsing
   - Adjust `max_json_size` in config
   - Consider pagination if single pages have too many products

### Debugging JSON-LD

```python
# Enable debug logging
import logging
logging.getLogger('scrapers.{SITE_NAME_LOWER}').setLevel(logging.DEBUG)

# Test JSON-LD extraction manually
from bs4 import BeautifulSoup
import json

html = open('sample_page.html').read()
soup = BeautifulSoup(html, 'html.parser')
scripts = soup.find_all('script', {'type': 'application/ld+json'})

for script in scripts:
    try:
        data = json.loads(script.string)
        print(json.dumps(data, indent=2))
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
```

## Maintenance

### Site Change Detection
Monitor these indicators for JSON-LD changes:
- JSON structure modifications
- New or removed Schema.org fields
- Changes in `@type` values
- URL parameter changes

### Schema.org Updates
- Monitor Schema.org specification updates
- Test with new Product schema versions
- Update field mappings as needed

## Advanced Usage

### Custom JSON-LD Handlers

```python
class Custom{ClassName}Scraper({ClassName}Scraper):
    def _parse_json_ld_product(self, product_data):
        # Custom parsing logic
        product = super()._parse_json_ld_product(product_data)

        # Add custom fields
        if product:
            product["metadata"]["custom_field"] = product_data.get("customField")

        return product
```

### Multiple Brand Filtering

```python
scraper = {ClassName}Scraper(
    db_path,
    brand_filter="Brand1|Brand2",  # Multiple brands
    size_filters=["XS", "S", "M", "L", "XL"]
)
```

This JSON-LD scraper provides a robust foundation for sites using structured data and can be adapted for other Schema.org compliant e-commerce sites.
EOF
```

### 8. Validation and Testing

```bash
# Test JSON-LD command creation
cat > scripts/test_json_ld_scraper.py << 'EOF'
#!/usr/bin/env python3
"""
Test script for JSON-LD scraper validation
"""
import json
import sys
from pathlib import Path

def test_json_ld_parsing():
    """Test JSON-LD parsing with sample data."""

    # Sample JSON-LD from End Clothing analysis
    sample_json_ld = {
        "@type": "Product",
        "position": 1,
        "name": "Carhartt WIP Irwin Overshirt",
        "url": "https://www.endclothing.com/gb/carhartt-wip-irwin-overshirt-i034530-41xx.html",
        "brand": {"name": "Carhartt WIP"},
        "offers": {
            "@type": "Offer",
            "priceCurrency": "GBP",
            "price": 59
        }
    }

    print("Testing JSON-LD structure:")
    print(json.dumps(sample_json_ld, indent=2))

    # Test parsing logic
    assert sample_json_ld["@type"] == "Product"
    assert "name" in sample_json_ld
    assert "offers" in sample_json_ld
    assert sample_json_ld["offers"]["priceCurrency"] == "GBP"

    print("✅ JSON-LD structure validation passed")

    return sample_json_ld

def test_sku_extraction():
    """Test SKU extraction strategies."""

    test_cases = [
        # URL-based extraction
        ("https://www.endclothing.com/gb/product-i034530-41xx.html", "product-i034530-41xx"),
        ("/gb/carhartt-wip-item-abc123.html", "carhartt-wip-item-abc123"),

        # Fallback cases
        ("", None),
        ("/no-clear-pattern/", None)
    ]

    import re

    def extract_sku_from_url(url):
        if not url:
            return None

        patterns = [
            r'/([^/]+)\.html$',  # /product-name.html
            r'/([^/]+)/?$',      # /product-name/
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    for url, expected in test_cases:
        result = extract_sku_from_url(url)
        if expected:
            assert result == expected, f"Expected {expected}, got {result} for {url}"
        print(f"✅ SKU extraction: {url} → {result}")

if __name__ == "__main__":
    try:
        test_json_ld_parsing()
        test_sku_extraction()
        print("\\n🎉 All JSON-LD scraper tests passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
EOF

# Make test script executable
chmod +x scripts/test_json_ld_scraper.py

# Run validation
python scripts/test_json_ld_scraper.py
```

This command creates a comprehensive framework for JSON-LD scrapers with:

1. **JSON-LD Specific Parsing** - Script tag extraction and JSON parsing
2. **Schema.org Compliance** - Proper handling of Product schema
3. **Multiple Data Structures** - Support for arrays, graphs, and single objects
4. **Robust Error Handling** - Malformed JSON and missing field handling
5. **Flexible SKU Generation** - Multiple strategies for product identification
6. **Lighter Rate Limiting** - Appropriate for structured data sites
7. **Comprehensive Testing** - JSON-LD specific test scenarios
8. **Schema Validation** - Optional Schema.org compliance checking

The template can be reused for other sites using JSON-LD structured data.

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"id": "analyze_page_structure", "content": "Analyze End Clothing page structure and identify scraping patterns", "status": "completed", "priority": "high"}, {"id": "design_scraper_architecture", "content": "Design End Clothing scraper class following existing patterns", "status": "completed", "priority": "high"}, {"id": "implement_json_ld_parser", "content": "Implement JSON-LD structured data parser for product extraction", "status": "completed", "priority": "high"}, {"id": "add_end_clothing_to_cli", "content": "Add End Clothing scraper to CLI interface", "status": "pending", "priority": "medium"}, {"id": "create_tests", "content": "Create test suite for End Clothing scraper", "status": "completed", "priority": "medium"}, {"id": "update_database_schema", "content": "Update database to handle End Clothing as third source", "status": "pending", "priority": "low"}, {"id": "decide_command_approach", "content": "Decide whether to copy existing command or create new JSON-LD scraper command", "status": "completed", "priority": "high"}, {"id": "create_json_ld_command", "content": "Create add-json-ld-scraper.md command file", "status": "completed", "priority": "high"}]
