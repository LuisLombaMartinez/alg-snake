# ai/astar.py

import heapq

from algorithms.algorithm import ConfigurableAlgorithm
from algorithms.heuristics import Heuristic, ManhattanDistance
from algorithms.path_utils import reconstruct_path


class AStar(ConfigurableAlgorithm):
    def __init__(self, heuristic: Heuristic | None = None):
        """Initialize A* with optional heuristic (defaults to Manhattan distance)."""
        self.heuristic = heuristic if heuristic else ManhattanDistance()

    def find_path(self, start, goal, blocked, grid_size, max_steps=None, prev=None):
        width, height = grid_size
        open_set = [(0, start)]
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {}
        g_score = {start: 0}
        visited = set()
        steps = 0

        while open_set:
            if max_steps is not None and steps >= max_steps:
                break

            _, current = heapq.heappop(open_set)
            steps += 1
            visited.add(current)

            if current == goal:
                return reconstruct_path(came_from, start, goal, steps, max_steps, prev)

            x, y = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if not (0 <= neighbor[0] < width and 0 <= neighbor[1] < height):
                    continue
                if neighbor in blocked or neighbor in visited:
                    continue

                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (int(f_score), neighbor))

        return reconstruct_path(came_from, start, goal, steps, max_steps, prev)
