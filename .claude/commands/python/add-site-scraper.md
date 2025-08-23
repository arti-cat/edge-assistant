# Add Site Scraper

Add a new site-specific scraper to the WIPWatch product price monitoring system. This command provides structured implementation patterns based on our existing scrapers: Tony McDonald (defensive parsing), Carhartt WIP (Playwright browser automation), End Clothing (JSON-LD parsing), and HUH Store (Shopify parsing).

## Usage

```bash
# Add a Playwright browser automation scraper (for Next.js/React sites with client-side rendering)
/add-site-scraper --site="new_site" --type="playwright" --base-url="https://example.com"

# Add a JSON-LD structured data scraper (for sites with Schema.org product data)
/add-site-scraper --site="new_site" --type="json-ld" --base-url="https://example.com"

# Add a defensive scraper (for sites with complex/changing structure)
/add-site-scraper --site="new_site" --type="defensive" --base-url="https://example.com"

# Add a Shopify scraper (for Shopify-based stores)
/add-site-scraper --site="new_site" --type="shopify" --base-url="https://example.com"
```

## Instructions

### 1. Analyze Target Site Structure

First, download and analyze the target site to determine the appropriate parsing strategy:

```bash
# Download sample page for analysis
SITE_NAME="${1:-new_site}"
TARGET_URL="${2:-https://example.com/products}"

curl -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
     "$TARGET_URL" -o "${SITE_NAME}_sample.html"

# Examine structure
head -200 "${SITE_NAME}_sample.html"
```

Identify using our proven patterns:

**Use Carhartt WIP as your Playwright browser automation example:**
- Next.js site with client-side rendering requiring browser automation
- JavaScript-generated product data that needs page interaction
- Categories: men-sale, women-sale, accessories with pagination
- Uses Playwright for browser automation and data extraction

**Use End Clothing as your JSON-LD structured data example:**
- Rich Schema.org Product objects in JSON-LD script tags
- Well-structured product data: name, offers, brand, description
- Clean parsing from structured data without complex HTML traversal

**Use Tony McDonald as your defensive parsing example:**
- Missing data attributes requiring element parsing and regex fallbacks
- Complex nested HTML requiring multiple selector strategies
- Prices embedded in text: regex patterns like `r"£\s?\d+[.,]?\d*"`

**Use HUH Store as your Shopify example:**
- Shopify-based store with predictable URL patterns
- Product data in JSON format or structured HTML
- Category-based navigation with collection pages

Create analysis document:

```bash
cat > docs/site_analysis_${SITE_NAME}.md << 'EOF'
# Site Analysis: Example Site (use Carhartt WIP as reference)

## Strategy Decision
Based on HTML analysis: [X] Data-driven (like Carhartt WIP) [ ] Defensive (like Tony McDonald)

## URL Structure (Carhartt WIP Pattern)
- Base URL: https://www.carhartt-wip.com
- Sale pages: /en/men-summer-sale, /en/women-summer-sale
- Pagination: ?page=1 through ?page=14+
- Size filters: ?filter_size=XS&filter_size=S&filter_size=M

## Product Structure (Carhartt WIP Pattern)
- Product container: `article.product-grid-item`
- Product link: `a.product-grid-item-container`
- SKU extraction: `data-productId="'I034405_02_XX'"` (strip quotes)
- Name extraction: `data-name="'S/S Drip Script T-Shirt White'"` (strip quotes)
- Price structure: `span.strikeout.country_gbp` (original), `span.sale.country_gbp` (current)

## Rate Limiting Requirements (Carhartt WIP Standards)
- Delay range: 5-15 seconds (cryptographically secure)
- Required headers: Mozilla/5.0 User-Agent, Accept-Language: en-GB
- Robots.txt compliance: Respectful scraping, check robots.txt

## Implementation Notes
Use data-driven approach like Carhartt WIP for reliable extraction
EOF
```

### 2. Think and Choose Implementation Template

Before implementing, ask Claude to think about the best approach:

```
Think about the scraping strategy for this site:
1. Does it have clean data attributes like Carhartt WIP's data-productId, data-name, data-price?
2. Or does it need defensive parsing like Tony McDonald with regex fallbacks?
3. How should pagination be handled?
4. What rate limiting is appropriate?
```

Based on your analysis, select the appropriate template:

#### Template A: Data-Driven Approach (Carhartt WIP Pattern)
Use when sites provide rich `data-*` attributes and structured HTML like Carhartt WIP:

```python
# Create scraper using data-driven template (based on Carhartt WIP pattern)
cat > src/product_prices/scrapers/${SITE_NAME}.py << 'EOF'
"""
{SITE_NAME} Scraper - Data-Driven Implementation
Based on Carhartt WIP scraper pattern with clean data attributes
"""
import secrets
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup

from ..database_v2 import get_database_type, get_db_connection
from ..category_mapper import CategoryMapper
from ..utils import normalize_category


class {ClassName}Scraper:
    """Scraper for {SITE_NAME} using modern PostgreSQL database and structured parsing."""

    def __init__(self, db_path: Path | None, **kwargs: Any) -> None:
        self.source_name = "{SITE_NAME_LOWER}"
        self.base_url = "{BASE_URL}"
        # db_path kept for compatibility but not used with database_v2
        self.db_path = db_path
        # Site-specific configuration
        self.categories = kwargs.get('categories', ['{DEFAULT_CATEGORY}'])
        self.sizes = kwargs.get('sizes', ['{DEFAULT_SIZES}'])
        self.max_pages = kwargs.get('max_pages', 15)

        # Category mapping for normalized categories
        self.category_mapper = CategoryMapper()

        # Configure session
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self) -> None:
        """Configure session with appropriate headers."""
        self.session.headers.update({
            'User-Agent': '{USER_AGENT}',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def get_urls(self) -> list[str]:
        """Generate URLs for all categories and pages."""
        urls = []

        for category in self.categories:
            # Build base URL with filters
            size_params = "&".join(f"filter_size={size}" for size in self.sizes)
            base_category_url = f"{self.base_url}/{category}"

            # Add pagination
            for page in range(1, self.max_pages + 1):
                url = f"{base_category_url}?{size_params}&page={page}"
                urls.append(url)

        return urls

    def get_product_selector(self) -> str:
        """Return CSS selector for product containers."""
        return "article.product-grid-item"  # Use Carhartt WIP pattern

    def parse_product_page(self, url: str, content: str) -> list[dict[str, Any]]:
        """Parse products using structured approach with database integration."""
        soup = BeautifulSoup(content, "html.parser")
        products = []

        for item in soup.select(self.get_product_selector()):
            try:
                product = self._parse_product_item(item)
                if product:
                    products.append(product)
            except Exception as e:
                print(f"Failed to parse product item: {e}")
                continue

        return products

    def _parse_product_item(self, item) -> dict[str, Any] | None:
        """Parse individual product using data attributes with category normalization."""
        # Extract from primary data attributes
        link_el = item.select_one("a.product-grid-item-container")
        if not link_el:
            return None

        # Core product data from attributes
        sku = link_el.get("data-productId", "").strip("'\"")
        name = link_el.get("data-name", "").strip("'\"")
        current_price = link_el.get("data-price", "").strip("'\"")
        product_url = link_el.get("data-link", "").strip("'\"")

        if not sku or not name:
            return None

        # Extract original price (sale detection)
        original_price = None
        strikeout_el = item.select_one("span.strikeout.country_gbp")
        if strikeout_el:
            original_price = strikeout_el.get_text(strip=True)

        # Stock status
        in_stock = self._check_stock_status(item)

        # Construct full URL
        full_url = self._build_product_url(product_url)

        # Category normalization using CategoryMapper
        category = link_el.get("data-categoryId", "").strip("'\"")
        normalized_category = normalize_category(self.category_mapper.map_product_to_category(name))

        # Extract metadata
        metadata = {
            "category": category,
            "variant": link_el.get("data-variant", "").strip("'\""),
            "brand": "{BRAND_NAME}",
        }

        return {
            "sku": sku,
            "source": self.source_name,
            "name": name,
            "url": full_url,
            "current_price": current_price,
            "original_price": original_price,
            "currency": "{DEFAULT_CURRENCY}",
            "in_stock": in_stock,
            "normalized_category": normalized_category,
            "metadata": metadata,
        }

    def _check_stock_status(self, item) -> bool:
        """Determine if product is in stock."""
        # Check for out-of-stock indicators
        stock_indicators = [
            "{OUT_OF_STOCK_SELECTOR_1}",
            "{OUT_OF_STOCK_SELECTOR_2}"
        ]

        for selector in stock_indicators:
            if item.select_one(selector):
                return False

        return True  # Assume in stock if no negative indicators

    def _build_product_url(self, relative_url: str) -> str | None:
        """Build complete product URL."""
        if not relative_url:
            return None

        if relative_url.startswith('http'):
            return relative_url

        return f"{self.base_url}{relative_url}"
EOF
```

#### Template B: Defensive Parsing Approach
Use when sites lack structured data attributes:

```python
# Create scraper using defensive parsing template
cat > src/product_prices/scrapers/${SITE_NAME_LOWER}.py << 'EOF'
"""
{SITE_NAME} Scraper - Defensive Parsing Implementation
"""
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup

from ..database_v2 import get_database_type, get_db_connection
from ..category_mapper import CategoryMapper
from ..utils import normalize_category


class {ClassName}Scraper:
    """Scraper for {SITE_NAME} using defensive parsing with fallbacks."""

    def __init__(self, db_path: Path | None, **kwargs: Any) -> None:
        self.source_name = "{SITE_NAME_LOWER}"
        self.base_url = "{BASE_URL}"
        # db_path kept for compatibility but not used with database_v2
        self.db_path = db_path

        # Category mapping for normalized categories
        self.category_mapper = CategoryMapper()

        # Configure session
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

        # Parsing patterns
        self.price_patterns = [
            r"£\s*(\d+[.,]?\d*)",
            r"(\d+[.,]?\d*)\s*£",
            r"GBP\s*(\d+[.,]?\d*)",
        ]

        self.sku_selectors = [
            "{SKU_SELECTOR_1}",
            "{SKU_SELECTOR_2}",
            "{SKU_SELECTOR_3}"
        ]

        self.name_selectors = [
            "{NAME_SELECTOR_1}",
            "{NAME_SELECTOR_2}",
            "{NAME_SELECTOR_3}"
        ]

    def parse_product_page(self, url: str, content: str) -> List[Product]:
        """Parse products using defensive strategies."""
        soup = BeautifulSoup(content, "html.parser")
        products = []

        for item in soup.select(self.get_product_selector()):
            try:
                product = self._parse_product_item_defensive(item)
                if product:
                    products.append(product)
            except Exception as e:
                self.logger.warning(f"Failed to parse product item: {e}")
                continue

        return products

    def _parse_product_item_defensive(self, item) -> Product | None:
        """Parse product using multiple fallback strategies."""
        # Try multiple methods to extract SKU
        sku = self._extract_sku(item)
        if not sku:
            return None

        # Try multiple methods to extract name
        name = self._extract_name(item)
        if not name:
            return None

        # Extract prices with fallbacks
        current_price = self._extract_current_price(item)
        original_price = self._extract_original_price(item)

        # Extract URL
        product_url = self._extract_url(item)

        # Stock status
        in_stock = self._check_stock_defensive(item)

        return Product(
            sku=sku,
            source=self.source_name,
            name=name,
            url=product_url,
            current_price=current_price,
            original_price=original_price,
            currency="{DEFAULT_CURRENCY}",
            in_stock=in_stock,
            last_seen=datetime.now(),
            metadata={}
        )

    def _extract_sku(self, item) -> str | None:
        """Extract SKU using multiple strategies."""
        # Strategy 1: Data attributes
        for attr in ['data-sku', 'data-product-id', 'data-id']:
            if item.has_attr(attr):
                return str(item[attr])

        # Strategy 2: CSS selectors
        for selector in self.sku_selectors:
            el = item.select_one(selector)
            if el:
                # Try data attributes first
                for attr in ['data-sku', 'id', 'data-product-id']:
                    if el.has_attr(attr):
                        return str(el[attr])

                # Try text content
                text = el.get_text(strip=True)
                if text:
                    return text

        # Strategy 3: URL-based extraction
        link_el = item.select_one('a[href]')
        if link_el:
            href = link_el.get('href', '')
            # Extract from URL patterns
            match = re.search(r'/product/([^/]+)', href)
            if match:
                return match.group(1)

        return None

    def _extract_name(self, item) -> str | None:
        """Extract product name using multiple strategies."""
        for selector in self.name_selectors:
            el = item.select_one(selector)
            if el:
                name = el.get_text(strip=True)
                if name:
                    return name

        return None

    def _extract_current_price(self, item) -> str | None:
        """Extract current price with regex fallbacks."""
        # Strategy 1: Specific price selectors
        price_selectors = [
            "{CURRENT_PRICE_SELECTOR_1}",
            "{CURRENT_PRICE_SELECTOR_2}",
            ".price-current",
            ".sale-price"
        ]

        for selector in price_selectors:
            el = item.select_one(selector)
            if el:
                price_text = el.get_text(strip=True)
                price = self._normalize_price(price_text)
                if price:
                    return price

        # Strategy 2: Regex fallback on entire item text
        item_text = item.get_text(" ")
        for pattern in self.price_patterns:
            matches = re.findall(pattern, item_text)
            if matches:
                return self._normalize_price(matches[-1])  # Take last match

        return None

    def _extract_original_price(self, item) -> str | None:
        """Extract original/strikethrough price."""
        original_selectors = [
            "{ORIGINAL_PRICE_SELECTOR_1}",
            "{ORIGINAL_PRICE_SELECTOR_2}",
            ".price-original",
            ".strikeout",
            ".was-price"
        ]

        for selector in original_selectors:
            el = item.select_one(selector)
            if el:
                price_text = el.get_text(strip=True)
                price = self._normalize_price(price_text)
                if price:
                    return price

        return None

    def _normalize_price(self, price_text: str) -> str | None:
        """Normalize price string to standard format."""
        if not price_text:
            return None

        # Remove common prefixes/suffixes
        price_text = re.sub(r'^(Price:|Was:|Now:|£|GBP)\s*', '', price_text, flags=re.IGNORECASE)
        price_text = re.sub(r'\s*(each|per|item)$', '', price_text, flags=re.IGNORECASE)

        # Extract numeric value
        match = re.search(r'(\d+[.,]?\d*)', price_text)
        if match:
            return match.group(1)

        return None

    def _check_stock_defensive(self, item) -> bool:
        """Check stock status with multiple indicators."""
        out_of_stock_text = [
            "out of stock", "sold out", "unavailable",
            "coming soon", "pre-order"
        ]

        item_text = item.get_text(" ").lower()

        for text in out_of_stock_text:
            if text in item_text:
                return False

        # Check for disabled/sold-out CSS classes
        if item.select_one('.sold-out, .out-of-stock, .unavailable'):
            return False

        return True
EOF
```

### 3. Create Site Configuration

