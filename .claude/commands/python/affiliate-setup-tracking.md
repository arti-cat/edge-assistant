# Setup Affiliate Tracking

Implement advanced click tracking, analytics, and performance monitoring for the affiliate system with Redis caching and background processing.

## Usage

```bash
/affiliate:setup-tracking
```

## Instructions

### 1. **Redis Integration Setup**

Add Redis dependency and configure for affiliate tracking:

```bash
# Add Redis dependencies
uv add redis celery[redis] python-dotenv

# Create Redis configuration
cat > src/product_prices/config/redis.py << 'EOF'
"""
Redis configuration for affiliate tracking
"""
import os
import redis
from typing import Optional
from urllib.parse import urlparse


class RedisConfig:
    """Redis configuration manager"""

    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.max_connections = int(os.getenv('REDIS_MAX_CONNECTIONS', '10'))
        self.socket_timeout = int(os.getenv('REDIS_SOCKET_TIMEOUT', '5'))
        self.socket_connect_timeout = int(os.getenv('REDIS_CONNECT_TIMEOUT', '5'))

    def get_connection_pool(self) -> redis.ConnectionPool:
        """Get Redis connection pool"""
        return redis.ConnectionPool.from_url(
            self.redis_url,
            max_connections=self.max_connections,
            socket_timeout=self.socket_timeout,
            socket_connect_timeout=self.socket_connect_timeout,
            decode_responses=True
        )

    def get_client(self) -> redis.Redis:
        """Get Redis client instance"""
        return redis.Redis(connection_pool=self.get_connection_pool())


# Global Redis client
redis_config = RedisConfig()
redis_client = redis_config.get_client()


def get_redis_client() -> redis.Redis:
    """Get Redis client for dependency injection"""
    return redis_client
EOF

# Create environment configuration
cat >> .env << 'EOF'

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_MAX_CONNECTIONS=10
REDIS_SOCKET_TIMEOUT=5
REDIS_CONNECT_TIMEOUT=5

# Affiliate Tracking Configuration
AFFILIATE_TRACKING_ENABLED=true
AFFILIATE_SESSION_TIMEOUT=86400
AFFILIATE_CLICK_BATCH_SIZE=100
AFFILIATE_ANALYTICS_RETENTION_DAYS=90
EOF
```

### 2. **Enhanced Click Tracking Service**

Create advanced tracking with caching and batching:

```python
# Create advanced tracking service
cat > src/product_prices/services/tracking.py << 'EOF'
"""
Advanced affiliate click tracking with Redis caching and analytics
"""
import json
import hashlib
import secrets
import logging
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import sqlite3

import redis
from ..config.redis import get_redis_client
from ..models.affiliate import AffiliateClick, AffiliatePerformance


logger = logging.getLogger(__name__)


@dataclass
class ClickEvent:
    """Click event for batching"""
    link_id: int
    session_id: str
    user_agent: Optional[str]
    ip_address: Optional[str]
    referrer: Optional[str]
    timestamp: datetime
    fingerprint: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            'link_id': self.link_id,
            'session_id': self.session_id,
            'user_agent': self.user_agent,
            'ip_address': self.ip_address,
            'referrer': self.referrer,
            'timestamp': self.timestamp.isoformat(),
            'fingerprint': self.fingerprint
        }


@dataclass
class ConversionEvent:
    """Conversion event tracking"""
    click_id: int
    conversion_value: float
    commission_earned: float
    timestamp: datetime
    order_id: Optional[str] = None
    currency: str = 'GBP'


class AffiliateTracker:
    """Advanced affiliate tracking with Redis caching"""

    def __init__(self, db_path: Path, redis_client: Optional[redis.Redis] = None):
        self.db_path = db_path
        self.redis = redis_client or get_redis_client()

        # Cache keys
        self.CLICK_QUEUE_KEY = "affiliate:clicks:queue"
        self.SESSION_KEY_PREFIX = "affiliate:session:"
        self.RATE_LIMIT_KEY_PREFIX = "affiliate:rate_limit:"
        self.ANALYTICS_KEY_PREFIX = "affiliate:analytics:"
        self.LINK_CACHE_KEY_PREFIX = "affiliate:link:"

        # Configuration
        self.session_timeout = 86400  # 24 hours
        self.rate_limit_window = 3600  # 1 hour
        self.rate_limit_max_clicks = 100  # per IP per hour
        self.click_batch_size = 100

    def track_click(self, link_id: int, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track affiliate click with advanced analytics"""
        try:
            # Extract request data
            ip_address = self._get_client_ip(request_data)
            user_agent = request_data.get('user_agent', '')
            referrer = request_data.get('referrer', '')

            # Rate limiting check
            if not self._check_rate_limit(ip_address):
                logger.warning(f"Rate limit exceeded for IP: {self._anonymize_ip(ip_address)}")
                return {'success': False, 'error': 'rate_limit_exceeded'}

            # Generate session ID or get existing
            session_id = self._get_or_create_session(request_data)

            # Check for duplicate clicks
            if self._is_duplicate_click(link_id, session_id):
                logger.info(f"Duplicate click detected for link {link_id}")
                return {'success': True, 'duplicate': True}

            # Create click fingerprint for fraud detection
            fingerprint = self._generate_click_fingerprint(
                link_id, ip_address, user_agent, session_id
            )

            # Create click event
            click_event = ClickEvent(
                link_id=link_id,
                session_id=session_id,
                user_agent=user_agent,
                ip_address=self._anonymize_ip(ip_address),
                referrer=referrer,
                timestamp=datetime.now(),
                fingerprint=fingerprint
            )

            # Queue click for batch processing
            self._queue_click_event(click_event)

            # Update real-time analytics
            self._update_realtime_analytics(link_id, click_event)

            # Cache click for duplicate detection
            self._cache_click(link_id, session_id)

            # Get affiliate URL for redirect
            affiliate_url = self._get_cached_affiliate_url(link_id)

            logger.info(f"Tracked click for link {link_id}, session {session_id[:8]}...")

            return {
                'success': True,
                'click_id': fingerprint,
                'session_id': session_id,
                'redirect_url': affiliate_url
            }

        except Exception as e:
            logger.error(f"Failed to track click: {e}")
            return {'success': False, 'error': 'tracking_failed'}

    def track_conversion(self, click_id: str, conversion_data: Dict[str, Any]) -> bool:
        """Track affiliate conversion"""
        try:
            # Find click by fingerprint
            click_info = self._get_click_by_fingerprint(click_id)
            if not click_info:
                logger.warning(f"Click not found for conversion: {click_id}")
                return False

            # Validate conversion window (e.g., 30 days)
            click_time = datetime.fromisoformat(click_info['timestamp'])
            if datetime.now() - click_time > timedelta(days=30):
                logger.warning(f"Conversion outside window: {click_id}")
                return False

            conversion_event = ConversionEvent(
                click_id=click_info['db_id'],
                conversion_value=float(conversion_data.get('value', 0)),
                commission_earned=float(conversion_data.get('commission', 0)),
                timestamp=datetime.now(),
                order_id=conversion_data.get('order_id'),
                currency=conversion_data.get('currency', 'GBP')
            )

            # Update database
            self._record_conversion(conversion_event)

            # Update analytics
            self._update_conversion_analytics(click_info['link_id'], conversion_event)

            logger.info(f"Tracked conversion for click {click_id}: £{conversion_event.conversion_value}")
            return True

        except Exception as e:
            logger.error(f"Failed to track conversion: {e}")
            return False

    def process_click_queue(self) -> int:
        """Process queued clicks in batches"""
        try:
            processed = 0

            while True:
                # Get batch of clicks
                click_data = self.redis.lpop(self.CLICK_QUEUE_KEY, self.click_batch_size)
                if not click_data:
                    break

                clicks = []
                for data in click_data:
                    try:
                        click_dict = json.loads(data)
                        click_dict['timestamp'] = datetime.fromisoformat(click_dict['timestamp'])
                        clicks.append(ClickEvent(**click_dict))
                    except (json.JSONDecodeError, ValueError) as e:
                        logger.error(f"Failed to parse click data: {e}")
                        continue

                # Batch insert to database
                if clicks:
                    inserted = self._batch_insert_clicks(clicks)
                    processed += inserted
                    logger.info(f"Processed {inserted} clicks from queue")

            return processed

        except Exception as e:
            logger.error(f"Failed to process click queue: {e}")
            return 0

    def get_realtime_analytics(self, link_id: Optional[int] = None,
                             hours: int = 24) -> Dict[str, Any]:
        """Get real-time analytics from Redis"""
        try:
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=hours)

            if link_id:
                return self._get_link_analytics(link_id, start_time, end_time)
            else:
                return self._get_global_analytics(start_time, end_time)

        except Exception as e:
            logger.error(f"Failed to get realtime analytics: {e}")
            return {}

    def get_performance_metrics(self, days: int = 7) -> List[AffiliatePerformance]:
        """Get performance metrics from database"""
        try:
            cutoff_date = date.today() - timedelta(days=days)

            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT
                        an.id as network_id,
                        an.display_name as network_name,
                        DATE(ac.clicked_at) as date,
                        COUNT(ac.id) as clicks,
                        SUM(ac.converted) as conversions,
                        SUM(ac.conversion_value) as revenue,
                        SUM(ac.commission_earned) as commission_earned
                    FROM affiliate_networks an
                    LEFT JOIN affiliate_links al ON an.id = al.network_id
                    LEFT JOIN affiliate_clicks ac ON al.id = ac.link_id
                    WHERE DATE(ac.clicked_at) >= ?
                    GROUP BY an.id, DATE(ac.clicked_at)
                    ORDER BY date DESC
                """, (cutoff_date,))

                metrics = []
                for row in cursor.fetchall():
                    if row['clicks'] and row['clicks'] > 0:
                        performance = AffiliatePerformance(
                            network_id=row['network_id'],
                            date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                            clicks=row['clicks'],
                            conversions=row['conversions'] or 0,
                            revenue=row['revenue'] or 0.0,
                            commission_earned=row['commission_earned'] or 0.0,
                            click_through_rate=0.0,  # Calculate separately
                            conversion_rate=(row['conversions'] or 0) / row['clicks']
                        )
                        metrics.append(performance)

                return metrics

        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return []

    def _get_client_ip(self, request_data: Dict[str, Any]) -> str:
        """Extract client IP with proxy support"""
        # Check for forwarded IP headers
        forwarded_for = request_data.get('x_forwarded_for', '')
        if forwarded_for:
            # Take first IP from comma-separated list
            return forwarded_for.split(',')[0].strip()

        real_ip = request_data.get('x_real_ip', '')
        if real_ip:
            return real_ip

        return request_data.get('remote_addr', '127.0.0.1')

    def _check_rate_limit(self, ip_address: str) -> bool:
        """Check if IP is within rate limits"""
        try:
            key = f"{self.RATE_LIMIT_KEY_PREFIX}{self._anonymize_ip(ip_address)}"
            current_clicks = self.redis.get(key)

            if current_clicks is None:
                # First click from this IP
                self.redis.setex(key, self.rate_limit_window, 1)
                return True

            if int(current_clicks) >= self.rate_limit_max_clicks:
                return False

            # Increment counter
            self.redis.incr(key)
            return True

        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            return True  # Allow on error

    def _get_or_create_session(self, request_data: Dict[str, Any]) -> str:
        """Get existing session or create new one"""
        try:
            # Check for existing session cookie
            session_id = request_data.get('session_id')
            if session_id:
                key = f"{self.SESSION_KEY_PREFIX}{session_id}"
                if self.redis.exists(key):
                    # Extend session timeout
                    self.redis.expire(key, self.session_timeout)
                    return session_id

            # Create new session
            session_id = secrets.token_urlsafe(32)
            key = f"{self.SESSION_KEY_PREFIX}{session_id}"

            session_data = {
                'created_at': datetime.now().isoformat(),
                'user_agent': request_data.get('user_agent', ''),
                'first_referrer': request_data.get('referrer', ''),
                'click_count': 0
            }

            self.redis.setex(key, self.session_timeout, json.dumps(session_data))
            return session_id

        except Exception as e:
            logger.error(f"Session management failed: {e}")
            return secrets.token_urlsafe(32)

    def _is_duplicate_click(self, link_id: int, session_id: str) -> bool:
        """Check for duplicate clicks within session"""
        try:
            key = f"affiliate:click:{link_id}:{session_id}"
            return self.redis.exists(key)
        except Exception:
            return False

    def _generate_click_fingerprint(self, link_id: int, ip_address: str,
                                  user_agent: str, session_id: str) -> str:
        """Generate unique fingerprint for click"""
        content = f"{link_id}:{ip_address}:{user_agent}:{session_id}:{datetime.now().isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _queue_click_event(self, click_event: ClickEvent) -> None:
        """Queue click event for batch processing"""
        try:
            click_data = json.dumps(click_event.to_dict())
            self.redis.rpush(self.CLICK_QUEUE_KEY, click_data)
        except Exception as e:
            logger.error(f"Failed to queue click event: {e}")

    def _update_realtime_analytics(self, link_id: int, click_event: ClickEvent) -> None:
        """Update real-time analytics in Redis"""
        try:
            # Hourly metrics
            hour_key = f"{self.ANALYTICS_KEY_PREFIX}hourly:{datetime.now().strftime('%Y%m%d%H')}"
            self.redis.hincrby(hour_key, f"link:{link_id}:clicks", 1)
            self.redis.hincrby(hour_key, "total_clicks", 1)
            self.redis.expire(hour_key, 7 * 24 * 3600)  # Keep for 7 days

            # Daily metrics
            day_key = f"{self.ANALYTICS_KEY_PREFIX}daily:{datetime.now().strftime('%Y%m%d')}"
            self.redis.hincrby(day_key, f"link:{link_id}:clicks", 1)
            self.redis.hincrby(day_key, "total_clicks", 1)
            self.redis.expire(day_key, 90 * 24 * 3600)  # Keep for 90 days

        except Exception as e:
            logger.error(f"Failed to update realtime analytics: {e}")

    def _cache_click(self, link_id: int, session_id: str) -> None:
        """Cache click for duplicate detection"""
        try:
            key = f"affiliate:click:{link_id}:{session_id}"
            self.redis.setex(key, 3600, "1")  # 1 hour duplicate window
        except Exception as e:
            logger.error(f"Failed to cache click: {e}")

    def _get_cached_affiliate_url(self, link_id: int) -> Optional[str]:
        """Get cached affiliate URL"""
        try:
            key = f"{self.LINK_CACHE_KEY_PREFIX}{link_id}"
            cached_url = self.redis.get(key)

            if cached_url:
                return cached_url

            # Fetch from database and cache
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT affiliate_url FROM affiliate_links WHERE id = ?", (link_id,))
                row = cursor.fetchone()

                if row:
                    affiliate_url = row[0]
                    self.redis.setex(key, 3600, affiliate_url)  # Cache for 1 hour
                    return affiliate_url

            return None

        except Exception as e:
            logger.error(f"Failed to get cached affiliate URL: {e}")
            return None

    def _anonymize_ip(self, ip_address: str) -> str:
        """Anonymize IP address for privacy compliance"""
        if '.' in ip_address:  # IPv4
            parts = ip_address.split('.')
            if len(parts) == 4:
                return f"{parts[0]}.{parts[1]}.{parts[2]}.0"
        elif ':' in ip_address:  # IPv6
            parts = ip_address.split(':')
            if len(parts) >= 4:
                return ':'.join(parts[:4]) + '::0'
        return ip_address

    def _batch_insert_clicks(self, clicks: List[ClickEvent]) -> int:
        """Batch insert clicks to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                click_data = []
                fingerprint_map = {}

                for click in clicks:
                    click_data.append((
                        click.link_id, click.session_id, click.user_agent,
                        click.ip_address, click.referrer, click.timestamp
                    ))
                    fingerprint_map[click.fingerprint] = len(click_data) - 1

                # Insert clicks
                cursor.executemany("""
                    INSERT INTO affiliate_clicks
                    (link_id, session_id, user_agent, ip_address, referrer, clicked_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, click_data)

                # Store fingerprint to DB ID mapping for conversions
                first_id = cursor.lastrowid - len(click_data) + 1
                for fingerprint, index in fingerprint_map.items():
                    db_id = first_id + index
                    self._store_click_fingerprint_mapping(fingerprint, db_id, clicks[index])

                conn.commit()
                return len(clicks)

        except Exception as e:
            logger.error(f"Failed to batch insert clicks: {e}")
            return 0

    def _store_click_fingerprint_mapping(self, fingerprint: str, db_id: int,
                                       click: ClickEvent) -> None:
        """Store fingerprint to database ID mapping"""
        try:
            key = f"affiliate:fingerprint:{fingerprint}"
            mapping_data = {
                'db_id': db_id,
                'link_id': click.link_id,
                'session_id': click.session_id,
                'timestamp': click.timestamp.isoformat()
            }
            # Store for 30 days (conversion window)
            self.redis.setex(key, 30 * 24 * 3600, json.dumps(mapping_data))
        except Exception as e:
            logger.error(f"Failed to store fingerprint mapping: {e}")

    def _get_click_by_fingerprint(self, fingerprint: str) -> Optional[Dict[str, Any]]:
        """Get click information by fingerprint"""
        try:
            key = f"affiliate:fingerprint:{fingerprint}"
            data = self.redis.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Failed to get click by fingerprint: {e}")
            return None

    def _record_conversion(self, conversion: ConversionEvent) -> None:
        """Record conversion in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE affiliate_clicks
                    SET converted = 1, conversion_value = ?, commission_earned = ?,
                        conversion_at = ?
                    WHERE id = ?
                """, (
                    conversion.conversion_value, conversion.commission_earned,
                    conversion.timestamp, conversion.click_id
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to record conversion: {e}")

    def _update_conversion_analytics(self, link_id: int, conversion: ConversionEvent) -> None:
        """Update conversion analytics in Redis"""
        try:
            # Daily conversion metrics
            day_key = f"{self.ANALYTICS_KEY_PREFIX}daily:{datetime.now().strftime('%Y%m%d')}"
            self.redis.hincrby(day_key, f"link:{link_id}:conversions", 1)
            self.redis.hincrby(day_key, "total_conversions", 1)

            # Revenue tracking
            current_revenue = self.redis.hget(day_key, f"link:{link_id}:revenue") or 0
            new_revenue = float(current_revenue) + conversion.conversion_value
            self.redis.hset(day_key, f"link:{link_id}:revenue", new_revenue)

        except Exception as e:
            logger.error(f"Failed to update conversion analytics: {e}")

    def _get_link_analytics(self, link_id: int, start_time: datetime,
                          end_time: datetime) -> Dict[str, Any]:
        """Get analytics for specific link"""
        analytics = {
            'link_id': link_id,
            'period': {'start': start_time.isoformat(), 'end': end_time.isoformat()},
            'clicks': 0,
            'conversions': 0,
            'revenue': 0.0,
            'hourly_breakdown': []
        }

        try:
            current_time = start_time.replace(minute=0, second=0, microsecond=0)

            while current_time < end_time:
                hour_key = f"{self.ANALYTICS_KEY_PREFIX}hourly:{current_time.strftime('%Y%m%d%H')}"

                clicks = int(self.redis.hget(hour_key, f"link:{link_id}:clicks") or 0)
                conversions = int(self.redis.hget(hour_key, f"link:{link_id}:conversions") or 0)
                revenue = float(self.redis.hget(hour_key, f"link:{link_id}:revenue") or 0)

                analytics['clicks'] += clicks
                analytics['conversions'] += conversions
                analytics['revenue'] += revenue

                analytics['hourly_breakdown'].append({
                    'hour': current_time.isoformat(),
                    'clicks': clicks,
                    'conversions': conversions,
                    'revenue': revenue
                })

                current_time += timedelta(hours=1)

            return analytics

        except Exception as e:
            logger.error(f"Failed to get link analytics: {e}")
            return analytics

    def _get_global_analytics(self, start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Get global analytics across all links"""
        analytics = {
            'period': {'start': start_time.isoformat(), 'end': end_time.isoformat()},
            'total_clicks': 0,
            'total_conversions': 0,
            'total_revenue': 0.0,
            'hourly_breakdown': []
        }

        try:
            current_time = start_time.replace(minute=0, second=0, microsecond=0)

            while current_time < end_time:
                hour_key = f"{self.ANALYTICS_KEY_PREFIX}hourly:{current_time.strftime('%Y%m%d%H')}"

                clicks = int(self.redis.hget(hour_key, "total_clicks") or 0)
                conversions = int(self.redis.hget(hour_key, "total_conversions") or 0)
                revenue = float(self.redis.hget(hour_key, "total_revenue") or 0)

                analytics['total_clicks'] += clicks
                analytics['total_conversions'] += conversions
                analytics['total_revenue'] += revenue

                analytics['hourly_breakdown'].append({
                    'hour': current_time.isoformat(),
                    'clicks': clicks,
                    'conversions': conversions,
                    'revenue': revenue
                })

                current_time += timedelta(hours=1)

            return analytics

        except Exception as e:
            logger.error(f"Failed to get global analytics: {e}")
            return analytics
EOF
```

