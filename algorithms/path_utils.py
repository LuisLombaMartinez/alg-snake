"""
Utility functions for pathfinding algorithms.
Consolidates common logic to avoid code duplication.
"""

from typing import Dict, Tuple, List, Optional
from utils.move_utils import get_random_move


def reconstruct_path(
    came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
    steps: int,
    max_steps: Optional[int] = None,
    prev: Optional[Tuple[int, int]] = None,
) -> Tuple[List[Tuple[int, int]], int]:
    """
    Reconstruct path from came_from dictionary.

    Args:
        came_from: Dictionary mapping positions to their predecessors
        start: Starting position
        goal: Goal position
        steps: Number of steps taken during search
        max_steps: Maximum allowed steps (optional)
        prev: Previous position for fallback random move

    Returns:
        Tuple of (path, steps) where path is list of positions from start to goal
    """
    # Check if goal was reached and within step limit
    if goal not in came_from or (max_steps is not None and steps >= max_steps):
        return [get_random_move(start, prev=prev if prev is not None else start)], steps

    # Reconstruct path by following came_from backwards
    path = []
    current: tuple[int, int] | None = goal
    while current is not None and current != start:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path, steps


def is_valid_position(
    pos: Tuple[int, int],
    grid_size: Tuple[int, int],
    blocked: set,
) -> bool:
    """
    Check if a position is valid (within bounds and not blocked).

    Args:
        pos: Position to check
        grid_size: (width, height) of grid
        blocked: Set of blocked positions

    Returns:
        True if position is valid, False otherwise
    """
    width, height = grid_size
    x, y = pos
    return 0 <= x < width and 0 <= y < height and pos not in blocked


def get_neighbors(
    pos: Tuple[int, int],
    grid_size: Tuple[int, int],
    blocked: set,
) -> List[Tuple[int, int]]:
    """
    Get valid neighboring positions (up, down, left, right).

    Args:
        pos: Current position
        grid_size: (width, height) of grid
        blocked: Set of blocked positions

    Returns:
        List of valid neighbor positions
    """
    x, y = pos
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
    neighbors = []

    for dx, dy in directions:
        neighbor = (x + dx, y + dy)
        if is_valid_position(neighbor, grid_size, blocked):
            neighbors.append(neighbor)

    return neighbors
