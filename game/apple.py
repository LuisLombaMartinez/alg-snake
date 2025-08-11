import pygame
from .grid_item import GridItem
from config.colors import RED


class Apple(GridItem):
    def __init__(self, pos, color=RED, points: int = 1):
        self.pos = pos
        self.color = color
        self.points = points

    def blocked_cells(self):
        return set()  # Apples don't block anything

    def position_cells(self):
        return {self.pos}

    def draw(self, screen, cell_size):
        x, y = self.pos
        pygame.draw.rect(
            screen, self.color, (x * cell_size, y * cell_size, cell_size, cell_size)
        )
