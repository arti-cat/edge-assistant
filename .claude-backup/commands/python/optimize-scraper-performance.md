# Optimize Scraper Performance

Comprehensive performance optimization for web scraping operations, focusing on request efficiency, memory management, database optimization, concurrent processing, caching strategies, and scalability.

## Instructions

Follow these systematic steps to optimize your web scraper's performance:

### 1. Request Optimization

**Implement connection pooling and session reuse:**
```python
# Install dependencies
uv add httpx[http2] aiohttp requests-cache

# Create optimized HTTP client
import httpx
import asyncio
from typing import Optional, Dict, Any

class OptimizedHTTPClient:
    def __init__(self,
                 max_connections: int = 100,
                 max_keepalive_connections: int = 20,
                 keepalive_expiry: int = 5):
        # Configure connection limits and HTTP/2 support
        limits = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
            keepalive_expiry=keepalive_expiry
        )

        # Optimized headers for scraping
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; OptimizedScraper/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        self.client = httpx.AsyncClient(
            limits=limits,
            timeout=httpx.Timeout(30.0, connect=10.0),
            headers=headers,
            http2=True,
            follow_redirects=True
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
```

**Configure optimal timeout and retry strategies:**
```python
import tenacity
from tenacity import retry, stop_after_attempt, wait_exponential

class RetryableHTTPClient(OptimizedHTTPClient):
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=tenacity.retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError))
    )
    async def get_with_retry(self, url: str, **kwargs) -> httpx.Response:
        response = await self.client.get(url, **kwargs)
        response.raise_for_status()
        return response

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=5)
    )
    async def get_resilient(self, url: str, **kwargs) -> Optional[httpx.Response]:
        try:
            return await self.get_with_retry(url, **kwargs)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            return None
```

**Set up request batching and concurrent processing:**
```python
import asyncio
from asyncio import Semaphore
from typing import List, Callable, TypeVar, Coroutine

T = TypeVar('T')

class BatchProcessor:
    def __init__(self, max_concurrent: int = 10, batch_size: int = 50):
        self.max_concurrent = max_concurrent
        self.batch_size = batch_size
        self.semaphore = Semaphore(max_concurrent)

    async def process_urls_batch(self,
                                urls: List[str],
                                processor: Callable[[str], Coroutine[Any, Any, T]]) -> List[Optional[T]]:
        """Process URLs in batches with controlled concurrency"""
        results = []

        for i in range(0, len(urls), self.batch_size):
            batch = urls[i:i + self.batch_size]
            batch_tasks = [self._process_with_semaphore(url, processor) for url in batch]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            results.extend(batch_results)

            # Small delay between batches to be respectful
            await asyncio.sleep(0.1)

        return results

    async def _process_with_semaphore(self, url: str, processor: Callable) -> Optional[T]:
        async with self.semaphore:
            try:
                return await processor(url)
            except Exception as e:
                print(f"Error processing {url}: {e}")
                return None
```

### 2. Memory Management

**Implement memory-efficient product processing:**
```python
# Install memory profiling tools
uv add memory-profiler psutil py-spy

import gc
import psutil
from typing import Iterator, Dict, Any
from dataclasses import dataclass
import weakref

@dataclass
class ProductData:
    """Lightweight product data structure"""
    __slots__ = ['id', 'name', 'price', 'url', 'last_updated']
    id: str
    name: str
    price: float
    url: str
    last_updated: str

class MemoryEfficientProcessor:
    def __init__(self, max_memory_mb: int = 500):
        self.max_memory_mb = max_memory_mb
        self._processed_count = 0
        self._product_cache = weakref.WeakValueDictionary()

    def check_memory_usage(self) -> float:
        """Monitor memory usage and trigger cleanup if needed"""
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024

        if memory_mb > self.max_memory_mb:
            self.cleanup_memory()

        return memory_mb

    def cleanup_memory(self):
        """Force garbage collection and clear caches"""
        self._product_cache.clear()
        gc.collect()
        print(f"Memory cleanup performed after processing {self._processed_count} items")

    def process_products_stream(self, products: Iterator[Dict[str, Any]]) -> Iterator[ProductData]:
        """Process products in a memory-efficient streaming manner"""
        for product_data in products:
            if self._processed_count % 1000 == 0:
                self.check_memory_usage()

            # Create lightweight product object
            product = ProductData(
                id=product_data.get('id', ''),
                name=product_data.get('name', '')[:100],  # Limit string length
                price=float(product_data.get('price', 0)),
                url=product_data.get('url', ''),
                last_updated=product_data.get('last_updated', '')
            )

            self._processed_count += 1
            yield product
```

