# Testing Setup Troubleshooting Guide

## Quick Start

If you're getting import errors when running tests, follow these steps:

### 1. Install Dependencies
```bash
# Option A: Use the setup script (recommended)
python setup_tests.py

# Option B: Manual installation
pip install -r requirements.txt

# Option C: Install specific packages
pip install pygame==2.6.1 pytest==7.4.0 pytest-cov==4.1.0
```

### 2. Run Tests
```bash
# Check if setup worked
python run_tests.py all

# Or run pytest directly
pytest tests/ -v
```

## Common Issues and Solutions

### Issue: `ModuleNotFoundError: No module named 'pygame'`

**Solution:**
```bash
pip install pygame
# or
pip install -r requirements.txt
```

### Issue: `ModuleNotFoundError: No module named 'pytest'`

**Solution:**
```bash
pip install pytest pytest-cov
```

### Issue: `ImportError while loading conftest`

This usually means pygame is not installed or there's a virtual environment issue.

**Solutions:**
1. **Check your Python environment:**
   ```bash
   which python
   pip list | grep pygame
   pip list | grep pytest
   ```

2. **If using virtual environment:**
   ```bash
   # Activate your venv first
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   
   # Then install requirements
   pip install -r requirements.txt
   ```

3. **Create new virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Issue: `SDL_VIDEODRIVER` errors or display issues

The test configuration sets `SDL_VIDEODRIVER=dummy` to prevent pygame from trying to initialize a display during testing. If you still get display-related errors:

**Solution:**
```bash
export SDL_VIDEODRIVER=dummy
pytest tests/ -v
```

### Issue: Tests run but fail with import errors

This can happen if the project structure changed or there are circular imports.

**Solutions:**
1. **Check test configuration:**
   ```bash
   # Run from project root directory
   cd /path/to/alg-snake
   pytest tests/ -v
   ```

2. **Clear Python cache:**
   ```bash
   find . -name "*.pyc" -delete
   find . -name "__pycache__" -type d -exec rm -rf {} +
   ```

## Virtual Environment Setup

If you prefer to use a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv alg-snake-env

# Activate it
source alg-snake-env/bin/activate  # Linux/Mac
# or
alg-snake-env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python run_tests.py all
```

## Testing Different Scenarios

### Unit Tests Only (Fast)
```bash
python run_tests.py unit
# or
pytest tests/unit/ -m unit -v
```

### Integration Tests Only
```bash
python run_tests.py integration
# or  
pytest tests/integration/ -m integration -v
```

### All Tests with Coverage
```bash
python run_tests.py coverage
# or
pytest tests/ --cov=. --cov-report=html --cov-report=term
```

### Skip Slow Tests
```bash
pytest tests/ -v -m "not slow"
```

## IDE Setup

### VS Code
Add to your `settings.json`:
```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "python.defaultInterpreterPath": "./.venv/bin/python"
}
```

### PyCharm
1. Go to Settings → Tools → Python Integrated Tools
2. Set Testing → Default test runner to "pytest" 
3. Set Testing → Test runner to "pytest"

## Debugging Tests

### Run Single Test
```bash
pytest tests/unit/genetics/test_fitness_evaluators.py::TestFitnessEvaluators::test_single_player_apple_evaluator -v
```

### Run with Debug Output
```bash
pytest tests/ -v -s --tb=long
```

### Run with PDB Debugger
```bash
pytest tests/ --pdb
```

## Environment Variables

Set these environment variables if needed:

```bash
# Prevent pygame display initialization
export SDL_VIDEODRIVER=dummy

# Python path (usually not needed with proper test setup)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## Getting Help

If you're still having issues:

1. **Check Python version:** `python --version` (should be 3.8+)
2. **Check pip version:** `pip --version`
3. **List installed packages:** `pip list`
4. **Check test discovery:** `pytest --collect-only tests/`

For more help, check the project's issues or documentation.