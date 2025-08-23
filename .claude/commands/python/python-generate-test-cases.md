# Python Generate Test Cases

Automatically generate comprehensive test cases for Python projects using modern testing frameworks and tools

## Instructions

1. **Project and Target Analysis**
   - Parse target file, class, or function from arguments: `$ARGUMENTS`
   - If no target specified, analyze current Python project structure
   - Examine Python version, framework (Django, Flask, FastAPI, etc.), and dependencies
   - Identify testing framework in use (pytest preferred) or recommend setup
   - Analyze code structure, type hints, docstrings, and existing test patterns

2. **Python Code Structure Analysis**
   - Parse function signatures, type annotations, and return types
   - Extract docstring information for test scenario generation
   - Analyze class inheritance, methods, and property definitions
   - Identify async/await patterns, coroutines, and concurrency
   - Examine error handling, exceptions, and validation logic
   - Review data models, serializers, and business logic patterns

3. **Modern Python Testing Framework Setup**
   - Install comprehensive testing stack with uv:
   ```bash
   uv add --dev pytest pytest-cov pytest-asyncio pytest-mock
   uv add --dev pytest-xdist pytest-benchmark pytest-timeout
   uv add --dev hypothesis pytest-sugar pytest-clarity
   ```
   - Configure pytest.ini or pyproject.toml with modern settings:
   ```toml
   [tool.pytest.ini_options]
   testpaths = ["tests"]
   python_files = ["test_*.py", "*_test.py"]
   python_classes = ["Test*", "*Tests"]
   python_functions = ["test_*"]
   addopts = "-v --tb=short --strict-markers --strict-config"
   markers = [
       "unit: Unit tests",
       "integration: Integration tests",
       "e2e: End-to-end tests",
       "slow: Slow running tests",
       "async: Async tests",
       "property: Property-based tests",
   ]
   asyncio_mode = "auto"
   timeout = 300
   ```

4. **Test File Generation and Structure**
   - Create test files following Python conventions (test_*.py)
   - Generate comprehensive test directory structure:
   ```
   tests/
   ├── conftest.py
   ├── unit/
   │   ├── __init__.py
   │   ├── test_models.py
   │   ├── test_services.py
   │   └── test_utils.py
   ├── integration/
   │   ├── __init__.py
   │   ├── test_api.py
   │   └── test_database.py
   ├── e2e/
   │   ├── __init__.py
   │   └── test_workflows.py
   ├── fixtures/
   │   ├── __init__.py
   │   ├── sample_data.py
   │   └── factories.py
   └── property/
       ├── __init__.py
       └── test_properties.py
   ```

5. **Unit Test Case Generation**
   - Generate pytest test classes and functions with descriptive names
   - Create tests for all public methods and functions
   - Generate tests based on type hints and docstring examples:
   ```python
   import pytest
   from hypothesis import given, strategies as st
   from unittest.mock import Mock, patch, AsyncMock

   class TestUserService:
       @pytest.fixture
       def user_service(self):
           return UserService()

       def test_create_user_valid_data(self, user_service):
           # Test normal operation
           pass

       def test_create_user_invalid_email_raises_validation_error(self, user_service):
           # Test validation
           pass

       @pytest.mark.asyncio
       async def test_async_user_creation(self, user_service):
           # Test async operations
           pass
   ```

6. **Property-Based Testing with Hypothesis**
   - Install and configure hypothesis: `uv add --dev hypothesis`
   - Generate property-based tests for functions with clear invariants:
   ```python
   from hypothesis import given, strategies as st, assume

   @given(st.text(min_size=1), st.integers(min_value=0))
   def test_string_processing_properties(text, count):
       assume(len(text.strip()) > 0)
       result = process_string(text, count)
       assert isinstance(result, str)
       assert len(result) >= 0

   @given(st.lists(st.integers()))
   def test_sort_function_properties(numbers):
       result = custom_sort(numbers)
       assert len(result) == len(numbers)
       assert all(a <= b for a, b in zip(result, result[1:]))
   ```

7. **Async Testing Patterns**
   - Generate comprehensive async test patterns:
   ```python
   import pytest
   import asyncio
   from unittest.mock import AsyncMock

   @pytest.mark.asyncio
   async def test_async_function():
       result = await async_function()
       assert result is not None

   @pytest.mark.asyncio
   async def test_async_context_manager():
       async with AsyncContextManager() as manager:
           result = await manager.process()
           assert result is not None

   @pytest.mark.asyncio
   async def test_concurrent_operations():
       tasks = [async_operation(i) for i in range(5)]
       results = await asyncio.gather(*tasks)
       assert len(results) == 5
   ```

