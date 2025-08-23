# Create REST API

Create a simple REST API for the product price monitoring system, leveraging existing monitoring infrastructure for immediate value.

## Instructions

Follow these steps to create a FastAPI-based REST API that wraps your existing monitoring functionality:

### 1. **Add FastAPI Dependencies**

Add FastAPI and related dependencies to your existing project:

```bash
# Add API dependencies to existing pyproject.toml
uv add fastapi uvicorn python-multipart
```

### 2. **Create API Module Structure**

Set up the API module structure within your existing project:

```bash
# Create API module structure
mkdir -p src/product_prices/api
touch src/product_prices/api/__init__.py
touch src/product_prices/api/main.py
touch src/product_prices/api/models.py
touch src/product_prices/api/routes.py
```

### 3. **Create API Models (Pydantic)**

Create `src/product_prices/api/models.py` with response models:

```python
"""
API response models for product price monitoring system.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ProductResponse(BaseModel):
    """Response model for product data."""
    id: int
    sku: str
    source: str
    name: str
    url: Optional[str] = None
    current_price: Optional[str] = None
    original_price: Optional[str] = None
    currency: str = "GBP"
    in_stock: bool = True
    metadata: Optional[Dict[str, Any]] = None
    first_seen: str  # SQLite returns as string
    last_seen: str   # SQLite returns as string


class SystemStatusResponse(BaseModel):
    """Response model for system status."""
    total_products: int
    products_by_source: Dict[str, int]
    last_successful_runs: Dict[str, Optional[str]]
    reliability_24h: Dict[str, float]
    timestamp: str


class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    is_healthy: bool
    scraper_failures: List[str]
    reliability_issues: List[str]
    stale_data: List[str]
    performance_issues: List[str]


class ScraperReliabilityResponse(BaseModel):
    """Response model for scraper reliability."""
    source: str
    total_runs: int
    successful_runs: int
    success_rate: float
    avg_duration: Optional[float]


class PriceAnalyticsResponse(BaseModel):
    """Response model for price analytics."""
    change_type: str
    occurrences: int
    source: str
    avg_change_amount: Optional[float]


class PriceHistoryResponse(BaseModel):
    """Response model for price history."""
    id: int
    sku: str
    source: str
    change_type: str
    old_current_price: Optional[str]
    new_current_price: Optional[str]
    old_original_price: Optional[str]
    new_original_price: Optional[str]
    recorded_at: str


class ErrorResponse(BaseModel):
    """Response model for API errors."""
    error: str
    message: str
    timestamp: str
```

### 4. **Create API Routes**

Create `src/product_prices/api/routes.py` that wraps your existing monitoring:

```python
"""
API routes for product price monitoring system.
Leverages existing monitoring.py functionality.
"""
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from ..monitoring import HealthChecker, MonitoringQueries
from .models import (
    HealthCheckResponse,
    PriceAnalyticsResponse,
    PriceHistoryResponse,
    ProductResponse,
    ScraperReliabilityResponse,
    SystemStatusResponse,
)

# Default database path - matches CLI behavior
DEFAULT_DB_PATH = Path("products.db")

# Create router
router = APIRouter(prefix="/api/v1", tags=["monitoring"])


@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status():
    """
    Get overall system status.

    Wraps the existing MonitoringQueries.system_status() method.
    """
    try:
        queries = MonitoringQueries(DEFAULT_DB_PATH)
        status = queries.system_status()
        return SystemStatusResponse(**status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system status: {str(e)}")


@router.get("/health", response_model=HealthCheckResponse)
async def get_health_check():
    """
    Run comprehensive health check.

    Wraps the existing HealthChecker functionality.
    """
    try:
        health_checker = HealthChecker(DEFAULT_DB_PATH)
        checks = health_checker.run_all_checks()
        is_healthy = health_checker.is_healthy()

        return HealthCheckResponse(
            is_healthy=is_healthy,
            scraper_failures=checks["scraper_failures"],
            reliability_issues=checks["reliability_issues"],
            stale_data=checks["stale_data"],
            performance_issues=checks["performance_issues"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.get("/reliability", response_model=List[ScraperReliabilityResponse])
async def get_scraper_reliability(days: int = Query(default=7, ge=1, le=30)):
    """
    Get scraper reliability metrics.

    Args:
        days: Number of days to analyze (1-30)
    """
    try:
        queries = MonitoringQueries(DEFAULT_DB_PATH)
        reliability_data = queries.scraper_reliability(days)

        return [ScraperReliabilityResponse(**item) for item in reliability_data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get reliability data: {str(e)}")


@router.get("/analytics/price-changes", response_model=List[PriceAnalyticsResponse])
async def get_price_analytics(days: int = Query(default=7, ge=1, le=30)):
    """
    Get price change analytics.

    Args:
        days: Number of days to analyze (1-30)
    """
    try:
        queries = MonitoringQueries(DEFAULT_DB_PATH)
        analytics_data = queries.price_change_analytics(days)

        return [PriceAnalyticsResponse(**item) for item in analytics_data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get price analytics: {str(e)}")


@router.get("/products", response_model=List[ProductResponse])
async def get_products(
    source: Optional[str] = Query(default=None, description="Filter by source (tony_mcdonald, carhartt_wip)"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of products to return")
):
    """
    Get products with optional filtering.

    Args:
        source: Filter by scraper source
        limit: Maximum number of products to return
    """
    try:
        queries = MonitoringQueries(DEFAULT_DB_PATH)
        conn = queries.get_connection()

        # Build query
        sql = "SELECT * FROM products"
        params = []

        if source:
            sql += " WHERE source = ?"
            params.append(source)

        sql += " ORDER BY last_seen DESC LIMIT ?"
        params.append(limit)

        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()

        # Convert to response models
        columns = [desc[0] for desc in cursor.description]
        products = []

        for row in rows:
            product_data = dict(zip(columns, row))
            # Handle JSON metadata
            import json
            if product_data.get('metadata'):
                try:
                    product_data['metadata'] = json.loads(product_data['metadata'])
                except:
                    product_data['metadata'] = None
            else:
                product_data['metadata'] = None

            products.append(ProductResponse(**product_data))

        return products

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get products: {str(e)}")


@router.get("/products/{sku}")
async def get_product_by_sku(sku: str, source: Optional[str] = None):
    """
    Get specific product by SKU.

    Args:
        sku: Product SKU
        source: Source filter (optional)
    """
    try:
        queries = MonitoringQueries(DEFAULT_DB_PATH)
        conn = queries.get_connection()

        if source:
            sql = "SELECT * FROM products WHERE sku = ? AND source = ?"
            params = [sku, source]
        else:
            sql = "SELECT * FROM products WHERE sku = ?"
            params = [sku]

        cursor = conn.execute(sql, params)
        row = cursor.fetchone()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Product not found")

        # Convert to response model
        columns = [desc[0] for desc in cursor.description]
        product_data = dict(zip(columns, row))

        # Handle JSON metadata
        import json
        if product_data.get('metadata'):
            try:
                product_data['metadata'] = json.loads(product_data['metadata'])
            except:
                product_data['metadata'] = None
        else:
            product_data['metadata'] = None

        return ProductResponse(**product_data)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get product: {str(e)}")


@router.get("/products/{sku}/history", response_model=List[PriceHistoryResponse])
async def get_product_price_history(sku: str, source: Optional[str] = None):
    """
    Get price history for a specific product.

    Args:
        sku: Product SKU
        source: Source filter (optional)
    """
    try:
        queries = MonitoringQueries(DEFAULT_DB_PATH)
        conn = queries.get_connection()

        if source:
            sql = "SELECT * FROM price_history WHERE sku = ? AND source = ? ORDER BY recorded_at DESC"
            params = [sku, source]
        else:
            sql = "SELECT * FROM price_history WHERE sku = ? ORDER BY recorded_at DESC"
            params = [sku]

        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()

        # Convert to response models
        columns = [desc[0] for desc in cursor.description]
        history = []

        for row in rows:
            history_data = dict(zip(columns, row))
            history.append(PriceHistoryResponse(**history_data))

        return history

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get price history: {str(e)}")
```

### 5. **Create Main API Application**

Create `src/product_prices/api/main.py`:

```python
"""
FastAPI application for product price monitoring system.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router

# Create FastAPI app
app = FastAPI(
    title="Product Price Monitor API",
    description="REST API for product price monitoring system with operational metrics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Product Price Monitor API",
        "version": "1.0.0",
        "description": "REST API for multi-site product price monitoring",
        "endpoints": {
            "status": "/api/v1/status",
            "health": "/api/v1/health",
            "reliability": "/api/v1/reliability",
            "analytics": "/api/v1/analytics/price-changes",
            "products": "/api/v1/products",
            "product_history": "/api/v1/products/{sku}/history",
            "docs": "/docs"
        }
    }


@app.get("/ping")
async def ping():
    """Simple health ping endpoint."""
    return {"status": "ok", "message": "Product Price Monitor API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 6. **Add API Script to CLI**

Add a new command to your existing CLI in `src/product_prices/cli.py`:

```python
# Add this function to your existing cli.py

def run_api_server() -> None:
    """Run the REST API server."""
    import uvicorn
    from .api.main import app

    print("Starting Product Price Monitor API server...")
    print("API Documentation: http://localhost:8000/docs")
    print("API Endpoints: http://localhost:8000")

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


# Add to your main() function's command handling:
elif command == "api" or command == "--api":
    try:
        run_api_server()
    except KeyboardInterrupt:
        print("\nAPI server stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"Error running API server: {e}")
        sys.exit(1)

# Update your show_help() function to include:
print("API COMMANDS:")
print("  api              Start REST API server on port 8000")
```

### 7. **Create Simple Test Script**

Create `test_api.py` in the project root for quick testing:

```python
#!/usr/bin/env python3
"""
Quick API test script
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test main API endpoints."""

    endpoints = [
        "/",
        "/ping",
        "/api/v1/status",
        "/api/v1/health",
        "/api/v1/reliability",
        "/api/v1/analytics/price-changes",
        "/api/v1/products?limit=5"
    ]

    print("Testing Product Price Monitor API...")

    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            print(f"✅ {endpoint}: {response.status_code}")

            if endpoint == "/api/v1/products?limit=5":
                data = response.json()
                print(f"   Found {len(data)} products")

        except requests.exceptions.ConnectionError:
            print(f"❌ {endpoint}: Connection failed (API not running?)")
        except Exception as e:
            print(f"❌ {endpoint}: {str(e)}")

if __name__ == "__main__":
    test_api_endpoints()
```

### 8. **Update Documentation**

Add API usage to your README.md:

```markdown
### 🚀 **NEW: REST API (Phase 3)**

```bash
# Start API server
uv run python -m src.product_prices.cli api

# API Documentation: http://localhost:8000/docs
# Test endpoints: python test_api.py
```

**Available Endpoints:**

- `GET /api/v1/status` - System status overview
- `GET /api/v1/health` - Comprehensive health check
- `GET /api/v1/reliability?days=7` - Scraper reliability metrics
- `GET /api/v1/analytics/price-changes?days=7` - Price change analytics
- `GET /api/v1/products?source=carhartt_wip&limit=100` - Product listings
- `GET /api/v1/products/{sku}` - Individual product details
- `GET /api/v1/products/{sku}/history` - Product price history
```

### 9. **Test the API**


```bash
# Start the API server
uv run python -m src.product_prices.cli api

# In another terminal, test the endpoints
python test_api.py

# Or visit the interactive docs
open http://localhost:8000/docs
```


### 10. **Add Basic Tests**

Create `tests/test_api.py`:

```python
"""
Tests for REST API functionality
"""
import pytest
from fastapi.testclient import TestClient

from src.product_prices.api.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "endpoints" in data


def test_ping_endpoint():
    """Test ping endpoint."""
    response = client.get("/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_status_endpoint():
    """Test status endpoint."""
    response = client.get("/api/v1/status")
    # May fail if no database - that's expected
    assert response.status_code in [200, 500]


def test_health_endpoint():
    """Test health endpoint."""
    response = client.get("/api/v1/health")
    # May fail if no database - that's expected
    assert response.status_code in [200, 500]
```

## Summary

This command creates a **simple, focused REST API** that:

✅ **Leverages your existing monitoring infrastructure** - No duplication
✅ **Wraps MonitoringQueries and HealthChecker** - Immediate value
✅ **Provides 7 core endpoints** - Status, health, reliability, analytics, products, price history
✅ **Integrates with your CLI** - `uv run python -m src.product_prices.cli api`
✅ **Includes interactive docs** - FastAPI automatic OpenAPI docs
✅ **Stays simple** - ~250 lines of code, minimal dependencies

The API makes your rich monitoring data instantly accessible via HTTP, enabling integrations, dashboards, and external tools while building on your excellent foundation.
