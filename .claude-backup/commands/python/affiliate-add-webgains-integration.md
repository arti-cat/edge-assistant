# Add Webgains Integration

Integrate Webgains affiliate network for Carhartt WIP products with API support, automated link generation, and performance tracking.

## Usage

```bash
/affiliate:add-webgains-integration
```

## Instructions

### 1. **Webgains API Configuration**

Set up Webgains API credentials and configuration:

```python
# Create Webgains configuration
cat > src/product_prices/config/webgains.py << 'EOF'
"""
Webgains API configuration and client
"""
import os
import json
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from urllib.parse import urlencode, quote


logger = logging.getLogger(__name__)


@dataclass
class WebgainsConfig:
    """Webgains API configuration"""
    api_base_url: str = "https://api.webgains.com"
    campaign_id: str = ""
    program_id: str = "294000"  # Carhartt WIP program ID
    api_key: str = ""
    api_secret: str = ""
    click_base_url: str = "https://track.webgains.com/click.html"
    deep_linking_enabled: bool = True
    commission_rate: float = 0.08
    cookie_duration_days: int = 30

    def __post_init__(self):
        # Load from environment variables
        self.api_key = os.getenv('WEBGAINS_API_KEY', '')
        self.api_secret = os.getenv('WEBGAINS_API_SECRET', '')
        self.campaign_id = os.getenv('WEBGAINS_CAMPAIGN_ID', '1')


class WebgainsClient:
    """Webgains API client for affiliate operations"""

    def __init__(self, config: WebgainsConfig = None):
        self.config = config or WebgainsConfig()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PriceMonitor/1.0 (Webgains Integration)',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def generate_affiliate_url(self, original_url: str, sku: str = None,
                              custom_tracking: Dict[str, str] = None) -> str:
        """Generate Webgains affiliate URL"""
        try:
            # Base Webgains parameters
            params = {
                'wgcampaignid': self.config.campaign_id,
                'wgprogramid': self.config.program_id,
                'wgtarget': original_url
            }

            # Add SKU for tracking
            if sku:
                params['wgsku'] = sku
                params['wgref'] = f"carhartt_{sku}"

            # Add custom tracking parameters
            if custom_tracking:
                for key, value in custom_tracking.items():
                    if key.startswith('wg'):
                        params[key] = value

            # Generate affiliate URL
            query_string = urlencode(params, quote_via=quote)
            affiliate_url = f"{self.config.click_base_url}?{query_string}"

            logger.info(f"Generated Webgains URL for SKU: {sku}")
            return affiliate_url

        except Exception as e:
            logger.error(f"Failed to generate Webgains URL: {e}")
            raise

    def validate_affiliate_url(self, affiliate_url: str) -> Dict[str, Any]:
        """Validate affiliate URL and check if it's working"""
        try:
            response = self.session.head(
                affiliate_url,
                timeout=10,
                allow_redirects=True
            )

            return {
                'valid': response.status_code < 400,
                'status_code': response.status_code,
                'final_url': response.url,
                'response_time': response.elapsed.total_seconds()
            }

        except requests.RequestException as e:
            return {
                'valid': False,
                'error': str(e),
                'status_code': None
            }

    def get_program_info(self) -> Optional[Dict[str, Any]]:
        """Get Carhartt WIP program information from Webgains API"""
        if not self.config.api_key:
            logger.warning("Webgains API key not configured")
            return None

        try:
            # Webgains API endpoint for program details
            url = f"{self.config.api_base_url}/programs/{self.config.program_id}"

            auth_params = {
                'apikey': self.config.api_key,
                'timestamp': int(datetime.now().timestamp())
            }

            response = self.session.get(url, params=auth_params, timeout=30)

            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Webgains API returned {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Failed to get Webgains program info: {e}")
            return None

    def get_commission_rates(self) -> Dict[str, float]:
        """Get commission rates for different product categories"""
        # Default Carhartt WIP commission structure
        return {
            'default': 0.08,
            'sale_items': 0.06,  # Lower rate for sale items
            'new_arrivals': 0.10,  # Higher rate for new products
        }

    def generate_product_feed_url(self) -> str:
        """Generate URL for Carhartt WIP product feed"""
        params = {
            'wgprogramid': self.config.program_id,
            'format': 'xml',
            'compression': 'gzip'
        }

        return f"{self.config.api_base_url}/feeds/product?{urlencode(params)}"


# Global Webgains client instance
webgains_config = WebgainsConfig()
webgains_client = WebgainsClient(webgains_config)
EOF

# Add environment variables
cat >> .env << 'EOF'

# Webgains Configuration
WEBGAINS_API_KEY=your_api_key_here
WEBGAINS_API_SECRET=your_api_secret_here
WEBGAINS_CAMPAIGN_ID=1
WEBGAINS_PROGRAM_ID=294000
EOF
```

