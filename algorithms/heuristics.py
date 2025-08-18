from abc import ABC, abstractmethod
import math


class Heuristic(ABC):
    @abstractmethod
    def __call__(self, pos: tuple[int, int], goal: tuple[int, int]) -> float:
        pass


class ManhattanDistance(Heuristic):
    def __call__(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


class EuclideanDistance(Heuristic):
    def __call__(self, pos, goal):
        return math.hypot(pos[0] - goal[0], pos[1] - goal[1])


class ZeroHeuristic(Heuristic):
    """Returns 0 always — effectively turns A* into Dijkstra."""

    def __call__(self, pos, goal):
        return 0
