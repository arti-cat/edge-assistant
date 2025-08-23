# WorkwearWatch Database Schema Specification

**Database**: SQLite (`products.db` / supabase for prod)
**Context**: 1,593+ premium streetwear products across 4 retailers

## Core Tables

### `products` Table
Primary product catalog with current state information.

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL,                    -- Product SKU/identifier
    source TEXT NOT NULL,                 -- Retailer: carhartt_wip, end_clothing, huh_store, tony_mcdonald
    name TEXT NOT NULL,                   -- Product name/title
    url TEXT,                            -- Product page URL
    current_price TEXT,                  -- Current price as string (e.g., "29.99")
    original_price TEXT,                 -- Original/RRP price as string
    currency TEXT DEFAULT 'GBP',        -- Currency code
    in_stock BOOLEAN DEFAULT TRUE,       -- Stock status
    metadata JSON,                       -- Additional scraper data
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sku, source)                  -- Composite key for multi-source products
);
```

**Key Points:**
- Prices stored as TEXT for precision (use `CAST(current_price AS REAL)` for math)
- Multi-source support: same SKU can exist across retailers
- No `brand` column - brand info may be in `name` or `metadata`

### `price_history` Table
Tracks all price changes with detailed change types.

```sql
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL,
    source TEXT NOT NULL,
    change_type TEXT NOT NULL,           -- 'price_increase', 'price_decrease', 'new_product', etc.
    old_current_price TEXT,             -- Previous current price
    new_current_price TEXT,             -- New current price
    old_original_price TEXT,            -- Previous original price
    new_original_price TEXT,            -- New original price
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sku, source) REFERENCES products(sku, source)
);
```

**Change Types:**
- `new_product` - First time seen
- `price_increase` - Price went up
- `price_decrease` - Price went down
- `back_in_stock` - Returned to stock
- `out_of_stock` - Went out of stock
- `price_correction` - Price data correction
- `sale_started` - Sale/discount began

### `scraping_runs` Table
Operational monitoring and performance tracking.

```sql
CREATE TABLE scraping_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,               -- Retailer scraped
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    status TEXT NOT NULL,               -- 'success', 'failed', 'partial'
    products_found INTEGER DEFAULT 0,
    products_added INTEGER DEFAULT 0,
    products_updated INTEGER DEFAULT 0,
    products_changed INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    errors JSON,                        -- Array of error details
    duration_seconds REAL,
    metadata JSON
);
```

## Common Query Patterns

### Recent Price Changes
```sql
SELECT p.name, p.current_price, p.source,
       ph.old_current_price, ph.new_current_price, ph.change_type, ph.recorded_at
FROM products p
JOIN price_history ph ON p.sku = ph.sku AND p.source = ph.source
WHERE ph.recorded_at > datetime('now', '-7 days')
ORDER BY ph.recorded_at DESC;
```

### Best Current Deals
```sql
SELECT name, current_price, source, url
FROM products
WHERE current_price IS NOT NULL AND current_price <> ''
ORDER BY CAST(current_price AS REAL) ASC
LIMIT 10;
```

### Retailer Performance
```sql
SELECT source,
       COUNT(*) as total_runs,
       SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_runs,
       AVG(duration_seconds) as avg_duration,
       AVG(products_found) as avg_products
FROM scraping_runs
WHERE started_at > datetime('now', '-30 days')
GROUP BY source;
```

### Price Volatility Analysis
```sql
SELECT source, COUNT(*) as changes,
       AVG(CAST(new_current_price AS REAL) - CAST(old_current_price AS REAL)) as avg_change
FROM price_history
WHERE recorded_at > datetime('now', '-30 days')
  AND old_current_price IS NOT NULL
  AND new_current_price IS NOT NULL
  AND old_current_price <> ''
  AND new_current_price <> ''
GROUP BY source;
```

## Data Quality Notes

### Price Handling
- **Always use `CAST(price AS REAL)`** for mathematical operations
- Check for empty strings: `current_price <> ''`
- Handle NULL values: `current_price IS NOT NULL`

### Source Values
- `carhartt_wip` - Carhartt WIP official (largest dataset ~1,128 products)
- `end_clothing` - End Clothing (~141 products)
- `huh_store` - HUH Store (~253 products)
- `tony_mcdonald` - Tony Mc Donnell (~71 products)

### Common Gotchas
- No `brand` column - extract from `name` if needed
- Price columns are TEXT, not NUMERIC
- Use `recorded_at` not `timestamp` for price_history
- Composite keys: `(sku, source)` for multi-retailer products

## Current Stats (Live Data)
- **Total Products**: 1,593
- **Price History Records**: 6,136+
- **Recent Activity**: 4,366 changes in last 7 days
- **Data Quality Score**: 95.2%