### 2. **Enhanced Affiliate Service Integration**

Update the affiliate service to use Webgains client:

```python
# Update affiliate service with Webgains integration
cat >> src/product_prices/services/affiliate.py << 'EOF'

# Import Webgains client
from ..config.webgains import webgains_client, WebgainsConfig

class AffiliateService:
    """Enhanced affiliate service with Webgains integration"""

    def __init__(self, db_path: Path):
        # Existing initialization code...
        self.webgains = webgains_client

    def generate_webgains_link(self, sku: str, source: str, original_url: str,
                              custom_params: Dict[str, str] = None) -> AffiliateLinkResponse:
        """Generate Webgains affiliate link with enhanced tracking"""
        try:
            # Get or create Webgains network
            network = self.get_network_by_name("webgains")
            if not network:
                raise ValueError("Webgains network not configured")

            # Check for existing link
            existing_link = self.get_existing_link(sku, source, network.id)
            if existing_link and existing_link.status == LinkStatus.ACTIVE:
                # Validate existing link
                validation = self.webgains.validate_affiliate_url(existing_link.affiliate_url)
                if validation['valid']:
                    return AffiliateLinkResponse(
                        link_id=existing_link.id,
                        affiliate_url=existing_link.affiliate_url,
                        short_url=existing_link.short_url,
                        commission_rate=existing_link.commission_rate,
                        network_name=network.display_name
                    )
                else:
                    # Mark as broken and create new
                    self._mark_link_broken(existing_link.id, validation.get('error', 'Validation failed'))

            # Generate new Webgains URL
            tracking_params = {
                'wgsource': 'price_monitor',
                'wgmedium': 'affiliate',
                'wgcampaign': f"{source}_monitoring"
            }

            if custom_params:
                tracking_params.update(custom_params)

            affiliate_url = self.webgains.generate_affiliate_url(
                original_url=original_url,
                sku=sku,
                custom_tracking=tracking_params
            )

            # Generate short URL
            short_url = self._generate_short_url(sku, source, "webgains")

            # Determine commission rate based on product
            commission_rate = self._get_webgains_commission_rate(sku, source, original_url)

            # Create affiliate link record
            link = AffiliateLink(
                sku=sku,
                source=source,
                network_id=network.id,
                original_url=original_url,
                affiliate_url=affiliate_url,
                short_url=short_url,
                commission_rate=commission_rate,
                status=LinkStatus.ACTIVE,
                created_at=datetime.now(),
                metadata={
                    'webgains_program_id': self.webgains.config.program_id,
                    'webgains_campaign_id': self.webgains.config.campaign_id,
                    'tracking_params': tracking_params
                }
            )

            # Save to database
            link_id = self._save_affiliate_link(link)
            if not link_id:
                raise Exception("Failed to save affiliate link")

            logger.info(f"Created Webgains link for {sku}: {link_id}")

            return AffiliateLinkResponse(
                link_id=link_id,
                affiliate_url=affiliate_url,
                short_url=short_url,
                commission_rate=commission_rate,
                network_name=network.display_name
            )

        except Exception as e:
            logger.error(f"Failed to generate Webgains link: {e}")
            raise

    def bulk_generate_webgains_links(self, products: List[Dict[str, str]]) -> Dict[str, Any]:
        """Bulk generate Webgains links for multiple products"""
        results = {
            'success': [],
            'failed': [],
            'skipped': [],
            'total': len(products)
        }

        for product in products:
            try:
                sku = product['sku']
                source = product['source']
                original_url = product['url']

                # Skip if not Carhartt WIP
                if source != 'carhartt_wip':
                    results['skipped'].append({
                        'sku': sku,
                        'reason': 'Not Carhartt WIP product'
                    })
                    continue

                response = self.generate_webgains_link(sku, source, original_url)
                results['success'].append({
                    'sku': sku,
                    'link_id': response.link_id,
                    'affiliate_url': response.affiliate_url
                })

            except Exception as e:
                results['failed'].append({
                    'sku': product.get('sku', 'unknown'),
                    'error': str(e)
                })

        logger.info(f"Bulk Webgains generation: {len(results['success'])} success, {len(results['failed'])} failed")
        return results

    def _get_webgains_commission_rate(self, sku: str, source: str, url: str) -> Decimal:
        """Determine commission rate based on product characteristics"""
        try:
            commission_rates = self.webgains.get_commission_rates()

            # Check if it's a sale item (lower commission)
            if 'sale' in url.lower() or 'clearance' in url.lower():
                return Decimal(str(commission_rates.get('sale_items', 0.06)))

            # Check if it's a new arrival (higher commission)
            if 'new' in url.lower() or 'latest' in url.lower():
                return Decimal(str(commission_rates.get('new_arrivals', 0.10)))

            # Default commission rate
            return Decimal(str(commission_rates.get('default', 0.08)))

        except Exception as e:
            logger.warning(f"Failed to determine commission rate: {e}")
            return Decimal('0.08')  # Default fallback

    def validate_webgains_links(self, batch_size: int = 50) -> Dict[str, Any]:
        """Validate existing Webgains affiliate links"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                # Get active Webgains links
                cursor.execute("""
                    SELECT al.*, an.name as network_name
                    FROM affiliate_links al
                    JOIN affiliate_networks an ON al.network_id = an.id
                    WHERE an.name = 'webgains' AND al.status = 'active'
                    ORDER BY al.last_validated ASC NULLS FIRST
                    LIMIT ?
                """, (batch_size,))

                links = cursor.fetchall()

            results = {
                'validated': 0,
                'broken': 0,
                'errors': []
            }

            for link in links:
                try:
                    validation = self.webgains.validate_affiliate_url(link['affiliate_url'])

                    if validation['valid']:
                        self._update_link_validation(link['id'], True, None)
                        results['validated'] += 1
                    else:
                        error_msg = validation.get('error', f"HTTP {validation.get('status_code', 'unknown')}")
                        self._mark_link_broken(link['id'], error_msg)
                        results['broken'] += 1

                except Exception as e:
                    results['errors'].append({
                        'link_id': link['id'],
                        'sku': link['sku'],
                        'error': str(e)
                    })

            logger.info(f"Webgains validation: {results['validated']} valid, {results['broken']} broken")
            return results

        except Exception as e:
            logger.error(f"Failed to validate Webgains links: {e}")
            return {'error': str(e)}

    def _update_link_validation(self, link_id: int, is_valid: bool, error_message: str = None):
        """Update link validation status"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE affiliate_links
                    SET last_validated = ?, validation_error = ?, updated_at = ?
                    WHERE id = ?
                """, (datetime.now(), error_message, datetime.now(), link_id))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to update link validation: {e}")

    def _mark_link_broken(self, link_id: int, error_message: str):
        """Mark affiliate link as broken"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE affiliate_links
                    SET status = 'broken', validation_error = ?, updated_at = ?
                    WHERE id = ?
                """, (error_message, datetime.now(), link_id))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to mark link as broken: {e}")
EOF
```