```python
# Create site-specific configuration
cat > config/sites/${SITE_NAME}.py << 'EOF'
"""
Configuration for {SITE_NAME} scraper
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class {ClassName}Config:
    """Site-specific configuration for {SITE_NAME}."""

    # Basic settings
    enabled: bool = True
    base_url: str = "{BASE_URL}"

    # Scraping behavior
    delay_range: tuple[int, int] = ({MIN_DELAY}, {MAX_DELAY})
    max_retries: int = 3
    timeout: int = 30

    # Site-specific settings
    categories: List[str] = None
    sizes: List[str] = None
    max_pages: int = 15

    # Headers and user agent
    user_agent: str = "{USER_AGENT}"
    custom_headers: Dict[str, str] = None

    # Parsing configuration
    selectors: Dict[str, str] = None

    def __post_init__(self):
        if self.categories is None:
            self.categories = ["{DEFAULT_CATEGORY}"]

        if self.sizes is None:
            self.sizes = ["{DEFAULT_SIZES}"]

        if self.custom_headers is None:
            self.custom_headers = {
                'Accept': 'text/html,application/xhtml+xml',
                'Accept-Language': 'en-GB,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }

        if self.selectors is None:
            self.selectors = {
                'product_container': '{PRODUCT_SELECTOR}',
                'product_link': '{LINK_SELECTOR}',
                'name': '{NAME_SELECTOR}',
                'current_price': '{CURRENT_PRICE_SELECTOR}',
                'original_price': '{ORIGINAL_PRICE_SELECTOR}',
                'stock_status': '{STOCK_SELECTOR}',
            }


# Default configuration instance
DEFAULT_CONFIG = {ClassName}Config()

# Size mapping for common sizes
SIZE_MAPPING = {
    'XS': '{XS_VALUE}',
    'S': '{S_VALUE}',
    'M': '{M_VALUE}',
    'L': '{L_VALUE}',
    'XL': '{XL_VALUE}',
}

# Category mapping
CATEGORY_MAPPING = {
    'sale': '{SALE_CATEGORY}',
    'new': '{NEW_CATEGORY}',
    'mens': '{MENS_CATEGORY}',
    'womens': '{WOMENS_CATEGORY}',
}
EOF
```

### 4. Create Test Suite