**Create streaming parsers for large HTML documents:**
```python
# Install streaming parsers
uv add lxml beautifulsoup4 selectolax

from selectolax.parser import HTMLParser
import ijson
from typing import Iterator

class StreamingHTMLParser:
    """Memory-efficient HTML parsing for large documents"""

    @staticmethod
    def parse_products_selectolax(html_content: str, selector: str) -> Iterator[Dict[str, Any]]:
        """Fast parsing using selectolax (C-based parser)"""
        parser = HTMLParser(html_content)

        for element in parser.css(selector):
            yield {
                'name': element.css_first('.product-name')?.text(),
                'price': element.css_first('.price')?.text(),
                'url': element.css_first('a')?.attributes.get('href'),
                'id': element.attributes.get('data-id')
            }

        # Clear parser to free memory
        del parser

    @staticmethod
    def parse_json_stream(json_response: str) -> Iterator[Dict[str, Any]]:
        """Stream parse large JSON responses"""
        # For JSON arrays: ijson.items(json_response, 'products.item')
        for product in ijson.items(json_response, 'item'):
            yield product

class ChunkedHTMLProcessor:
    """Process HTML in chunks to manage memory"""

    def __init__(self, chunk_size: int = 1024 * 1024):  # 1MB chunks
        self.chunk_size = chunk_size

    def process_large_html(self, html_content: str, processor_func: Callable) -> Iterator:
        """Process large HTML documents in manageable chunks"""
        if len(html_content) <= self.chunk_size:
            yield from processor_func(html_content)
            return

        # For very large documents, implement sliding window parsing
        overlap = 1000  # Character overlap to avoid splitting elements

        for i in range(0, len(html_content), self.chunk_size - overlap):
            chunk = html_content[i:i + self.chunk_size]

            # Ensure we don't split in the middle of an HTML tag
            if i + self.chunk_size < len(html_content):
                last_tag = chunk.rfind('>')
                if last_tag > 0:
                    chunk = chunk[:last_tag + 1]

            yield from processor_func(chunk)
```

### 3. Database Optimization

**Optimize SQLite configuration for scraping workloads:**
```python
# Install database optimization tools
uv add aiosqlite sqlalchemy[asyncio] sqlite-utils

import aiosqlite
import sqlite3
from contextlib import asynccontextmanager
from typing import List, Dict, Any

class OptimizedSQLiteManager:
    def __init__(self, db_path: str, pool_size: int = 5):
        self.db_path = db_path
        self.pool_size = pool_size
        self._connection_pool = []

    async def initialize_db(self):
        """Initialize database with optimized settings"""
        async with aiosqlite.connect(self.db_path) as db:
            # Optimize SQLite for scraping workloads
            await db.execute("PRAGMA journal_mode = WAL")
            await db.execute("PRAGMA synchronous = NORMAL")
            await db.execute("PRAGMA cache_size = -64000")  # 64MB cache
            await db.execute("PRAGMA temp_store = MEMORY")
            await db.execute("PRAGMA mmap_size = 268435456")  # 256MB mmap
            await db.execute("PRAGMA optimize")

            # Create optimized schema
            await db.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    url TEXT NOT NULL,
                    last_updated INTEGER NOT NULL,
                    created_at INTEGER DEFAULT (strftime('%s', 'now'))
                )
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id TEXT NOT NULL,
                    price REAL NOT NULL,
                    timestamp INTEGER DEFAULT (strftime('%s', 'now')),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            """)

            # Create optimized indexes
            await db.execute("CREATE INDEX IF NOT EXISTS idx_products_updated ON products(last_updated)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_price_history_product ON price_history(product_id)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_price_history_timestamp ON price_history(timestamp)")

            await db.commit()

    @asynccontextmanager
    async def get_connection(self):
        """Connection pool manager"""
        conn = await aiosqlite.connect(self.db_path)
        try:
            yield conn
        finally:
            await conn.close()
```

**Create efficient bulk insert and update operations:**
```python
class BulkDatabaseOperations:
    def __init__(self, db_manager: OptimizedSQLiteManager):
        self.db_manager = db_manager

    async def bulk_upsert_products(self, products: List[ProductData], batch_size: int = 1000):
        """Efficient bulk upsert with batching"""
        async with self.db_manager.get_connection() as db:
            await db.execute("BEGIN TRANSACTION")

            try:
                for i in range(0, len(products), batch_size):
                    batch = products[i:i + batch_size]

                    # Prepare batch data
                    product_data = [
                        (p.id, p.name, p.price, p.url, int(time.time()))
                        for p in batch
                    ]

                    # Use INSERT OR REPLACE for upsert behavior
                    await db.executemany("""
                        INSERT OR REPLACE INTO products
                        (id, name, price, url, last_updated)
                        VALUES (?, ?, ?, ?, ?)
                    """, product_data)

                    if i % (batch_size * 10) == 0:
                        print(f"Processed {i} products...")

                await db.execute("COMMIT")
                print(f"Successfully upserted {len(products)} products")

            except Exception as e:
                await db.execute("ROLLBACK")
                print(f"Bulk upsert failed: {e}")
                raise

    async def bulk_insert_price_history(self, price_changes: List[Dict[str, Any]]):
        """Efficient price history tracking"""
        async with self.db_manager.get_connection() as db:
            price_data = [
                (change['product_id'], change['price'], change.get('timestamp', int(time.time())))
                for change in price_changes
            ]

            await db.executemany("""
                INSERT INTO price_history (product_id, price, timestamp)
                VALUES (?, ?, ?)
            """, price_data)

            await db.commit()
```

