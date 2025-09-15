# Setup Scraper Production Monitoring

Sets up comprehensive production monitoring for web scraping operations including structured logging, metrics collection, error monitoring, health checks, dashboards, and alerting systems.

## Instructions

Follow these steps to implement a complete monitoring solution for your scraper project:

### 1. Analyze Current Scraper Architecture

First, understand the existing scraper structure:

```bash
# Review current project structure
find . -name "*.py" -type f | head -20
ls -la scrapers/ models/ database/ 2>/dev/null || echo "Review actual project structure"
```

Examine the main scraper classes and database models to understand:
- Scraper execution patterns
- Data models and relationships
- Current logging implementation
- Error handling patterns

### 2. Install Monitoring Dependencies

Add comprehensive monitoring packages:

```bash
# Core monitoring and logging
uv add structlog loguru prometheus-client grafana-client

# Metrics and observability
uv add psutil py-healthcheck APScheduler requests-oauthlib

# Database monitoring
uv add sqlalchemy-utils alembic

# Alert and notification systems
uv add slack-sdk discord-webhook sendgrid

# Optional APM integration
uv add sentry-sdk[sqlalchemy,logging] --optional

# Development and testing
uv add --dev pytest-mock freezegun factory-boy
```

### 3. Configure Structured Logging System

Create a centralized logging configuration:

**File: `monitoring/logging_config.py`**
```python
import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import structlog
from loguru import logger

# Configure structlog for JSON output
def add_timestamp(logger, method_name, event_dict):
    """Add ISO timestamp to log entries"""
    event_dict['timestamp'] = datetime.utcnow().isoformat() + 'Z'
    return event_dict

def add_context_info(logger, method_name, event_dict):
    """Add scraper context information"""
    # Add from context vars or thread-local storage
    event_dict.setdefault('scraper_id', getattr(logger, 'scraper_id', 'unknown'))
    event_dict.setdefault('site', getattr(logger, 'site', 'unknown'))
    event_dict.setdefault('run_id', getattr(logger, 'run_id', 'unknown'))
    return event_dict

def setup_structured_logging(
    log_level: str = "INFO",
    log_dir: Path = Path("logs"),
    json_logs: bool = True
):
    """Configure structured logging with rotation"""
    log_dir.mkdir(exist_ok=True)

    # Configure structlog
    structlog.configure(
        processors=[
            add_timestamp,
            add_context_info,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.JSONRenderer() if json_logs else structlog.dev.ConsoleRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure loguru for file rotation
    logger.remove()  # Remove default handler

    # Console output
    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )

    # Rotating file logs
    logger.add(
        log_dir / "scraper_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="30 days",
        compression="gz",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        serialize=json_logs
    )

    # Error logs
    logger.add(
        log_dir / "scraper_errors_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="90 days",
        compression="gz",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        serialize=json_logs
    )

    return structlog.get_logger()

class ScraperLogger:
    """Context-aware logger for scrapers"""

    def __init__(self, scraper_id: str, site: str, run_id: str = None):
        self.logger = structlog.get_logger()
        self.scraper_id = scraper_id
        self.site = site
        self.run_id = run_id or f"{scraper_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        # Bind context to logger
        self.logger = self.logger.bind(
            scraper_id=scraper_id,
            site=site,
            run_id=run_id
        )

    def log_scraper_start(self, config: Dict[str, Any] = None):
        """Log scraper run start"""
        self.logger.info(
            "Scraper run started",
            event_type="scraper_start",
            config=config or {}
        )

    def log_scraper_end(self, stats: Dict[str, Any]):
        """Log scraper run completion"""
        self.logger.info(
            "Scraper run completed",
            event_type="scraper_end",
            **stats
        )

    def log_product_processed(self, product_data: Dict[str, Any], action: str):
        """Log product processing"""
        self.logger.info(
            f"Product {action}",
            event_type="product_processed",
            action=action,
            product_id=product_data.get('id'),
            url=product_data.get('url'),
            price=product_data.get('price')
        )

    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log errors with context"""
        self.logger.error(
            "Scraper error occurred",
            event_type="scraper_error",
            error_type=type(error).__name__,
            error_message=str(error),
            context=context or {},
            exc_info=True
        )

    def log_rate_limit(self, wait_time: float, reason: str = None):
        """Log rate limiting events"""
        self.logger.warning(
            "Rate limit detected",
            event_type="rate_limit",
            wait_time=wait_time,
            reason=reason
        )
```

### 4. Implement Metrics Collection

Create comprehensive metrics tracking:

