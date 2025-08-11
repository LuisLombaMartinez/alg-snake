from game.grid_item import GridItem
import pygame


class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.items: list[GridItem] = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def get_blocked_cells(self):
        blocked = set()
        for item in self.items:
            blocked.update(item.blocked_cells())
        return blocked

    def get_occupied_cells(self):
        occupied = set()
        for item in self.items:
            occupied |= item.position_cells()
        return occupied

    def in_bounds(self, pos) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def get_size(self):
        return (self.width, self.height)

    def render(self, screen):
        # Fill background
        screen.fill((0, 0, 0))  # Black

        for x in range(self.width):
            for y in range(self.height):
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(screen, (40, 40, 40), rect, 1)  # Dark gray grid lines

        # Draw all items
        for item in self.items:
            item.draw(screen, self.cell_size)