### 4. Concurrent Scraping

**Set up controlled concurrent scraping with rate limiting:**
```python
# Install rate limiting and async tools
uv add aiolimiter asyncio-throttle

import time
from aiolimiter import AsyncLimiter
from asyncio_throttle import Throttler

class RateLimitedScraper:
    def __init__(self,
                 requests_per_second: float = 2.0,
                 requests_per_minute: int = 100,
                 max_concurrent: int = 5):

        # Multiple rate limiters for different time windows
        self.second_limiter = AsyncLimiter(requests_per_second, 1.0)
        self.minute_limiter = AsyncLimiter(requests_per_minute, 60.0)
        self.throttler = Throttler(rate_limit=requests_per_second)

        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.request_times = []

    async def respectful_request(self, url: str, client: OptimizedHTTPClient) -> Optional[httpx.Response]:
        """Make request with proper rate limiting"""
        async with self.semaphore:
            # Apply rate limiting
            async with self.second_limiter:
                async with self.minute_limiter:
                    async with self.throttler:

                        # Track request timing
                        start_time = time.time()

                        try:
                            response = await client.get_with_retry(url)

                            # Log performance metrics
                            duration = time.time() - start_time
                            self.request_times.append(duration)

                            # Keep only recent timing data
                            if len(self.request_times) > 1000:
                                self.request_times = self.request_times[-500:]

                            return response

                        except Exception as e:
                            print(f"Request failed for {url}: {e}")
                            return None

    def get_performance_stats(self) -> Dict[str, float]:
        """Get scraping performance statistics"""
        if not self.request_times:
            return {}

        return {
            'avg_response_time': sum(self.request_times) / len(self.request_times),
            'min_response_time': min(self.request_times),
            'max_response_time': max(self.request_times),
            'total_requests': len(self.request_times)
        }
```

**Implement async/await patterns for I/O-bound operations:**
```python
class AsyncScrapingPipeline:
    def __init__(self, db_manager: OptimizedSQLiteManager, rate_limiter: RateLimitedScraper):
        self.db_manager = db_manager
        self.rate_limiter = rate_limiter
        self.results_queue = asyncio.Queue(maxsize=1000)

    async def scrape_product_urls(self, urls: List[str]) -> None:
        """Async scraping pipeline with proper coordination"""

        async with OptimizedHTTPClient() as client:
            # Create producer tasks for fetching
            producer_tasks = [
                self._fetch_and_parse(url, client)
                for url in urls
            ]

            # Create consumer task for database operations
            consumer_task = asyncio.create_task(self._consume_results())

            # Wait for all producers to complete
            await asyncio.gather(*producer_tasks, return_exceptions=True)

            # Signal consumer to finish
            await self.results_queue.put(None)
            await consumer_task

    async def _fetch_and_parse(self, url: str, client: OptimizedHTTPClient):
        """Fetch URL and parse products"""
        response = await self.rate_limiter.respectful_request(url, client)

        if response and response.status_code == 200:
            # Parse products from response
            products = list(StreamingHTMLParser.parse_products_selectolax(
                response.text, '.product-item'
            ))

            # Add to processing queue
            for product in products:
                await self.results_queue.put(product)

    async def _consume_results(self):
        """Consumer task for database operations"""
        batch = []
        batch_size = 100

        while True:
            try:
                # Get item with timeout
                item = await asyncio.wait_for(self.results_queue.get(), timeout=5.0)

                if item is None:  # Shutdown signal
                    break

                batch.append(ProductData(**item))

                # Process batch when full
                if len(batch) >= batch_size:
                    await self._process_batch(batch)
                    batch = []

            except asyncio.TimeoutError:
                # Process remaining items on timeout
                if batch:
                    await self._process_batch(batch)
                    batch = []

    async def _process_batch(self, products: List[ProductData]):
        """Process a batch of products"""
        bulk_ops = BulkDatabaseOperations(self.db_manager)
        await bulk_ops.bulk_upsert_products(products)
```

### 5. Caching Strategies