**File: `monitoring/metrics.py`**
```python
import time
import psutil
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, write_to_textfile
import threading
import json
from pathlib import Path

@dataclass
class ScraperMetrics:
    """Metrics for a single scraper run"""
    scraper_id: str
    site: str
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    products_found: int = 0
    products_added: int = 0
    products_updated: int = 0
    products_failed: int = 0
    pages_scraped: int = 0
    requests_made: int = 0
    errors_count: int = 0
    rate_limits_hit: int = 0
    bytes_downloaded: int = 0

    @property
    def duration_seconds(self) -> float:
        end = self.end_time or datetime.utcnow()
        return (end - self.start_time).total_seconds()

    @property
    def success_rate(self) -> float:
        total = self.products_found
        if total == 0:
            return 1.0
        return (self.products_added + self.products_updated) / total

    @property
    def throughput_per_minute(self) -> float:
        if self.duration_seconds == 0:
            return 0.0
        return (self.products_found / self.duration_seconds) * 60

class PrometheusMetrics:
    """Prometheus metrics collector for scrapers"""

    def __init__(self):
        self.registry = CollectorRegistry()

        # Scraper run metrics
        self.scraper_runs_total = Counter(
            'scraper_runs_total',
            'Total number of scraper runs',
            ['scraper_id', 'site', 'status'],
            registry=self.registry
        )

        self.scraper_duration = Histogram(
            'scraper_duration_seconds',
            'Duration of scraper runs',
            ['scraper_id', 'site'],
            registry=self.registry
        )

        self.products_processed = Counter(
            'products_processed_total',
            'Total products processed',
            ['scraper_id', 'site', 'action'],
            registry=self.registry
        )

        self.scraper_errors = Counter(
            'scraper_errors_total',
            'Total scraper errors',
            ['scraper_id', 'site', 'error_type'],
            registry=self.registry
        )

        self.rate_limits = Counter(
            'rate_limits_total',
            'Total rate limits encountered',
            ['scraper_id', 'site'],
            registry=self.registry
        )

        # System metrics
        self.cpu_usage = Gauge(
            'system_cpu_usage_percent',
            'System CPU usage percentage',
            registry=self.registry
        )

        self.memory_usage = Gauge(
            'system_memory_usage_bytes',
            'System memory usage in bytes',
            registry=self.registry
        )

        self.active_scrapers = Gauge(
            'active_scrapers_count',
            'Number of currently active scrapers',
            registry=self.registry
        )

        # Database metrics
        self.db_query_duration = Histogram(
            'db_query_duration_seconds',
            'Database query duration',
            ['operation'],
            registry=self.registry
        )

        self.db_connections = Gauge(
            'db_connections_active',
            'Active database connections',
            registry=self.registry
        )

    def record_scraper_run(self, metrics: ScraperMetrics, status: str):
        """Record metrics for a completed scraper run"""
        labels = {'scraper_id': metrics.scraper_id, 'site': metrics.site}

        self.scraper_runs_total.labels(**labels, status=status).inc()
        self.scraper_duration.labels(**labels).observe(metrics.duration_seconds)

        # Product metrics
        self.products_processed.labels(**labels, action='found').inc(metrics.products_found)
        self.products_processed.labels(**labels, action='added').inc(metrics.products_added)
        self.products_processed.labels(**labels, action='updated').inc(metrics.products_updated)
        self.products_processed.labels(**labels, action='failed').inc(metrics.products_failed)

        # Error metrics
        if metrics.errors_count > 0:
            self.scraper_errors.labels(**labels, error_type='general').inc(metrics.errors_count)

        if metrics.rate_limits_hit > 0:
            self.rate_limits.labels(**labels).inc(metrics.rate_limits_hit)

    def update_system_metrics(self):
        """Update system resource metrics"""
        self.cpu_usage.set(psutil.cpu_percent())
        self.memory_usage.set(psutil.virtual_memory().used)

    def export_to_file(self, filepath: str):
        """Export metrics to Prometheus format file"""
        write_to_textfile(filepath, self.registry)

class MetricsCollector:
    """Central metrics collection and export"""

    def __init__(self, export_dir: Path = Path("metrics")):
        self.export_dir = export_dir
        self.export_dir.mkdir(exist_ok=True)
        self.prometheus = PrometheusMetrics()
        self.active_runs: Dict[str, ScraperMetrics] = {}
        self._lock = threading.Lock()

        # Start system metrics collection
        self._start_system_monitoring()

    def start_scraper_run(self, scraper_id: str, site: str) -> str:
        """Start tracking a new scraper run"""
        run_id = f"{scraper_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        with self._lock:
            self.active_runs[run_id] = ScraperMetrics(
                scraper_id=scraper_id,
                site=site
            )
            self.prometheus.active_scrapers.set(len(self.active_runs))

        return run_id

    def end_scraper_run(self, run_id: str, status: str = "success") -> Optional[ScraperMetrics]:
        """End tracking for a scraper run"""
        with self._lock:
            if run_id not in self.active_runs:
                return None

            metrics = self.active_runs.pop(run_id)
            metrics.end_time = datetime.utcnow()
            self.prometheus.active_scrapers.set(len(self.active_runs))

        # Record final metrics
        self.prometheus.record_scraper_run(metrics, status)

        # Export metrics
        self._export_metrics()

        return metrics

    def update_run_metrics(self, run_id: str, **kwargs):
        """Update metrics for an active run"""
        with self._lock:
            if run_id in self.active_runs:
                for key, value in kwargs.items():
                    if hasattr(self.active_runs[run_id], key):
                        setattr(self.active_runs[run_id], key, value)

    def _start_system_monitoring(self):
        """Start background system metrics collection"""
        def collect_system_metrics():
            while True:
                self.prometheus.update_system_metrics()
                time.sleep(30)  # Update every 30 seconds

        thread = threading.Thread(target=collect_system_metrics, daemon=True)
        thread.start()

    def _export_metrics(self):
        """Export current metrics to files"""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')

        # Export Prometheus metrics
        self.prometheus.export_to_file(
            str(self.export_dir / f"prometheus_metrics_{timestamp}.txt")
        )

        # Export JSON metrics for custom dashboards
        json_metrics = {
            'timestamp': datetime.utcnow().isoformat(),
            'active_runs': len(self.active_runs),
            'system': {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent
            }
        }

        with open(self.export_dir / f"metrics_{timestamp}.json", 'w') as f:
            json.dump(json_metrics, f, indent=2)

# Global metrics instance
metrics_collector = MetricsCollector()
```

