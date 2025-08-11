from controllers.controller import Controller
from game.snake import Snake
from ai.step_limiter import StepLimitedPathfinder


class AIController(Controller):
    def __init__(self, step_limited: StepLimitedPathfinder):
        self.step_limited = step_limited
        self.total_steps = 0

    def get_next_move(
        self, snake: Snake, grid_size, **kwargs: dict[str, any]
    ) -> tuple[int, int]:
        apple_pos = kwargs.get("apple_pos")
        blocked_cells = kwargs.get("blocked_cells")
        path, steps = self.step_limited.find_path(
            snake.head(),
            apple_pos,
            blocked_cells - {snake.head()},
            grid_size,
        )
        self.total_steps += steps
        # Guarantee a tuple is returned
        if path and isinstance(path[0], tuple):
            return path[0]
        return snake.head()

    def get_display_info(self):
        algo_name = getattr(
            self.step_limited.algorithm, "__class__", type(self.step_limited.algorithm)
        ).__name__
        return f"{algo_name} | Steps: {self.total_steps}"