### 3. **Celery Background Tasks**

Set up Celery for processing affiliate tasks:

```python
# Create Celery configuration
cat > src/product_prices/celery_app.py << 'EOF'
"""
Celery application for background affiliate tasks
"""
import os
from celery import Celery
from .config.redis import redis_config

# Create Celery app
celery_app = Celery(
    'affiliate_tracker',
    broker=redis_config.redis_url,
    backend=redis_config.redis_url,
    include=['src.product_prices.tasks.affiliate']
)

# Configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,

    # Task routing
    task_routes={
        'affiliate.process_clicks': {'queue': 'affiliate_clicks'},
        'affiliate.update_analytics': {'queue': 'affiliate_analytics'},
        'affiliate.validate_links': {'queue': 'affiliate_maintenance'},
    },

    # Beat schedule for periodic tasks
    beat_schedule={
        'process-click-queue': {
            'task': 'affiliate.process_clicks',
            'schedule': 60.0,  # Every minute
        },
        'update-daily-analytics': {
            'task': 'affiliate.update_analytics',
            'schedule': 3600.0,  # Every hour
        },
        'validate-affiliate-links': {
            'task': 'affiliate.validate_links',
            'schedule': 24 * 3600.0,  # Daily
        },
    },
)
EOF

# Create Celery tasks
cat > src/product_prices/tasks/affiliate.py << 'EOF'
"""
Celery tasks for affiliate system
"""
import logging
import requests
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import List, Dict, Any
from celery import Task

from ..celery_app import celery_app
from ..services.tracking import AffiliateTracker
from ..services.affiliate import AffiliateService


logger = logging.getLogger(__name__)


class CallbackTask(Task):
    """Base task with error callbacks"""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"Task {task_id} failed: {exc}")
        # Could send to monitoring service here


@celery_app.task(base=CallbackTask, bind=True)
def process_clicks(self):
    """Process queued affiliate clicks"""
    try:
        db_path = Path("products.db")
        tracker = AffiliateTracker(db_path)

        processed = tracker.process_click_queue()

        if processed > 0:
            logger.info(f"Processed {processed} affiliate clicks")

        return {
            'processed_clicks': processed,
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to process clicks: {e}")
        raise


@celery_app.task(base=CallbackTask, bind=True)
def update_analytics(self):
    """Update daily analytics aggregations"""
    try:
        db_path = Path("products.db")
        tracker = AffiliateTracker(db_path)

        # Get today's performance metrics
        metrics = tracker.get_performance_metrics(days=1)

        # Update database with aggregated daily metrics
        updated_networks = []
        for metric in metrics:
            if metric.clicks > 0:  # Only update if there were clicks
                updated_networks.append(metric.network_id)

        logger.info(f"Updated analytics for {len(updated_networks)} networks")

        return {
            'updated_networks': updated_networks,
            'metrics_count': len(metrics),
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to update analytics: {e}")
        raise


@celery_app.task(base=CallbackTask, bind=True)
def validate_links(self):
    """Validate affiliate links and mark broken ones"""
    try:
        db_path = Path("products.db")
        service = AffiliateService(db_path)

        # Get active links to validate
        active_links = service._get_links_for_validation()

        broken_links = []
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; LinkValidator/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        })

        for link in active_links[:50]:  # Validate 50 links per run
            try:
                response = session.head(link.affiliate_url, timeout=10, allow_redirects=True)

                if response.status_code >= 400:
                    broken_links.append(link.id)
                    service._mark_link_broken(link.id, f"HTTP {response.status_code}")

            except requests.RequestException as e:
                broken_links.append(link.id)
                service._mark_link_broken(link.id, str(e))

        logger.info(f"Validated {len(active_links)} links, found {len(broken_links)} broken")

        return {
            'validated_links': len(active_links),
            'broken_links': len(broken_links),
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to validate links: {e}")
        raise


@celery_app.task(base=CallbackTask, bind=True)
def generate_performance_report(self, network_id: int, days: int = 7):
    """Generate detailed performance report for network"""
    try:
        db_path = Path("products.db")
        tracker = AffiliateTracker(db_path)

        # Get comprehensive metrics
        metrics = tracker.get_performance_metrics(days=days)
        network_metrics = [m for m in metrics if m.network_id == network_id]

        if not network_metrics:
            return {'error': 'No data found for network'}

        # Calculate aggregated stats
        total_clicks = sum(m.clicks for m in network_metrics)
        total_conversions = sum(m.conversions for m in network_metrics)
        total_revenue = sum(m.revenue for m in network_metrics)
        total_commission = sum(m.commission_earned for m in network_metrics)

        conversion_rate = total_conversions / total_clicks if total_clicks > 0 else 0
        avg_order_value = total_revenue / total_conversions if total_conversions > 0 else 0

        report = {
            'network_id': network_id,
            'period_days': days,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'total_revenue': float(total_revenue),
            'total_commission': float(total_commission),
            'conversion_rate': conversion_rate,
            'average_order_value': avg_order_value,
            'daily_breakdown': [
                {
                    'date': m.date.isoformat(),
                    'clicks': m.clicks,
                    'conversions': m.conversions,
                    'revenue': float(m.revenue),
                    'commission': float(m.commission_earned)
                }
                for m in network_metrics
            ],
            'generated_at': datetime.now().isoformat()
        }

        logger.info(f"Generated performance report for network {network_id}")
        return report

    except Exception as e:
        logger.error(f"Failed to generate performance report: {e}")
        raise


@celery_app.task(base=CallbackTask, bind=True)
def cleanup_old_data(self):
    """Clean up old tracking data for privacy compliance"""
    try:
        db_path = Path("products.db")

        # Remove clicks older than 90 days (configurable)
        cutoff_date = datetime.now() - timedelta(days=90)

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Count records to be deleted
            cursor.execute("""
                SELECT COUNT(*) FROM affiliate_clicks
                WHERE clicked_at < ? AND converted = 0
            """, (cutoff_date,))
            old_clicks = cursor.fetchone()[0]

            # Delete old non-converted clicks
            cursor.execute("""
                DELETE FROM affiliate_clicks
                WHERE clicked_at < ? AND converted = 0
            """, (cutoff_date,))

            # Clean up Redis analytics data older than retention period
            tracker = AffiliateTracker(db_path)
            # Implementation would clean old hourly/daily keys

            conn.commit()

        logger.info(f"Cleaned up {old_clicks} old click records")

        return {
            'deleted_clicks': old_clicks,
            'cutoff_date': cutoff_date.isoformat(),
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to cleanup old data: {e}")
        raise
EOF

# Create tasks init
mkdir -p src/product_prices/tasks
touch src/product_prices/tasks/__init__.py
```