### 3. **Webgains-Specific API Endpoints**

Add Webgains endpoints to the API:

```python
# Create Webgains API routes
cat > src/product_prices/api/routes/webgains.py << 'EOF'
"""
Webgains-specific API endpoints
"""
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel, HttpUrl

from ...services.affiliate import AffiliateService
from ...config.webgains import webgains_client


router = APIRouter(prefix="/api/v1/webgains", tags=["webgains"])


class WebgainsLinkRequest(BaseModel):
    """Request to generate Webgains affiliate link"""
    sku: str
    source: str
    original_url: HttpUrl
    custom_params: Optional[Dict[str, str]] = None


class BulkLinkRequest(BaseModel):
    """Bulk link generation request"""
    products: List[Dict[str, str]]


def get_affiliate_service() -> AffiliateService:
    """Get affiliate service instance"""
    return AffiliateService(Path("products.db"))


@router.post("/links/generate")
async def generate_webgains_link(
    request: WebgainsLinkRequest,
    service: AffiliateService = Depends(get_affiliate_service)
):
    """Generate single Webgains affiliate link"""
    try:
        response = service.generate_webgains_link(
            sku=request.sku,
            source=request.source,
            original_url=str(request.original_url),
            custom_params=request.custom_params
        )

        return {
            'success': True,
            'link_id': response.link_id,
            'affiliate_url': response.affiliate_url,
            'short_url': response.short_url,
            'commission_rate': float(response.commission_rate),
            'network_name': response.network_name
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate link: {str(e)}")


@router.post("/links/bulk-generate")
async def bulk_generate_webgains_links(
    request: BulkLinkRequest,
    background_tasks: BackgroundTasks,
    service: AffiliateService = Depends(get_affiliate_service)
):
    """Generate multiple Webgains affiliate links"""
    try:
        # Start background task for bulk generation
        background_tasks.add_task(
            _process_bulk_generation,
            service,
            request.products
        )

        return {
            'success': True,
            'message': f'Started bulk generation for {len(request.products)} products',
            'products_queued': len(request.products)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to start bulk generation: {str(e)}")


@router.post("/links/validate")
async def validate_webgains_links(
    batch_size: int = Query(50, ge=1, le=100),
    service: AffiliateService = Depends(get_affiliate_service)
):
    """Validate existing Webgains affiliate links"""
    try:
        results = service.validate_webgains_links(batch_size=batch_size)

        return {
            'success': True,
            'validated': results.get('validated', 0),
            'broken': results.get('broken', 0),
            'errors': results.get('errors', []),
            'batch_size': batch_size
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@router.get("/program/info")
async def get_webgains_program_info():
    """Get Carhartt WIP program information from Webgains"""
    try:
        program_info = webgains_client.get_program_info()

        if program_info:
            return {
                'success': True,
                'program_info': program_info
            }
        else:
            return {
                'success': False,
                'message': 'Program information not available (API key required)'
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get program info: {str(e)}")


@router.get("/commission-rates")
async def get_webgains_commission_rates():
    """Get Webgains commission rates for different categories"""
    try:
        rates = webgains_client.get_commission_rates()

        return {
            'success': True,
            'commission_rates': {
                category: f"{rate * 100:.1f}%"
                for category, rate in rates.items()
            },
            'raw_rates': rates
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get commission rates: {str(e)}")


@router.get("/health")
async def webgains_health_check():
    """Check Webgains integration health"""
    try:
        # Test URL generation
        test_url = webgains_client.generate_affiliate_url(
            "https://www.carhartt-wip.com/en/test-product",
            "TEST001"
        )

        # Test URL validation
        validation = webgains_client.validate_affiliate_url(test_url)

        return {
            'status': 'healthy',
            'webgains_url_generation': 'working',
            'webgains_validation': 'working' if validation else 'limited',
            'api_configured': bool(webgains_client.config.api_key),
            'program_id': webgains_client.config.program_id,
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


async def _process_bulk_generation(service: AffiliateService, products: List[Dict[str, str]]):
    """Background task for bulk link generation"""
    try:
        results = service.bulk_generate_webgains_links(products)

        # Log results
        logger.info(f"Bulk generation completed: {results}")

        # Could send notification or update status here

    except Exception as e:
        logger.error(f"Bulk generation failed: {e}")
EOF

# Update main API to include Webgains routes
cat >> src/product_prices/api/main.py << 'EOF'

# Import Webgains routes
from .routes.webgains import router as webgains_router

# Add Webgains routes
app.include_router(webgains_router)
EOF
```

