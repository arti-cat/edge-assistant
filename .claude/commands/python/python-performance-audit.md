# Python Performance Audit

Comprehensive performance analysis for Python applications using modern profiling tools and optimization techniques

## Instructions

Conduct a thorough Python performance audit following these systematic steps:

1. **Environment and Dependencies Analysis**
   - Analyze Python version compatibility and performance implications
   - Review virtual environment setup and package management with uv
   - Identify heavy dependencies and their performance impact
   - Check for outdated packages that may have performance regressions
   - Assess compiled extensions (C extensions, Cython) usage

2. **Setup Modern Profiling Tools**
   - Install performance analysis tools with uv:
   ```bash
   uv add --dev cProfile py-spy memray line-profiler
   uv add --dev memory-profiler psutil py-heat-magic
   uv add --dev pympler objgraph tracemalloc
   ```
   - Configure profiling environment and output directories
   - Set up profiling scripts and automation

3. **CPU Performance Profiling**
   - Run cProfile for comprehensive function-level analysis:
   ```python
   python -m cProfile -o profile.stats -s cumtime your_app.py
   ```
   - Use py-spy for sampling profiler without code modification:
   ```bash
   py-spy record -o profile.svg --duration 60 --pid <PID>
   py-spy top --pid <PID>
   ```
   - Implement line_profiler for line-by-line analysis:
   ```python
   @profile
   def critical_function():
       pass
   ```
   - Identify CPU hotspots, expensive function calls, and algorithmic inefficiencies

4. **Memory Usage Analysis**
   - Use memray for comprehensive memory profiling:
   ```bash
   memray run --live your_app.py
   memray flamegraph memory_profile.bin
   ```
   - Implement tracemalloc for memory allocation tracking:
   ```python
   import tracemalloc
   tracemalloc.start()
   # Your code here
   snapshot = tracemalloc.take_snapshot()
   ```
   - Use memory_profiler for line-by-line memory analysis
   - Identify memory leaks, excessive allocations, and garbage collection issues

5. **Database Query Optimization**
   - Profile database queries using SQLAlchemy echo and logging
   - Use Django Debug Toolbar for Django applications
   - Analyze query patterns with django-silk or similar tools
   - Check for N+1 queries, missing indexes, and inefficient joins
   - Profile connection pooling and connection overhead
   - Implement query result caching where appropriate

6. **Import Performance Analysis**
   - Use importtime to analyze module loading performance:
   ```bash
   python -X importtime -c "import your_module" 2> importtime.log
   ```
   - Identify slow imports and heavy module dependencies
   - Analyze circular imports and import order optimization
   - Profile startup time and lazy loading opportunities
   - Check for unnecessary imports in hot paths

7. **Async/Await Performance Audit**
   - Profile asyncio event loop performance
   - Analyze coroutine creation and scheduling overhead
   - Check for blocking operations in async code
   - Profile concurrent.futures and thread pool usage
   - Identify async/await anti-patterns and synchronization issues
   - Use aiomonitor for live async debugging and profiling

8. **I/O and Network Performance**
   - Profile file I/O operations and disk access patterns
   - Analyze network request patterns and connection reuse
   - Check for synchronous I/O in async contexts
   - Profile serialization/deserialization (JSON, pickle, msgpack)
   - Analyze compression and data transfer efficiency

9. **Data Structure and Algorithm Analysis**
   - Profile list vs set vs dict performance for specific use cases
   - Analyze pandas DataFrame operations and memory usage
   - Check NumPy array operations and vectorization opportunities
   - Profile custom data structures and algorithms
   - Identify opportunities for collections.deque, heapq, or other specialized structures

10. **Memory Leak Detection**
    - Use objgraph to track object references:
    ```python
    import objgraph
    objgraph.show_most_common_types()
    objgraph.show_growth()
    ```
    - Implement pympler for detailed memory analysis
    - Check for unclosed resources (files, connections, threads)
    - Profile generator vs list comprehension memory usage
    - Analyze weakref usage and circular reference patterns

11. **Concurrency and Parallelism Profiling**
    - Profile multiprocessing vs threading performance
    - Analyze GIL (Global Interpreter Lock) impact
    - Check concurrent.futures ThreadPoolExecutor and ProcessPoolExecutor usage
    - Profile asyncio task scheduling and execution
    - Analyze queue performance and producer-consumer patterns

12. **Framework-Specific Performance Analysis**
    - **Django**: Use django-debug-toolbar, django-silk, django-querycount
    - **FastAPI**: Profile request handling, dependency injection, and serialization
    - **Flask**: Analyze route handling, template rendering, and middleware overhead
    - **Celery**: Profile task execution, queue performance, and worker efficiency
    - Check framework-specific caching and optimization features

13. **Compilation and JIT Analysis**
    - Profile PyPy compatibility and JIT compilation benefits
    - Analyze Numba JIT compilation opportunities:
    ```python
    from numba import jit
    @jit(nopython=True)
    def optimized_function():
        pass
    ```
    - Check Cython integration possibilities for performance-critical code
    - Profile compiled extensions and C API usage

14. **Performance Testing and Benchmarking**
    - Set up pytest-benchmark for micro-benchmarks:
    ```python
    def test_performance(benchmark):
        result = benchmark(function_to_test, arg1, arg2)
    ```
    - Implement timeit for precise timing measurements
    - Create performance regression tests
    - Set up continuous performance monitoring

15. **Optimization Recommendations and Implementation**
    - Prioritize optimizations by impact vs effort matrix
    - Implement caching strategies (functools.lru_cache, Redis, Memcached)
    - Optimize data serialization (use orjson instead of json)
    - Implement connection pooling and resource reuse
    - Suggest algorithmic improvements and data structure optimizations
    - Configure production-specific optimizations (bytecode caching, etc.)

16. **Performance Monitoring Setup**
    - Install application performance monitoring (APM) tools
    - Set up custom metrics collection with statsd or Prometheus
    - Configure logging for performance-related events
    - Implement health checks and performance alerts
    - Create performance dashboards and reporting

17. **Production Environment Analysis**
    - Profile application under realistic load conditions
    - Analyze production metrics and bottlenecks
    - Check resource utilization (CPU, memory, disk, network)
    - Profile garbage collection behavior in production
    - Analyze scaling patterns and resource requirements

Provide specific performance metrics, before/after comparisons, and actionable optimization recommendations with estimated performance impact. Include code examples and configuration changes where applicable.