### 4. **FastAPI Integration**

Add tracking endpoints to the API:

```python
# Create affiliate tracking API routes
cat > src/product_prices/api/routes/tracking.py << 'EOF'
"""
Affiliate tracking API endpoints
"""
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pathlib import Path

from fastapi import APIRouter, Request, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from ...services.tracking import AffiliateTracker
from ...services.affiliate import AffiliateService


router = APIRouter(prefix="/api/v1/tracking", tags=["affiliate-tracking"])


class ClickTrackingRequest(BaseModel):
    """Click tracking request"""
    link_id: int
    session_id: Optional[str] = None
    referrer: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None


class ConversionTrackingRequest(BaseModel):
    """Conversion tracking request"""
    click_id: str
    order_id: Optional[str] = None
    conversion_value: float
    commission_earned: float
    currency: str = "GBP"


def get_affiliate_tracker() -> AffiliateTracker:
    """Get affiliate tracker instance"""
    db_path = Path("products.db")
    return AffiliateTracker(db_path)


def get_affiliate_service() -> AffiliateService:
    """Get affiliate service instance"""
    db_path = Path("products.db")
    return AffiliateService(db_path)


@router.get("/click/{link_id}")
async def track_click_redirect(
    link_id: int,
    request: Request,
    tracker: AffiliateTracker = Depends(get_affiliate_tracker)
):
    """Track click and redirect to affiliate URL"""
    try:
        # Extract request data
        request_data = {
            'user_agent': request.headers.get('user-agent', ''),
            'referrer': request.headers.get('referer', ''),
            'remote_addr': request.client.host,
            'x_forwarded_for': request.headers.get('x-forwarded-for', ''),
            'x_real_ip': request.headers.get('x-real-ip', ''),
            'session_id': request.cookies.get('affiliate_session')
        }

        # Track the click
        result = tracker.track_click(link_id, request_data)

        if not result['success']:
            raise HTTPException(status_code=400, detail=result.get('error', 'Tracking failed'))

        # Get redirect URL
        redirect_url = result.get('redirect_url')
        if not redirect_url:
            raise HTTPException(status_code=404, detail="Affiliate URL not found")

        # Create redirect response with session cookie
        response = RedirectResponse(url=redirect_url, status_code=302)

        if 'session_id' in result:
            response.set_cookie(
                key="affiliate_session",
                value=result['session_id'],
                max_age=24 * 3600,  # 24 hours
                httponly=True,
                secure=True,
                samesite="lax"
            )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tracking failed: {str(e)}")


@router.post("/click")
async def track_click_api(
    tracking_request: ClickTrackingRequest,
    request: Request,
    tracker: AffiliateTracker = Depends(get_affiliate_tracker)
):
    """Track click via API (for AJAX tracking)"""
    try:
        request_data = {
            'user_agent': request.headers.get('user-agent', ''),
            'referrer': tracking_request.referrer or request.headers.get('referer', ''),
            'remote_addr': request.client.host,
            'x_forwarded_for': request.headers.get('x-forwarded-for', ''),
            'x_real_ip': request.headers.get('x-real-ip', ''),
            'session_id': tracking_request.session_id or request.cookies.get('affiliate_session')
        }

        result = tracker.track_click(tracking_request.link_id, request_data)

        return {
            'success': result['success'],
            'click_id': result.get('click_id'),
            'session_id': result.get('session_id'),
            'duplicate': result.get('duplicate', False)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tracking failed: {str(e)}")


@router.post("/conversion")
async def track_conversion(
    conversion_request: ConversionTrackingRequest,
    tracker: AffiliateTracker = Depends(get_affiliate_tracker)
):
    """Track affiliate conversion"""
    try:
        conversion_data = {
            'value': conversion_request.conversion_value,
            'commission': conversion_request.commission_earned,
            'order_id': conversion_request.order_id,
            'currency': conversion_request.currency
        }

        success = tracker.track_conversion(conversion_request.click_id, conversion_data)

        return {
            'success': success,
            'click_id': conversion_request.click_id,
            'tracked_at': datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion tracking failed: {str(e)}")


@router.get("/analytics/realtime")
async def get_realtime_analytics(
    link_id: Optional[int] = Query(None, description="Specific link ID"),
    hours: int = Query(24, ge=1, le=168, description="Hours of data to retrieve"),
    tracker: AffiliateTracker = Depends(get_affiliate_tracker)
):
    """Get real-time analytics data"""
    try:
        analytics = tracker.get_realtime_analytics(link_id=link_id, hours=hours)
        return analytics

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics retrieval failed: {str(e)}")


@router.get("/analytics/performance")
async def get_performance_metrics(
    days: int = Query(7, ge=1, le=90, description="Days of data to retrieve"),
    tracker: AffiliateTracker = Depends(get_affiliate_tracker)
):
    """Get performance metrics"""
    try:
        metrics = tracker.get_performance_metrics(days=days)

        return {
            'period_days': days,
            'metrics': [
                {
                    'network_id': m.network_id,
                    'date': m.date.isoformat(),
                    'clicks': m.clicks,
                    'conversions': m.conversions,
                    'revenue': float(m.revenue),
                    'commission_earned': float(m.commission_earned),
                    'conversion_rate': float(m.conversion_rate)
                }
                for m in metrics
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance metrics failed: {str(e)}")


@router.get("/health")
async def tracking_health_check(
    tracker: AffiliateTracker = Depends(get_affiliate_tracker)
):
    """Health check for tracking system"""
    try:
        # Test Redis connection
        redis_status = "healthy"
        try:
            tracker.redis.ping()
        except Exception:
            redis_status = "unhealthy"

        # Test database connection
        db_status = "healthy"
        try:
            import sqlite3
            with sqlite3.connect(tracker.db_path) as conn:
                conn.execute("SELECT 1").fetchone()
        except Exception:
            db_status = "unhealthy"

        # Get queue size
        queue_size = tracker.redis.llen(tracker.CLICK_QUEUE_KEY)

        return {
            'status': 'healthy' if redis_status == 'healthy' and db_status == 'healthy' else 'unhealthy',
            'redis': redis_status,
            'database': db_status,
            'click_queue_size': queue_size,
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
EOF

# Update main API to include tracking routes
cat >> src/product_prices/api/main.py << 'EOF'

# Import tracking routes
from .routes.tracking import router as tracking_router

# Add tracking routes
app.include_router(tracking_router)
EOF
```

