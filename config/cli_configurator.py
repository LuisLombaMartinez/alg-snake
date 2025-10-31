from config.configurator import Configurator
from config.configuration import Configuration
from config.colors import COLOR_CHOICES
from algorithms.heuristics import ManhattanDistance, EuclideanDistance, ZeroHeuristic
from algorithms.a_star import AStar
from algorithms.dijkstra import Dijkstra
from algorithms.bfs import BFS
from algorithms.step_limiter import StepLimitedPathfinder
from controllers.algorithmic_controller import AlgorithmicController
from controllers.human_controller import HumanController
from controllers.random_controller import RandomController
from controllers.replay_controller import ReplayController
from controllers.genetic_controller import GeneticController
from genetics.fitness_evalutor import (
    SinglePlayerAppleFitnessEvaluator,
    SinglePlayerTimeFitnessEvaluator,
    MultiplayerAppleFitnessEvaluator,
    AggressiveFitnessEvaluator,
    BalancedFitnessEvaluator,
)
from genetics.snake_simulation import GreedySnakeSimulation, ObstacleAwareSnakeSimulation, ConservativeSnakeSimulation
from game.snake import Snake
from utils.move_loader import MoveLoader


class CLIConfigurator(Configurator):
    def build_configuration(self):
        use_default = input("Do you want to use default configuration? (Y/n): ")
        if use_default.lower() in ("y", "yes", ""):
            return self.build_default_configuration()
        else:
            return self.build_custom_configuration()

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
        print("5 - Genetic Controller")
        choice = input("Enter choice [1-5]: ").strip()
        if choice == "2":
            return HumanController()
        elif choice == "3":
            return RandomController()
        elif choice == "4":
            path = input("Enter path to replay moves file: ").strip()
            moves = MoveLoader.load_from_file(path)
            return ReplayController(moves)
        elif choice == "5":
            return self.__configure_genetic_controller()
        else:
            return self.__configure_algorithmic_controller()

    def __configure_algorithmic_controller(self):
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

    def __configure_genetic_controller(self):
        print("Configuring Genetic Algorithm Controller:")

        # Choose fitness evaluator
        print("\nChoose fitness evaluator strategy:")
        print("1 - Single Player (Apple focus)")
        print("2 - Single Player (Survival focus)")
        print("3 - Multiplayer Competitive (Beat opponents to apple)")
        print("4 - Aggressive (Attack other snakes)")
        print("5 - Balanced (Mix of competitive and aggressive)")

        fitness_choice = input("Enter choice [1-5]: ").strip()

        # Map choices to evaluator classes for checking simulation needs
        evaluator_classes = {
            "1": SinglePlayerAppleFitnessEvaluator,
            "2": SinglePlayerTimeFitnessEvaluator,
            "3": MultiplayerAppleFitnessEvaluator,
            "4": AggressiveFitnessEvaluator,
            "5": BalancedFitnessEvaluator,
        }

        # Get the evaluator class to check if it needs simulation
        evaluator_class = evaluator_classes.get(fitness_choice, SinglePlayerAppleFitnessEvaluator)

        # Check if we need opponent simulation using class attribute
        simulation = None
        if evaluator_class.NEEDS_OPPONENT_SIMULATION:
            print("\nChoose opponent prediction model:")
            print("1 - Greedy (Always toward apple)")
            print("2 - Obstacle Aware (Avoid collisions)")
            print("3 - Conservative (Safety first)")

            sim_choice = input("Enter choice [1-3]: ").strip()

            # Create simulation
            if sim_choice == "2":
                simulation = ObstacleAwareSnakeSimulation()
            elif sim_choice == "3":
                simulation = ConservativeSnakeSimulation()
            else:
                simulation = GreedySnakeSimulation()

        # Create fitness evaluator
        if fitness_choice == "1":
            fitness_evaluator = SinglePlayerAppleFitnessEvaluator()
        elif fitness_choice == "2":
            fitness_evaluator = SinglePlayerTimeFitnessEvaluator()
        elif fitness_choice == "3":
            fitness_evaluator = MultiplayerAppleFitnessEvaluator(simulation)
        elif fitness_choice == "4":
            aggression = self.__choose_aggression_level()
            fitness_evaluator = AggressiveFitnessEvaluator(simulation, aggression)
        elif fitness_choice == "5":
            aggression_weight, cooperation_weight = self.__choose_balance_weights()
            fitness_evaluator = BalancedFitnessEvaluator(simulation, aggression_weight, cooperation_weight)
        else:
            fitness_evaluator = SinglePlayerAppleFitnessEvaluator()

        # GA parameters
        population_size = self.__choose_population_size()
        sequence_length = self.__choose_sequence_length()
        mutation_rate = self.__choose_mutation_rate()

        return GeneticController(
            fitness_evaluator=fitness_evaluator,
            population_size=population_size,
            sequence_length=sequence_length,
            mutation_rate=mutation_rate,
        )

    def __choose_aggression_level(self):
        try:
            level = float(input("Enter aggression level (0.5-2.0, default 1.0): ").strip())
            return max(0.5, min(2.0, level))
        except ValueError:
            print("Invalid input, using default aggression level 1.0")
            return 1.0

    def __choose_balance_weights(self):
        try:
            aggression = float(input("Enter aggression weight (0.0-1.0, default 0.3): ").strip())
            aggression = max(0.0, min(1.0, aggression))
            cooperation = 1.0 - aggression
            print(f"Cooperation weight will be: {cooperation:.2f}")
            return aggression, cooperation
        except ValueError:
            print("Invalid input, using default weights: aggression=0.3, cooperation=0.7")
            return 0.3, 0.7

    def __choose_population_size(self):
        try:
            size = int(input("Enter population size (10-100, default 20): ").strip())
            return max(10, min(100, size))
        except ValueError:
            print("Invalid input, using default population size 20")
            return 20

    def __choose_sequence_length(self):
        try:
            length = int(input("Enter sequence length (50-500, default 100): ").strip())
            return max(50, min(500, length))
        except ValueError:
            print("Invalid input, using default sequence length 100")
            return 100

    def __choose_mutation_rate(self):
        try:
            rate = float(input("Enter mutation rate (0.01-0.5, default 0.05): ").strip())
            return max(0.01, min(0.5, rate))
        except ValueError:
            print("Invalid input, using default mutation rate 0.05")
            return 0.05