**Implement intelligent response caching:**
```python
# Install caching libraries
uv add redis aioredis diskcache requests-cache

import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Union
import aioredis
from diskcache import Cache

class IntelligentCache:
    def __init__(self,
                 redis_url: str = "redis://localhost:6379",
                 disk_cache_dir: str = "./cache",
                 default_ttl: int = 3600):

        self.redis_url = redis_url
        self.disk_cache = Cache(disk_cache_dir, size_limit=1024*1024*1024)  # 1GB limit
        self.default_ttl = default_ttl
        self.redis = None

    async def initialize(self):
        """Initialize Redis connection"""
        try:
            self.redis = await aioredis.from_url(self.redis_url)
            await self.redis.ping()
            print("Redis cache initialized")
        except Exception as e:
            print(f"Redis unavailable, using disk cache only: {e}")
            self.redis = None

    def _get_cache_key(self, url: str, params: Dict = None) -> str:
        """Generate consistent cache key"""
        cache_data = f"{url}:{json.dumps(params or {}, sort_keys=True)}"
        return hashlib.md5(cache_data.encode()).hexdigest()

    async def get_cached_response(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Get cached response with fallback to disk cache"""
        cache_key = self._get_cache_key(url, params)

        # Try Redis first (faster)
        if self.redis:
            try:
                cached = await self.redis.get(cache_key)
                if cached:
                    return json.loads(cached)
            except Exception as e:
                print(f"Redis get error: {e}")

        # Fallback to disk cache
        cached = self.disk_cache.get(cache_key)
        if cached and not self._is_expired(cached):
            return cached

        return None

    async def cache_response(self, url: str, response_data: Dict, ttl: int = None, params: Dict = None):
        """Cache response with intelligent TTL"""
        cache_key = self._get_cache_key(url, params)
        ttl = ttl or self._calculate_dynamic_ttl(url, response_data)

        # Add metadata
        cached_data = {
            'data': response_data,
            'cached_at': datetime.now().isoformat(),
            'ttl': ttl,
            'url': url
        }

        # Cache in Redis
        if self.redis:
            try:
                await self.redis.setex(
                    cache_key,
                    ttl,
                    json.dumps(cached_data, default=str)
                )
            except Exception as e:
                print(f"Redis set error: {e}")

        # Also cache on disk as backup
        self.disk_cache.set(cache_key, cached_data, expire=ttl)

    def _calculate_dynamic_ttl(self, url: str, response_data: Dict) -> int:
        """Calculate TTL based on content type and update frequency"""

        # Product listing pages - shorter TTL
        if 'products' in url or 'search' in url:
            return 1800  # 30 minutes

        # Individual product pages - medium TTL
        if 'product' in url:
            return 3600  # 1 hour

        # Static content - longer TTL
        if any(ext in url for ext in ['.css', '.js', '.png', '.jpg']):
            return 86400  # 24 hours

        return self.default_ttl

    def _is_expired(self, cached_data: Dict) -> bool:
        """Check if cached data is expired"""
        try:
            cached_at = datetime.fromisoformat(cached_data['cached_at'])
            ttl = cached_data.get('ttl', self.default_ttl)
            return datetime.now() > cached_at + timedelta(seconds=ttl)
        except:
            return True
```

**Create cache invalidation strategies:**
```python
class CacheInvalidationManager:
    def __init__(self, cache: IntelligentCache):
        self.cache = cache
        self.invalidation_patterns = {
            'price_change': r'.*product.*',
            'inventory_update': r'.*stock.*',
            'new_products': r'.*category.*|.*search.*'
        }

    async def invalidate_pattern(self, pattern: str, reason: str = "manual"):
        """Invalidate cache entries matching pattern"""
        invalidated_count = 0

        if self.cache.redis:
            try:
                # Get all keys matching pattern
                keys = await self.cache.redis.keys(f"*{pattern}*")
                if keys:
                    await self.cache.redis.delete(*keys)
                    invalidated_count += len(keys)
            except Exception as e:
                print(f"Redis invalidation error: {e}")

        # Also clear disk cache
        # Note: diskcache doesn't support pattern deletion easily
        # Consider implementing custom indexing for pattern invalidation

        print(f"Invalidated {invalidated_count} cache entries for pattern '{pattern}' - reason: {reason}")

    async def smart_invalidation(self, event_type: str, affected_urls: List[str] = None):
        """Intelligent cache invalidation based on events"""

        if event_type == 'price_update':
            # Invalidate product and search caches
            await self.invalidate_pattern('product', 'price_update')
            await self.invalidate_pattern('search', 'price_update')

        elif event_type == 'inventory_change':
            # Invalidate specific product caches
            if affected_urls:
                for url in affected_urls:
                    cache_key = self.cache._get_cache_key(url)
                    if self.cache.redis:
                        await self.cache.redis.delete(cache_key)

        elif event_type == 'new_product':
            # Invalidate category and search caches
            await self.invalidate_pattern('category', 'new_product')
            await self.invalidate_pattern('search', 'new_product')
```

### 6. Performance Monitoring