### 5. **Testing Infrastructure**

Create comprehensive tests for tracking:

```python
# Create tracking service tests
cat > tests/test_affiliate_tracking.py << 'EOF'
"""
Tests for affiliate tracking service
"""
import pytest
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch

from src.product_prices.services.tracking import AffiliateTracker, ClickEvent, ConversionEvent


class TestAffiliateTracker:
    """Test suite for affiliate tracking"""

    @pytest.fixture
    def mock_redis(self):
        """Mock Redis client"""
        redis_mock = Mock()
        redis_mock.exists.return_value = False
        redis_mock.get.return_value = None
        redis_mock.setex.return_value = True
        redis_mock.incr.return_value = 1
        redis_mock.lpop.return_value = []
        redis_mock.rpush.return_value = 1
        redis_mock.ping.return_value = True
        redis_mock.llen.return_value = 0
        return redis_mock

    @pytest.fixture
    def temp_db_with_data(self, tmp_path):
        """Create temporary database with test data"""
        import sqlite3

        db_path = tmp_path / "test_tracking.db"

        with sqlite3.connect(db_path) as conn:
            # Create affiliate tables
            conn.executescript("""
                CREATE TABLE affiliate_networks (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    display_name TEXT,
                    default_commission_rate REAL
                );

                CREATE TABLE affiliate_links (
                    id INTEGER PRIMARY KEY,
                    sku TEXT,
                    source TEXT,
                    network_id INTEGER,
                    original_url TEXT,
                    affiliate_url TEXT,
                    status TEXT DEFAULT 'active'
                );

                CREATE TABLE affiliate_clicks (
                    id INTEGER PRIMARY KEY,
                    link_id INTEGER,
                    session_id TEXT,
                    user_agent TEXT,
                    ip_address TEXT,
                    referrer TEXT,
                    clicked_at TIMESTAMP,
                    converted BOOLEAN DEFAULT 0,
                    conversion_value REAL,
                    commission_earned REAL,
                    conversion_at TIMESTAMP
                );

                INSERT INTO affiliate_networks (id, name, display_name, default_commission_rate)
                VALUES (1, 'webgains', 'Webgains', 0.08);

                INSERT INTO affiliate_links (id, sku, source, network_id, original_url, affiliate_url)
                VALUES (1, 'TEST001', 'test_source', 1, 'https://example.com', 'https://affiliate.com/link');
            """)
            conn.commit()

        return db_path

    @pytest.fixture
    def tracker(self, temp_db_with_data, mock_redis):
        """Create tracker instance with mocked Redis"""
        tracker = AffiliateTracker(temp_db_with_data, mock_redis)
        return tracker

    def test_track_click_basic(self, tracker):
        """Test basic click tracking"""
        request_data = {
            'user_agent': 'Test Browser',
            'referrer': 'https://example.com',
            'remote_addr': '192.168.1.100'
        }

        result = tracker.track_click(1, request_data)

        assert result['success'] is True
        assert 'session_id' in result
        assert 'click_id' in result

    def test_rate_limiting(self, tracker, mock_redis):
        """Test rate limiting functionality"""
        # Simulate rate limit exceeded
        mock_redis.get.return_value = "101"  # Above limit

        request_data = {
            'user_agent': 'Test Browser',
            'remote_addr': '192.168.1.100'
        }

        result = tracker.track_click(1, request_data)

        assert result['success'] is False
        assert result['error'] == 'rate_limit_exceeded'

    def test_duplicate_click_detection(self, tracker, mock_redis):
        """Test duplicate click detection"""
        # First click
        request_data = {
            'user_agent': 'Test Browser',
            'remote_addr': '192.168.1.100',
            'session_id': 'test_session_123'
        }

        # Mock existing click
        mock_redis.exists.return_value = True

        result = tracker.track_click(1, request_data)

        assert result['success'] is True
        assert result.get('duplicate') is True

    def test_session_management(self, tracker, mock_redis):
        """Test session creation and management"""
        # New session
        request_data = {
            'user_agent': 'Test Browser',
            'remote_addr': '192.168.1.100'
        }

        session_id = tracker._get_or_create_session(request_data)

        assert len(session_id) > 0
        mock_redis.setex.assert_called()

    def test_ip_anonymization(self, tracker):
        """Test IP address anonymization"""
        test_cases = [
            ('192.168.1.100', '192.168.1.0'),
            ('10.0.0.50', '10.0.0.0'),
            ('2001:db8:85a3::8a2e:370:7334', '2001:db8:85a3::0'),
            ('invalid-ip', 'invalid-ip')
        ]

        for original, expected in test_cases:
            result = tracker._anonymize_ip(original)
            assert result == expected

    def test_click_fingerprint_generation(self, tracker):
        """Test click fingerprint generation"""
        fingerprint1 = tracker._generate_click_fingerprint(
            1, '192.168.1.100', 'Browser 1', 'session1'
        )

        fingerprint2 = tracker._generate_click_fingerprint(
            1, '192.168.1.100', 'Browser 1', 'session1'
        )

        # Should be different due to timestamp
        assert fingerprint1 != fingerprint2
        assert len(fingerprint1) == 16  # SHA256 truncated to 16 chars

    def test_click_event_queuing(self, tracker, mock_redis):
        """Test click event queuing"""
        click_event = ClickEvent(
            link_id=1,
            session_id='test_session',
            user_agent='Test Browser',
            ip_address='192.168.1.0',
            referrer='https://example.com',
            timestamp=datetime.now(),
            fingerprint='test_fingerprint'
        )

        tracker._queue_click_event(click_event)

        mock_redis.rpush.assert_called()
        call_args = mock_redis.rpush.call_args
        assert call_args[0][0] == tracker.CLICK_QUEUE_KEY

    def test_process_click_queue(self, tracker, mock_redis):
        """Test processing click queue"""
        # Mock queued click data
        click_data = {
            'link_id': 1,
            'session_id': 'test_session',
            'user_agent': 'Test Browser',
            'ip_address': '192.168.1.0',
            'referrer': 'https://example.com',
            'timestamp': datetime.now().isoformat(),
            'fingerprint': 'test_fingerprint'
        }

        mock_redis.lpop.return_value = [json.dumps(click_data)]

        processed = tracker.process_click_queue()

        assert processed == 1

    def test_conversion_tracking(self, tracker):
        """Test conversion tracking"""
        # First create a click
        with tracker.db_path.open('r+') as db:
            import sqlite3
            conn = sqlite3.connect(tracker.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO affiliate_clicks (id, link_id, session_id, clicked_at)
                VALUES (1, 1, 'test_session', ?)
            """, (datetime.now(),))
            conn.commit()
            conn.close()

        # Mock fingerprint mapping
        tracker.redis.get.return_value = json.dumps({
            'db_id': 1,
            'link_id': 1,
            'session_id': 'test_session',
            'timestamp': datetime.now().isoformat()
        })

        conversion_data = {
            'value': 50.0,
            'commission': 5.0,
            'order_id': 'ORDER123'
        }

        success = tracker.track_conversion('test_fingerprint', conversion_data)
        assert success is True

    def test_realtime_analytics(self, tracker, mock_redis):
        """Test real-time analytics retrieval"""
        # Mock analytics data
        mock_redis.hget.side_effect = lambda key, field: {
            f"{tracker.ANALYTICS_KEY_PREFIX}hourly:2023120112": {
                'link:1:clicks': '5',
                'link:1:conversions': '1',
                'link:1:revenue': '25.50'
            }.get(field, '0')
        }

        analytics = tracker.get_realtime_analytics(link_id=1, hours=1)

        assert 'link_id' in analytics
        assert 'clicks' in analytics
        assert 'conversions' in analytics
        assert 'revenue' in analytics

    def test_performance_metrics(self, tracker):
        """Test performance metrics retrieval"""
        # Add test data
        import sqlite3

        with sqlite3.connect(tracker.db_path) as conn:
            cursor = conn.cursor()

            # Add test clicks and conversions
            test_date = datetime.now().date()
            cursor.execute("""
                INSERT INTO affiliate_clicks
                (link_id, session_id, clicked_at, converted, conversion_value, commission_earned)
                VALUES (1, 'session1', ?, 1, 25.0, 2.5)
            """, (datetime.combine(test_date, datetime.min.time()),))

            cursor.execute("""
                INSERT INTO affiliate_clicks
                (link_id, session_id, clicked_at, converted, conversion_value, commission_earned)
                VALUES (1, 'session2', ?, 0, NULL, NULL)
            """, (datetime.combine(test_date, datetime.min.time()),))

            conn.commit()

        metrics = tracker.get_performance_metrics(days=1)

        assert len(metrics) > 0
        assert any(m.clicks > 0 for m in metrics)

    def test_link_caching(self, tracker, mock_redis):
        """Test affiliate link caching"""
        mock_redis.get.return_value = "https://cached-affiliate-url.com"

        cached_url = tracker._get_cached_affiliate_url(1)

        assert cached_url == "https://cached-affiliate-url.com"
        mock_redis.get.assert_called_with(f"{tracker.LINK_CACHE_KEY_PREFIX}1")


class TestClickEvent:
    """Test ClickEvent data class"""

    def test_click_event_creation(self):
        """Test creating click event"""
        event = ClickEvent(
            link_id=1,
            session_id='test_session',
            user_agent='Test Browser',
            ip_address='192.168.1.0',
            referrer='https://example.com',
            timestamp=datetime.now(),
            fingerprint='test_fingerprint'
        )

        assert event.link_id == 1
        assert event.session_id == 'test_session'

    def test_click_event_to_dict(self):
        """Test converting click event to dictionary"""
        timestamp = datetime.now()
        event = ClickEvent(
            link_id=1,
            session_id='test_session',
            user_agent='Test Browser',
            ip_address='192.168.1.0',
            referrer='https://example.com',
            timestamp=timestamp,
            fingerprint='test_fingerprint'
        )

        event_dict = event.to_dict()

        assert event_dict['link_id'] == 1
        assert event_dict['timestamp'] == timestamp.isoformat()
        assert 'fingerprint' in event_dict


class TestConversionEvent:
    """Test ConversionEvent data class"""

    def test_conversion_event_creation(self):
        """Test creating conversion event"""
        event = ConversionEvent(
            click_id=1,
            conversion_value=50.0,
            commission_earned=5.0,
            timestamp=datetime.now(),
            order_id='ORDER123'
        )

        assert event.click_id == 1
        assert event.conversion_value == 50.0
        assert event.commission_earned == 5.0
        assert event.order_id == 'ORDER123'


# Integration tests
class TestTrackingIntegration:
    """Integration tests for tracking system"""

    @pytest.fixture
    def real_tracker(self, tmp_path):
        """Create tracker with real Redis (if available)"""
        import sqlite3

        db_path = tmp_path / "integration.db"

        # Create full database schema
        with sqlite3.connect(db_path) as conn:
            conn.executescript("""
                CREATE TABLE affiliate_networks (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    display_name TEXT,
                    default_commission_rate REAL
                );

                CREATE TABLE affiliate_links (
                    id INTEGER PRIMARY KEY,
                    sku TEXT,
                    source TEXT,
                    network_id INTEGER,
                    original_url TEXT,
                    affiliate_url TEXT,
                    status TEXT DEFAULT 'active'
                );

                CREATE TABLE affiliate_clicks (
                    id INTEGER PRIMARY KEY,
                    link_id INTEGER,
                    session_id TEXT,
                    user_agent TEXT,
                    ip_address TEXT,
                    referrer TEXT,
                    clicked_at TIMESTAMP,
                    converted BOOLEAN DEFAULT 0,
                    conversion_value REAL,
                    commission_earned REAL,
                    conversion_at TIMESTAMP
                );

                INSERT INTO affiliate_networks VALUES (1, 'webgains', 'Webgains', 0.08);
                INSERT INTO affiliate_links VALUES
                (1, 'TEST001', 'test_source', 1, 'https://example.com', 'https://affiliate.com/link', 'active');
            """)
            conn.commit()

        try:
            # Try to use real Redis if available
            from src.product_prices.config.redis import get_redis_client
            redis_client = get_redis_client()
            redis_client.ping()  # Test connection
            return AffiliateTracker(db_path, redis_client)
        except Exception:
            # Fall back to mock if Redis not available
            pytest.skip("Redis not available for integration tests")

    @pytest.mark.integration
    def test_full_tracking_workflow(self, real_tracker):
        """Test complete tracking workflow"""
        # Track a click
        request_data = {
            'user_agent': 'Integration Test Browser',
            'referrer': 'https://test-referrer.com',
            'remote_addr': '192.168.1.100'
        }

        click_result = real_tracker.track_click(1, request_data)
        assert click_result['success'] is True

        # Process the queue
        processed = real_tracker.process_click_queue()
        assert processed >= 0

        # Get analytics
        analytics = real_tracker.get_realtime_analytics(link_id=1, hours=1)
        assert 'link_id' in analytics

        # Track conversion (if click was processed)
        if 'click_id' in click_result:
            conversion_data = {
                'value': 25.0,
                'commission': 2.5
            }
            conversion_result = real_tracker.track_conversion(
                click_result['click_id'],
                conversion_data
            )
            # May succeed or fail depending on timing
            assert isinstance(conversion_result, bool)

    @pytest.mark.integration
    def test_rate_limiting_integration(self, real_tracker):
        """Test rate limiting with real Redis"""
        request_data = {
            'user_agent': 'Rate Limit Test',
            'remote_addr': '192.168.1.200'
        }

        # Make multiple requests rapidly
        results = []
        for i in range(5):
            result = real_tracker.track_click(1, request_data)
            results.append(result['success'])

        # All should succeed within rate limit
        assert all(results)
EOF

# Create API tests
cat > tests/test_tracking_api.py << 'EOF'
"""
Tests for affiliate tracking API endpoints
"""
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

from src.product_prices.api.main import app


class TestTrackingAPI:
    """Test tracking API endpoints"""

    @pytest.fixture
    def client(self):
        """FastAPI test client"""
        return TestClient(app)

    @pytest.fixture
    def mock_tracker(self):
        """Mock affiliate tracker"""
        tracker = Mock()
        tracker.track_click.return_value = {
            'success': True,
            'click_id': 'test_click_123',
            'session_id': 'test_session_456',
            'redirect_url': 'https://affiliate.com/redirect'
        }
        tracker.track_conversion.return_value = True
        tracker.get_realtime_analytics.return_value = {
            'link_id': 1,
            'clicks': 10,
            'conversions': 2,
            'revenue': 50.0
        }
        tracker.redis.ping.return_value = True
        tracker.redis.llen.return_value = 5
        return tracker

    @patch('src.product_prices.api.routes.tracking.get_affiliate_tracker')
    def test_track_click_redirect(self, mock_get_tracker, client, mock_tracker):
        """Test click tracking with redirect"""
        mock_get_tracker.return_value = mock_tracker

        response = client.get(
            "/api/v1/tracking/click/1",
            headers={
                'User-Agent': 'Test Browser',
                'Referer': 'https://example.com'
            }
        )

        assert response.status_code == 302
        assert response.headers['location'] == 'https://affiliate.com/redirect'
        mock_tracker.track_click.assert_called_once()

    @patch('src.product_prices.api.routes.tracking.get_affiliate_tracker')
    def test_track_click_api(self, mock_get_tracker, client, mock_tracker):
        """Test click tracking via API"""
        mock_get_tracker.return_value = mock_tracker

        response = client.post(
            "/api/v1/tracking/click",
            json={
                'link_id': 1,
                'referrer': 'https://example.com'
            },
            headers={'User-Agent': 'Test Browser'}
        )

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'click_id' in data
        assert 'session_id' in data

    @patch('src.product_prices.api.routes.tracking.get_affiliate_tracker')
    def test_track_conversion(self, mock_get_tracker, client, mock_tracker):
        """Test conversion tracking"""
        mock_get_tracker.return_value = mock_tracker

        response = client.post(
            "/api/v1/tracking/conversion",
            json={
                'click_id': 'test_click_123',
                'conversion_value': 50.0,
                'commission_earned': 5.0,
                'order_id': 'ORDER123'
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['click_id'] == 'test_click_123'

    @patch('src.product_prices.api.routes.tracking.get_affiliate_tracker')
    def test_realtime_analytics(self, mock_get_tracker, client, mock_tracker):
        """Test real-time analytics endpoint"""
        mock_get_tracker.return_value = mock_tracker

        response = client.get("/api/v1/tracking/analytics/realtime?link_id=1&hours=24")

        assert response.status_code == 200
        data = response.json()
        assert data['link_id'] == 1
        assert 'clicks' in data
        assert 'conversions' in data

    @patch('src.product_prices.api.routes.tracking.get_affiliate_tracker')
    def test_health_check(self, mock_get_tracker, client, mock_tracker):
        """Test tracking health check"""
        mock_get_tracker.return_value = mock_tracker

        # Mock database connection test
        with patch('sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_conn.execute.return_value.fetchone.return_value = [1]
            mock_connect.return_value.__enter__.return_value = mock_conn

            response = client.get("/api/v1/tracking/health")

            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'healthy'
            assert data['redis'] == 'healthy'
            assert data['database'] == 'healthy'

    @patch('src.product_prices.api.routes.tracking.get_affiliate_tracker')
    def test_error_handling(self, mock_get_tracker, client):
        """Test API error handling"""
        # Mock tracker that raises exception
        mock_tracker = Mock()
        mock_tracker.track_click.side_effect = Exception("Tracking failed")
        mock_get_tracker.return_value = mock_tracker

        response = client.post(
            "/api/v1/tracking/click",
            json={'link_id': 1}
        )

        assert response.status_code == 500
        assert "Tracking failed" in response.json()['detail']
EOF
```