```python
# Create comprehensive test suite
cat > tests/test_${SITE_NAME}_scraper.py << 'EOF'
"""
Tests for {SITE_NAME} scraper
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime

from scrapers.{SITE_NAME_LOWER}_scraper import {ClassName}Scraper
from models import Product


class Test{ClassName}Scraper:
    """Test suite for {SITE_NAME} scraper."""

    @pytest.fixture
    def scraper(self, tmp_path):
        """Create scraper instance for testing."""
        db_path = tmp_path / "test.db"
        return {ClassName}Scraper(db_path)

    @pytest.fixture
    def sample_html(self):
        """Sample HTML for testing."""
        return '''
        <html>
            <body>
                <div class="products">
                    <{PRODUCT_TAG} class="{PRODUCT_CLASS}">
                        <a class="{LINK_CLASS}"
                           {SKU_ATTRIBUTE}="{SAMPLE_SKU}"
                           {NAME_ATTRIBUTE}="{SAMPLE_NAME}"
                           {PRICE_ATTRIBUTE}="{SAMPLE_PRICE}"
                           {URL_ATTRIBUTE}="{SAMPLE_URL}">
                            <span class="{ORIGINAL_PRICE_CLASS}">{SAMPLE_ORIGINAL_PRICE}</span>
                        </a>
                    </{PRODUCT_TAG}>
                </div>
            </body>
        </html>
        '''

    def test_get_urls(self, scraper):
        """Test URL generation."""
        urls = scraper.get_urls()

        assert len(urls) > 0
        assert all(scraper.base_url in url for url in urls)
        assert any("page=" in url for url in urls)

    def test_product_selector(self, scraper):
        """Test product selector."""
        selector = scraper.get_product_selector()
        assert selector == "{PRODUCT_SELECTOR}"

    def test_parse_product_page(self, scraper, sample_html):
        """Test product parsing."""
        url = "https://example.com/test"
        products = scraper.parse_product_page(url, sample_html)

        assert len(products) == 1

        product = products[0]
        assert product.sku == "{SAMPLE_SKU}"
        assert product.name == "{SAMPLE_NAME}"
        assert product.current_price == "{SAMPLE_PRICE}"
        assert product.source == "{SITE_NAME_LOWER}"
        assert product.currency == "{DEFAULT_CURRENCY}"

    def test_parse_product_with_sale_price(self, scraper):
        """Test parsing product with sale price."""
        html_with_sale = '''
        <{PRODUCT_TAG} class="{PRODUCT_CLASS}">
            <a class="{LINK_CLASS}"
               {SKU_ATTRIBUTE}="test-sku-sale"
               {NAME_ATTRIBUTE}="Test Product Sale"
               {PRICE_ATTRIBUTE}="25.00"
               {URL_ATTRIBUTE}="/test-product-sale">
                <span class="{ORIGINAL_PRICE_CLASS}">50.00</span>
            </a>
        </{PRODUCT_TAG}>
        '''

        products = scraper.parse_product_page("test", html_with_sale)

        assert len(products) == 1
        product = products[0]
        assert product.current_price == "25.00"
        assert product.original_price == "50.00"

    def test_parse_out_of_stock_product(self, scraper):
        """Test parsing out-of-stock product."""
        html_out_of_stock = '''
        <{PRODUCT_TAG} class="{PRODUCT_CLASS}">
            <a class="{LINK_CLASS}"
               {SKU_ATTRIBUTE}="test-sku-oos"
               {NAME_ATTRIBUTE}="Test Product OOS"
               {PRICE_ATTRIBUTE}="30.00">
                <span class="stock-status">Out of Stock</span>
            </a>
        </{PRODUCT_TAG}>
        '''

        products = scraper.parse_product_page("test", html_out_of_stock)

        assert len(products) == 1
        product = products[0]
        assert product.in_stock == False

    def test_invalid_product_skipped(self, scraper):
        """Test that invalid products are skipped."""
        html_invalid = '''
        <{PRODUCT_TAG} class="{PRODUCT_CLASS}">
            <a class="{LINK_CLASS}">
                <!-- Missing required attributes -->
            </a>
        </{PRODUCT_TAG}>
        '''

        products = scraper.parse_product_page("test", html_invalid)
        assert len(products) == 0

    @patch('requests.Session.get')
    def test_fetch_with_retry(self, mock_get, scraper):
        """Test request retry logic."""
        # Simulate network error then success
        mock_response = Mock()
        mock_response.text = "<html></html>"
        mock_response.status_code = 200
        mock_get.side_effect = [ConnectionError(), mock_response]

        result = scraper._fetch_with_retry("https://example.com")
        assert result.status_code == 200

    def test_price_normalization(self, scraper):
        """Test price string normalization."""
        test_cases = [
            ("£25.00", "25.00"),
            ("25.50", "25.50"),
            ("Price: £30.00", "30.00"),
            ("GBP 40.00", "40.00"),
            ("", None),
            ("Invalid", None),
        ]

        for input_price, expected in test_cases:
            result = scraper._normalize_price(input_price)
            assert result == expected

    def test_url_building(self, scraper):
        """Test URL construction."""
        test_cases = [
            ("/product/test", f"{scraper.base_url}/product/test"),
            ("https://example.com/product", "https://example.com/product"),
            ("", None),
            (None, None),
        ]

        for input_url, expected in test_cases:
            result = scraper._build_product_url(input_url)
            assert result == expected


class Test{ClassName}Integration:
    """Integration tests for {SITE_NAME} scraper."""

    @pytest.fixture
    def scraper(self, tmp_path):
        """Create scraper for integration testing."""
        db_path = tmp_path / "integration.db"
        return {ClassName}Scraper(db_path)

    @pytest.mark.integration
    @patch('time.sleep')  # Speed up tests
    def test_full_scraping_workflow(self, mock_sleep, scraper):
        """Test complete scraping workflow."""
        with patch.object(scraper, 'get_urls') as mock_urls:
            mock_urls.return_value = ["https://example.com/test"]

            with patch.object(scraper, '_fetch_with_retry') as mock_fetch:
                mock_response = Mock()
                mock_response.text = '''
                <{PRODUCT_TAG} class="{PRODUCT_CLASS}">
                    <a {SKU_ATTRIBUTE}="test-integration"
                       {NAME_ATTRIBUTE}="Integration Test"
                       {PRICE_ATTRIBUTE}="15.00">
                    </a>
                </{PRODUCT_TAG}>
                '''
                mock_response.status_code = 200
                mock_fetch.return_value = mock_response

                result = scraper.run()

                assert result.source == "{SITE_NAME_LOWER}"
                assert result.products_found > 0
                assert len(result.errors) == 0


# HTML fixtures for testing
SAMPLE_PRODUCT_HTML = '''
<{PRODUCT_TAG} class="{PRODUCT_CLASS}">
    <a class="{LINK_CLASS}"
       {SKU_ATTRIBUTE}="fixture-sku-001"
       {NAME_ATTRIBUTE}="Fixture Product Name"
       {PRICE_ATTRIBUTE}="42.00"
       {URL_ATTRIBUTE}="/fixture-product">
        <img src="/image.jpg" alt="Product">
        <span class="{ORIGINAL_PRICE_CLASS}">60.00</span>
    </a>
</{PRODUCT_TAG}>
'''

SAMPLE_PAGE_HTML = f'''
<!DOCTYPE html>
<html>
<head><title>Test Page</title></head>
<body>
    <div class="product-grid">
        {SAMPLE_PRODUCT_HTML}
        {SAMPLE_PRODUCT_HTML.replace("fixture-sku-001", "fixture-sku-002")}
    </div>
</body>
</html>
'''
EOF
```

### 5. Register Scraper in CLI

```python
# Add scraper to CLI registry
cat >> src/product_prices/cli.py << 'EOF'

# Add {SITE_NAME} scraper import and main function
from .scrapers.{SITE_NAME_LOWER} import {ClassName}Scraper

def scrape_{SITE_NAME_LOWER}(**kwargs):
    """Run {SITE_NAME} scraper."""
    scraper = {ClassName}Scraper(db_path=None, **kwargs)
    return scraper.fetch_current()

EOF

# Update main CLI function to include new scraper
echo "Add '{SITE_NAME_LOWER}': scrape_{SITE_NAME_LOWER}, to the scraper dispatch in main()"
```

### 6. Create Integration Documentation

```markdown
# Create scraper documentation
cat > docs/scrapers/${SITE_NAME_LOWER}.md << 'EOF'
# {SITE_NAME} Scraper Documentation

## Overview

{SITE_DESCRIPTION}

## Configuration

### Basic Setup

```python
from scrapers.{SITE_NAME_LOWER}_scraper import {ClassName}Scraper