**Set up performance profiling and benchmarking:**
```python
# Install monitoring tools
uv add prometheus-client grafana-api py-spy line-profiler

import time
import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Any
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import cProfile
import pstats
from contextlib import contextmanager

@dataclass
class PerformanceMetrics:
    """Performance metrics container"""
    request_count: int = 0
    total_response_time: float = 0.0
    error_count: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    products_processed: int = 0
    memory_usage_mb: float = 0.0
    start_time: float = field(default_factory=time.time)

class PerformanceMonitor:
    def __init__(self, prometheus_port: int = 8000):
        self.metrics = PerformanceMetrics()
        self.prometheus_port = prometheus_port

        # Prometheus metrics
        self.request_counter = Counter('scraper_requests_total', 'Total requests made')
        self.response_time_histogram = Histogram('scraper_response_time_seconds', 'Response times')
        self.error_counter = Counter('scraper_errors_total', 'Total errors')
        self.cache_hit_ratio = Gauge('scraper_cache_hit_ratio', 'Cache hit ratio')
        self.products_per_second = Gauge('scraper_products_per_second', 'Products processed per second')
        self.memory_usage = Gauge('scraper_memory_usage_mb', 'Memory usage in MB')

        # Start Prometheus server
        start_http_server(prometheus_port)
        print(f"Prometheus metrics available at http://localhost:{prometheus_port}")

    @contextmanager
    def time_operation(self, operation_name: str):
        """Context manager for timing operations"""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            self.record_response_time(duration)
            print(f"{operation_name} took {duration:.2f} seconds")

    def record_request(self):
        """Record a request"""
        self.metrics.request_count += 1
        self.request_counter.inc()

    def record_response_time(self, duration: float):
        """Record response time"""
        self.metrics.total_response_time += duration
        self.response_time_histogram.observe(duration)

    def record_error(self):
        """Record an error"""
        self.metrics.error_count += 1
        self.error_counter.inc()

    def record_cache_hit(self):
        """Record cache hit"""
        self.metrics.cache_hits += 1
        self._update_cache_ratio()

    def record_cache_miss(self):
        """Record cache miss"""
        self.metrics.cache_misses += 1
        self._update_cache_ratio()

    def _update_cache_ratio(self):
        """Update cache hit ratio"""
        total = self.metrics.cache_hits + self.metrics.cache_misses
        if total > 0:
            ratio = self.metrics.cache_hits / total
            self.cache_hit_ratio.set(ratio)

    def record_products_processed(self, count: int):
        """Record products processed"""
        self.metrics.products_processed += count
        elapsed = time.time() - self.metrics.start_time
        if elapsed > 0:
            rate = self.metrics.products_processed / elapsed
            self.products_per_second.set(rate)

    def update_memory_usage(self, memory_mb: float):
        """Update memory usage"""
        self.metrics.memory_usage_mb = memory_mb
        self.memory_usage.set(memory_mb)

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        elapsed = time.time() - self.metrics.start_time
        avg_response_time = (self.metrics.total_response_time / self.metrics.request_count
                           if self.metrics.request_count > 0 else 0)

        return {
            'elapsed_time': elapsed,
            'total_requests': self.metrics.request_count,
            'requests_per_second': self.metrics.request_count / elapsed if elapsed > 0 else 0,
            'average_response_time': avg_response_time,
            'error_rate': self.metrics.error_count / self.metrics.request_count if self.metrics.request_count > 0 else 0,
            'cache_hit_ratio': self.metrics.cache_hits / (self.metrics.cache_hits + self.metrics.cache_misses) if (self.metrics.cache_hits + self.metrics.cache_misses) > 0 else 0,
            'products_processed': self.metrics.products_processed,
            'products_per_second': self.metrics.products_processed / elapsed if elapsed > 0 else 0,
            'memory_usage_mb': self.metrics.memory_usage_mb
        }

class ProfiledScraper:
    """Scraper with built-in profiling"""

    def __init__(self, performance_monitor: PerformanceMonitor):
        self.monitor = performance_monitor
        self.profiler = None

    @contextmanager
    def profile_execution(self, profile_file: str = "scraper_profile.prof"):
        """Context manager for code profiling"""
        self.profiler = cProfile.Profile()
        self.profiler.enable()

        try:
            yield
        finally:
            self.profiler.disable()
            self.profiler.dump_stats(profile_file)

            # Print top time consumers
            stats = pstats.Stats(profile_file)
            stats.sort_stats('cumulative')
            print("\nTop 10 time consuming functions:")
            stats.print_stats(10)

    async def profile_async_scraping(self, urls: List[str]):
        """Profile async scraping operations"""
        with self.profile_execution("async_scraper_profile.prof"):
            # Your async scraping code here
            pipeline = AsyncScrapingPipeline(db_manager, rate_limiter)
            await pipeline.scrape_product_urls(urls)
```

### 7. Resource Optimization

