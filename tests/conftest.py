"""
Pytest configuration and shared fixtures for alg-snake tests.
"""

import pytest
import sys
import os
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set environment variable to prevent pygame from initializing display during imports
os.environ["SDL_VIDEODRIVER"] = "dummy"

try:
    # Import after adding to path and setting environment
    from game.snake import Snake, SnakeInfo
    from genetics.snake_simulation import GreedySnakeSimulation
    from controllers.random_controller import RandomController
    from config.colors import COLOR_CHOICES
except ImportError as e:
    pytest.skip(f"Missing dependencies for tests: {e}", allow_module_level=True)


@pytest.fixture
def sample_snake():
    """Create a sample snake for testing."""
    controller = RandomController()
    snake = Snake("TestSnake", (5, 5), COLOR_CHOICES["green"], controller)
    return snake


@pytest.fixture
def sample_snake_with_body():
    """Create a snake with a longer body for testing."""
    controller = RandomController()
    snake = Snake("TestSnake", (5, 5), COLOR_CHOICES["green"], controller)
    # Add some body segments
    snake.body = [(5, 5), (4, 5), (3, 5)]
    return snake


@pytest.fixture
def grid_size():
    """Standard grid size for testing."""
    return (20, 20)


@pytest.fixture
def apple_pos():
    """Standard apple position for testing."""
    return (10, 10)


@pytest.fixture
def blocked_cells():
    """Sample blocked cells for testing."""
    return {(0, 0), (1, 1), (19, 19)}


@pytest.fixture
def other_snakes_info():
    """Sample other snakes info for testing."""
    return [
        SnakeInfo(Snake("Snake1", (8, 8), COLOR_CHOICES["blue"], RandomController())),
        SnakeInfo(Snake("Snake2", (12, 12), COLOR_CHOICES["red"], RandomController())),
    ]


@pytest.fixture
def greedy_simulation():
    """Greedy snake simulation instance."""
    return GreedySnakeSimulation()


@pytest.fixture
def test_sequence():
    """Sample move sequence for testing."""
    return ["right", "right", "down", "down", "left"]


# Pytest configuration
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