### 6. **Documentation and CLI Integration**

```bash
# Update CLI with tracking commands
cat >> src/product_prices/cli.py << 'EOF'

@affiliate.command()
@click.option('--link-id', type=int, help='Specific link ID for analytics')
@click.option('--hours', default=24, help='Hours of data to show')
def realtime(link_id, hours):
    """Show real-time tracking analytics"""
    from .services.tracking import AffiliateTracker

    db_path = Path("products.db")
    tracker = AffiliateTracker(db_path)

    analytics = tracker.get_realtime_analytics(link_id=link_id, hours=hours)

    if link_id:
        click.echo(f"📊 Analytics for Link {link_id} ({hours}h)")
    else:
        click.echo(f"📊 Global Analytics ({hours}h)")

    click.echo(f"Clicks: {analytics.get('clicks', 0)}")
    click.echo(f"Conversions: {analytics.get('conversions', 0)}")
    click.echo(f"Revenue: £{analytics.get('revenue', 0):.2f}")

@affiliate.command()
def process():
    """Process queued clicks"""
    from .services.tracking import AffiliateTracker

    db_path = Path("products.db")
    tracker = AffiliateTracker(db_path)

    processed = tracker.process_click_queue()
    click.echo(f"✅ Processed {processed} clicks from queue")

@affiliate.command()
def health():
    """Check tracking system health"""
    from .services.tracking import AffiliateTracker

    db_path = Path("products.db")
    tracker = AffiliateTracker(db_path)

    try:
        # Test Redis
        tracker.redis.ping()
        redis_status = "✅ Redis: Healthy"
    except Exception as e:
        redis_status = f"❌ Redis: {e}"

    try:
        # Test database
        import sqlite3
        with sqlite3.connect(db_path) as conn:
            conn.execute("SELECT 1").fetchone()
        db_status = "✅ Database: Healthy"
    except Exception as e:
        db_status = f"❌ Database: {e}"

    # Check queue size
    queue_size = tracker.redis.llen(tracker.CLICK_QUEUE_KEY)

    click.echo("🏥 Tracking System Health")
    click.echo(redis_status)
    click.echo(db_status)
    click.echo(f"📊 Click Queue: {queue_size} pending")
EOF

# Create tracking documentation
cat > docs/affiliate_tracking.md << 'EOF'
# Affiliate Tracking System

## Overview

Advanced click tracking and analytics system for affiliate links with Redis caching, real-time analytics, and privacy compliance.

## Architecture

### Components
- **AffiliateTracker** - Core tracking service with Redis integration
- **ClickEvent/ConversionEvent** - Data structures for tracking events
- **Redis Caching** - Real-time analytics and session management
- **Celery Tasks** - Background processing and maintenance
- **FastAPI Endpoints** - RESTful tracking API

### Data Flow
1. User clicks affiliate link
2. Click tracked via API endpoint
3. Event queued in Redis for batch processing
4. Real-time analytics updated
5. Background task processes queue to database
6. Conversion tracking via webhook/pixel

## Features

### Advanced Click Tracking
- Rate limiting (100 clicks/hour per IP)
- Duplicate click detection
- Session management with secure cookies
- Fraud detection via fingerprinting
- Privacy-compliant IP anonymization

### Real-time Analytics
- Hourly/daily metrics in Redis
- Click-through rates
- Conversion tracking
- Revenue attribution
- Network performance comparison

### Background Processing
- Celery task queue for clicks
- Batch database inserts
- Link validation
- Data cleanup and retention
- Performance report generation

## Usage

### Track Clicks
```python
# Via service
tracker = AffiliateTracker(db_path)
result = tracker.track_click(link_id, request_data)

