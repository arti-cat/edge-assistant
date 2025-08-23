# Python Debug Setup

Setup comprehensive debugging and development tools for Python projects using modern debugging practices and uv package management

## Instructions

1. **Environment Analysis and Debugging Requirements**
   - Analyze current Python project structure and debugging needs
   - Identify target deployment environments (local, container, remote)
   - Assess team debugging workflows and IDE preferences
   - Check existing debugging configuration and tools
   - Determine performance debugging requirements
   - Evaluate container and remote debugging needs

2. **Core Debugging Tools Installation**
   - Install essential debugging packages with uv:
   ```bash
   uv add --dev debugpy ipdb pdb++ pudb
   uv add --dev icecream rich-traceback better-exceptions
   uv add --dev hunter snoop loguru structlog
   ```
   - Configure debugpy for VS Code and remote debugging
   - Set up enhanced Python debuggers (ipdb, pdb++, pudb)
   - Install visual debugging and tracing tools

3. **VS Code Debugging Configuration**
   - Create `.vscode/launch.json` with comprehensive debug configurations:
   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Python: Current File",
         "type": "python",
         "request": "launch",
         "program": "${file}",
         "console": "integratedTerminal",
         "justMyCode": false,
         "env": {"PYTHONPATH": "${workspaceFolder}"}
       },
       {
         "name": "Python: Remote Attach",
         "type": "python",
         "request": "attach",
         "connect": {"host": "localhost", "port": 5678},
         "pathMappings": [{"localRoot": "${workspaceFolder}", "remoteRoot": "/app"}]
       },
       {
         "name": "Python: Django Debug",
         "type": "python",
         "request": "launch",
         "program": "${workspaceFolder}/manage.py",
         "args": ["runserver", "--noreload"],
         "django": true,
         "justMyCode": false
       },
       {
         "name": "Python: FastAPI Debug",
         "type": "python",
         "request": "launch",
         "module": "uvicorn",
         "args": ["main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
         "jinja": true,
         "justMyCode": false
       }
     ]
   }
   ```

4. **Enhanced Debugger Configuration**
   - Configure ipdb as default debugger in pyproject.toml:
   ```toml
   [tool.ipdb]
   context = 5
   colors = "light"
   ```
   - Set up pdb++ configuration in ~/.pdbrc:
   ```python
   # Enhanced pdb++ configuration
   import pdb
   class Config(pdb.DefaultConfig):
       sticky_by_default = True
       current_line_color = 40
       use_pygments = True
       bg = "dark"
       colorscheme = "vim"
   ```
   - Configure pudb for visual debugging interface
   - Set up PYTHONBREAKPOINT environment variable for quick debugging

5. **Remote and Container Debugging Setup**
   - Configure debugpy server for remote debugging:
   ```python
   # debug_server.py
   import debugpy
   debugpy.listen(("0.0.0.0", 5678))
   print("Waiting for debugger attach...")
   debugpy.wait_for_client()
   ```
   - Create Docker debugging configuration:
   ```dockerfile
   # Add to Dockerfile for debugging
   RUN pip install debugpy
   EXPOSE 5678
   CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "your_app"]
   ```
   - Set up docker-compose debugging services
   - Configure Kubernetes debugging with debugpy

6. **Profiling and Performance Debugging Tools**
   - Install profiling tools with uv:
   ```bash
   uv add --dev cProfile py-spy memray line-profiler
   uv add --dev memory-profiler psutil pympler tracemalloc
   uv add --dev scalene austin-python
   ```
   - Configure line_profiler for line-by-line analysis
   - Set up py-spy for live profiling without code modification
   - Configure memray for memory profiling and leak detection
   - Install scalene for CPU and memory profiling

7. **Logging and Debug Output Management**
   - Configure structured logging with loguru:
   ```python
   # logging_config.py
   from loguru import logger
   import sys

   logger.remove()
   logger.add(
       sys.stderr,
       format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
       level="DEBUG"
   )
   logger.add("debug.log", rotation="10 MB", retention="7 days", level="DEBUG")
   ```
   - Set up structured logging with structlog for complex applications
   - Configure debug logging levels and output formatting
   - Set up log aggregation and analysis tools
   - Create debug logging decorators and context managers

8. **Interactive Debugging Enhancements**
   - Install and configure icecream for print debugging:
   ```python
   # debug_utils.py
   from icecream import ic
   ic.configureOutput(prefix='Debug | ')
   ic.includeContext = True
   ```
   - Set up rich-traceback for enhanced error messages
   - Configure better-exceptions for improved traceback formatting
   - Install ptpython or ipython for enhanced REPL debugging
   - Set up debugging utilities and helper functions

9. **Code Tracing and Inspection Tools**
   - Configure hunter for advanced code tracing:
   ```python
   # trace_config.py
   import hunter
   hunter.trace(
       hunter.Q(module__contains='your_module'),
       action=hunter.CallPrinter(stream=open('trace.log', 'w'))
   )
   ```
   - Set up snoop for function call tracing and variable inspection
   - Configure sys.settrace for custom debugging workflows
   - Install and configure objgraph for object reference tracking
   - Set up code coverage tools for debugging test coverage

10. **Testing and Debug Integration**
    - Configure pytest with debugging plugins:
    ```bash
    uv add --dev pytest-xdist pytest-cov pytest-mock
    uv add --dev pytest-sugar pytest-clarity pytest-html
    uv add --dev pytest-benchmark pytest-timeout
    ```
    - Set up pytest debugging configurations in pyproject.toml:
    ```toml
    [tool.pytest.ini_options]
    addopts = "-v --tb=short --strict-markers --disable-warnings"
    testpaths = ["tests"]
    python_files = ["test_*.py", "*_test.py"]
    markers = [
        "slow: marks tests as slow",
        "integration: marks tests as integration tests",
        "debug: marks tests for debugging"
    ]
    ```
    - Configure test debugging workflows and breakpoint strategies

11. **Framework-Specific Debugging Setup**
    - **Django Debug Configuration**:
    ```python
    # settings/debug.py
    INSTALLED_APPS += ['debug_toolbar', 'django_extensions']
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
    INTERNAL_IPS = ['127.0.0.1', 'localhost']
    DEBUG_TOOLBAR_CONFIG = {'SHOW_TEMPLATE_CONTEXT': True}
    ```
    - **FastAPI Debug Setup**:
    ```python
    # debug_middleware.py
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn

    app = FastAPI(debug=True)
    if __name__ == "__main__":
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
    ```
    - **Flask Debug Configuration**:
    ```python
    # debug_config.py
    from flask_debugtoolbar import DebugToolbarExtension
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'debug-secret-key'
    toolbar = DebugToolbarExtension(app)
    ```

12. **Memory Debugging and Leak Detection**
    - Set up tracemalloc for memory allocation tracking:
    ```python
    # memory_debug.py
    import tracemalloc
    tracemalloc.start()

    # Your application code

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    for stat in top_stats[:10]:
        print(stat)
    ```
    - Configure pympler for detailed memory analysis
    - Set up objgraph for reference cycle detection
    - Install memory_profiler for line-by-line memory usage
    - Configure weakref monitoring for garbage collection debugging

13. **Async/Concurrency Debugging**
    - Configure asyncio debugging and warnings:
    ```python
    # async_debug.py
    import asyncio
    import warnings
    asyncio.get_event_loop().set_debug(True)
    warnings.simplefilter('always', ResourceWarning)
    ```
    - Install aiomonitor for async debugging:
    ```bash
    uv add --dev aiomonitor aiohttp-devtools
    ```
    - Set up concurrent.futures debugging for thread/process pools
    - Configure asyncio task tracking and leak detection

14. **Exception Handling and Error Debugging**
    - Configure comprehensive exception handling:
    ```python
    # exception_debug.py
    import sys
    import traceback
    from rich.traceback import install
    install(show_locals=True)

    def debug_exception_handler(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        print("Uncaught exception:", file=sys.stderr)
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)

    sys.excepthook = debug_exception_handler
    ```
    - Set up Sentry or similar error tracking for production debugging
    - Configure custom exception classes for better debugging context
    - Set up error logging and notification systems

15. **Development Environment Debug Workflows**
    - Create debug utility scripts and commands:
    ```python
    # debug_cli.py
    import click
    import subprocess

    @click.group()
    def debug():
        """Debug utilities for development"""
        pass

    @debug.command()
    @click.argument('pid', type=int)
    def profile(pid):
        """Profile running process with py-spy"""
        subprocess.run(['py-spy', 'record', '-o', 'profile.svg', '--pid', str(pid)])

    @debug.command()
    def memory():
        """Start memory profiling session"""
        subprocess.run(['python', '-m', 'memray', 'run', '--live', 'your_app.py'])
    ```
    - Set up debug environment variables and configuration
    - Configure hot-reloading with debugging capabilities
    - Create debugging checklists and workflows

16. **IDE Integration and Tool Configuration**
    - Configure PyCharm debugging settings and breakpoints
    - Set up Vim/Neovim debugging with vimspector or nvim-dap
    - Configure Emacs debugging with dap-mode
    - Set up debugging keybindings and shortcuts
    - Configure debugging plugins and extensions

17. **Production Debugging and Monitoring**
    - Set up APM integration (New Relic, DataDog, etc.):
    ```bash
    uv add newrelic
    ```
    - Configure production-safe debugging techniques
    - Set up remote logging and monitoring
    - Configure health check debugging endpoints
    - Set up debugging flags and feature toggles

18. **Debug Documentation and Best Practices**
    - Create debugging runbooks and troubleshooting guides
    - Document common debugging scenarios and solutions
    - Set up debugging workflow documentation
    - Create debugging checklists for different issue types
    - Document performance debugging procedures

19. **Automated Debug Analysis**
    - Set up automated debugging reports and analysis
    - Configure debug log analysis and alerting
    - Set up regression testing for debugging tools
    - Create automated debugging workflows with CI/CD
    - Configure debug metric collection and reporting

20. **Validation and Testing**
    - Test all debugging configurations and tools
    - Verify VS Code debugging functionality
    - Test remote and container debugging setups
    - Validate profiling and performance debugging tools
    - Test logging and error tracking integration
    - Verify framework-specific debugging configurations
    - Create debugging validation script: `uv run python -c "import debugpy, ipdb, icecream; print('All debugging tools installed successfully!')"`

Provide comprehensive debugging setup with modern Python debugging practices, IDE integration, and production-ready debugging workflows that enhance development productivity and troubleshooting capabilities.