**Optimize CPU usage for HTML parsing:**
```python
# Install performance parsing libraries
uv add selectolax lxml[html_clean] html5lib

import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
import psutil

class OptimizedHTMLProcessor:
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or min(32, (psutil.cpu_count() or 1) + 4)
        self.process_pool = ProcessPoolExecutor(max_workers=self.max_workers)
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers * 2)

    def parse_html_batch_parallel(self, html_documents: List[str], selector: str) -> List[List[Dict]]:
        """Parse HTML documents in parallel processes"""

        # Create partial function with selector
        parser_func = partial(self._parse_single_document, selector=selector)

        # Process in parallel
        with self.process_pool:
            results = list(self.process_pool.map(parser_func, html_documents))

        return results

    @staticmethod
    def _parse_single_document(html_content: str, selector: str) -> List[Dict[str, Any]]:
        """Parse single HTML document (for multiprocessing)"""
        from selectolax.parser import HTMLParser

        parser = HTMLParser(html_content)
        products = []

        for element in parser.css(selector):
            product = {
                'name': element.css_first('.product-name')?.text() or '',
                'price': element.css_first('.price')?.text() or '0',
                'url': element.css_first('a')?.attributes.get('href') or '',
                'id': element.attributes.get('data-id') or ''
            }
            products.append(product)

        return products

    async def parse_html_async_optimized(self, html_documents: List[str], selector: str) -> List[List[Dict]]:
        """Async HTML parsing with thread pool for CPU-bound tasks"""
        loop = asyncio.get_event_loop()

        # Use thread pool for CPU-bound parsing
        tasks = [
            loop.run_in_executor(
                self.thread_pool,
                partial(self._parse_single_document, selector=selector),
                html_doc
            )
            for html_doc in html_documents
        ]

        return await asyncio.gather(*tasks)

class ResourceMonitor:
    """Monitor and optimize resource usage"""

    def __init__(self):
        self.cpu_threshold = 80.0  # CPU usage threshold
        self.memory_threshold = 1024  # Memory threshold in MB

    def get_resource_usage(self) -> Dict[str, float]:
        """Get current resource usage"""
        process = psutil.Process()

        return {
            'cpu_percent': process.cpu_percent(),
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'open_files': len(process.open_files()),
            'threads': process.num_threads(),
            'system_cpu': psutil.cpu_percent(),
            'system_memory': psutil.virtual_memory().percent
        }

    def should_throttle(self) -> bool:
        """Check if scraper should throttle due to resource usage"""
        usage = self.get_resource_usage()

        return (usage['cpu_percent'] > self.cpu_threshold or
                usage['memory_mb'] > self.memory_threshold or
                usage['system_cpu'] > 90.0)

    async def adaptive_delay(self):
        """Implement adaptive delays based on resource usage"""
        if self.should_throttle():
            usage = self.get_resource_usage()
            delay = min(5.0, max(0.1, usage['cpu_percent'] / 20.0))
            print(f"High resource usage detected, sleeping for {delay:.1f}s")
            await asyncio.sleep(delay)
```

### 8. Scalability Planning

**Design horizontal scaling strategies:**
```python
# Install distributed computing tools
uv add celery[redis] dask[distributed] ray

import os
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from celery import Celery
import redis

@dataclass
class ScrapingTask:
    """Serializable scraping task"""
    url: str
    task_id: str
    priority: int = 1
    retry_count: int = 0
    metadata: Dict[str, Any] = None

class DistributedScrapingCoordinator:
    """Coordinate scraping across multiple workers"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url)
        self.task_queue = "scraping_tasks"
        self.result_queue = "scraping_results"
        self.worker_status = "worker_status"

        # Initialize Celery for distributed task processing
        self.celery_app = Celery('scraper', broker=redis_url, backend=redis_url)
        self._configure_celery()

    def _configure_celery(self):
        """Configure Celery for scraping tasks"""
        self.celery_app.conf.update(
            task_serializer='json',
            accept_content=['json'],
            result_serializer='json',
            timezone='UTC',
            enable_utc=True,
            task_routes={
                'scraper.scrape_url': {'queue': 'scraping'},
                'scraper.parse_html': {'queue': 'parsing'},
                'scraper.store_results': {'queue': 'storage'}
            },
            worker_prefetch_multiplier=1,
            task_acks_late=True,
            worker_max_tasks_per_child=1000,
        )

    def distribute_scraping_tasks(self, urls: List[str], batch_size: int = 100) -> List[str]:
        """Distribute scraping tasks across workers"""
        task_ids = []

        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]

            # Create task
            task = ScrapingTask(
                url=json.dumps(batch),  # Serialize batch
                task_id=f"batch_{i // batch_size}",
                priority=1,
                metadata={'batch_size': len(batch), 'batch_index': i // batch_size}
            )

            # Queue task
            self.redis_client.lpush(self.task_queue, json.dumps(task.__dict__))
            task_ids.append(task.task_id)

        return task_ids

    def get_worker_status(self) -> Dict[str, Any]:
        """Get status of all workers"""
        status_data = self.redis_client.get(self.worker_status)
        if status_data:
            return json.loads(status_data)
        return {}

    def monitor_task_progress(self, task_ids: List[str]) -> Dict[str, str]:
        """Monitor progress of distributed tasks"""
        progress = {}

        for task_id in task_ids:
            # Check if task is completed
            result = self.redis_client.get(f"result_{task_id}")
            if result:
                progress[task_id] = "completed"
            else:
                # Check if task is still in queue
                queue_length = self.redis_client.llen(self.task_queue)
                progress[task_id] = f"queued ({queue_length} tasks remaining)"

        return progress

# Celery tasks for distributed processing
@dataclass
class CeleryScrapingTasks:
    """Celery tasks for distributed scraping"""

    @staticmethod
    @celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
    def scrape_url_batch(self, url_batch: str) -> Dict[str, Any]:
        """Celery task for scraping URL batch"""
        try:
            urls = json.loads(url_batch)
            # Your scraping logic here
            results = []

            for url in urls:
                # Implement actual scraping
                result = {'url': url, 'status': 'success', 'products': []}
                results.append(result)

            return {'status': 'success', 'results': results, 'count': len(results)}

        except Exception as exc:
            # Retry with exponential backoff
            raise self.retry(countdown=60 * (2 ** self.request.retries))

class LoadBalancer:
    """Load balancer for scraping workers"""

    def __init__(self, worker_endpoints: List[str]):
        self.worker_endpoints = worker_endpoints
        self.current_worker = 0
        self.worker_loads = {endpoint: 0 for endpoint in worker_endpoints}

    def get_next_worker(self) -> str:
        """Get next available worker using round-robin with load consideration"""
        # Find worker with lowest load
        min_load_worker = min(self.worker_loads, key=self.worker_loads.get)

        # Increment load for selected worker
        self.worker_loads[min_load_worker] += 1

        return min_load_worker

    def report_task_completed(self, worker_endpoint: str):
        """Report task completion to update load"""
        if worker_endpoint in self.worker_loads:
            self.worker_loads[worker_endpoint] = max(0, self.worker_loads[worker_endpoint] - 1)

    def get_load_distribution(self) -> Dict[str, int]:
        """Get current load distribution across workers"""
        return self.worker_loads.copy()
```

