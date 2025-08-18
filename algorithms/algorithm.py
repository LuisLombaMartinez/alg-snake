from abc import ABC, abstractmethod
import random


class PathAlgorithm(ABC):
    @abstractmethod
    def find_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        prev: tuple[int, int] | None,
        blocked: set[tuple[int, int]],
        grid_size: tuple[int, int],
        max_steps: int,
    ) -> tuple[list[tuple[int, int]], int]:
        """
        Find a path from start to goal, avoiding blocked cells.
        Returns a list of positions in the path, or an empty list if no path is found.
        """
        pass

    def get_algorithm_name(self) -> str:
        """
        Returns the name of the algorithm.
        This can be overridden by subclasses to provide a custom name.
        """
        return self.__class__.__name__

    def get_random_move(
        self, start: tuple[int, int], prev: tuple[int, int] = None
    ) -> tuple[int, int]:
        """
        Returns a random move from the start position, excluding the direction it came from.
        - start: current head position
        - prev: previous head position (None for first move)
        """
        x, y = start
        moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        if prev is not None:
            # Remove the move that would return to prev
            moves = [m for m in moves if m != prev]
        return random.choice(moves) if moves else start


class ConfigurableAlgorithm(PathAlgorithm):
    def configure(self):
        """
        Optionally called before the algorithm is used.
        Responsible for asking any CLI prompts or internal setup.
        """
        pass