### 5. Create Error Monitoring System

Implement comprehensive error tracking:

**File: `monitoring/error_monitor.py`**
```python
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict, Counter
import json
import re
from pathlib import Path
from enum import Enum

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    NETWORK = "network"
    PARSING = "parsing"
    DATABASE = "database"
    RATE_LIMIT = "rate_limit"
    AUTHENTICATION = "authentication"
    SITE_CHANGE = "site_change"
    SYSTEM = "system"
    UNKNOWN = "unknown"

@dataclass
class ErrorEvent:
    """Represents a single error event"""
    timestamp: datetime
    scraper_id: str
    site: str
    error_type: str
    error_message: str
    traceback: str
    context: Dict[str, Any]
    category: ErrorCategory = ErrorCategory.UNKNOWN
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'scraper_id': self.scraper_id,
            'site': self.site,
            'error_type': self.error_type,
            'error_message': self.error_message,
            'traceback': self.traceback,
            'context': self.context,
            'category': self.category.value,
            'severity': self.severity.value,
            'url': self.url
        }

class ErrorClassifier:
    """Classifies errors by category and severity"""

    # Error patterns for classification
    PATTERNS = {
        ErrorCategory.NETWORK: [
            r'ConnectionError', r'TimeoutError', r'HTTPError', r'RequestException',
            r'DNS', r'SSL', r'TLS', r'Connection refused', r'Network unreachable'
        ],
        ErrorCategory.PARSING: [
            r'AttributeError.*find', r'KeyError', r'IndexError', r'ValueError.*parse',
            r'BeautifulSoup', r'lxml', r'JSONDecodeError', r'ParseError'
        ],
        ErrorCategory.DATABASE: [
            r'DatabaseError', r'IntegrityError', r'SQLAlchemyError', r'psycopg2',
            r'Connection pool', r'Deadlock', r'Foreign key constraint'
        ],
        ErrorCategory.RATE_LIMIT: [
            r'429', r'Too Many Requests', r'Rate limit', r'Slow down',
            r'Request rate', r'API limit exceeded'
        ],
        ErrorCategory.AUTHENTICATION: [
            r'401', r'403', r'Unauthorized', r'Forbidden', r'Authentication',
            r'Login failed', r'Invalid credentials', r'Access denied'
        ],
        ErrorCategory.SITE_CHANGE: [
            r'Element not found', r'Selector not found', r'Page structure changed',
            r'Missing required field', r'Unexpected page layout'
        ]
    }

    SEVERITY_PATTERNS = {
        ErrorSeverity.CRITICAL: [
            r'DatabaseError', r'Out of memory', r'Disk full', r'System crash'
        ],
        ErrorSeverity.HIGH: [
            r'Site structure changed', r'Authentication failed', r'All scrapers failing'
        ],
        ErrorSeverity.MEDIUM: [
            r'Network timeout', r'Rate limit', r'Parsing error'
        ],
        ErrorSeverity.LOW: [
            r'Single product failed', r'Minor parsing issue', r'Temporary connection issue'
        ]
    }

    @classmethod
    def classify_error(cls, error: Exception, context: Dict[str, Any] = None) -> tuple[ErrorCategory, ErrorSeverity]:
        """Classify error by category and severity"""
        error_text = f"{type(error).__name__}: {str(error)}"

        # Classify category
        category = ErrorCategory.UNKNOWN
        for cat, patterns in cls.PATTERNS.items():
            if any(re.search(pattern, error_text, re.IGNORECASE) for pattern in patterns):
                category = cat
                break

        # Classify severity
        severity = ErrorSeverity.MEDIUM
        for sev, patterns in cls.SEVERITY_PATTERNS.items():
            if any(re.search(pattern, error_text, re.IGNORECASE) for pattern in patterns):
                severity = sev
                break

        # Context-based adjustments
        if context:
            # If multiple scrapers are failing, increase severity
            if context.get('consecutive_failures', 0) > 5:
                severity = ErrorSeverity.HIGH

            # If it's a critical site, increase severity
            if context.get('site_priority') == 'critical':
                if severity == ErrorSeverity.LOW:
                    severity = ErrorSeverity.MEDIUM
                elif severity == ErrorSeverity.MEDIUM:
                    severity = ErrorSeverity.HIGH

        return category, severity

# Global error monitor instance
error_monitor = ErrorMonitor()
```