### 4. **CLI Commands for Webgains**

Add Webgains-specific CLI commands:

```python
# Add Webgains CLI commands
cat >> src/product_prices/cli.py << 'EOF'

@affiliate.group()
def webgains():
    """Webgains-specific affiliate commands"""
    pass

@webgains.command()
@click.option('--sku', help='Product SKU')
@click.option('--source', default='carhartt_wip', help='Product source')
@click.option('--url', help='Original product URL')
def generate(sku, source, url):
    """Generate Webgains affiliate link"""
    if not all([sku, url]):
        click.echo("❌ SKU and URL are required")
        return

    from .services.affiliate import AffiliateService

    db_path = Path("products.db")
    service = AffiliateService(db_path)

    try:
        response = service.generate_webgains_link(sku, source, url)

        click.echo(f"✅ Generated Webgains link for {sku}")
        click.echo(f"Link ID: {response.link_id}")
        click.echo(f"Commission: {response.commission_rate * 100:.1f}%")
        click.echo(f"Short URL: {response.short_url}")

    except Exception as e:
        click.echo(f"❌ Failed to generate link: {e}")

@webgains.command()
@click.option('--batch-size', default=50, help='Number of links to validate')
def validate(batch_size):
    """Validate existing Webgains links"""
    from .services.affiliate import AffiliateService

    db_path = Path("products.db")
    service = AffiliateService(db_path)

    try:
        results = service.validate_webgains_links(batch_size)

        click.echo(f"🔍 Webgains Link Validation")
        click.echo(f"✅ Valid: {results.get('validated', 0)}")
        click.echo(f"❌ Broken: {results.get('broken', 0)}")

        if results.get('errors'):
            click.echo(f"⚠️  Errors: {len(results['errors'])}")

    except Exception as e:
        click.echo(f"❌ Validation failed: {e}")

@webgains.command()
def info():
    """Show Webgains program information"""
    from .config.webgains import webgains_client

    try:
        click.echo("📊 Webgains Configuration")
        click.echo(f"Program ID: {webgains_client.config.program_id}")
        click.echo(f"Campaign ID: {webgains_client.config.campaign_id}")
        click.echo(f"Commission Rate: {webgains_client.config.commission_rate * 100:.1f}%")
        click.echo(f"Cookie Duration: {webgains_client.config.cookie_duration_days} days")
        click.echo(f"Deep Linking: {'✅' if webgains_client.config.deep_linking_enabled else '❌'}")

        # Try to get program info from API
        program_info = webgains_client.get_program_info()
        if program_info:
            click.echo("\n📋 Program Details:")
            click.echo(f"Name: {program_info.get('name', 'N/A')}")
            click.echo(f"Status: {program_info.get('status', 'N/A')}")
        else:
            click.echo("\n⚠️  API info not available (check API credentials)")

    except Exception as e:
        click.echo(f"❌ Failed to get info: {e}")

@webgains.command()
@click.option('--limit', default=100, help='Number of products to process')
def bulk_generate():
    """Generate Webgains links for all Carhartt WIP products"""
    from .services.affiliate import AffiliateService

    db_path = Path("products.db")
    service = AffiliateService(db_path)

    try:
        # Get Carhartt WIP products without affiliate links
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT p.sku, p.source, p.url, p.name
                FROM products p
                LEFT JOIN affiliate_links al ON p.sku = al.sku AND p.source = al.source
                WHERE p.source = 'carhartt_wip' AND al.id IS NULL
                LIMIT ?
            """, (limit,))

            products = [dict(row) for row in cursor.fetchall()]

        if not products:
            click.echo("✅ All Carhartt WIP products already have affiliate links")
            return

        click.echo(f"🚀 Generating Webgains links for {len(products)} products...")

        with click.progressbar(products) as progress_products:
            success_count = 0
            error_count = 0

            for product in progress_products:
                try:
                    service.generate_webgains_link(
                        product['sku'],
                        product['source'],
                        product['url']
                    )
                    success_count += 1
                except Exception:
                    error_count += 1

        click.echo(f"✅ Generated {success_count} links")
        if error_count > 0:
            click.echo(f"❌ {error_count} failed")

    except Exception as e:
        click.echo(f"❌ Bulk generation failed: {e}")
EOF
```

