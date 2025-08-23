# Python Memory Profiling

Comprehensive memory usage analysis and optimization for Python applications using advanced profiling tools and modern memory management techniques

## Instructions

Conduct thorough Python memory profiling and optimization following these systematic steps: **$ARGUMENTS**

1. **Environment Setup and Tool Installation**
   - Install comprehensive memory profiling toolkit with uv:
   ```bash
   uv add --dev memray memory-profiler pympler objgraph
   uv add --dev tracemalloc-tools guppy3 psutil
   uv add --dev py-spy line-profiler scalene
   uv add --dev matplotlib seaborn plotly  # For visualizations
   ```
   - Configure profiling environment and output directories
   - Set up memory profiling automation scripts
   - Verify Python version and memory management features

2. **Baseline Memory Analysis with Memray**
   - Run comprehensive memory profiling with memray:
   ```bash
   # Record memory allocations during program execution
   memray run --live --live-port 8080 your_app.py

   # Generate various analysis reports
   memray flamegraph memory_profile.bin
   memray table memory_profile.bin
   memray tree memory_profile.bin
   memray summary memory_profile.bin

   # Live memory tracking
   memray run --live-mode your_app.py
   ```
   - Analyze allocation patterns, peak memory usage, and allocation sources
   - Identify memory hotspots and high-frequency allocation sites
   - Generate interactive flamegraphs for memory visualization

3. **Built-in Memory Tracking with Tracemalloc**
   ```python
   import tracemalloc
   import linecache
   import os

   def start_memory_tracking():
       """Initialize comprehensive memory tracking"""
       tracemalloc.start()
       return tracemalloc.take_snapshot()

   def analyze_memory_growth(snapshot1, snapshot2):
       """Analyze memory growth between snapshots"""
       top_stats = snapshot2.compare_to(snapshot1, 'lineno')

       print("Top 10 memory growth sources:")
       for index, stat in enumerate(top_stats[:10], 1):
           frame = stat.traceback.format()
           print(f"{index}. {stat.size_diff / 1024 / 1024:.1f} MB")
           print(f"   {frame}")

   def memory_profiler_decorator():
       """Decorator for function-level memory profiling"""
       def decorator(func):
           def wrapper(*args, **kwargs):
               tracemalloc.start()
               result = func(*args, **kwargs)
               current, peak = tracemalloc.get_traced_memory()
               tracemalloc.stop()
               print(f"{func.__name__}: Current={current/1024/1024:.1f}MB, Peak={peak/1024/1024:.1f}MB")
               return result
           return wrapper
       return decorator
   ```

4. **Line-by-Line Memory Analysis**
   ```python
   # Install and use memory_profiler for detailed analysis
   # Add @profile decorator to functions of interest
   from memory_profiler import profile

   @profile
   def memory_intensive_function():
       # Your code here
       large_list = [i for i in range(1000000)]
       return large_list

   # Run with: python -m memory_profiler your_script.py
   ```
   - Use `mprof` for memory usage over time:
   ```bash
   mprof run your_script.py
   mprof plot  # Generate memory usage plots
   ```
   - Analyze memory usage patterns and identify memory spikes

5. **Advanced Memory Leak Detection with Objgraph**
   ```python
   import objgraph
   import gc
   from collections import defaultdict

   class MemoryLeakDetector:
       def __init__(self):
           self.baseline = None
           self.snapshots = []

       def take_baseline(self):
           """Take initial memory baseline"""
           gc.collect()  # Force garbage collection
           self.baseline = objgraph.get_leaking_objects()
           objgraph.show_most_common_types(limit=20)

       def check_for_leaks(self):
           """Check for memory leaks since baseline"""
           if not self.baseline:
               self.take_baseline()
               return

           gc.collect()
           current_objects = objgraph.get_leaking_objects()

           # Show objects that have grown since baseline
           objgraph.show_growth(limit=10)

           # Find reference chains for potential leaks
           leak_candidates = objgraph.by_type('dict')[:5]
           for obj in leak_candidates:
               objgraph.show_backrefs([obj], max_depth=3)

       def find_circular_references(self):
           """Detect circular reference patterns"""
           import weakref
           circular_refs = []

           for obj in gc.get_objects():
               if hasattr(obj, '__dict__'):
                   for attr_name, attr_value in obj.__dict__.items():
                       if attr_value is obj:
                           circular_refs.append((obj, attr_name))

           return circular_refs
   ```

