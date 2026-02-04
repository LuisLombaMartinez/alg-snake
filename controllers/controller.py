from abc import ABC, abstractmethod
from typing import Tuple, Any


class Controller(ABC):
    @abstractmethod
    def get_next_move(self, snake, grid_size: Tuple[int, int], **kwargs: Any) -> Tuple[int, int]:
        """
        Return the next head position for this snake.
        
        Args:
            snake: The Snake instance (inspect head(), body, etc.)
            grid_size: (width, height) of the grid
            **kwargs: Additional context (apple_pos, blocked_cells, etc.)
        
        Returns:
            Next position as (x, y) tuple
        """
        pass

    @abstractmethod
    def get_display_info(self) -> str:
        """
        Return a string with information to display in the game.
        This can include algorithm name, steps taken, etc.
        """
        pass
