# Python Optimize Imports

Comprehensive Python import optimization for performance, organization, and maintainability using modern tools and best practices

## Instructions

Optimize Python imports systematically following these steps: **$ARGUMENTS**

1. **Import Analysis and Setup**
   - Analyze current import patterns and module dependencies
   - Check Python version compatibility and import performance implications
   - Review project structure and module organization
   - Install optimization tools with uv:
   ```bash
   uv add --dev isort autoflake unimport vulture
   uv add --dev importtime-waterfall pydeps pipdeptree
   uv add --dev ruff pyupgrade
   ```
   - Set up analysis output directories and logging

2. **Import Performance Profiling**
   - Profile module loading times using importtime:
   ```bash
   python -X importtime -c "import your_module" 2> import_profile.log
   uv run python -X importtime your_app.py 2> startup_profile.log
   ```
   - Use importtime-waterfall for visual analysis:
   ```bash
   uv run importtime-waterfall import_profile.log
   ```
   - Measure application startup time:
   ```python
   import time
   start_time = time.perf_counter()
   # Your imports here
   import_time = time.perf_counter() - start_time
   print(f"Import time: {import_time:.4f} seconds")
   ```
   - Identify slowest imports and heavy dependencies

3. **Unused Import Detection and Removal**
   - Use autoflake for automatic unused import removal:
   ```bash
   uv run autoflake --remove-all-unused-imports --recursive --in-place .
   uv run autoflake --remove-unused-variables --recursive --in-place .
   ```
   - Use unimport for comprehensive unused import analysis:
   ```bash
   uv run unimport --check --diff .
   uv run unimport --remove-all .
   ```
   - Use vulture for dead code detection:
   ```bash
   uv run vulture . --min-confidence 60
   uv run vulture . --make-whitelist > whitelist.py
   ```
   - Manual review of flagged imports and false positives

4. **Import Organization and Sorting**
   - Configure isort for consistent import organization:
   ```toml
   [tool.isort]
   profile = "black"
   multi_line_output = 3
   line_length = 88
   known_first_party = ["your_package"]
   known_third_party = ["requests", "pandas", "numpy"]
   sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
   force_alphabetical_sort_within_sections = true
   group_by_package = true
   ```
   - Run import sorting:
   ```bash
   uv run isort . --check-only --diff
   uv run isort . --atomic
   ```
   - Use ruff for additional import organization:
   ```bash
   uv run ruff check --select I --fix .
   ```

5. **Lazy Loading Implementation**
   - Implement lazy imports for heavy modules:
   ```python
   # Traditional import
   import pandas as pd

   # Lazy import pattern
   def get_pandas():
       global pd
       if 'pd' not in globals():
           import pandas as pd
       return pd

   # Usage
   def process_data():
       pd = get_pandas()
       return pd.DataFrame(data)
   ```
   - Use importlib for dynamic imports:
   ```python
   import importlib

   def lazy_import(module_name):
       return importlib.import_module(module_name)

   # Conditional imports
   def get_optional_dependency():
       try:
           return importlib.import_module('optional_package')
       except ImportError:
           return None
   ```

6. **Import-on-Demand Patterns**
   - Implement context-specific imports:
   ```python
   def require_ml_libraries():
       """Import ML libraries only when needed"""
       global np, sklearn, torch
       if 'np' not in globals():
           import numpy as np
           import sklearn
           try:
               import torch
           except ImportError:
               torch = None
       return np, sklearn, torch

   def ml_function():
       np, sklearn, torch = require_ml_libraries()
       # Use libraries here
   ```
   - Use TYPE_CHECKING for type-only imports:
   ```python
   from typing import TYPE_CHECKING

   if TYPE_CHECKING:
       from expensive_module import ExpensiveClass
   else:
       ExpensiveClass = None

   def function() -> 'ExpensiveClass':
       if ExpensiveClass is None:
           from expensive_module import ExpensiveClass
       return ExpensiveClass()
   ```

