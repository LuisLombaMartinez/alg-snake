from abc import ABC, abstractmethod
from ai.heuristics import Heuristic
from game.snake import Snake
from config.configuration import Configuration
from config.colors import BLACK, WHITE


class Configurator(ABC):
    @abstractmethod
    def choose_cell_size(self) -> int:
        """Choose the size of each cell in the grid."""
        pass

    @abstractmethod
    def choose_heuristic(self) -> Heuristic:
        """Choose the heuristic for pathfinding algorithms."""
        pass

    @abstractmethod
    def choose_width(self) -> int:
        """Choose the width of the grid."""
        pass

    @abstractmethod
    def choose_height(self) -> int:
        """Choose the height of the grid."""
        pass

    @abstractmethod
    def choose_number_of_snakes(self) -> int:
        """Choose the number of snakes in the game."""
        pass

    @abstractmethod
    def configure_snake(
        self: str, snake_number: int, grid_size: tuple[int, int]
    ) -> Snake:
        """Configure a snake with its controller and initial position."""
        pass

    def choose_max_steps(self) -> int:
        """Choose the maximum number of steps for pathfinding algorithms."""
        pass

    @abstractmethod
    def choose_background_color(self) -> tuple[int, int, int]:
        """Choose the background color of the game."""
        pass

    @abstractmethod
    def choose_grid_color(self) -> tuple[int, int, int]:
        """Choose the color of the grid lines."""
        pass

    @abstractmethod
    def choose_fps(self) -> int:
        """Choose the frames per second for the game."""
        pass

    def build_configuration(self) -> Configuration:
        """Build and return a Configuration object based on user choices."""
        return Configuration(
            background_color=self.choose_background_color(),
            grid_color=self.choose_grid_color(),
            fps=self.choose_fps(),
        )

    def build_default_configuration(self) -> Configuration:
        """Build and return a default Configuration object."""
        return Configuration(
            background_color=BLACK,
            grid_color=WHITE,
            fps=10,
        )