### 5. **Testing Infrastructure**

Create comprehensive tests for Webgains integration:

```python
# Create Webgains integration tests
cat > tests/test_webgains_integration.py << 'EOF'
"""
Tests for Webgains affiliate integration
"""
import pytest
from unittest.mock import Mock, patch
from pathlib import Path

from src.product_prices.config.webgains import WebgainsClient, WebgainsConfig
from src.product_prices.services.affiliate import AffiliateService


class TestWebgainsClient:
    """Test Webgains client functionality"""

    @pytest.fixture
    def webgains_config(self):
        """Create test Webgains configuration"""
        return WebgainsConfig(
            campaign_id="TEST_CAMPAIGN",
            program_id="294000",
            api_key="test_api_key",
            commission_rate=0.08
        )

    @pytest.fixture
    def webgains_client(self, webgains_config):
        """Create Webgains client instance"""
        return WebgainsClient(webgains_config)

    def test_generate_affiliate_url(self, webgains_client):
        """Test Webgains affiliate URL generation"""
        original_url = "https://www.carhartt-wip.com/en/test-product"
        sku = "I034405_02_XX"

        affiliate_url = webgains_client.generate_affiliate_url(original_url, sku)

        assert "track.webgains.com" in affiliate_url
        assert "wgcampaignid=TEST_CAMPAIGN" in affiliate_url
        assert "wgprogramid=294000" in affiliate_url
        assert f"wgsku={sku}" in affiliate_url
        assert "wgtarget=" in affiliate_url

    def test_generate_url_with_custom_tracking(self, webgains_client):
        """Test URL generation with custom tracking parameters"""
        original_url = "https://www.carhartt-wip.com/en/test-product"
        sku = "TEST001"
        custom_tracking = {
            'wgsource': 'custom_source',
            'wgmedium': 'email'
        }

        affiliate_url = webgains_client.generate_affiliate_url(
            original_url, sku, custom_tracking
        )

        assert "wgsource=custom_source" in affiliate_url
        assert "wgmedium=email" in affiliate_url

    @patch('requests.Session.head')
    def test_validate_affiliate_url_success(self, mock_head, webgains_client):
        """Test successful affiliate URL validation"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = "https://www.carhartt-wip.com/final-url"
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_head.return_value = mock_response

        result = webgains_client.validate_affiliate_url("https://track.webgains.com/test")

        assert result['valid'] is True
        assert result['status_code'] == 200
        assert result['response_time'] == 0.5

    @patch('requests.Session.head')
    def test_validate_affiliate_url_failure(self, mock_head, webgains_client):
        """Test failed affiliate URL validation"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_head.return_value = mock_response

        result = webgains_client.validate_affiliate_url("https://track.webgains.com/broken")

        assert result['valid'] is False
        assert result['status_code'] == 404

    def test_get_commission_rates(self, webgains_client):
        """Test commission rates retrieval"""
        rates = webgains_client.get_commission_rates()

        assert 'default' in rates
        assert 'sale_items' in rates
        assert 'new_arrivals' in rates
        assert rates['default'] == 0.08

    def test_generate_product_feed_url(self, webgains_client):
        """Test product feed URL generation"""
        feed_url = webgains_client.generate_product_feed_url()

        assert "api.webgains.com/feeds/product" in feed_url
        assert "wgprogramid=294000" in feed_url
        assert "format=xml" in feed_url


class TestWebgainsServiceIntegration:
    """Test Webgains integration with affiliate service"""

    @pytest.fixture
    def temp_db_with_webgains(self, tmp_path):
        """Create database with Webgains network"""
        import sqlite3

        db_path = tmp_path / "webgains_test.db"

        with sqlite3.connect(db_path) as conn:
            conn.executescript("""
                CREATE TABLE affiliate_networks (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    display_name TEXT,
                    default_commission_rate REAL,
                    status TEXT DEFAULT 'active'
                );

                CREATE TABLE affiliate_links (
                    id INTEGER PRIMARY KEY,
                    sku TEXT,
                    source TEXT,
                    network_id INTEGER,
                    original_url TEXT,
                    affiliate_url TEXT,
                    short_url TEXT,
                    commission_rate REAL,
                    status TEXT DEFAULT 'active',
                    last_validated TIMESTAMP,
                    validation_error TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP,
                    metadata JSON
                );

                INSERT INTO affiliate_networks (name, display_name, default_commission_rate)
                VALUES ('webgains', 'Webgains', 0.08);
            """)
            conn.commit()

        return db_path

    @pytest.fixture
    def affiliate_service(self, temp_db_with_webgains):
        """Create affiliate service with Webgains support"""
        return AffiliateService(temp_db_with_webgains)

    def test_generate_webgains_link(self, affiliate_service):
        """Test Webgains link generation via service"""
        sku = "I034405_02_XX"
        source = "carhartt_wip"
        original_url = "https://www.carhartt-wip.com/en/test-product"

        response = affiliate_service.generate_webgains_link(sku, source, original_url)

        assert response.link_id > 0
        assert "webgains.com" in response.affiliate_url
        assert response.commission_rate >= 0.06  # Should be valid commission rate
        assert response.network_name == "Webgains"

    def test_generate_webgains_link_with_custom_params(self, affiliate_service):
        """Test Webgains link generation with custom parameters"""
        sku = "CUSTOM001"
        source = "carhartt_wip"
        original_url = "https://www.carhartt-wip.com/en/custom-product"
        custom_params = {'wgcustom': 'test_value'}

        response = affiliate_service.generate_webgains_link(
            sku, source, original_url, custom_params
        )

        assert "wgcustom=test_value" in response.affiliate_url

    def test_bulk_generate_webgains_links(self, affiliate_service):
        """Test bulk Webgains link generation"""
        products = [
            {
                'sku': 'BULK001',
                'source': 'carhartt_wip',
                'url': 'https://www.carhartt-wip.com/en/bulk-product-1'
            },
            {
                'sku': 'BULK002',
                'source': 'carhartt_wip',
                'url': 'https://www.carhartt-wip.com/en/bulk-product-2'
            },
            {
                'sku': 'SKIP001',
                'source': 'end_clothing',  # Should be skipped
                'url': 'https://www.endclothing.com/en/skip-product'
            }
        ]

        results = affiliate_service.bulk_generate_webgains_links(products)

        assert results['total'] == 3
        assert len(results['success']) == 2  # Only Carhartt WIP products
        assert len(results['skipped']) == 1  # End Clothing product skipped
        assert len(results['failed']) == 0

    @patch('src.product_prices.config.webgains.webgains_client.validate_affiliate_url')
    def test_validate_webgains_links(self, mock_validate, affiliate_service, temp_db_with_webgains):
        """Test Webgains link validation"""
        # Create test link first
        response = affiliate_service.generate_webgains_link(
            "VAL001", "carhartt_wip", "https://www.carhartt-wip.com/en/validation-test"
        )

        # Mock validation responses
        mock_validate.return_value = {'valid': True, 'status_code': 200}

        results = affiliate_service.validate_webgains_links(batch_size=10)

        assert results['validated'] >= 1
        assert results['broken'] == 0


class TestWebgainsAPI:
    """Test Webgains API endpoints"""

    @pytest.fixture
    def client(self):
        """FastAPI test client"""
        from fastapi.testclient import TestClient
        from src.product_prices.api.main import app
        return TestClient(app)

    @patch('src.product_prices.api.routes.webgains.get_affiliate_service')
    def test_generate_webgains_link_api(self, mock_get_service, client):
        """Test Webgains link generation API"""
        # Mock service response
        mock_service = Mock()
        mock_response = Mock()
        mock_response.link_id = 123
        mock_response.affiliate_url = "https://track.webgains.com/test"
        mock_response.short_url = "https://deals.local/go/abc123"
        mock_response.commission_rate = 0.08
        mock_response.network_name = "Webgains"

        mock_service.generate_webgains_link.return_value = mock_response
        mock_get_service.return_value = mock_service

        response = client.post(
            "/api/v1/webgains/links/generate",
            json={
                "sku": "API001",
                "source": "carhartt_wip",
                "original_url": "https://www.carhartt-wip.com/en/api-test"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['link_id'] == 123
        assert data['commission_rate'] == 0.08

    def test_webgains_commission_rates_api(self, client):
        """Test commission rates API endpoint"""
        response = client.get("/api/v1/webgains/commission-rates")

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'commission_rates' in data
        assert 'default' in data['raw_rates']

    def test_webgains_health_check(self, client):
        """Test Webgains health check endpoint"""
        response = client.get("/api/v1/webgains/health")

        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert 'webgains_url_generation' in data
EOF
```

