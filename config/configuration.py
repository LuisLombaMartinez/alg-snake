import config.colors as colors
from game.snake import Snake


class Configuration:
    def __init__(
        self,
        width,
        height,
        cell_size,
        background_color=colors.BLACK,
        grid_color=colors.WHITE,
        fps=10,
        snakes: list[Snake] = [],
    ):
        self.background_color = background_color
        self.grid_color = grid_color
        self.fps = fps
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.snakes = snakes

    def get_fps(self):
        return self.fps

    def set_fps(self, fps):
        self.fps = fps
