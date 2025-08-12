import random
import pygame
from controllers.human_controller import HumanController, KEY_TO_DIR
from game.apple import Apple
from game.grid import Grid
from config.configurator import Configurator
from config.configuration import Configuration


class Game:
    def __init__(
        self,
        config: Configuration = None,
    ):
        self.config = config
        self.grid_size = (config.width, config.height)
        self.grid = Grid(config.width, config.height, config.cell_size)
        for snake in config.snakes:
            self.grid.add_item(snake)
        self.snakes = config.snakes
        self.apple = None
        self.spawn_apple()

    @classmethod
    def from_configurator(cls, configurator: Configurator):
        config = configurator.build_configuration()

        return cls(config=config)

    def spawn_apple(self):
        if self.apple:
            self.grid.remove_item(self.apple)

        blocked = self.grid.get_blocked_cells()
        free = [
            (x, y)
            for x in range(self.grid.width)
            for y in range(self.grid.height)
            if (x, y) not in blocked
        ]

        if not free:
            self.apple = None
            return

        pos = random.choice(free)
        self.apple = Apple(pos)
        self.grid.add_item(self.apple)

    def step(self):
        if not self.apple:
            return  # Game over

        blocked = self.grid.get_blocked_cells()
        next_positions = {}

        # First, get all next moves
        for snake in self.snakes:
            if not snake.alive:
                continue
            next_move = snake.controller.get_next_move(
                snake,
                self.grid.get_size(),
                apple_pos=self.apple.pos,
                blocked_cells=blocked,
            )

            next_positions[snake] = next_move

        # Move snakes
        for snake, next_move in next_positions.items():
            grow = next_move == self.apple.pos
            snake.move(next_move, grow)

        # Check for collisions
        positions = [snake.head() for snake in self.snakes if snake.alive]
        for snake in self.snakes:
            if not snake.alive:
                continue
            # Collision with wall
            if not self.grid.in_bounds(snake.head()):
                snake.alive = False
            # Collision with own body
            elif snake.head() in list(snake.body)[1:]:
                snake.alive = False
            # Collision with other snakes' bodies
            elif any(
                snake.head() in list(other.body)
                for other in self.snakes
                if other is not snake and other.alive
            ):
                snake.alive = False
            # Collision with another snake's head
            if positions.count(snake.head()) > 1:
                snake.alive = False

            # Handle apple consumption and respawn
            if self.apple and snake.head() == self.apple.pos:
                snake.score += self.apple.points
                self.spawn_apple()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(
            (
                self.config.width * self.config.cell_size,
                self.config.height * self.config.cell_size,
            )
        )
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 24)  # Add font initialization
        running = True

        while running and any(snake.alive for snake in self.snakes):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    for snake in self.snakes:
                        if isinstance(snake.controller, HumanController):
                            if event.key in KEY_TO_DIR:
                                snake.controller.last_dir = KEY_TO_DIR[event.key]
            self.step()
            self.grid.render(screen)

            # Draw scores for each snake
            for idx, snake in enumerate(self.snakes):
                info = snake.controller.get_display_info()
                score_text = (
                    f"Snake {snake.name}: {snake.score} | {info} | Alive: {snake.alive}"
                )
                text_surface = font.render(score_text, True, (255, 255, 255))
                screen.blit(
                    text_surface, (10, 10 + idx * 30)
                )  # Stacks scores vertically

            pygame.display.flip()
            clock.tick(10)

        pygame.quit()
