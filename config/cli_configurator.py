from config.configurator import Configurator
from config.configuration import Configuration
from config.colors import COLOR_CHOICES
from ai.heuristics import ManhattanDistance, EuclideanDistance, ZeroHeuristic
from ai.a_star import AStar
from ai.dijkstra import Dijkstra
from ai.bfs import BFS
from ai.step_limiter import StepLimitedPathfinder
from controllers.ai_controller import AIController
from controllers.human_controller import HumanController
from game.snake import Snake


class CLIConfigurator(Configurator):
    def build_configuration(self):
        use_default = input("Do you want to use default configuration? (Y/n): ")
        if use_default.lower() in ("y", "yes", ""):
            snake1 = Snake(
                "Snake 1",
                (5, 5),
                COLOR_CHOICES["green"],
                AIController(
                    StepLimitedPathfinder(AStar(ManhattanDistance()), max_steps=1000)
                ),
            )
            snake2 = Snake(
                "Snake 2",
                (5, 15),
                COLOR_CHOICES["blue"],
                AIController(StepLimitedPathfinder(Dijkstra(), max_steps=1000)),
            )
            return Configuration(
                background_color=COLOR_CHOICES["black"],
                grid_color=COLOR_CHOICES["white"],
                width=25,
                height=25,
                cell_size=20,
                snakes=[snake1, snake2],
                fps=20,
            )
        else:
            return self.build_custom_configuration()

    def build_custom_configuration(self):
        width = self.choose_width()
        height = self.choose_height()
        cell_size = self.choose_cell_size()

        background_color = self.choose_background_color()
        grid_color = self.choose_grid_color()
        fps = self.choose_fps()

        num_snakes = self.choose_number_of_snakes()
        snakes = []

        for i in range(num_snakes):
            snake = self.configure_snake(i, (width, height))
            snakes.append(snake)

        return Configuration(
            width=width,
            height=height,
            cell_size=cell_size,
            background_color=background_color,
            grid_color=grid_color,
            fps=fps,
            snakes=snakes,
        )

    def choose_cell_size(self) -> int:
        return int(input("Enter cell size: ").strip())

    def choose_width(self) -> int:
        return int(input("Enter grid width: ").strip())

    def choose_height(self) -> int:
        return int(input("Enter grid height: ").strip())

    def choose_number_of_snakes(self):
        try:
            num_snakes = int(input("Enter number of snakes: ").strip())
            return max(1, num_snakes)  # Ensure at least one snake
        except ValueError:
            print("Invalid input, defaulting to 2 snakes.")
            return 2

    def __choose_controller(self):
        print("Choose controller:")
        print("1 - AI Controller")
        print("2 - Human Controller")
        choice = input("Enter choice [1-2]: ").strip()
        if choice == "2":
            return HumanController()
        else:
            return self.__configure_ai_controller()

    def __configure_ai_controller(self):
        print("Choose algorithm:")
        print("1 - A*")
        print("2 - Dijkstra")
        print("3 - BFS")
        algo_choice = input("Enter choice [1-3]: ").strip()

        if algo_choice == "1":
            heuristic = self.choose_heuristic()
            algo = AStar(heuristic)
        elif algo_choice == "2":
            algo = Dijkstra()
        else:
            algo = BFS()

        step_limited = StepLimitedPathfinder(algo, max_steps=self.choose_max_steps())
        return AIController(step_limited)

    def __choose_snake_color(self):
        print("Choose snake color:")
        for i, color in enumerate(COLOR_CHOICES.keys(), start=1):
            print(f"{i} - {color}")
        choice = int(input("Enter choice: ").strip())
        if choice < 1 or choice > len(COLOR_CHOICES):
            print("Invalid choice, defaulting to green.")
            return COLOR_CHOICES["green"]
        return list(COLOR_CHOICES.values())[choice - 1]

    def configure_snake(self, snake_number, grid_size) -> Snake:
        name = input("Enter snake name: ").strip()
        if not name:
            name = "Snake"
        print(f"--- Configuring {name} ---")

        controller = self.__choose_controller()

        color = self.__choose_snake_color()

        # Start position is centered in the grid, with a slight offset for each snake
        start_x = grid_size[0] // 2 - 1
        start_y = grid_size[1] // 2 - 1 + snake_number
        start_pos = (start_x, start_y)

        return Snake(name, start_pos, color, controller)
    
    def choose_max_steps(self) -> int:
        try:
            max_steps = int(input("Enter maximum steps for pathfinding: ").strip())
            return max_steps if max_steps > 0 else 100  # Default to 100 if invalid input
        except ValueError:
            print("Invalid input, defaulting to 100 steps.")
            return 100

    def choose_heuristic(self):
        print("Choose heuristic:")
        print("1 - Manhattan")
        print("2 - Euclidean")
        print("3 - Zero (Dijkstra)")
        choice = input("Enter choice [1-3]: ").strip()
        if choice == "2":
            return EuclideanDistance()
        elif choice == "3":
            return ZeroHeuristic()
        return ManhattanDistance()

    def choose_background_color(self):
        print("Choose background color:")
        for i, color in enumerate(COLOR_CHOICES.keys(), start=1):
            print(f"{i} - {color}")
        choice = int(input("Enter choice: ").strip())
        return list(COLOR_CHOICES.values())[choice - 1]

    def choose_grid_color(self):
        print("Choose grid color:")
        for i, color in enumerate(COLOR_CHOICES.keys(), start=1):
            print(f"{i} - {color}")
        choice = int(input("Enter choice: ").strip())
        return list(COLOR_CHOICES.values())[choice - 1]

    def choose_fps(self):
        try:
            fps = int(input("Enter frames per second (FPS): ").strip())
            return fps if fps > 0 else 10  # Default to 10 FPS if invalid input
        except ValueError:
            print("Invalid input, defaulting to 10 FPS.")
            return 10