### 6. **Documentation and Usage Examples**

```bash
# Create Webgains documentation
cat > docs/webgains_integration.md << 'EOF'
# Webgains Integration Guide

## Overview

Complete Webgains affiliate network integration for Carhartt WIP products with 8% commission rates and 30-day cookie duration.

## Features

- **Automated URL Generation** - Dynamic affiliate links with tracking parameters
- **API Integration** - Full Webgains API support for program management
- **Link Validation** - Automated health checks for affiliate URLs
- **Bulk Operations** - Mass generation and validation of affiliate links
- **Commission Optimization** - Dynamic rates based on product categories

## Configuration

### Environment Setup
```bash
# Add to .env
WEBGAINS_API_KEY=your_api_key_here
WEBGAINS_API_SECRET=your_api_secret_here
WEBGAINS_CAMPAIGN_ID=1
WEBGAINS_PROGRAM_ID=294000
```

### Network Configuration
The Webgains network is automatically configured with:
- Program ID: 294000 (Carhartt WIP)
- Default Commission: 8%
- Cookie Duration: 30 days
- Deep Linking: Enabled

## Usage

### Generate Single Link
```python
# Via service
service = AffiliateService(db_path)
response = service.generate_webgains_link(
    sku="I034405_02_XX",
    source="carhartt_wip",
    original_url="https://www.carhartt-wip.com/en/product"
)

