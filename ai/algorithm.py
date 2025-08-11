from abc import ABC, abstractmethod
import random


class PathAlgorithm(ABC):
    @abstractmethod
    def find_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
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

    def get_random_move(self, start: tuple[int, int]) -> tuple[int, int]:
        """
        Returns a random move from the start position within the grid size.
        This is a fallback method if no path is found.
        """
        x, y = start
        moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return random.choice(moves)


class ConfigurableAlgorithm(PathAlgorithm):
    def configure(self):
        """
        Optionally called before the algorithm is used.
        Responsible for asking any CLI prompts or internal setup.
        """
        pass