scraper = {ClassName}Scraper(
    db_path=Path("products.db"),
    sizes=["XS", "S", "M"],
    categories=["sale", "new"],
    max_pages=10
)
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `sizes` | List[str] | {DEFAULT_SIZES} | Size filters to apply |
| `categories` | List[str] | {DEFAULT_CATEGORIES} | Product categories |
| `max_pages` | int | 15 | Maximum pages to scrape |

### CLI Usage

```bash
# Run {SITE_NAME} scraper only
uv run python -m product_prices.cli {SITE_NAME_LOWER}

# Run with summary output
uv run python -m product_prices.cli {SITE_NAME_LOWER} --summary

# Run all scrapers
uv run python -m product_prices.cli all
```

## Site-Specific Details

### URL Structure
- Base URL: `{BASE_URL}`
- Category pages: `{CATEGORY_PATTERN}`
- Pagination: `{PAGINATION_PATTERN}`

### HTML Structure
- Product containers: `{PRODUCT_SELECTOR}`
- Product data: {DATA_ATTRIBUTE_STRATEGY}
- Price display: {PRICE_STRUCTURE}

### Parsing Strategy
{PARSING_STRATEGY_DESCRIPTION}

### Rate Limiting
- Delay between requests: {MIN_DELAY}-{MAX_DELAY} seconds
- Recommended concurrent requests: 1
- User agent: `{USER_AGENT}`

## Testing

### Run Tests
```bash
# Unit tests
uv run pytest tests/test_{SITE_NAME_LOWER}.py

# All tests
uv run pytest

# Test scraper integration
uv run python tests/manual/test_core_functions.py
```

### Test Data
Test fixtures are available in `tests/fixtures/{SITE_NAME_LOWER}/`:
- `sample_page.html` - Complete product page
- `single_product.html` - Individual product HTML
- `empty_page.html` - Page with no products

## Troubleshooting

### Common Issues

1. **No products found**
   - Check if site structure changed
   - Verify product selector: `{PRODUCT_SELECTOR}`
   - Check network connectivity

2. **Price parsing errors**
   - Review price selectors in config
   - Check currency format changes
   - Verify sale price detection

3. **Rate limiting**
   - Increase delay range in config
   - Check for blocking indicators
   - Verify user agent acceptance

### Debugging

```python
# Enable debug logging
import logging
logging.getLogger('scrapers.{SITE_NAME_LOWER}').setLevel(logging.DEBUG)

# Test individual components
scraper = {ClassName}Scraper(db_path)
urls = scraper.get_urls()
html = scraper._fetch_with_retry(urls[0]).text
products = scraper.parse_product_page(urls[0], html)
```

## Maintenance

### Site Change Detection
Monitor these indicators for site changes:
- Product count drops significantly
- Parse errors increase
- New CSS classes appear
- URL structure changes

### Update Process
1. Run tests to identify failures
2. Update selectors in `config/sites/{SITE_NAME_LOWER}.py`
3. Add new test cases for changed elements
4. Update documentation if needed

## Examples

### Complete Scraper Implementation
```python
{COMPLETE_EXAMPLE_CODE}
```

### Custom Configuration
```python
{CUSTOM_CONFIG_EXAMPLE}
```
EOF
```

### 7. Run Tests and Validation

```bash
# Create and run validation suite
cat > scripts/validate_scraper.py << 'EOF'
#!/usr/bin/env python3
"""
Validation script for new scrapers
"""
import sys
from pathlib import Path
from typing import List

def validate_scraper(site_name: str) -> List[str]:
    """Validate scraper implementation."""
    errors = []

    # Check required files exist
    required_files = [
        f"scrapers/{site_name}_scraper.py",
        f"config/sites/{site_name}.py",
        f"tests/test_{site_name}_scraper.py",
        f"docs/scrapers/{site_name}.md"
    ]

    for file_path in required_files:
        if not Path(file_path).exists():
            errors.append(f"Missing required file: {file_path}")

    # Import and validate scraper class
    try:
        module = __import__(f"scrapers.{site_name}_scraper", fromlist=[f"{site_name.title()}Scraper"])
        scraper_class = getattr(module, f"{site_name.title()}Scraper")

        # Check required methods
        required_methods = ["get_urls", "parse_product_page", "get_product_selector"]
        for method in required_methods:
            if not hasattr(scraper_class, method):
                errors.append(f"Missing required method: {method}")

    except ImportError as e:
        errors.append(f"Failed to import scraper: {e}")

    return errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_scraper.py <site_name>")
        sys.exit(1)

    site_name = sys.argv[1]
    errors = validate_scraper(site_name)

    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print(f"✅ Scraper {site_name} validation passed!")
EOF

# Run quality checks
./scripts/quality_check.sh

# Test the new scraper
uv run python -m product_prices.cli {SITE_NAME_LOWER} --summary
```

### 8. Complete Implementation Examples

#### Carhartt WIP (Data-Driven) Implementation

```python
# Complete Carhartt WIP scraper example
cat > examples/carhartt_wip_complete.py << 'EOF'
"""
Complete Carhartt WIP scraper implementation
Demonstrates data-driven parsing approach
"""
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List

from base_scraper import BaseScraper
from models import Product


