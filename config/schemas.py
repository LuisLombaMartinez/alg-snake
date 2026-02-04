"""
Configuration schemas using Pydantic for validation.

This module demonstrates:
- Data validation with Pydantic
- Type-safe configuration models
- Clear error messages for invalid configs
- Nested data structures

Students will learn:
- How to validate external data (YAML, JSON, APIs)
- Type hints and runtime validation
- Domain modeling with Python classes
"""

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class ColorRGB(BaseModel):
    """RGB color as a list of three integers [R, G, B]."""

    r: int = Field(ge=0, le=255, description="Red component (0-255)")
    g: int = Field(ge=0, le=255, description="Green component (0-255)")
    b: int = Field(ge=0, le=255, description="Blue component (0-255)")

    @classmethod
    def from_list(cls, rgb: list[int]) -> "ColorRGB":
        """Create from [R, G, B] list."""
        if len(rgb) != 3:
            raise ValueError(f"Color must have exactly 3 values, got {len(rgb)}")
        return cls(r=rgb[0], g=rgb[1], b=rgb[2])

    def to_tuple(self) -> tuple[int, int, int]:
        """Convert to tuple for pygame."""
        return (self.r, self.g, self.b)


class PositionXY(BaseModel):
    """2D position as [X, Y]."""

    x: int = Field(ge=0, description="X coordinate")
    y: int = Field(ge=0, description="Y coordinate")

    @classmethod
    def from_list(cls, pos: list[int]) -> "PositionXY":
        """Create from [X, Y] list."""
        if len(pos) != 2:
            raise ValueError(f"Position must have exactly 2 values, got {len(pos)}")
        return cls(x=pos[0], y=pos[1])

    def to_tuple(self) -> tuple[int, int]:
        """Convert to tuple."""
        return (self.x, self.y)


class AlgorithmicControllerConfig(BaseModel):
    """Configuration for algorithmic (pathfinding) controller."""

    type: Literal["algorithmic"] = "algorithmic"
    algorithm: Literal["astar", "dijkstra", "bfs"] = Field(description="Pathfinding algorithm to use")
    heuristic: Literal["manhattan", "euclidean", "zero"] | None = Field(
        default="manhattan", description="Heuristic function (only for A*)"
    )
    max_steps: int = Field(default=1000, ge=10, le=10000, description="Maximum pathfinding steps")

    @model_validator(mode="after")
    def validate_heuristic_for_algorithm(self):
        """A* requires a heuristic, others ignore it."""
        if self.algorithm == "astar" and self.heuristic == "zero":
            raise ValueError("A* with zero heuristic is just Dijkstra - use dijkstra instead")
        return self


class HumanControllerConfig(BaseModel):
    """Configuration for human keyboard controller."""

    type: Literal["human"] = "human"


class RandomControllerConfig(BaseModel):
    """Configuration for random movement controller."""

    type: Literal["random"] = "random"


class ReplayControllerConfig(BaseModel):
    """Configuration for replay controller."""

    type: Literal["replay"] = "replay"
    replay_file: str = Field(description="Path to replay file with moves")

    @field_validator("replay_file")
    @classmethod
    def validate_replay_file(cls, v: str) -> str:
        """Check replay file exists."""
        from pathlib import Path

        if not Path(v).exists():
            raise ValueError(f"Replay file not found: {v}")
        return v


# Union of all controller types
ControllerConfig = AlgorithmicControllerConfig | HumanControllerConfig | RandomControllerConfig | ReplayControllerConfig


class SnakeConfig(BaseModel):
    """Configuration for a single snake."""

    name: str = Field(min_length=1, max_length=50, description="Snake display name")
    start_position: list[int] = Field(description="Starting position as [X, Y]")
    color: list[int] = Field(description="RGB color as [R, G, B]")
    controller: ControllerConfig = Field(discriminator="type", description="Controller configuration")

    @field_validator("start_position")
    @classmethod
    def validate_position(cls, v: list[int]) -> list[int]:
        """Validate position format."""
        if len(v) != 2:
            raise ValueError(f"Position must be [X, Y], got {len(v)} values")
        if v[0] < 0 or v[1] < 0:
            raise ValueError(f"Position coordinates must be non-negative, got {v}")
        return v

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: list[int]) -> list[int]:
        """Validate RGB color format."""
        if len(v) != 3:
            raise ValueError(f"Color must be [R, G, B], got {len(v)} values")
        for i, component in enumerate(v):
            if not 0 <= component <= 255:
                raise ValueError(f"Color component {i} must be 0-255, got {component}")
        return v


class GameConfig(BaseModel):
    """Configuration for game settings."""

    width: int = Field(ge=10, le=200, description="Grid width in cells")
    height: int = Field(ge=10, le=200, description="Grid height in cells")
    cell_size: int = Field(ge=5, le=50, description="Size of each cell in pixels")
    fps: int = Field(ge=1, le=120, description="Frames per second (game speed)")
    background_color: list[int] = Field(description="Background RGB color as [R, G, B]")
    grid_color: list[int] = Field(description="Grid line RGB color as [R, G, B]")

    @field_validator("background_color", "grid_color")
    @classmethod
    def validate_color(cls, v: list[int]) -> list[int]:
        """Validate RGB color format."""
        if len(v) != 3:
            raise ValueError(f"Color must be [R, G, B], got {len(v)} values")
        for i, component in enumerate(v):
            if not 0 <= component <= 255:
                raise ValueError(f"Color component {i} must be 0-255, got {component}")
        return v


class ConfigSchema(BaseModel):
    """
    Root configuration schema for alg-snake YAML files.

    Example:
        game:
          width: 50
          height: 50
          cell_size: 15
          fps: 20
          background_color: [0, 0, 0]
          grid_color: [255, 255, 255]

        snakes:
          - name: "A* Snake"
            start_position: [5, 5]
            color: [0, 255, 0]
            controller:
              type: "algorithmic"
              algorithm: "astar"
              heuristic: "manhattan"
              max_steps: 1000
    """

    game: GameConfig = Field(description="Game settings")
    snakes: list[SnakeConfig] = Field(min_length=1, max_length=10, description="List of snake configurations")

    @model_validator(mode="after")
    def validate_snakes_fit_in_grid(self):
        """Ensure all snake starting positions are within grid bounds."""
        for snake in self.snakes:
            x, y = snake.start_position
            if x >= self.game.width:
                raise ValueError(f"Snake '{snake.name}' X position ({x}) is outside grid width ({self.game.width})")
            if y >= self.game.height:
                raise ValueError(f"Snake '{snake.name}' Y position ({y}) is outside grid height ({self.game.height})")
        return self

    @model_validator(mode="after")
    def validate_no_duplicate_positions(self):
        """Ensure snakes don't start at the same position."""
        positions = [tuple(snake.start_position) for snake in self.snakes]
        if len(positions) != len(set(positions)):
            raise ValueError("Multiple snakes cannot start at the same position")
        return self

    @model_validator(mode="after")
    def validate_human_controller_limit(self):
        """Only allow one human controller."""
        human_count = sum(1 for snake in self.snakes if snake.controller.type == "human")
        if human_count > 1:
            raise ValueError("Only one snake can have a human controller")
        return self