### 9. Complete Integration Example

**Integrate all optimizations into a complete scraper:**
```python
import asyncio
import time
from typing import List, Dict, Any, Optional

class OptimizedWebScraper:
    """Complete optimized web scraper with all performance enhancements"""

    def __init__(self,
                 db_path: str = "./products.db",
                 redis_url: str = "redis://localhost:6379",
                 max_concurrent: int = 10,
                 requests_per_second: float = 2.0):

        # Initialize components
        self.db_manager = OptimizedSQLiteManager(db_path)
        self.cache = IntelligentCache(redis_url)
        self.rate_limiter = RateLimitedScraper(
            requests_per_second=requests_per_second,
            max_concurrent=max_concurrent
        )
        self.performance_monitor = PerformanceMonitor()
        self.memory_processor = MemoryEfficientProcessor()
        self.resource_monitor = ResourceMonitor()
        self.html_processor = OptimizedHTMLProcessor()

        # Scalability components
        self.coordinator = DistributedScrapingCoordinator(redis_url)
        self.cache_invalidator = CacheInvalidationManager(self.cache)

    async def initialize(self):
        """Initialize all components"""
        await self.db_manager.initialize_db()
        await self.cache.initialize()
        print("Optimized scraper initialized successfully")

    async def scrape_products_optimized(self,
                                      urls: List[str],
                                      use_cache: bool = True,
                                      enable_profiling: bool = False) -> Dict[str, Any]:
        """Main optimized scraping method"""

        start_time = time.time()
        total_products = 0

        try:
            async with OptimizedHTTPClient() as client:
                # Create processing pipeline
                pipeline = AsyncScrapingPipeline(self.db_manager, self.rate_limiter)

                if enable_profiling:
                    profiled_scraper = ProfiledScraper(self.performance_monitor)
                    with profiled_scraper.profile_execution():
                        await pipeline.scrape_product_urls(urls)
                else:
                    await pipeline.scrape_product_urls(urls)

                # Update performance metrics
                elapsed = time.time() - start_time
                self.performance_monitor.record_products_processed(total_products)

                # Generate performance report
                performance_report = self.performance_monitor.get_performance_report()

                return {
                    'status': 'success',
                    'products_processed': total_products,
                    'elapsed_time': elapsed,
                    'performance_metrics': performance_report,
                    'resource_usage': self.resource_monitor.get_resource_usage()
                }

        except Exception as e:
            self.performance_monitor.record_error()
            return {
                'status': 'error',
                'error': str(e),
                'elapsed_time': time.time() - start_time
            }

    async def run_distributed_scraping(self, urls: List[str], batch_size: int = 100) -> str:
        """Run distributed scraping across multiple workers"""

        # Distribute tasks
        task_ids = self.coordinator.distribute_scraping_tasks(urls, batch_size)

        print(f"Distributed {len(urls)} URLs across {len(task_ids)} batches")
        print(f"Task IDs: {task_ids}")

        # Monitor progress
        while True:
            progress = self.coordinator.monitor_task_progress(task_ids)
            completed = sum(1 for status in progress.values() if status == "completed")

            print(f"Progress: {completed}/{len(task_ids)} batches completed")

            if completed == len(task_ids):
                break

            await asyncio.sleep(10)  # Check every 10 seconds

        return "Distributed scraping completed successfully"

    async def cleanup(self):
        """Cleanup resources"""
        if hasattr(self.cache, 'redis') and self.cache.redis:
            await self.cache.redis.close()

        # Close other resources as needed
        print("Scraper cleanup completed")

# Usage example
async def main():
    """Example usage of optimized scraper"""

    scraper = OptimizedWebScraper(
        db_path="./optimized_products.db",
        max_concurrent=15,
        requests_per_second=3.0
    )

    await scraper.initialize()

    # Example URLs (replace with actual URLs)
    urls = [
        "https://example-store.com/products?page=1",
        "https://example-store.com/products?page=2",
        # Add more URLs...
    ]

    try:
        # Run optimized scraping
        result = await scraper.scrape_products_optimized(
            urls=urls,
            use_cache=True,
            enable_profiling=True
        )

        print("Scraping Results:")
        print(json.dumps(result, indent=2))

        # Optional: Run distributed scraping for large scale
        # await scraper.run_distributed_scraping(urls, batch_size=50)

    finally:
        await scraper.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

### 10. Performance Testing and Validation

**Create performance benchmarks:**
```python
# Install benchmarking tools
uv add pytest-benchmark pytest-asyncio