6. **Heap Analysis with Pympler**
   ```python
   from pympler import tracker, muppy, summary
   from pympler.classtracker import ClassTracker
   import sys

   class HeapAnalyzer:
       def __init__(self):
           self.tr = tracker.SummaryTracker()
           self.class_tracker = ClassTracker()

       def start_tracking(self):
           """Begin tracking object allocations"""
           self.tr.print_diff()
           self.class_tracker.track_class(dict)
           self.class_tracker.track_class(list)
           self.class_tracker.track_class(str)

       def analyze_heap(self):
           """Comprehensive heap analysis"""
           # Get all objects in memory
           all_objects = muppy.get_objects()

           # Summarize by type
           sum1 = summary.summarize(all_objects)
           summary.print_(sum1)

           # Track specific object types
           self.class_tracker.create_snapshot('current')
           self.class_tracker.stats.print_summary()

       def memory_profiling_context(self):
           """Context manager for memory profiling"""
           class MemoryContext:
               def __enter__(self):
                   self.initial_memory = self.get_memory_usage()
                   return self

               def __exit__(self, exc_type, exc_val, exc_tb):
                   final_memory = self.get_memory_usage()
                   print(f"Memory used: {final_memory - self.initial_memory:.2f} MB")

               def get_memory_usage(self):
                   return sum(summary.summarize(muppy.get_objects())[0][2] for _ in [0]) / 1024 / 1024

           return MemoryContext()
   ```

7. **Garbage Collection Performance Analysis**
   ```python
   import gc
   import time
   import sys
   from collections import defaultdict

   class GCAnalyzer:
       def __init__(self):
           self.gc_stats = defaultdict(list)
           self.old_gc_stats = gc.get_stats()

       def analyze_gc_performance(self):
           """Analyze garbage collection performance"""
           # Get current GC statistics
           current_stats = gc.get_stats()

           print("Garbage Collection Statistics:")
           for i, stat in enumerate(current_stats):
               print(f"Generation {i}:")
               print(f"  Collections: {stat['collections']}")
               print(f"  Collected: {stat['collected']}")
               print(f"  Uncollectable: {stat['uncollectable']}")

           # Check GC thresholds
           thresholds = gc.get_threshold()
           print(f"GC Thresholds: {thresholds}")

           # Analyze objects by generation
           for generation in range(3):
               objects = gc.get_objects(generation)
               print(f"Generation {generation}: {len(objects)} objects")

       def tune_gc_performance(self):
           """Optimize garbage collection settings"""
           # Disable automatic GC for performance-critical sections
           gc.disable()

           # Custom GC scheduling
           def custom_gc_collect():
               start_time = time.time()
               collected = gc.collect()
               gc_time = time.time() - start_time
               print(f"GC collected {collected} objects in {gc_time:.4f}s")
               return collected

           # Re-enable with custom thresholds
           gc.set_threshold(700, 10, 10)  # Tune based on workload
           gc.enable()

           return custom_gc_collect
   ```

8. **Memory Usage Patterns and Data Structure Analysis**
   ```python
   import sys
   from collections import deque, defaultdict
   import array
   import numpy as np

   class DataStructureAnalyzer:
       def __init__(self):
           self.results = {}

       def compare_data_structures(self, data_size=1000000):
           """Compare memory usage of different data structures"""
           test_data = list(range(data_size))

           # Test list vs array vs numpy
           structures = {
               'list': list(test_data),
               'array': array.array('i', test_data),
               'numpy_array': np.array(test_data, dtype=np.int32),
               'deque': deque(test_data),
               'set': set(test_data),
               'dict': {i: i for i in test_data}
           }

           for name, structure in structures.items():
               memory_usage = sys.getsizeof(structure)
               self.results[name] = memory_usage
               print(f"{name}: {memory_usage / 1024 / 1024:.2f} MB")

           return self.results

       def analyze_string_memory(self):
           """Analyze string memory usage patterns"""
           # String interning analysis
           a = "hello world"
           b = "hello world"
           interned = sys.intern("hello world")

           print(f"String a id: {id(a)}")
           print(f"String b id: {id(b)}")
           print(f"Interned string id: {id(interned)}")
           print(f"a is b: {a is b}")
           print(f"a is interned: {a is interned}")

       def memory_efficient_iteration(self, data):
           """Demonstrate memory-efficient iteration patterns"""
           # Generator vs list comprehension
           def generator_approach():
               return (x * 2 for x in data)

           def list_comprehension_approach():
               return [x * 2 for x in data]

           # Memory usage comparison
           gen = generator_approach()
           lst = list_comprehension_approach()

           print(f"Generator memory: {sys.getsizeof(gen)} bytes")
           print(f"List memory: {sys.getsizeof(lst)} bytes")
   ```