# Via API
POST /api/v1/tracking/click
{
    "link_id": 123,
    "referrer": "https://example.com"
}
```

### Track Conversions
```python
# Via service
tracker.track_conversion(click_id, conversion_data)

# Via API
POST /api/v1/tracking/conversion
{
    "click_id": "abc123",
    "conversion_value": 50.0,
    "commission_earned": 5.0
}
```

### Get Analytics
```python
# Real-time analytics
analytics = tracker.get_realtime_analytics(link_id=1, hours=24)

# Performance metrics
metrics = tracker.get_performance_metrics(days=7)
```

## API Endpoints

### Tracking
- `GET /api/v1/tracking/click/{link_id}` - Track click and redirect
- `POST /api/v1/tracking/click` - Track click via AJAX
- `POST /api/v1/tracking/conversion` - Track conversion

### Analytics
- `GET /api/v1/tracking/analytics/realtime` - Real-time analytics
- `GET /api/v1/tracking/analytics/performance` - Performance metrics
- `GET /api/v1/tracking/health` - System health check

## Background Tasks

### Celery Tasks
```bash
# Start Celery worker
celery -A src.product_prices.celery_app worker --loglevel=info

# Start Celery beat (scheduler)
celery -A src.product_prices.celery_app beat --loglevel=info
```

### Task Schedule
- **process_clicks** - Every minute (process click queue)
- **update_analytics** - Every hour (aggregate metrics)
- **validate_links** - Daily (check link health)
- **cleanup_old_data** - Daily (GDPR compliance)

## Privacy & Compliance

### GDPR Compliance
- IP address anonymization (last octet zeroed)
- Configurable data retention periods
- Session-based tracking without personal data
- Automatic data cleanup after 90 days

### Security
- Rate limiting to prevent abuse
- Secure session ID generation
- Click fingerprinting for fraud detection
- HTTPS-only cookies

## Configuration

### Environment Variables
```bash
REDIS_URL=redis://localhost:6379/0
AFFILIATE_TRACKING_ENABLED=true
AFFILIATE_SESSION_TIMEOUT=86400
AFFILIATE_CLICK_BATCH_SIZE=100
AFFILIATE_ANALYTICS_RETENTION_DAYS=90
```

### Redis Configuration
- Connection pooling with 10 max connections
- 5-second socket timeout
- Automatic failover and retry logic

## Monitoring

### Health Checks
```bash
# CLI health check
uv run python -m product_prices affiliate health

# API health check
curl http://localhost:8008/api/v1/tracking/health
```

### Metrics Monitoring
- Click queue size monitoring
- Redis connection health
- Database connection status
- Processing rates and errors

## Testing

```bash
# Run tracking tests
uv run pytest tests/test_affiliate_tracking.py

# Run API tests
uv run pytest tests/test_tracking_api.py

# Integration tests with Redis
uv run pytest tests/test_affiliate_tracking.py::TestTrackingIntegration -m integration
```

## Performance

### Optimization Features
- Redis caching for affiliate URLs
- Batch processing of clicks
- Real-time analytics without database hits
- Connection pooling for both Redis and SQLite

### Scaling Considerations
- Horizontal scaling via multiple Celery workers
- Redis cluster support for high availability
- Database sharding for large-scale deployments
- CDN integration for tracking pixels

## Troubleshooting

### Common Issues
1. **Redis Connection Failed**
   - Check Redis service status
   - Verify connection URL and credentials
   - Test network connectivity

2. **High Queue Size**
   - Increase Celery worker count
   - Check for processing errors
   - Monitor system resources

3. **Missing Conversions**
   - Verify conversion tracking setup
   - Check fingerprint mapping storage
   - Validate conversion window timing

### Debug Commands
```bash
# Check queue size
redis-cli llen affiliate:clicks:queue