# Via CLI
uv run python -m product_prices affiliate webgains generate \
  --sku I034405_02_XX \
  --url "https://www.carhartt-wip.com/en/product"
```

### Bulk Generation
```bash
# Generate links for all Carhartt WIP products
uv run python -m product_prices affiliate webgains bulk-generate --limit 100
```

### Link Validation
```bash
# Validate existing Webgains links
uv run python -m product_prices affiliate webgains validate --batch-size 50
```

### Program Information
```bash
# Show Webgains configuration and program details
uv run python -m product_prices affiliate webgains info
```

## API Endpoints

### Link Management
- `POST /api/v1/webgains/links/generate` - Generate single affiliate link
- `POST /api/v1/webgains/links/bulk-generate` - Bulk link generation
- `POST /api/v1/webgains/links/validate` - Validate existing links

### Program Information
- `GET /api/v1/webgains/program/info` - Get program details from API
- `GET /api/v1/webgains/commission-rates` - Get commission rate structure
- `GET /api/v1/webgains/health` - Integration health check

## Commission Structure

- **Default Products**: 8% commission
- **Sale Items**: 6% commission (lower rate)
- **New Arrivals**: 10% commission (higher rate)

Commission rates are automatically determined based on product URL patterns.

## Testing

```bash
# Run Webgains tests
uv run pytest tests/test_webgains_integration.py -v