7. **Dependency Graph Analysis**
   - Create dependency visualization with pydeps:
   ```bash
   uv run pydeps your_package --show-deps --max-bacon=3
   uv run pydeps . --cluster --show-cycles
   ```
   - Analyze pip dependency tree:
   ```bash
   uv run pipdeptree --warn silence
   uv run pipdeptree --graph-output png > dependencies.png
   ```
   - Identify circular imports and dependency cycles
   - Map heavy dependencies and optimization opportunities

8. **Circular Import Resolution**
   - Detect circular imports:
   ```python
   import ast
   import os

   def find_circular_imports(directory):
       imports = {}
       for root, dirs, files in os.walk(directory):
           for file in files:
               if file.endswith('.py'):
                   filepath = os.path.join(root, file)
                   with open(filepath, 'r') as f:
                       tree = ast.parse(f.read())
                       module_imports = []
                       for node in ast.walk(tree):
                           if isinstance(node, ast.Import):
                               for alias in node.names:
                                   module_imports.append(alias.name)
                           elif isinstance(node, ast.ImportFrom):
                               if node.module:
                                   module_imports.append(node.module)
                       imports[filepath] = module_imports
       return imports
   ```
   - Refactor to eliminate circular dependencies
   - Use dependency injection and interface patterns

9. **Module Loading Optimization**
   - Implement module caching strategies:
   ```python
   import sys
   import importlib.util

   _module_cache = {}

   def cached_import(module_name):
       if module_name not in _module_cache:
           spec = importlib.util.find_spec(module_name)
           module = importlib.util.module_from_spec(spec)
           _module_cache[module_name] = module
           spec.loader.exec_module(module)
       return _module_cache[module_name]
   ```
   - Use __all__ to control public interface:
   ```python
   # In module files
   __all__ = ['public_function', 'PublicClass']

   def public_function():
       pass

   def _private_function():
       pass
   ```
   - Optimize import order for faster loading

10. **Import Performance Measurement**
    - Create import timing decorator:
    ```python
    import time
    import functools

    def time_imports(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"{func.__name__} import time: {end - start:.4f}s")
            return result
        return wrapper

    @time_imports
    def import_heavy_module():
        import pandas as pd
        return pd
    ```
    - Benchmark different import strategies:
    ```python
    import timeit

    # Test traditional vs lazy imports
    traditional = timeit.timeit('import pandas as pd', number=1000)
    lazy = timeit.timeit('lambda: __import__("pandas")', number=1000)
    print(f"Traditional: {traditional:.4f}s, Lazy: {lazy:.4f}s")
    ```

11. **Startup Time Optimization**
    - Profile application startup phases:
    ```python
    import atexit
    import time

    class StartupProfiler:
        def __init__(self):
            self.start_time = time.perf_counter()
            self.checkpoints = []
            atexit.register(self.report)

        def checkpoint(self, name):
            current_time = time.perf_counter()
            self.checkpoints.append((name, current_time - self.start_time))

        def report(self):
            print("Startup Profile:")
            for name, duration in self.checkpoints:
                print(f"  {name}: {duration:.4f}s")

    profiler = StartupProfiler()
    # Add checkpoints after major import groups
    ```
    - Defer heavy imports to runtime:
    ```python
    # Instead of top-level imports
    import matplotlib.pyplot as plt

    # Use function-level imports
    def create_plot():
        import matplotlib.pyplot as plt
        return plt.figure()
    ```

12. **Import Path Optimization**
    - Optimize PYTHONPATH and sys.path:
    ```python
    import sys
    import os

    # Add project root to path efficiently
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    ```
    - Use relative imports appropriately:
    ```python
    # In package structure
    from . import module  # Relative import
    from ..parent import module  # Parent relative import
    ```
    - Configure package discovery and namespace packages