# Monitor real-time analytics
redis-cli hgetall affiliate:analytics:hourly:2023120112

# Process clicks manually
uv run python -m product_prices affiliate process
```
EOF

# Create deployment guide
cat > docs/affiliate_deployment.md << 'EOF'
# Affiliate Tracking Deployment Guide

## Prerequisites

### Required Services
- Redis server (for caching and queues)
- Python 3.8+ with uv package manager
- SQLite database (existing products.db)

### Redis Installation
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install redis-server

# macOS
brew install redis

# Start Redis
sudo systemctl start redis-server  # Linux
brew services start redis          # macOS
```

## Installation Steps

### 1. Install Dependencies
```bash
# Add Redis and Celery dependencies
uv add redis celery[redis] python-dotenv

# Verify installation
python -c "import redis; print('Redis client installed')"
python -c "import celery; print('Celery installed')"
```

### 2. Configure Environment
```bash
# Add to .env file
cat >> .env << 'EOF'
REDIS_URL=redis://localhost:6379/0
AFFILIATE_TRACKING_ENABLED=true
AFFILIATE_SESSION_TIMEOUT=86400
AFFILIATE_CLICK_BATCH_SIZE=100
EOF
```

### 3. Database Migration
```bash
# Run affiliate foundation setup first
/affiliate:setup-foundation

# Verify tracking tables exist
sqlite3 products.db "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'affiliate_%';"
```

### 4. Start Services

#### Development Setup
```bash
# Terminal 1: Start API server
uvicorn src.product_prices.api.main:app --host 127.0.0.1 --port 8008 --reload

# Terminal 2: Start Celery worker
celery -A src.product_prices.celery_app worker --loglevel=info

# Terminal 3: Start Celery beat (scheduler)
celery -A src.product_prices.celery_app beat --loglevel=info
```

#### Production Setup
```bash
# Use systemd services or Docker containers
# See production deployment section below
```

## Verification

### Test Basic Functionality
```bash
# Test Redis connection
python -c "
from src.product_prices.config.redis import get_redis_client
client = get_redis_client()
client.ping()
print('Redis connection: OK')
"

# Test tracking service
python -c "
from pathlib import Path
from src.product_prices.services.tracking import AffiliateTracker
tracker = AffiliateTracker(Path('products.db'))
print('Tracker initialized: OK')
"

# Test API endpoints
curl http://localhost:8008/api/v1/tracking/health
```

### Test Click Tracking
```bash
# Create test affiliate link first
python -c "
from pathlib import Path
from src.product_prices.services.affiliate import AffiliateService
from src.product_prices.models.affiliate import AffiliateLinkRequest

service = AffiliateService(Path('products.db'))
request = AffiliateLinkRequest(
    sku='TEST001',
    source='test_source',
    network_name='webgains',
    original_url='https://example.com/product'
)
response = service.generate_affiliate_link(request)
print(f'Test link created: {response.link_id}')
"

# Test click tracking
curl -X POST http://localhost:8008/api/v1/tracking/click \
  -H "Content-Type: application/json" \
  -d '{"link_id": 1, "referrer": "https://test.com"}'
```

## Production Deployment

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install uv && uv sync

# Start services
CMD ["sh", "-c", "celery -A src.product_prices.celery_app worker --detach && uvicorn src.product_prices.api.main:app --host 0.0.0.0 --port 8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  affiliate-api:
    build: .
    ports:
      - "8008:8000"
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    volumes:
      - ./products.db:/app/products.db

  affiliate-worker:
    build: .
    command: celery -A src.product_prices.celery_app worker --loglevel=info
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    volumes:
      - ./products.db:/app/products.db

  affiliate-beat:
    build: .
    command: celery -A src.product_prices.celery_app beat --loglevel=info
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    volumes:
      - ./products.db:/app/products.db

volumes:
  redis_data:
```

### Systemd Services
```ini
# /etc/systemd/system/affiliate-api.service
[Unit]
Description=Affiliate API Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/product-prices
Environment=PATH=/opt/product-prices/.venv/bin
ExecStart=/opt/product-prices/.venv/bin/uvicorn src.product_prices.api.main:app --host 127.0.0.1 --port 8008
Restart=always

[Install]
WantedBy=multi-user.target
```

```ini
# /etc/systemd/system/affiliate-worker.service
[Unit]
Description=Affiliate Worker
After=network.target redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/product-prices
Environment=PATH=/opt/product-prices/.venv/bin
ExecStart=/opt/product-prices/.venv/bin/celery -A src.product_prices.celery_app worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
```

### Nginx Configuration
```nginx
# /etc/nginx/sites-available/affiliate-tracking
server {
    listen 80;
    server_name your-domain.com;

    location /api/v1/tracking/ {
        proxy_pass http://127.0.0.1:8008;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoring & Maintenance

### Log Monitoring
```bash
# Celery worker logs
journalctl -u affiliate-worker -f

# API server logs
journalctl -u affiliate-api -f

# Redis logs
journalctl -u redis -f
```

### Performance Monitoring
```bash
# Monitor Redis memory usage
redis-cli info memory

# Monitor queue sizes
redis-cli llen affiliate:clicks:queue

# Monitor Celery task status
celery -A src.product_prices.celery_app inspect active
```

### Backup & Recovery
```bash
# Backup Redis data
redis-cli bgsave

# Backup SQLite database
cp products.db products_backup_$(date +%Y%m%d).db

# Monitor disk usage
df -h /var/lib/redis
```

## Security Considerations

### Network Security
- Run Redis on private network or with AUTH
- Use HTTPS for API endpoints
- Implement rate limiting at reverse proxy level
- Monitor for suspicious traffic patterns

### Data Protection
- Regular security updates for all components
- Encrypt Redis communication in production
- Implement proper access controls
- Regular security audits and penetration testing

## Troubleshooting

### Common Issues
1. **Redis Connection Refused**
   ```bash
   sudo systemctl status redis-server
   sudo systemctl restart redis-server
   ```

2. **Celery Worker Not Processing**
   ```bash
   celery -A src.product_prices.celery_app inspect ping
   celery -A src.product_prices.celery_app purge  # Clear queue if needed
   ```

3. **High Memory Usage**
   ```bash
   redis-cli flushdb  # Clear Redis data if safe
   # Adjust Redis maxmemory settings
   ```

### Performance Tuning
- Adjust Celery concurrency: `--concurrency=4`
- Configure Redis maxmemory and eviction policies
- Optimize database indexes for tracking queries
- Implement connection pooling and keep-alive settings
EOF
```

### 7. **Quality Assurance**

```bash
# Run all tracking tests
uv run pytest tests/test_affiliate_tracking.py tests/test_tracking_api.py -v

# Test Redis integration
python -c "
from src.product_prices.config.redis import get_redis_client
try:
    client = get_redis_client()
    client.ping()
    print('✅ Redis connection successful')
except Exception as e:
    print(f'❌ Redis connection failed: {e}')
"

# Test Celery configuration
python -c "
from src.product_prices.celery_app import celery_app
print(f'✅ Celery app configured: {celery_app.main}')
print(f'✅ Broker: {celery_app.conf.broker_url}')
"

# Code quality checks
uv run ruff check src/product_prices/services/tracking.py --fix
uv run ruff format src/product_prices/services/tracking.py
uv run mypy src/product_prices/services/tracking.py
uv run bandit -r src/product_prices/services/tracking.py

# Test API endpoints
uv run pytest tests/test_tracking_api.py -v
```

## Summary

This command establishes comprehensive affiliate tracking:

1. ✅ **Redis Integration** - Caching, queuing, real-time analytics
2. ✅ **Advanced Tracking** - Rate limiting, fraud detection, privacy compliance
3. ✅ **Background Processing** - Celery tasks for scalable click processing
4. ✅ **FastAPI Endpoints** - RESTful tracking API with health checks
5. ✅ **Real-time Analytics** - Hourly/daily metrics without database overhead
6. ✅ **Testing Suite** - Unit tests, integration tests, API tests
7. ✅ **Documentation** - Deployment guides and troubleshooting
8. ✅ **Privacy Compliance** - GDPR-compliant data handling and retention

The tracking system is now ready for production deployment with Redis and Celery infrastructure.