class CarharttWIPScraper(BaseScraper):
    """Complete Carhartt WIP scraper with data-driven parsing."""

    def __init__(self, db_path: Path, sizes: List[str] = None) -> None:
        super().__init__(
            source_name="carhartt_wip",
            base_url="https://www.carhartt-wip.com",
            db_path=db_path
        )
        self.sizes = sizes or ["XS", "S", "M"]

        # Configure session
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; PriceMonitor/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def get_urls(self) -> list[str]:
        """Generate paginated URLs for men's summer sale."""
        base = "https://www.carhartt-wip.com/en/men-summer-sale"
        size_params = "&".join(f"filter_size={size}" for size in self.sizes)

        urls = []
        for page in range(1, 15):  # Carhartt typically has 14 pages
            url = f"{base}?{size_params}&page={page}"
            urls.append(url)
        return urls

    def get_product_selector(self) -> str:
        """Product container selector for Carhartt WIP."""
        return "article.product-grid-item"

    def parse_product_page(self, url: str, content: str) -> list[dict[str, Any]]:
        """Parse Carhartt WIP products using data attributes."""
        soup = BeautifulSoup(content, "html.parser")
        products = []

        for item in soup.select(self.get_product_selector()):
            try:
                product = self._parse_carhartt_product(item)
                if product:
                    products.append(product)
            except Exception as e:
                print(f"Failed to parse product: {e}")
                continue

        return products

    def _parse_carhartt_product(self, item) -> Product | None:
        """Parse individual Carhartt WIP product."""
        # Primary data extraction from link element
        link_el = item.select_one("a.product-grid-item-container")
        if not link_el:
            return None

        # Extract core data from attributes
        sku = link_el.get("data-productId", "").strip("'")
        name = link_el.get("data-name", "").strip("'")
        current_price = link_el.get("data-price", "").strip("'")
        product_url = link_el.get("data-link", "").strip("'")

        if not sku or not name:
            return None

        # Extract original/sale price
        original_price = None
        strikeout_el = item.select_one("span.strikeout.country_gbp")
        if strikeout_el:
            original_price = strikeout_el.get_text(strip=True)

        # Build complete URL
        full_url = f"{self.base_url}{product_url}" if product_url else None

        # Extract additional metadata
        metadata = {
            "category": link_el.get("data-categoryId", "").strip("'"),
            "variant": link_el.get("data-variant", "").strip("'"),
            "brand": "Carhartt WIP",
            "country": "GB"
        }

        return Product(
            sku=sku,
            source=self.source_name,
            name=name,
            url=full_url,
            current_price=current_price,
            original_price=original_price,
            currency="GBP",
            in_stock=True,  # Listed products assumed in stock
            last_seen=datetime.now(),
            metadata=metadata
        )
EOF
```

#### Tony McDonald (Defensive) Implementation

```python
# Complete Tony McDonald scraper example
cat > examples/tony_mcdonald_complete.py << 'EOF'
"""
Complete Tony McDonald scraper implementation
Demonstrates defensive parsing with fallbacks
"""
import re
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Optional

from base_scraper import BaseScraper
from models import Product


