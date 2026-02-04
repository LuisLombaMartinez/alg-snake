"""
YAML Configuration Loader with Pydantic Validation.

This module demonstrates:
- Loading external configuration files
- Validating data with Pydantic schemas
- Error handling and user-friendly messages
- Factory pattern for object creation

Students will learn:
- How to work with YAML configuration files
- Type-safe configuration loading
- Validation and error reporting
- Converting validated data to application objects
"""

from pathlib import Path

import yaml
from pydantic import ValidationError

from config.configuration import Configuration
from config.configurator import Configurator
from config.schemas import ConfigSchema
from controllers.algorithmic_controller import AlgorithmicController
from controllers.human_controller import HumanController
from controllers.random_controller import RandomController
from controllers.replay_controller import ReplayController


class YAMLConfigurationError(Exception):
    """Raised when YAML configuration is invalid."""

    pass


class YAMLConfigurator(Configurator):
    """
    Load and validate YAML configuration files.

    This configurator:
    1. Loads a YAML file and validates it with Pydantic schemas
    2. Provides clear error messages for validation failures
    3. Creates a Configuration object ready for the game

    Unlike CLIConfigurator which builds config step-by-step through user input,
    YAMLConfigurator loads everything at once and validates it upfront.
    """

    def __init__(self, config_path: str | Path):
        """
        Initialize the YAML configurator with a config file path.

        Args:
            config_path: Path to YAML configuration file (str or Path)

        Raises:
            YAMLConfigurationError: If file not found or validation fails
        """
        self.config_path = Path(config_path)

        if not self.config_path.exists():
            raise YAMLConfigurationError(f"Configuration file not found: {self.config_path}")

        # Load and validate config immediately in __init__
        try:
            with open(self.config_path) as f:
                raw_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise YAMLConfigurationError(f"Invalid YAML syntax in {self.config_path}:\n{e}") from e

        # Validate with Pydantic schema
        try:
            self._validated_schema = ConfigSchema.model_validate(raw_data)
        except ValidationError as e:
            # Format Pydantic errors in a user-friendly way
            error_messages = []
            for error in e.errors():
                location = " → ".join(str(loc) for loc in error["loc"])
                message = error["msg"]
                error_messages.append(f"  • {location}: {message}")

            raise YAMLConfigurationError(
                f"Configuration validation failed for {self.config_path}:\n" + "\n".join(error_messages)
            ) from e

    def build_configuration(self) -> Configuration:
        """
        Build Configuration object from validated YAML data.

        This is the only method required by the Configurator interface.
        All validation happened in __init__, so this just converts
        the validated schema to a Configuration object.

        Returns:
            Configuration: Complete game configuration ready to use
        """
        from game.snake import Snake

        # Create all snakes with their controllers
        snakes = []
        for snake_schema in self._validated_schema.snakes:
            # Create controller based on type
            controller = self._create_controller(snake_schema.controller)

            # Create snake with explicit type casts
            start_pos: tuple[int, int] = (snake_schema.start_position[0], snake_schema.start_position[1])
            color: tuple[int, int, int] = (snake_schema.color[0], snake_schema.color[1], snake_schema.color[2])

            snake = Snake(
                name=snake_schema.name,
                start_pos=start_pos,
                color=color,
                controller=controller,
            )
            snakes.append(snake)

        # Create Configuration object with all snakes
        config = Configuration(
            width=self._validated_schema.game.width,
            height=self._validated_schema.game.height,
            cell_size=self._validated_schema.game.cell_size,
            fps=self._validated_schema.game.fps,
            background_color=tuple(self._validated_schema.game.background_color),
            grid_color=tuple(self._validated_schema.game.grid_color),
            snakes=snakes,
        )

        return config

    def _create_controller(self, controller_schema):
        """
        Factory method to create controller instances.

        Internal helper - not part of Configurator interface.

        This demonstrates:
        - Factory pattern (creating objects based on type)
        - Discriminated unions (Pydantic ensures correct type)
        - Type-safe object creation

        Args:
            controller_schema: Validated controller configuration

        Returns:
            Controller instance of the appropriate type
        """
        if controller_schema.type == "algorithmic":
            # Import algorithm classes
            from algorithms.a_star import AStar
            from algorithms.algorithm import PathAlgorithm
            from algorithms.bfs import BFS
            from algorithms.dijkstra import Dijkstra
            from algorithms.heuristics import (
                EuclideanDistance,
                Heuristic,
                ManhattanDistance,
                ZeroHeuristic,
            )
            from algorithms.step_limiter import StepLimitedPathfinder

            # Create the base algorithm
            algorithm: PathAlgorithm
            if controller_schema.algorithm == "astar":
                # Choose heuristic for A*
                heuristic: Heuristic
                if controller_schema.heuristic == "manhattan":
                    heuristic = ManhattanDistance()
                elif controller_schema.heuristic == "euclidean":
                    heuristic = EuclideanDistance()
                else:  # zero
                    heuristic = ZeroHeuristic()
                algorithm = AStar(heuristic)
            elif controller_schema.algorithm == "dijkstra":
                algorithm = Dijkstra()
            else:  # bfs
                algorithm = BFS()

            # Wrap in step limiter
            step_limited = StepLimitedPathfinder(algorithm, max_steps=controller_schema.max_steps)
            return AlgorithmicController(step_limited)

        elif controller_schema.type == "human":
            return HumanController()

        elif controller_schema.type == "random":
            return RandomController()

        elif controller_schema.type == "replay":
            # Load moves from replay file
            from utils.move_loader import MoveLoader

            moves = MoveLoader.load_from_file(controller_schema.replay_file)
            return ReplayController(moves)

        else:
            # This should never happen due to Pydantic validation
            raise ValueError(f"Unknown controller type: {controller_schema.type}")
