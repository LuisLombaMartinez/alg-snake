from pathlib import Path

from algorithms.a_star import AStar
from algorithms.algorithm import PathAlgorithm
from algorithms.bfs import BFS
from algorithms.dijkstra import Dijkstra
from algorithms.heuristics import EuclideanDistance, ManhattanDistance, ZeroHeuristic
from algorithms.step_limiter import StepLimitedPathfinder
from config.colors import COLOR_CHOICES
from config.configuration import Configuration
from config.configurator import Configurator
from controllers.algorithmic_controller import AlgorithmicController
from controllers.human_controller import HumanController
from controllers.random_controller import RandomController
from controllers.replay_controller import ReplayController
from game.snake import Snake
from utils.move_loader import MoveLoader


class CLIConfigurator(Configurator):
    def build_configuration(self):
        """
        Build configuration with option to load from YAML presets or create custom.
        """
        print("\n" + "=" * 60)
        print("🐍 Welcome to alg-snake Configuration")
        print("=" * 60)
        print("\nChoose a configuration option:\n")

        # Try to load available YAML configs
        yaml_configs = self._get_available_yaml_configs()

        option_num = 1
        option_map = {}

        # Show YAML preset options
        if yaml_configs:
            print("📁 Preset Configurations:")
            for config_file in yaml_configs:
                description = self._get_config_description(config_file)
                print(f"  {option_num} - {config_file.stem}: {description}")
                option_map[str(option_num)] = ("yaml", config_file)
                option_num += 1
            print()

        # Show built-in options
        print("🔧 Built-in Configurations:")
        print(f"  {option_num} - Default (A* vs Dijkstra)")
        option_map[str(option_num)] = ("builtin", "default")
        option_num += 1

        print(f"  {option_num} - Custom (Configure manually)")
        option_map[str(option_num)] = ("builtin", "custom")

        print("\n" + "-" * 60)
        choice = input(f"Enter choice [1-{option_num}] (default 1): ").strip() or "1"
        print("=" * 60 + "\n")

        if choice not in option_map:
            print(f"Invalid choice '{choice}', using default...")
            choice = "1"

        config_type, config_value = option_map[choice]

        if config_type == "yaml":
            return self._load_yaml_config(config_value)
        elif config_value == "default":
            return self.build_default_configuration()
        else:  # custom
            return self.build_custom_configuration()

    def _get_available_yaml_configs(self):
        """Get list of available YAML configuration files."""
        configs_dir = Path("configs")
        if not configs_dir.exists():
            return []
        return sorted(configs_dir.glob("*.yaml"))

    def _get_config_description(self, config_path):
        """Extract description from first comment line of YAML file."""
        try:
            with open(config_path) as f:
                first_line = f.readline().strip()
                if first_line.startswith("#"):
                    return first_line[1:].strip()
        except Exception:
            pass
        return "Configuration file"

    def _load_yaml_config(self, config_path):
        """Load configuration from YAML file using YAMLConfigurator."""
        try:
            from config.yaml_configurator import YAMLConfigurator

            print(f"📄 Loading from {config_path.name}...\n")
            configurator = YAMLConfigurator(str(config_path))
            return configurator.build_configuration()
        except ImportError:
            print("⚠️  PyYAML not installed. Install with: pip install PyYAML")
            print("Falling back to default configuration...\n")
            return self.build_default_configuration()
        except Exception as e:
            print(f"⚠️  Error loading YAML config: {e}")
            print("Falling back to default configuration...\n")
            return self.build_default_configuration()

    def build_default_configuration(self):
        snake1 = Snake(
            "Snake 1",
            (5, 5),
            COLOR_CHOICES["green"],
            AlgorithmicController(StepLimitedPathfinder(AStar(ManhattanDistance()), max_steps=1000)),
        )
        snake2 = Snake(
            "Snake 2",
            (5, 15),
            COLOR_CHOICES["blue"],
            AlgorithmicController(StepLimitedPathfinder(Dijkstra(), max_steps=1000)),
        )
        return Configuration(
            background_color=COLOR_CHOICES["black"],
            grid_color=COLOR_CHOICES["white"],
            width=50,
            height=50,
            cell_size=15,
            snakes=[snake1, snake2],
            fps=20,
        )

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
        print("1 - Algorithmic Controller")
        print("2 - Human Controller")
        print("3 - Random Controller")
        print("4 - Replay Controller")
        choice = input("Enter choice [1-4]: ").strip()
        if choice == "2":
            return HumanController()
        elif choice == "3":
            return RandomController()
        elif choice == "4":
            path = input("Enter path to replay moves file: ").strip()
            moves = MoveLoader.load_from_file(path)
            return ReplayController(moves)
        else:
            return self.__configure_algorithmic_controller()

    def __configure_algorithmic_controller(self):
        print("Choose algorithm:")
        print("1 - A*")
        print("2 - Dijkstra")
        print("3 - BFS")
        algo_choice = input("Enter choice [1-3]: ").strip()

        algo: PathAlgorithm
        if algo_choice == "1":
            heuristic = self.choose_heuristic()
            algo = AStar(heuristic)
        elif algo_choice == "2":
            algo = Dijkstra()
        else:
            algo = BFS()

        step_limited = StepLimitedPathfinder(algo, max_steps=self.choose_max_steps())
        return AlgorithmicController(step_limited)

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