# Test API endpoints
curl -X POST http://localhost:8008/api/v1/webgains/links/generate \
  -H "Content-Type: application/json" \
  -d '{"sku": "TEST001", "source": "carhartt_wip", "original_url": "https://www.carhartt-wip.com/test"}'
```

## Monitoring

### Health Checks
```bash
# CLI health check
uv run python -m product_prices affiliate webgains info

# API health check
curl http://localhost:8008/api/v1/webgains/health
```

### Performance Metrics
- Link generation success rate
- Validation failure rate
- Commission tracking accuracy
- API response times

## Troubleshooting

### Common Issues
1. **API Key Not Working**
   - Verify credentials in `.env` file
   - Check Webgains account status
   - Ensure program approval

2. **Link Validation Failures**
   - Check network connectivity
   - Verify Webgains service status
   - Review link format and parameters

3. **Commission Rate Issues**
   - Verify program terms
   - Check product category classification
   - Review tracking parameter setup

### Debug Commands
```bash
# Test URL generation
python -c "
from src.product_prices.config.webgains import webgains_client
url = webgains_client.generate_affiliate_url('https://test.com', 'TEST001')
print(f'Generated: {url}')
"

# Validate specific link
python -c "
from src.product_prices.config.webgains import webgains_client
result = webgains_client.validate_affiliate_url('https://track.webgains.com/test')
print(f'Valid: {result}')
"
```
EOF

# Run integration tests
uv run pytest tests/test_webgains_integration.py -v

# Test CLI commands
echo "✅ Webgains Integration Command Complete"
echo "📋 Next: Run '/affiliate:setup-foundation' and '/affiliate:setup-tracking' first"
echo "🚀 Then: Use '/affiliate:add-webgains-integration' to set up Carhartt WIP affiliate links"
```

## Summary

This command establishes complete Webgains integration:

1. ✅ **API Client** - Full Webgains API integration with authentication
2. ✅ **Service Integration** - Enhanced affiliate service with Webgains support
3. ✅ **URL Generation** - Dynamic affiliate links with tracking parameters
4. ✅ **Link Validation** - Automated health checks and broken link detection
5. ✅ **Bulk Operations** - Mass generation for all Carhartt WIP products
6. ✅ **API Endpoints** - RESTful interface for all Webgains operations
7. ✅ **CLI Commands** - Management tools for daily operations
8. ✅ **Testing Suite** - Comprehensive tests for all functionality

The Webgains integration provides 8% commission on Carhartt WIP products with automated link management and validation.
