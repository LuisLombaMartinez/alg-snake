from typing import Any

from algorithms.step_limiter import StepLimitedPathfinder
from controllers.controller import Controller
from game.snake import Snake


class AlgorithmicController(Controller):
    def __init__(self, step_limited: StepLimitedPathfinder):
        self.step_limited = step_limited
        self.total_steps = 0

    def get_next_move(self, snake: Snake, grid_size: tuple[int, int], **kwargs: Any) -> tuple[int, int]:
        apple_pos = kwargs.get("apple_pos")
        blocked_cells = kwargs.get("blocked_cells", set())
        prev = snake.body[1] if len(snake.body) > 1 else snake.head()

        path, steps = self.step_limited.find_path(
            snake.head(),
            apple_pos,
            blocked_cells - {snake.head()},
            grid_size,
            prev=prev,
        )
        self.total_steps += steps
        # Guarantee a tuple is returned
        if path and len(path) > 0:
            next_move: tuple[int, int] = path[0]
            return next_move
        return snake.head()

    def get_display_info(self) -> str:
        algo_name = getattr(self.step_limited.algorithm, "__class__", type(self.step_limited.algorithm)).__name__
        return f"{algo_name} | Steps: {self.total_steps}"