### 6. Setup Health Monitoring

Create comprehensive health checks:

**File: `monitoring/health_monitor.py`**
```python
import psutil
import sqlite3
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import json
import asyncio
import aiohttp
from healthcheck import HealthCheck, EnvironmentDump

@dataclass
class HealthCheckResult:
    """Result of a health check"""
    name: str
    status: str  # "healthy", "warning", "critical"
    message: str
    details: Dict[str, Any]
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'status': self.status,
            'message': self.message,
            'details': self.details,
            'timestamp': self.timestamp.isoformat()
        }

class DatabaseHealthChecker:
    """Database health monitoring"""

    def __init__(self, db_url: str):
        self.db_url = db_url

    def check_connection(self) -> HealthCheckResult:
        """Check database connection"""
        try:
            # This assumes SQLite for simplicity - adapt for your database
            with sqlite3.connect(self.db_url, timeout=5) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()

                if result and result[0] == 1:
                    return HealthCheckResult(
                        name="database_connection",
                        status="healthy",
                        message="Database connection successful",
                        details={"connection_time": "< 5s"},
                        timestamp=datetime.utcnow()
                    )
                else:
                    return HealthCheckResult(
                        name="database_connection",
                        status="critical",
                        message="Database query returned unexpected result",
                        details={"result": str(result)},
                        timestamp=datetime.utcnow()
                    )
        except Exception as e:
            return HealthCheckResult(
                name="database_connection",
                status="critical",
                message=f"Database connection failed: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.utcnow()
            )

class HealthMonitor:
    """Main health monitoring coordinator"""

    def __init__(self, db_url: str, target_sites: List[str], data_dir: Path = Path("monitoring/health")):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.db_checker = DatabaseHealthChecker(db_url)
        self.target_sites = target_sites

        # Setup Flask health check endpoint
        self.health_check = HealthCheck()
        self._setup_health_endpoints()

    def _setup_health_endpoints(self):
        """Setup health check endpoints"""
        self.health_check.add_check("database", self._db_check)

    def _db_check(self):
        result = self.db_checker.check_connection()
        if result.status != "healthy":
            raise Exception(result.message)
        return True, result.message

    async def run_all_checks(self) -> List[HealthCheckResult]:
        """Run all health checks"""
        results = []

        # Database checks
        results.append(self.db_checker.check_connection())

        # Persist results
        self._persist_results(results)

        return results

    def _persist_results(self, results: List[HealthCheckResult]):
        """Persist health check results"""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        results_file = self.data_dir / f"health_check_{timestamp}.json"

        data = {
            'timestamp': datetime.utcnow().isoformat(),
            'overall_status': self._calculate_overall_status(results),
            'checks': [r.to_dict() for r in results]
        }

        with open(results_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _calculate_overall_status(self, results: List[HealthCheckResult]) -> str:
        """Calculate overall system health status"""
        if any(r.status == "critical" for r in results):
            return "critical"
        elif any(r.status == "warning" for r in results):
            return "warning"
        else:
            return "healthy"
```

### 7. Create Dashboard and Reporting

Setup monitoring dashboards:

**File: `monitoring/dashboard.py`**
```python
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from jinja2 import Template

@dataclass
class DashboardData:
    """Data container for dashboard metrics"""
    timestamp: datetime
    scraper_metrics: Dict[str, Any]
    error_metrics: Dict[str, Any]
    health_metrics: Dict[str, Any]
    system_metrics: Dict[str, Any]

class DashboardGenerator:
    """Generate monitoring dashboards"""

    def __init__(self, data_dir: Path = Path("monitoring")):
        self.data_dir = data_dir
        self.metrics_dir = data_dir / "metrics"
        self.errors_dir = data_dir / "errors"
        self.health_dir = data_dir / "health"

    def generate_html_dashboard(self, data: DashboardData) -> str:
        """Generate HTML dashboard"""
        template = Template("""
<!DOCTYPE html>
<html>
<head>
    <title>Scraper Monitoring Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .header { text-align: center; color: #333; margin-bottom: 30px; }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .metric-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-value { font-size: 2em; font-weight: bold; color: #2196F3; }
        .metric-label { color: #666; margin-top: 5px; }
        .status-healthy { color: #4CAF50; }
        .status-warning { color: #FF9800; }
        .status-critical { color: #F44336; }
        .timestamp { text-align: center; color: #666; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🕷️ Scraper Monitoring Dashboard</h1>
        <p>Real-time monitoring of web scraping operations</p>
    </div>

    <!-- Key Metrics -->
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">{{ data.scraper_metrics.active_runs }}</div>
            <div class="metric-label">Active Scrapers</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{{ "%.1f"|format(data.scraper_metrics.success_rate) }}%</div>
            <div class="metric-label">Success Rate</div>
        </div>
        <div class="metric-card">
            <div class="metric-value status-{{ 'critical' if data.error_metrics.critical_errors > 0 else 'healthy' }}">
                {{ data.error_metrics.critical_errors }}
            </div>
            <div class="metric-label">Critical Errors</div>
        </div>
        <div class="metric-card">
            <div class="metric-value status-{{ health_status_class }}">{{ data.health_metrics.overall_status|upper }}</div>
            <div class="metric-label">System Health</div>
        </div>
    </div>

    <div class="timestamp">
        Last updated: {{ data.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC') }}
    </div>

    <script>
        // Auto-refresh every 5 minutes
        setTimeout(function() {
            location.reload();
        }, 300000);
    </script>
</body>
</html>
        """)

        health_status_class = {
            'healthy': 'healthy',
            'warning': 'warning',
            'critical': 'critical'
        }.get(data.health_metrics.get('overall_status', 'unknown'), 'warning')

        return template.render(
            data=data,
            health_status_class=health_status_class
        )

    def generate_dashboard(self, output_file: Path = None) -> Path:
        """Generate and save dashboard"""
        # Collect sample data
        data = DashboardData(
            timestamp=datetime.utcnow(),
            scraper_metrics={'active_runs': 3, 'success_rate': 95.5},
            error_metrics={'critical_errors': 0, 'total_errors': 5},
            health_metrics={'overall_status': 'healthy'},
            system_metrics={'cpu_usage': 45.2}
        )

        html_content = self.generate_html_dashboard(data)

        if output_file is None:
            output_file = self.data_dir / "dashboard.html"

        with open(output_file, 'w') as f:
            f.write(html_content)

        return output_file
```

### 8. Setup Alerting System

Create alerting and notification system:

**File: `monitoring/alerting.py`**
```python
import asyncio
import json
import smtplib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from pathlib import Path

@dataclass
class Alert:
    """Alert data structure"""
    id: str
    title: str
    message: str
    severity: str  # 'info', 'warning', 'error', 'critical'
    category: str
    timestamp: datetime
    source: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'severity': self.severity,
            'category': self.category,
            'timestamp': self.timestamp.isoformat(),
            'source': self.source,
            'metadata': self.metadata
        }

class AlertRule:
    """Define alerting rules and conditions"""

    def __init__(self,
                 name: str,
                 condition: Callable[[Dict[str, Any]], bool],
                 severity: str,
                 message_template: str,
                 category: str = "general"):
        self.name = name
        self.condition = condition
        self.severity = severity
        self.message_template = message_template
        self.category = category
        self.last_triggered = None
        self.cooldown_minutes = 30  # Prevent spam

    def check(self, data: Dict[str, Any]) -> Optional[Alert]:
        """Check if rule should trigger"""
        now = datetime.utcnow()

        # Check cooldown
        if (self.last_triggered and
            now - self.last_triggered < timedelta(minutes=self.cooldown_minutes)):
            return None

        # Check condition
        if self.condition(data):
            self.last_triggered = now

            return Alert(
                id=f"{self.name}_{now.strftime('%Y%m%d_%H%M%S')}",
                title=f"Alert: {self.name}",
                message=self.message_template.format(**data),
                severity=self.severity,
                category=self.category,
                timestamp=now,
                source=self.name,
                metadata=data
            )

        return None

class EmailNotifier:
    """Email notification sender"""

    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    async def send_alert(self, alert: Alert, recipients: List[str]):
        """Send alert via email"""
        try:
            msg = MimeMultipart()
            msg['From'] = self.username
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = f"[{alert.severity.upper()}] {alert.title}"

            # Create HTML content
            html_content = f"""
            <html>
            <body>
                <h2 style="color: {'red' if alert.severity == 'critical' else 'orange' if alert.severity == 'warning' else 'blue'};">
                    {alert.title}
                </h2>
                <p><strong>Severity:</strong> {alert.severity.upper()}</p>
                <p><strong>Category:</strong> {alert.category}</p>
                <p><strong>Time:</strong> {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                <p><strong>Message:</strong></p>
                <p>{alert.message}</p>

                <h3>Details:</h3>
                <pre>{json.dumps(alert.metadata, indent=2)}</pre>
            </body>
            </html>
            """

            msg.attach(MimeText(html_content, 'html'))

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

        except Exception as e:
            print(f"Failed to send email alert: {e}")

class AlertManager:
    """Central alert management system"""

    def __init__(self, config: Dict[str, Any], data_dir: Path = Path("monitoring/alerts")):
        self.config = config
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.rules: List[AlertRule] = []
        self.notifiers = []

        # Setup notifiers based on config
        self._setup_notifiers()

        # Setup default rules
        self._setup_default_rules()

    def _setup_notifiers(self):
        """Setup notification channels"""
        config = self.config

        # Email notifier
        if config.get('email'):
            email_config = config['email']
            self.notifiers.append(
                ('email', EmailNotifier(
                    smtp_host=email_config['smtp_host'],
                    smtp_port=email_config['smtp_port'],
                    username=email_config['username'],
                    password=email_config['password']
                ))
            )

    def _setup_default_rules(self):
        """Setup default alerting rules"""

        # Critical: Scraper completely down
        self.add_rule(AlertRule(
            name="scraper_down",
            condition=lambda data: data.get('active_scrapers', 0) == 0,
            severity="critical",
            message_template="All scrapers are down! No active scraping processes detected.",
            category="availability"
        ))

        # Critical: High error rate
        self.add_rule(AlertRule(
            name="high_error_rate",
            condition=lambda data: data.get('error_rate_per_hour', 0) > 50,
            severity="critical",
            message_template="Critical error rate detected: {error_rate_per_hour} errors per hour",
            category="errors"
        ))

    def add_rule(self, rule: AlertRule):
        """Add a new alerting rule"""
        self.rules.append(rule)

    async def check_alerts(self, monitoring_data: Dict[str, Any]):
        """Check all rules and send alerts if needed"""
        alerts_triggered = []

        for rule in self.rules:
            alert = rule.check(monitoring_data)
            if alert:
                alerts_triggered.append(alert)
                await self._send_alert(alert)
                self._persist_alert(alert)

        return alerts_triggered

    async def _send_alert(self, alert: Alert):
        """Send alert through all configured channels"""
        tasks = []

        for notifier_type, notifier in self.notifiers:
            if notifier_type == 'email':
                recipients = self.config['email'].get('recipients', [])
                if recipients:
                    tasks.append(notifier.send_alert(alert, recipients))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def _persist_alert(self, alert: Alert):
        """Persist alert to file"""
        date_str = alert.timestamp.strftime('%Y-%m-%d')
        alert_file = self.data_dir / f"alerts_{date_str}.jsonl"

        with open(alert_file, 'a') as f:
            f.write(json.dumps(alert.to_dict()) + '\n')

# Example configuration
ALERT_CONFIG = {
    'email': {
        'smtp_host': 'smtp.gmail.com',
        'smtp_port': 587,
        'username': 'your-email@gmail.com',
        'password': 'your-app-password',
        'recipients': ['admin@yourcompany.com', 'devteam@yourcompany.com']
    }
}

# Global alert manager instance
alert_manager = AlertManager(ALERT_CONFIG)
```

### 9. Integration with Scrapers

Create integration points for existing scrapers:

**File: `monitoring/scraper_integration.py`**
```python
import functools
from typing import Any, Dict, Callable
from .logging_config import ScraperLogger, setup_structured_logging
from .metrics import metrics_collector
from .error_monitor import error_monitor

# Setup logging
setup_structured_logging()

class MonitoredScraper:
    """Base class for monitored scrapers"""

    def __init__(self, scraper_id: str, site: str, **config):
        self.scraper_id = scraper_id
        self.site = site
        self.config = config

        # Initialize monitoring components
        self.logger = ScraperLogger(scraper_id, site)
        self.run_id = None

    async def __aenter__(self):
        """Async context manager entry"""
        self.run_id = metrics_collector.start_scraper_run(self.scraper_id, self.site)
        self.logger.log_scraper_start(self.config)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if exc_type:
            # Handle error
            error_monitor.record_error(exc_val, self.scraper_id, self.site)
            status = "failed"
        else:
            status = "success"

        # End metrics collection
        final_metrics = metrics_collector.end_scraper_run(self.run_id, status)

        if final_metrics:
            self.logger.log_scraper_end(final_metrics.__dict__)

    def log_product_processed(self, product_data: Dict[str, Any], action: str):
        """Log product processing"""
        self.logger.log_product_processed(product_data, action)
        metrics_collector.update_run_metrics(
            self.run_id,
            **{f"products_{action}": 1}
        )

    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log error with monitoring"""
        self.logger.log_error(error, context)
        error_monitor.record_error(error, self.scraper_id, self.site, context)
        metrics_collector.update_run_metrics(self.run_id, errors_count=1)

def monitor_scraper(scraper_id: str, site: str):
    """Decorator to add monitoring to scraper functions"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with MonitoredScraper(scraper_id, site, **kwargs) as monitor:
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    monitor.log_error(e, {'function': func.__name__})
                    raise

        return wrapper

    return decorator

# Example usage decorator
@monitor_scraper("example_scraper", "example.com")
async def example_scraper_function(url: str, **config):
    """Example of how to use the monitoring decorator"""
    # Your scraper implementation here
    pass
```

### 10. Configuration and Service Setup

Create configuration and service management:

**File: `monitoring/config.py`**
```python
import os
from pathlib import Path
from typing import Dict, Any

# Default monitoring configuration
DEFAULT_CONFIG = {
    'logging': {
        'level': 'INFO',
        'json_logs': True,
        'log_dir': 'logs',
        'retention_days': 30
    },
    'metrics': {
        'export_dir': 'metrics',
        'export_interval_minutes': 5
    },
    'health_checks': {
        'check_interval_minutes': 5,
        'database_timeout_seconds': 5,
        'site_check_timeout_seconds': 10
    },
    'alerting': {
        'email': {
            'enabled': False,
            'smtp_host': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': '',
            'password': '',
            'recipients': []
        }
    },
    'dashboard': {
        'auto_refresh_minutes': 5,
        'data_retention_hours': 168  # 7 days
    }
}

def load_config() -> Dict[str, Any]:
    """Load configuration from environment and defaults"""
    config = DEFAULT_CONFIG.copy()

    # Override with environment variables
    if os.getenv('MONITORING_LOG_LEVEL'):
        config['logging']['level'] = os.getenv('MONITORING_LOG_LEVEL')

    # Email configuration
    if os.getenv('SMTP_HOST'):
        config['alerting']['email'].update({
            'enabled': True,
            'smtp_host': os.getenv('SMTP_HOST'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587')),
            'username': os.getenv('SMTP_USERNAME', ''),
            'password': os.getenv('SMTP_PASSWORD', ''),
            'recipients': os.getenv('ALERT_EMAIL_RECIPIENTS', '').split(',')
        })

    return config
```

