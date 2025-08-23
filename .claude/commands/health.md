# Health Check Command

Run comprehensive WorkwearWatch system health monitoring across all components.

## Usage
Type `/health` to execute complete system diagnostics.

## Actions Performed
1. **Database Health**: Check product count (target: 657+), recent scraping runs
2. **Scraper Status**: Validate all 4 retailers (Carhartt WIP, Tony McDonald, End Clothing, HUH)
3. **API Health**: Test FastAPI endpoints and response times
4. **Data Integrity**: Verify price history, detect stale URLs
5. **Performance Metrics**: Calculate success rates and system reliability

## Command Execution
```bash
# Execute comprehensive health monitoring
./scripts/health_monitor.py

# Database statistics
./scripts/db_stats.py

# Check for invalid URLs
./scripts/check_invalid_urls.py

# Validate sample URLs from each retailer
./scripts/check_sample_urls.py
```

## Expected Output
- System reliability percentage (target: 95%+)
- Product portfolio status (657+ products)
- Recent scraping performance
- API response time metrics
- Critical issues requiring attention

## Context
Maintains production-ready monitoring for sophisticated streetwear price tracking system.