class TonyMcDonaldScraper(BaseScraper):
    """Complete Tony McDonald scraper with defensive parsing."""

    def __init__(self, db_path: Path) -> None:
        super().__init__(
            source_name="tony_mcdonald",
            base_url="https://www.tonymcdonnell.com",
            db_path=db_path
        )

        # Defensive parsing patterns
        self.price_patterns = [
            r"£\s*(\d+[.,]?\d*)",  # £25.00 or £25
            r"(\d+[.,]?\d*)\s*£",  # 25.00£
            r"GBP\s*(\d+[.,]?\d*)", # GBP 25.00
        ]

    def get_urls(self) -> list[str]:
        """URLs for Tony McDonald sale with size filters."""
        return [
            "https://www.tonymcdonnell.com/tm_uk/sale.html"
            "?brand=4591&size_scale_01=4239,4131,4134,3950,4087,3945,3976,3970"
        ]

    def get_product_selector(self) -> str:
        """Product container selector."""
        return "li.product-item"

    def parse_product_page(self, url: str, content: str) -> list[dict[str, Any]]:
        """Parse Tony McDonald products with defensive strategies."""
        soup = BeautifulSoup(content, "html.parser")
        products = []

        for item in soup.select(self.get_product_selector()):
            try:
                product = self._parse_tony_product_defensive(item)
                if product:
                    products.append(product)
            except Exception as e:
                print(f"Failed to parse product: {e}")
                continue

        return products

    def _parse_tony_product_defensive(self, item) -> Product | None:
        """Parse Tony McDonald product with multiple fallback strategies."""
        # Multi-strategy SKU extraction
        sku = self._extract_tony_sku(item)
        if not sku:
            return None

        # Multi-strategy name extraction
        name = self._extract_tony_name(item)
        if not name:
            return None

        # Price extraction with fallbacks
        current_price = self._extract_tony_current_price(item)
        original_price = self._extract_tony_original_price(item)

        # URL extraction
        product_url = self._extract_tony_url(item)

        # Stock status
        in_stock = self._check_tony_stock(item)

        return Product(
            sku=sku,
            source=self.source_name,
            name=name,
            url=product_url,
            current_price=current_price,
            original_price=original_price,
            currency="GBP",
            in_stock=in_stock,
            last_seen=datetime.now(),
            metadata={"parsed_method": "defensive"}
        )

    def _extract_tony_sku(self, item) -> Optional[str]:
        """Extract SKU using multiple fallback strategies."""
        # Strategy 1: Look for price wrapper with data-sku
        price_wrapper = item.select_one("span.price-wrapper")
        if price_wrapper and price_wrapper.has_attr("data-sku"):
            return str(price_wrapper["data-sku"])

        # Strategy 2: Look for price wrapper with ID
        if price_wrapper and price_wrapper.has_attr("id"):
            return str(price_wrapper["id"])

        # Strategy 3: Extract from any element with data-sku
        sku_element = item.select_one("[data-sku]")
        if sku_element:
            return str(sku_element["data-sku"])

        # Strategy 4: Extract from URL
        link = item.select_one("a[href]")
        if link:
            href = link.get("href", "")
            # Look for product ID in URL
            match = re.search(r"product_id=(\d+)", href)
            if match:
                return match.group(1)

        return None

    def _extract_tony_name(self, item) -> Optional[str]:
        """Extract product name with fallbacks."""
        # Try multiple name selectors
        name_selectors = [
            "a.product-item-link",
            ".product-item-name",
            "h3",
            "h2",
            "a[href*='product']"
        ]

        for selector in name_selectors:
            element = item.select_one(selector)
            if element:
                name = element.get_text(strip=True)
                if name and len(name) > 3:  # Basic validation
                    return name

        return None

    def _extract_tony_current_price(self, item) -> Optional[str]:
        """Extract current price with regex fallbacks."""
        # Strategy 1: Look for sale/current price elements
        price_selectors = [
            ".price-current .price",
            ".price-sale .price",
            ".special-price .price",
            ".price-wrapper .price"
        ]

        for selector in price_selectors:
            element = item.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                price = self._normalize_price(price_text)
                if price:
                    return price

        # Strategy 2: Regex fallback on entire item
        item_text = item.get_text(" ")
        for pattern in self.price_patterns:
            matches = re.findall(pattern, item_text)
            if matches:
                # Take the last price found (often current price)
                return self._normalize_price(matches[-1])

        return None

    def _extract_tony_original_price(self, item) -> Optional[str]:
        """Extract original/was price."""
        # Look for strikethrough or "was" price elements
        original_selectors = [
            ".price-old .price",
            ".price-was .price",
            ".old-price",
            ".price-wrapper .price-old"
        ]

        for selector in original_selectors:
            element = item.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                price = self._normalize_price(price_text)
                if price:
                    return price

        return None

    def _extract_url(self, item) -> str | None:
        """Extract product URL."""
        link = item.select_one("a[href]")
        if link:
            href = link.get("href", "")
            if href.startswith('http'):
                return href
            elif href.startswith('/'):
                return f"{self.base_url}{href}"
            else:
                return f"{self.base_url}/{href}"

        return None

    def _check_tony_stock(self, item) -> bool:
        """Check stock status with multiple indicators."""
        # Check for out-of-stock text
        item_text = item.get_text(" ").lower()
        out_of_stock_indicators = [
            "out of stock", "sold out", "unavailable",
            "not available", "pre-order"
        ]

        for indicator in out_of_stock_indicators:
            if indicator in item_text:
                return False

        # Check for out-of-stock CSS classes
        if item.select_one('.out-of-stock, .sold-out, .unavailable'):
            return False

        return True  # Default to in stock

    def _normalize_price(self, price_text: str) -> Optional[str]:
        """Normalize price string to standard format."""
        if not price_text:
            return None

        # Clean up common price prefixes/suffixes
        price_text = re.sub(r'^(Price:|Was:|Now:|£|GBP)\s*', '', price_text, flags=re.IGNORECASE)
        price_text = re.sub(r'\s*(each|per|item)$', '', price_text, flags=re.IGNORECASE)

        # Extract numeric value
        match = re.search(r'(\d+[.,]?\d*)', price_text)
        if match:
            return match.group(1)

        return None
EOF
```

### 9. Final Integration and Testing

```bash
# Run complete integration test
uv run pytest tests/test_${SITE_NAME}_scraper.py -v

# Test CLI integration
uv run python -m product_prices --scraper ${SITE_NAME} --dry-run

# Validate configuration
python -c "
from config.sites.${SITE_NAME} import DEFAULT_CONFIG
print(f'Configuration valid: {DEFAULT_CONFIG.enabled}')
print(f'Base URL: {DEFAULT_CONFIG.base_url}')
print(f'Selectors: {DEFAULT_CONFIG.selectors}')
"

# Run full scraper test (be careful with real sites)
# uv run python -m product_prices --scraper ${SITE_NAME} --max-pages 1
```

### Summary

This command provides a comprehensive framework for adding new site scrapers:

1. **Site Analysis**: Systematic approach to understanding target sites
2. **Template Selection**: Choose between data-driven and defensive parsing
3. **Configuration Management**: Site-specific settings and customization
4. **Testing Framework**: Unit tests, integration tests, and validation
5. **Documentation**: Complete documentation for maintenance
6. **Integration**: CLI registration and configuration
7. **Examples**: Complete implementations for both parsing approaches

The templates include defensive strategies for sites that may change structure, comprehensive error handling, and extensive testing to ensure reliability in production.
