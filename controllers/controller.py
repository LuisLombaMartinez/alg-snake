from abc import ABC, abstractmethod


class Controller(ABC):
    @abstractmethod
    def get_next_move(self, snake, grid_size, **kwargs) -> tuple[int, int]:
        """
        Return the next head position for this snake.
        - snake: the Snake instance (so you can inspect head(), body, etc.)
        - grid_size: (width, height)
        """
        pass

    @abstractmethod
    def get_display_info(self):
        """
        Return a string with information to display in the game.
        This can include algorithm name, steps taken, etc.
        """
        pass
