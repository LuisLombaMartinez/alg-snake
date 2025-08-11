import pygame
from .grid_item import GridItem
from controllers.controller import Controller


class Snake(GridItem):
    def __init__(self, name: str, start_pos, color, controller: Controller):
        self.name = name
        self.body = [start_pos]
        self.color = color
        self.alive = True
        self.score = 0
        self.controller = controller

    def head(self):
        return self.body[0]

    def move(self, new_head, grow=False):
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()

    def blocked_cells(self):
        return set(self.body)

    def position_cells(self):
        return set(self.body)

    def draw(self, screen, cell_size):
        for x, y in self.body:
            pygame.draw.rect(
                screen, self.color, (x * cell_size, y * cell_size, cell_size, cell_size)
            )
            if self.body.index((x, y)) == 0:
                # Draw a white circle in the center of the head
                center = (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2)
                pygame.draw.circle(screen, (255, 255, 255), center, cell_size // 4)

    def get_next_move(self, apple_pos, blocked_cells, grid_size) -> tuple[int, int]:
        """Get the next move for the snake using its controller."""
        return self.controller.get_next_move(self, apple_pos, blocked_cells, grid_size)