13. **Import Security and Safety**
    - Validate import sources and prevent import hijacking:
    ```python
    import importlib.util
    import os

    def safe_import(module_name, allowed_paths=None):
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            raise ImportError(f"Module {module_name} not found")

        if allowed_paths:
            module_path = spec.origin
            if not any(module_path.startswith(path) for path in allowed_paths):
                raise ImportError(f"Module {module_name} not in allowed paths")

        return importlib.import_module(module_name)
    ```
    - Use requirements.txt hash verification with uv:
    ```bash
    uv pip compile requirements.in --generate-hashes > requirements.txt
    uv pip install -r requirements.txt
    ```

14. **Framework-Specific Import Optimization**
    - **Django**: Optimize Django imports and app loading:
    ```python
    # Use django.utils.module_loading for dynamic imports
    from django.utils.module_loading import import_string

    # Lazy load Django apps
    from django.apps import apps

    def get_model_class(app_label, model_name):
        return apps.get_model(app_label, model_name)
    ```
    - **FastAPI**: Optimize FastAPI imports and dependency injection:
    ```python
    from typing import Annotated
    from fastapi import Depends

    # Lazy dependency loading
    def get_service():
        from .services import MyService
        return MyService()

    async def endpoint(service: Annotated[MyService, Depends(get_service)]):
        return service.process()
    ```

15. **Import Configuration and Automation**
    - Set up pyproject.toml configuration:
    ```toml
    [tool.autoflake]
    remove-all-unused-imports = true
    remove-unused-variables = true
    remove-duplicate-keys = true
    in-place = true
    recursive = true

    [tool.unimport]
    sources = ["src/", "tests/"]
    exclude = ["__init__.py"]
    gitignore = true

    [tool.vulture]
    min_confidence = 60
    paths = ["src/", "tests/"]
    ```
    - Create automation scripts:
    ```toml
    [tool.uv.scripts]
    optimize-imports = [
        "autoflake --remove-all-unused-imports --recursive --in-place .",
        "isort .",
        "ruff check --select I --fix ."
    ]
    check-imports = [
        "unimport --check --diff .",
        "vulture . --min-confidence 60"
    ]
    ```

16. **Import Performance Monitoring**
    - Set up continuous import performance monitoring:
    ```python
    import sys
    import time
    from functools import wraps

    class ImportMonitor:
        def __init__(self):
            self.import_times = {}
            self.original_import = __builtins__.__import__
            __builtins__.__import__ = self.timed_import

        def timed_import(self, name, *args, **kwargs):
            start = time.perf_counter()
            module = self.original_import(name, *args, **kwargs)
            end = time.perf_counter()
            self.import_times[name] = end - start
            return module

        def report(self):
            sorted_imports = sorted(self.import_times.items(),
                                  key=lambda x: x[1], reverse=True)
            for name, duration in sorted_imports[:10]:
                print(f"{name}: {duration:.4f}s")

    # Usage
    monitor = ImportMonitor()
    # Your application code
    monitor.report()
    ```
    - Create import performance regression tests
    - Set up CI/CD import performance checks

17. **Advanced Import Patterns**
    - Implement plugin-based import systems:
    ```python
    import importlib
    import pkgutil

    def load_plugins(package_name):
        plugins = {}
        package = importlib.import_module(package_name)
        for _, name, ispkg in pkgutil.iter_modules(package.__path__):
            if not ispkg:
                module = importlib.import_module(f"{package_name}.{name}")
                plugins[name] = module
        return plugins
    ```
    - Use namespace packages for modular imports:
    ```python
    # In __init__.py files, use implicit namespace packages
    # Remove __init__.py from namespace package directories

    # Configure in pyproject.toml
    [tool.setuptools.packages.find]
    where = ["src"]
    exclude = ["tests*"]
    namespaces = false
    ```

Provide detailed import performance metrics, before/after startup time comparisons, and specific optimization recommendations. Include code examples for implementation and monitoring of import optimizations.
