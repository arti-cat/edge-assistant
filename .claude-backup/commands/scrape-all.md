# Scrape All Command

Execute comprehensive product data collection across all WorkwearWatch retailers with progress monitoring.

## Usage
Type `/scrape-all` to run full product portfolio refresh.

## Actions Performed
1. **Sequential Scraping**: Carhartt WIP → Tony McDonald → End Clothing → HUH Store
2. **Progress Monitoring**: Real-time status updates and product counts
3. **Error Handling**: Graceful failure recovery, detailed error logging
4. **Rate Limiting**: Cryptographic delays (5-15 seconds) between requests
5. **Data Validation**: Verify product integrity and price formatting

## Command Execution
```bash
# Full portfolio refresh with monitoring
echo "🚀 Starting WorkwearWatch Product Collection"
echo "============================================"

# Carhartt WIP (Heritage workwear focus)
echo "📦 Scraping Carhartt WIP..."
uv run python -m product_prices.cli carhartt-wip

# Tony McDonald (Premium streetwear)
echo "📦 Scraping Tony McDonald..."
uv run python -m product_prices.cli tony-mcdonald

# End Clothing (International premium)
echo "📦 Scraping End Clothing..."
uv run python -m product_prices.cli end-clothing

# HUH Store (Curated streetwear)
echo "📦 Scraping HUH Store..."
uv run python -m product_prices.cli huh-store

# Generate completion summary
echo "✅ Scraping Complete - Running health check..."
./scripts/health_monitor.py
```

## Expected Output
- Individual scraper progress and product counts
- Total products added/updated across 657+ portfolio
- Success rate percentage (target: 95%+)
- Price change notifications
- Error summary and recommendations

## Performance Notes
- Complete run takes 15-30 minutes (rate limiting)
- Monitors memory usage and connection stability
- Maintains sophisticated streetwear product catalog integrity