8. **Fixture and Factory Generation**
   - Create comprehensive fixture setup in conftest.py:
   ```python
   import pytest
   from factory import Factory, Faker, SubFactory
   from factory.alchemy import SQLAlchemyModelFactory

   @pytest.fixture
   def db_session():
       # Database session fixture
       pass

   @pytest.fixture
   def sample_user():
       return UserFactory()

   @pytest.fixture
   async def async_client():
       # Async HTTP client fixture
       pass

   class UserFactory(SQLAlchemyModelFactory):
       class Meta:
           model = User

       email = Faker('email')
       name = Faker('name')
       created_at = Faker('date_time')
   ```

9. **Parameterized Testing and Edge Cases**
   - Generate comprehensive parameterized tests:
   ```python
   @pytest.mark.parametrize("input_value,expected", [
       ("valid@email.com", True),
       ("invalid-email", False),
       ("", False),
       ("test@", False),
       ("@test.com", False),
   ])
   def test_email_validation(input_value, expected):
       assert validate_email(input_value) == expected

   @pytest.mark.parametrize("data", [
       pytest.param({}, id="empty_dict"),
       pytest.param({"key": "value"}, id="single_item"),
       pytest.param({"a": 1, "b": 2}, id="multiple_items"),
   ])
   def test_data_processing(data):
       result = process_data(data)
       assert isinstance(result, dict)
   ```

10. **Mock and Patch Generation**
    - Generate comprehensive mocking patterns:
    ```python
    from unittest.mock import Mock, patch, MagicMock, AsyncMock

    @patch('module.external_service')
    def test_with_external_service_mock(mock_service):
        mock_service.return_value = {"status": "success"}
        result = function_using_service()
        assert result["status"] == "success"
        mock_service.assert_called_once()

    @pytest.fixture
    def mock_database():
        with patch('module.database') as mock_db:
            mock_db.query.return_value = []
            yield mock_db

    @pytest.mark.asyncio
    async def test_async_mock():
        with patch('module.async_function', new_callable=AsyncMock) as mock_func:
            mock_func.return_value = "mocked_result"
            result = await function_using_async()
            assert result == "mocked_result"
    ```

11. **Integration Test Generation**
    - Generate integration tests for APIs, databases, and external services:
    ```python
    @pytest.mark.integration
    def test_api_integration(client):
        response = client.post('/api/users', json={'name': 'Test User'})
        assert response.status_code == 201
        assert 'id' in response.json()

    @pytest.mark.integration
    def test_database_integration(db_session):
        user = User(name="Test User")
        db_session.add(user)
        db_session.commit()

        retrieved = db_session.query(User).filter_by(name="Test User").first()
        assert retrieved is not None
        assert retrieved.name == "Test User"
    ```

12. **Test Data Generation and Management**
    - Generate test data factories and builders:
    ```python
    from factory import Factory, Faker, LazyAttribute
    import factory.fuzzy

    class UserDataBuilder:
        def __init__(self):
            self.data = {}

        def with_email(self, email):
            self.data['email'] = email
            return self

        def with_role(self, role):
            self.data['role'] = role
            return self

        def build(self):
            return User(**self.data)

    def generate_test_users(count=10):
        return [UserFactory() for _ in range(count)]
    ```

13. **Error Handling and Exception Testing**
    - Generate comprehensive exception testing:
    ```python
    def test_function_raises_value_error_on_invalid_input():
        with pytest.raises(ValueError, match="Invalid input"):
            function_with_validation("invalid_input")

    def test_function_handles_network_error():
        with patch('requests.get', side_effect=requests.ConnectionError):
            result = function_with_network_call()
            assert result is None

    @pytest.mark.asyncio
    async def test_async_timeout_handling():
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(slow_async_function(), timeout=0.1)
    ```

14. **Performance and Benchmark Testing**
    - Generate performance tests with pytest-benchmark:
    ```python
    def test_function_performance(benchmark):
        result = benchmark(expensive_function, large_input)
        assert result is not None

    @pytest.mark.benchmark(group="sorting")
    def test_sort_performance(benchmark):
        data = list(range(1000, 0, -1))
        result = benchmark(custom_sort, data)
        assert result == list(range(1, 1001))
    ```

15. **Test Configuration and Execution**
    - Generate test execution scripts and configurations:
    ```bash
    # Add to pyproject.toml
    [tool.uv.scripts]
    test = "pytest"
    test-unit = "pytest tests/unit -v"
    test-integration = "pytest tests/integration -v"
    test-cov = "pytest --cov=src --cov-report=html --cov-report=term"
    test-property = "pytest tests/property -v --hypothesis-show-statistics"
    test-fast = "pytest -x --ff"
    test-parallel = "pytest -n auto"
    ```

16. **Test Quality Validation**
    - Ensure generated tests follow Python testing best practices
    - Validate test isolation and independence
    - Check for proper assertion messages and test descriptions
    - Ensure comprehensive coverage of edge cases and error conditions
    - Validate async test patterns and proper fixture usage
    - Generate test execution validation and CI/CD integration scripts
