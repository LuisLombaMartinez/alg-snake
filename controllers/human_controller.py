import pygame
from controllers.controller import Controller
from game.snake import Snake

KEY_TO_DIR = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


class HumanController(Controller):
    def __init__(self):
        self.last_dir = (1, 0)  # start moving right

    def get_next_move(self, snake: Snake, grid_size, **kwargs) -> tuple[int, int]:
        head_x, head_y = snake.head()
        dx, dy = self.last_dir
        next_pos = (head_x + dx, head_y + dy)
        w, h = grid_size
        if not (0 <= next_pos[0] < w and 0 <= next_pos[1] < h):
            return snake.head()
        return next_pos

    def get_display_info(self):
        return "Human Controller", self.last_dir