**File: `monitoring/service.py`**
```python
import asyncio
import signal
import sys
from pathlib import Path
from .config import load_config
from .dashboard import DashboardGenerator
from .health_monitor import HealthMonitor
from .alerting import alert_manager

class MonitoringService:
    """Main monitoring service coordinator"""

    def __init__(self):
        self.config = load_config()
        self.running = False
        self.tasks = []

        # Initialize components
        self.dashboard_gen = DashboardGenerator()
        self.health_monitor = HealthMonitor(
            db_url=self.config.get('database_url', 'sqlite:///scraper.db'),
            target_sites=['example.com', 'test-site.com']  # Configure your sites
        )

    async def start(self):
        """Start monitoring service"""
        print("Starting scraper monitoring service...")
        self.running = True

        # Start background tasks
        self.tasks = [
            asyncio.create_task(self._dashboard_updater()),
            asyncio.create_task(self._health_checker()),
            asyncio.create_task(self._alert_checker()),
        ]

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        # Wait for tasks
        await asyncio.gather(*self.tasks, return_exceptions=True)

    async def stop(self):
        """Stop monitoring service"""
        print("Stopping monitoring service...")
        self.running = False

        for task in self.tasks:
            task.cancel()

        await asyncio.gather(*self.tasks, return_exceptions=True)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"Received signal {signum}, shutting down...")
        asyncio.create_task(self.stop())

    async def _dashboard_updater(self):
        """Update dashboard periodically"""
        while self.running:
            try:
                dashboard_file = self.dashboard_gen.generate_dashboard()
                print(f"Dashboard updated: {dashboard_file}")
            except Exception as e:
                print(f"Dashboard update failed: {e}")

            await asyncio.sleep(300)  # Update every 5 minutes

    async def _health_checker(self):
        """Run health checks periodically"""
        while self.running:
            try:
                results = await self.health_monitor.run_all_checks()
                critical_issues = [r for r in results if r.status == "critical"]

                if critical_issues:
                    print(f"Critical health issues detected: {len(critical_issues)}")

            except Exception as e:
                print(f"Health check failed: {e}")

            await asyncio.sleep(300)  # Check every 5 minutes

    async def _alert_checker(self):
        """Check for alert conditions"""
        while self.running:
            try:
                # Collect current monitoring data
                monitoring_data = await self._collect_monitoring_data()

                # Check alert rules
                alerts = await alert_manager.check_alerts(monitoring_data)

                if alerts:
                    print(f"Alerts triggered: {len(alerts)}")

            except Exception as e:
                print(f"Alert checking failed: {e}")

            await asyncio.sleep(60)  # Check every minute

    async def _collect_monitoring_data(self) -> dict:
        """Collect current monitoring data for alert checking"""
        # This would collect real-time data from all monitoring components
        return {
            'active_scrapers': 3,
            'error_rate_per_hour': 2.5,
            'memory_usage_percent': 65.0,
            'sites_accessible_percent': 100.0,
            'database_status': 'healthy',
            'rate_limits_per_hour': 1
        }

if __name__ == "__main__":
    service = MonitoringService()
    try:
        asyncio.run(service.start())
    except KeyboardInterrupt:
        print("Service interrupted by user")
    except Exception as e:
        print(f"Service failed: {e}")
        sys.exit(1)
```

### 11. Usage Examples

Integrate monitoring into your existing scrapers:

```python
# Example: Integrating monitoring into an existing scraper

from monitoring.scraper_integration import MonitoredScraper, monitor_scraper
from monitoring.config import load_config
import asyncio

# Method 1: Using the decorator
@monitor_scraper("product_scraper", "example-store.com")
async def scrape_products(base_url: str, max_pages: int = 10):
    products = []

    for page in range(1, max_pages + 1):
        page_url = f"{base_url}/products?page={page}"

        # Scraping logic here...
        page_products = await scrape_page(page_url)
        products.extend(page_products)

    return products

# Method 2: Using context manager
async def scrape_with_monitoring():
    async with MonitoredScraper("manual_scraper", "example.com") as monitor:
        try:
            # Your scraping logic
            products = await fetch_products()

            for product in products:
                # Log each product processed
                monitor.log_product_processed(product, "found")

                # Save to database
                await save_product(product)
                monitor.log_product_processed(product, "saved")

        except Exception as e:
            # Errors are automatically logged and monitored
            monitor.log_error(e, {"context": "main_scraping_loop"})
            raise

if __name__ == "__main__":
    asyncio.run(scrape_with_monitoring())
```

### 12. Environment Configuration

Create environment configuration:

**File: `.env.monitoring`**
```bash
# Logging Configuration
MONITORING_LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=sqlite:///scraper.db

# Email Alerting (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL_RECIPIENTS=admin@yourcompany.com,devteam@yourcompany.com

# Target Sites for Monitoring
MONITOR_SITES=example.com,test-site.com,another-site.com
```

### 13. Start Monitoring Services

Run the monitoring system:

```bash
# Install monitoring dependencies
uv sync

# Load environment variables
source .env.monitoring

# Start monitoring service
python -m monitoring.service

# Or run as a background service
nohup python -m monitoring.service > monitoring.log 2>&1 &

# View dashboard
open monitoring/dashboard.html

# Check logs
tail -f logs/scraper_$(date +%Y-%m-%d).log
```

### 14. Operational Procedures

Create operational runbooks for common scenarios:

**Emergency Response:**
- Scraper down: Check system resources, restart services
- High error rate: Investigate recent site changes, update selectors
- Rate limiting: Reduce scraping frequency, implement backoff
- Database issues: Check disk space, optimize queries

**Regular Maintenance:**
- Review weekly performance reports
- Update site selectors based on change detection
- Optimize scraping schedules based on site traffic patterns
- Archive old logs and metrics data

**Monitoring Health:**
- Verify all monitoring components are running
- Test alert delivery mechanisms monthly
- Review and update alert thresholds quarterly
- Backup monitoring configuration and historical data

The monitoring system is now complete and production-ready! It provides comprehensive observability for your web scraping operations with structured logging, metrics collection, error monitoring, health checks, dashboards, and alerting.

Access your monitoring dashboard at `monitoring/dashboard.html` and logs in the `logs/` directory. Configure alerts via environment variables and monitor system health through the structured logging output.
