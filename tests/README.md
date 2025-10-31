# Test Suite for alg-snake

This directory contains comprehensive tests for the alg-snake project using pytest.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Shared fixtures and configuration
├── data/                       # Test data files
│   └── moves1                  # Sample move sequences
├── unit/                       # Unit tests
│   ├── genetics/
│   │   └── test_fitness_evaluators.py  # Fitness evaluator tests
│   ├── controllers/            # Controller unit tests (placeholder)
│   ├── algorithms/            # Algorithm unit tests (placeholder) 
│   └── config/
│       └── test_cli_genetic_config.py  # CLI configuration tests
└── integration/               # Integration tests
    └── test_genetics_integration.py    # Genetics module integration tests
```

## Running Tests

### Prerequisites
```bash
pip install -r requirements.txt
```

### Using pytest directly
```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/ -m unit

# Run only integration tests  
pytest tests/integration/ -m integration

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html
```

### Using the test runner script
```bash
# Run unit tests
python run_tests.py unit

# Run integration tests
python run_tests.py integration

# Run all tests
python run_tests.py all

# Run with coverage report
python run_tests.py coverage
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Test individual components in isolation
- Fast execution
- No external dependencies
- Focus on correctness of single functions/classes

### Integration Tests (`@pytest.mark.integration`)
- Test interaction between components
- Test complete workflows
- May be slower
- Verify that components work together correctly

### Slow Tests (`@pytest.mark.slow`)
- Tests that take significant time to run
- Usually integration tests with many iterations
- Can be skipped for quick development cycles

## Available Fixtures

The `conftest.py` file provides shared fixtures:

- `sample_snake`: A basic snake for testing
- `sample_snake_with_body`: Snake with multiple body segments
- `grid_size`: Standard grid dimensions (20x20)
- `apple_pos`: Sample apple position (10, 10)
- `blocked_cells`: Sample blocked cell positions
- `other_snakes_info`: Sample other snakes for multiplayer tests
- `greedy_simulation`: GreedySnakeSimulation instance
- `test_sequence`: Sample move sequence for testing

## Writing New Tests

### Unit Test Example
```python
import pytest

class TestMyComponent:
    @pytest.mark.unit
    def test_my_function(self, sample_snake):
        """Test description."""
        result = my_function(sample_snake)
        assert result == expected_value
```

### Integration Test Example  
```python
import pytest

class TestMyIntegration:
    @pytest.mark.integration
    def test_component_interaction(self, sample_snake, grid_size):
        """Test multiple components working together."""
        # Test implementation
        pass
```

## Test Coverage

Run tests with coverage to identify untested code:

```bash
pytest --cov=. --cov-report=html --cov-report=term
```

Open `htmlcov/index.html` to view detailed coverage report.

## Continuous Integration

Tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ --cov=. --cov-report=xml
```

## Best Practices

1. **Test Naming**: Use descriptive names starting with `test_`
2. **Isolation**: Each test should be independent
3. **Fixtures**: Use fixtures for common test data
4. **Markers**: Mark tests appropriately (unit, integration, slow)
5. **Assertions**: Use clear, specific assertions
6. **Documentation**: Include docstrings for complex tests

## Adding New Test Categories

To add new test modules:

1. Create appropriate directory under `tests/unit/` or `tests/integration/`
2. Add `__init__.py` file
3. Create test files following naming convention `test_*.py`
4. Use appropriate pytest markers
5. Update this README if needed