9. **Production Memory Monitoring Setup**
   ```python
   import psutil
   import threading
   import time
   import json
   from datetime import datetime

   class ProductionMemoryMonitor:
       def __init__(self, interval=60, threshold_mb=1000):
           self.interval = interval
           self.threshold_mb = threshold_mb
           self.monitoring = False
           self.metrics = []

       def start_monitoring(self):
           """Start continuous memory monitoring"""
           self.monitoring = True
           monitor_thread = threading.Thread(target=self._monitor_loop)
           monitor_thread.daemon = True
           monitor_thread.start()

       def _monitor_loop(self):
           """Main monitoring loop"""
           process = psutil.Process()

           while self.monitoring:
               try:
                   memory_info = process.memory_info()
                   memory_percent = process.memory_percent()

                   metric = {
                       'timestamp': datetime.now().isoformat(),
                       'rss_mb': memory_info.rss / 1024 / 1024,
                       'vms_mb': memory_info.vms / 1024 / 1024,
                       'percent': memory_percent,
                       'num_threads': process.num_threads(),
                       'open_files': len(process.open_files())
                   }

                   self.metrics.append(metric)

                   # Alert on high memory usage
                   if metric['rss_mb'] > self.threshold_mb:
                       self._send_alert(metric)

                   time.sleep(self.interval)

               except Exception as e:
                   print(f"Monitoring error: {e}")
                   time.sleep(self.interval)

       def _send_alert(self, metric):
           """Send memory usage alert"""
           alert = {
               'type': 'HIGH_MEMORY_USAGE',
               'threshold_mb': self.threshold_mb,
               'current_mb': metric['rss_mb'],
               'timestamp': metric['timestamp']
           }
           print(f"MEMORY ALERT: {json.dumps(alert)}")

       def get_memory_report(self):
           """Generate memory usage report"""
           if not self.metrics:
               return None

           latest = self.metrics[-1]
           peak_memory = max(self.metrics, key=lambda x: x['rss_mb'])

           return {
               'current_memory_mb': latest['rss_mb'],
               'peak_memory_mb': peak_memory['rss_mb'],
               'average_memory_mb': sum(m['rss_mb'] for m in self.metrics) / len(self.metrics),
               'total_measurements': len(self.metrics)
           }
   ```

10. **Memory Optimization Strategies Implementation**
    ```python
    import weakref
    from functools import lru_cache
    import sys

    class MemoryOptimizer:
        def __init__(self):
            self.optimizations = []

        @staticmethod
        def implement_slots_optimization(cls):
            """Add __slots__ to reduce memory overhead"""
            # Example optimization for classes
            class OptimizedClass:
                __slots__ = ['attr1', 'attr2', 'attr3']

                def __init__(self, attr1, attr2, attr3):
                    self.attr1 = attr1
                    self.attr2 = attr2
                    self.attr3 = attr3

            return OptimizedClass

        @staticmethod
        def weak_reference_cache():
            """Implement weak reference caching"""
            class WeakCache:
                def __init__(self):
                    self._cache = weakref.WeakValueDictionary()

                def get_or_create(self, key, factory):
                    obj = self._cache.get(key)
                    if obj is None:
                        obj = factory()
                        self._cache[key] = obj
                    return obj

            return WeakCache()

        @staticmethod
        def memory_efficient_caching():
            """Implement memory-efficient caching strategies"""
            # Use lru_cache with size limits
            @lru_cache(maxsize=128)
            def expensive_computation(x):
                return x ** 2

            # Custom cache with memory limits
            class MemoryLimitedCache:
                def __init__(self, max_memory_mb=100):
                    self.cache = {}
                    self.max_memory_bytes = max_memory_mb * 1024 * 1024

                def set(self, key, value):
                    current_memory = sum(sys.getsizeof(v) for v in self.cache.values())
                    value_size = sys.getsizeof(value)

                    if current_memory + value_size > self.max_memory_bytes:
                        # Evict oldest entries
                        items_to_remove = list(self.cache.keys())[:len(self.cache)//2]
                        for key_to_remove in items_to_remove:
                            del self.cache[key_to_remove]

                    self.cache[key] = value

            return MemoryLimitedCache()
    ```

