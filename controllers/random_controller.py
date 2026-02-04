from controllers.controller import Controller
from utils.move_utils import get_random_move


class RandomController(Controller):
    def get_next_move(self, snake, grid_size, **kwargs) -> tuple[int, int]:
        """
        Return a random move for the snake.
        - snake: the Snake instance (so you can inspect head(), body, etc.)
        - grid_size: (width, height)
        """
        prev = snake.body[1] if len(snake.body) > 1 else snake.head()
        return get_random_move(snake.head(), prev=prev)

    def get_display_info(self):
        return "Random Controller"
