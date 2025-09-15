# Price Analytics Report Command

Generate sophisticated price intelligence and market analysis for WorkwearWatch's 657+ premium streetwear products.

## Usage
Type `/price-report` to create comprehensive price analytics dashboard.

## Actions Performed
1. **Trend Analysis**: Historical price movements and patterns
2. **Deal Discovery**: Current best discounts and opportunities
3. **Market Intelligence**: Cross-retailer pricing strategies
4. **Anomaly Detection**: Unusual price changes requiring attention
5. **Category Insights**: Workwear vs streetwear pricing dynamics

## Command Execution
```bash
echo "📊 WorkwearWatch Price Intelligence Report"
echo "========================================="

# Generate database statistics
echo "📈 Analyzing price trends..."
./scripts/db_stats.py --detailed

# Price movement analysis (see .claude/database-schema.md for schema)
echo "💰 Current market analysis..."
uv run python -c "
import sqlite3
import pandas as pd

conn = sqlite3.connect('products.db')

# Recent price changes (last 7 days)
recent_changes = pd.read_sql('''
    SELECT p.name, p.current_price, p.source,
           ph.old_current_price, ph.new_current_price, ph.change_type, ph.recorded_at
    FROM products p
    JOIN price_history ph ON p.sku = ph.sku AND p.source = ph.source
    WHERE ph.recorded_at > datetime('now', '-7 days')
    ORDER BY ph.recorded_at DESC
''', conn)

print(f'Recent Changes: {len(recent_changes)} products')

# Best current deals
best_deals = pd.read_sql('''
    SELECT name, current_price, source, url
    FROM products
    WHERE current_price IS NOT NULL AND current_price <> ''
    ORDER BY CAST(current_price AS REAL) ASC
    LIMIT 10
''', conn)

print('\n🎯 Best Current Deals:')
for _, deal in best_deals.iterrows():
    name_short = deal['name'][:50] + '...' if len(deal['name']) > 50 else deal['name']
    print(f'- {name_short}: £{deal.current_price} at {deal.source}')

# Price volatility by retailer
volatility = pd.read_sql('''
    SELECT source, COUNT(*) as changes,
           AVG(CAST(new_current_price AS REAL) - CAST(old_current_price AS REAL)) as avg_change
    FROM price_history
    WHERE recorded_at > datetime('now', '-30 days')
      AND old_current_price IS NOT NULL
      AND new_current_price IS NOT NULL
      AND old_current_price <> ''
      AND new_current_price <> ''
    GROUP BY source
''', conn)

print('\n📊 Retailer Price Activity (30 days):')
for _, vol in volatility.iterrows():
    print(f'- {vol.source}: {vol.changes} changes, avg £{vol.avg_change:.2f}')

conn.close()
"

# Health check for data freshness
echo "🔍 Data freshness check..."
./scripts/health_monitor.py | grep -E "(products|success|error)"

echo "✅ Price intelligence report complete"
```

## Report Sections
1. **Executive Summary**: Key market movements and opportunities
2. **Deal Alerts**: Best current discounts across all retailers
3. **Price Trends**: Historical analysis and seasonal patterns
4. **Retailer Intelligence**: Pricing strategies and positioning
5. **Category Performance**: Workwear vs accessories analysis
6. **Anomaly Alerts**: Unusual price movements requiring attention

## Expected Output
- Recent price change summary (7-day window)
- Top 10 best deals currently available
- Retailer pricing activity and volatility metrics
- Category-wise performance breakdown
- Data freshness and portfolio health status

## Context
Serves sophisticated streetwear enthusiasts with editorial-quality market intelligence focusing on heritage workwear and premium brands.