import pytest
import asyncio
import time
from typing import List

class PerformanceBenchmarks:
    """Performance benchmarks for scraper components"""

    @pytest.mark.asyncio
    @pytest.mark.benchmark(group="http_clients")
    async def test_http_client_performance(self, benchmark):
        """Benchmark HTTP client performance"""

        async def make_requests():
            async with OptimizedHTTPClient() as client:
                tasks = [
                    client.client.get("https://httpbin.org/delay/1")
                    for _ in range(10)
                ]
                await asyncio.gather(*tasks)

        await benchmark(make_requests)

    @pytest.mark.benchmark(group="html_parsing")
    def test_html_parsing_performance(self, benchmark):
        """Benchmark HTML parsing performance"""

        # Create test HTML
        test_html = """
        <div class="products">
        """ + """
            <div class="product-item">
                <span class="product-name">Test Product</span>
                <span class="price">$19.99</span>
                <a href="/product/123">View</a>
            </div>
        """ * 1000 + """
        </div>
        """

        def parse_html():
            return list(StreamingHTMLParser.parse_products_selectolax(
                test_html, '.product-item'
            ))

        result = benchmark(parse_html)
        assert len(result) == 1000

    @pytest.mark.asyncio
    @pytest.mark.benchmark(group="database")
    async def test_database_bulk_insert_performance(self, benchmark):
        """Benchmark database bulk insert performance"""

        # Create test data
        test_products = [
            ProductData(
                id=f"test_{i}",
                name=f"Test Product {i}",
                price=float(i * 10),
                url=f"https://example.com/product/{i}",
                last_updated=str(int(time.time()))
            )
            for i in range(1000)
        ]

        db_manager = OptimizedSQLiteManager(":memory:")
        await db_manager.initialize_db()
        bulk_ops = BulkDatabaseOperations(db_manager)

        async def bulk_insert():
            await bulk_ops.bulk_upsert_products(test_products)

        await benchmark(bulk_insert)

# Run benchmarks
# pytest performance_benchmarks.py --benchmark-only --benchmark-sort=mean
```

### 11. Monitoring Dashboard Setup

**Create monitoring dashboard configuration:**
```python
# Create monitoring configuration
monitoring_config = {
    'prometheus': {
        'port': 8000,
        'metrics_path': '/metrics'
    },
    'grafana': {
        'dashboard_config': {
            'title': 'Web Scraper Performance',
            'panels': [
                {
                    'title': 'Requests per Second',
                    'type': 'graph',
                    'targets': ['rate(scraper_requests_total[1m])']
                },
                {
                    'title': 'Response Times',
                    'type': 'graph',
                    'targets': ['scraper_response_time_seconds']
                },
                {
                    'title': 'Cache Hit Ratio',
                    'type': 'singlestat',
                    'targets': ['scraper_cache_hit_ratio']
                },
                {
                    'title': 'Memory Usage',
                    'type': 'graph',
                    'targets': ['scraper_memory_usage_mb']
                }
            ]
        }
    },
    'alerts': {
        'high_error_rate': {
            'condition': 'scraper_errors_total > 0.1',
            'duration': '5m'
        },
        'high_memory_usage': {
            'condition': 'scraper_memory_usage_mb > 1000',
            'duration': '2m'
        }
    }
}

# Save configuration
with open('monitoring_config.json', 'w') as f:
    json.dump(monitoring_config, f, indent=2)

print("Monitoring configuration saved to monitoring_config.json")
```

This comprehensive optimization ensures your scraper operates efficiently at scale while maintaining ethical scraping practices and robust error handling.

## Next Steps

1. **Implement optimizations incrementally** - Start with request optimization and add other components
2. **Benchmark before and after** - Measure performance improvements at each step
3. **Monitor in production** - Set up monitoring dashboards and alerts
4. **Tune parameters** - Adjust concurrency limits and cache settings based on target sites
5. **Scale gradually** - Test distributed scraping on small batches before full deployment
6. **Regular maintenance** - Update dependencies and optimize database indexes periodically

$ARGUMENTS