11. **Memory Profiling Automation and CI Integration**
    ```yaml
    # .github/workflows/memory-profiling.yml
    name: Memory Profiling
    on: [push, pull_request]

    jobs:
      memory-profile:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3

          - name: Set up Python
            uses: actions/setup-python@v4
            with:
              python-version: '3.11'

          - name: Install uv
            run: pip install uv

          - name: Install dependencies
            run: uv sync --dev

          - name: Run memory profiling
            run: |
              uv run memray run --output memory-profile.bin python -m pytest tests/
              uv run memray flamegraph memory-profile.bin
              uv run memray summary memory-profile.bin > memory-report.txt

          - name: Upload memory profile artifacts
            uses: actions/upload-artifact@v3
            with:
              name: memory-profiles
              path: |
                memory-profile.bin
                memory-profile.html
                memory-report.txt
    ```

12. **Memory Profiling Scripts and Automation**
    ```toml
    # Add to pyproject.toml
    [tool.uv.scripts]
    memory-profile = "memray run --live --live-port 8080"
    memory-analyze = "memray flamegraph memory_profile.bin"
    memory-report = [
        "memray summary memory_profile.bin > memory-summary.txt",
        "memray table memory_profile.bin > memory-table.txt"
    ]
    memory-leak-check = "python -m scripts.memory_leak_detector"
    memory-benchmark = "python -m scripts.memory_benchmark"

    [tool.memray]
    output = "profiles/"
    format = "html"

    [tool.memory-profiler]
    precision = 4
    backend = "psutil"
    ```

13. **Advanced Memory Analysis Techniques**
    ```python
    import mmap
    import os
    from contextlib import contextmanager

    class AdvancedMemoryAnalysis:
        @staticmethod
        def memory_mapped_file_analysis(filename):
            """Analyze memory-mapped file usage"""
            with open(filename, 'rb') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    print(f"Memory-mapped file size: {len(mm)} bytes")
                    return mm

        @staticmethod
        @contextmanager
        def memory_profiling_context():
            """Context manager for detailed memory profiling"""
            import tracemalloc
            import psutil

            process = psutil.Process()
            tracemalloc.start()
            start_memory = process.memory_info().rss

            try:
                yield
            finally:
                current, peak = tracemalloc.get_traced_memory()
                end_memory = process.memory_info().rss
                tracemalloc.stop()

                print(f"Memory usage: {(end_memory - start_memory) / 1024 / 1024:.2f} MB")
                print(f"Peak traced memory: {peak / 1024 / 1024:.2f} MB")

        @staticmethod
        def analyze_reference_cycles():
            """Detect and analyze reference cycles"""
            import gc

            # Find objects involved in reference cycles
            gc.collect()
            unreachable = gc.collect()

            if unreachable:
                print(f"Found {unreachable} unreachable objects")

                # Get objects that are part of cycles
                for obj in gc.garbage:
                    print(f"Garbage object: {type(obj)} - {repr(obj)[:100]}")
    ```

14. **Memory Optimization Best Practices**
    - Use generators instead of lists for large datasets
    - Implement `__slots__` for classes with many instances
    - Use weak references to avoid circular references
    - Profile before optimizing - measure actual memory usage
    - Consider using numpy arrays for numerical data
    - Implement lazy loading for large objects
    - Use memory-mapped files for large file processing
    - Clear unused references explicitly with `del`
    - Configure garbage collection thresholds for your workload

15. **Continuous Memory Monitoring Dashboard**
    ```python
    # Create memory monitoring dashboard
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots

    class MemoryDashboard:
        def __init__(self, metrics_data):
            self.metrics = metrics_data

        def create_dashboard(self):
            """Create interactive memory monitoring dashboard"""
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Memory Usage Over Time', 'Memory Distribution',
                              'GC Statistics', 'Memory Alerts'),
                specs=[[{"secondary_y": True}, {}],
                       [{}, {}]]
            )

            # Memory usage timeline
            timestamps = [m['timestamp'] for m in self.metrics]
            memory_usage = [m['rss_mb'] for m in self.metrics]

            fig.add_trace(
                go.Scatter(x=timestamps, y=memory_usage, name='Memory Usage (MB)'),
                row=1, col=1
            )

            # Save dashboard
            fig.write_html("memory_dashboard.html")
            print("Memory dashboard saved to memory_dashboard.html")
    ```

Provide comprehensive memory analysis reports, optimization recommendations, and establish continuous memory monitoring for production environments. Include specific memory metrics, leak detection results, and performance improvement strategies with measurable impact assessments.
