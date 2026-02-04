from controllers.controller import Controller
from game.snake import Snake
from utils.move_utils import DIRECTION_DELTAS


class ReplayController(Controller):
    def __init__(self, moves: list[str]):
        """
        Initialize replay controller with a list of direction strings.

        Args:
            moves: List of direction strings ("up", "down", "left", "right")
        """
        self.moves = moves
        self.current_index = 0

    def get_next_move(self, snake: Snake, grid_size, **kwargs) -> tuple[int, int]:
        if self.current_index >= len(self.moves):
            self.current_index = 0
        direction = self.moves[self.current_index]
        self.current_index += 1

        if direction not in DIRECTION_DELTAS:
            raise ValueError(f"Invalid move direction: {direction}")

        delta = DIRECTION_DELTAS[direction]
        head_x, head_y = snake.head()
        return (head_x + delta[0], head_y + delta[1])

    def get_display_info(self):
        return f"Replay Controller (step {self.current_index}/{len(self.moves)})"

    def _validate_moves(self):
        opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
        for i in range(1, len(self.moves)):
            prev = self.moves[i - 1]
            curr = self.moves[i]

            if curr == opposites.get(prev):
                raise ValueError(f"Invalid move sequence: {prev} followed by {curr}")

            if curr not in DIRECTION_DELTAS:
                raise ValueError(f"Invalid move direction: {curr}")
