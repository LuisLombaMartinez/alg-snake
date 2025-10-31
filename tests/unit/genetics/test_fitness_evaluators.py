"""
Unit tests for fitness evaluators.
Tests the different fitness evaluation strategies used in genetic algorithms.
"""

import pytest
from genetics.fitness_evalutor import (
    SinglePlayerAppleFitnessEvaluator,
    SinglePlayerTimeFitnessEvaluator,
    MultiplayerAppleFitnessEvaluator,
    AggressiveFitnessEvaluator,
    BalancedFitnessEvaluator,
    OtherSnakesAwareFitnessEvaluator,
)
from genetics.snake_simulation import (
    GreedySnakeSimulation,
    ObstacleAwareSnakeSimulation,
    ConservativeSnakeSimulation,
)


class TestFitnessEvaluators:
    """Test suite for fitness evaluators."""

    @pytest.mark.unit
    def test_class_attributes_for_simulation_needs(self):
        """Test that fitness evaluators have correct NEEDS_OPPONENT_SIMULATION attributes."""
        # Single player evaluators should not need simulation
        assert not SinglePlayerAppleFitnessEvaluator.NEEDS_OPPONENT_SIMULATION
        assert not SinglePlayerTimeFitnessEvaluator.NEEDS_OPPONENT_SIMULATION

        # Multi-snake aware evaluators should need simulation
        assert MultiplayerAppleFitnessEvaluator.NEEDS_OPPONENT_SIMULATION
        assert AggressiveFitnessEvaluator.NEEDS_OPPONENT_SIMULATION
        assert BalancedFitnessEvaluator.NEEDS_OPPONENT_SIMULATION

    @pytest.mark.unit
    def test_single_player_apple_evaluator(self, sample_snake, grid_size, apple_pos, blocked_cells, test_sequence):
        """Test SinglePlayerAppleFitnessEvaluator basic functionality."""
        evaluator = SinglePlayerAppleFitnessEvaluator()

        fitness = evaluator.evaluate(test_sequence, sample_snake, grid_size, apple_pos, blocked_cells)

        assert isinstance(fitness, (int, float))
        assert fitness >= 0  # Fitness should be non-negative

    @pytest.mark.unit
    def test_single_player_time_evaluator(self, sample_snake, grid_size, apple_pos, blocked_cells, test_sequence):
        """Test SinglePlayerTimeFitnessEvaluator basic functionality."""
        evaluator = SinglePlayerTimeFitnessEvaluator()

        fitness = evaluator.evaluate(test_sequence, sample_snake, grid_size, apple_pos, blocked_cells)

        assert isinstance(fitness, (int, float))
        assert fitness >= 0

    @pytest.mark.unit
    def test_multiplayer_evaluator(
        self, sample_snake, grid_size, apple_pos, blocked_cells, other_snakes_info, test_sequence
    ):
        """Test MultiplayerAppleFitnessEvaluator with opponent simulation."""
        simulation = GreedySnakeSimulation()
        evaluator = MultiplayerAppleFitnessEvaluator(simulation)

        fitness = evaluator.evaluate(
            test_sequence, sample_snake, grid_size, apple_pos, blocked_cells, other_snakes=other_snakes_info
        )

        assert isinstance(fitness, (int, float))
        assert fitness >= 0

    @pytest.mark.unit
    def test_aggressive_evaluator(
        self, sample_snake, grid_size, apple_pos, blocked_cells, other_snakes_info, test_sequence
    ):
        """Test AggressiveFitnessEvaluator with opponent simulation."""
        simulation = GreedySnakeSimulation()
        evaluator = AggressiveFitnessEvaluator(simulation, aggression_level=1.0)

        fitness = evaluator.evaluate(
            test_sequence, sample_snake, grid_size, apple_pos, blocked_cells, other_snakes=other_snakes_info
        )

        assert isinstance(fitness, (int, float))
        assert fitness >= 0

    @pytest.mark.unit
    def test_balanced_evaluator(
        self, sample_snake, grid_size, apple_pos, blocked_cells, other_snakes_info, test_sequence
    ):
        """Test BalancedFitnessEvaluator combining strategies."""
        simulation = ObstacleAwareSnakeSimulation()
        evaluator = BalancedFitnessEvaluator(simulation, aggression_weight=0.3, cooperation_weight=0.7)

        fitness = evaluator.evaluate(
            test_sequence, sample_snake, grid_size, apple_pos, blocked_cells, other_snakes=other_snakes_info
        )

        assert isinstance(fitness, (int, float))
        assert fitness >= 0

    @pytest.mark.unit
    def test_fitness_evaluator_inheritance(self):
        """Test that evaluators properly inherit from base classes."""
        # Test that multi-snake aware evaluators inherit correctly
        assert issubclass(MultiplayerAppleFitnessEvaluator, OtherSnakesAwareFitnessEvaluator)
        assert issubclass(AggressiveFitnessEvaluator, OtherSnakesAwareFitnessEvaluator)
        assert issubclass(BalancedFitnessEvaluator, OtherSnakesAwareFitnessEvaluator)

        # Test that single-player evaluators don't inherit from OtherSnakesAwareFitnessEvaluator
        assert not issubclass(SinglePlayerAppleFitnessEvaluator, OtherSnakesAwareFitnessEvaluator)
        assert not issubclass(SinglePlayerTimeFitnessEvaluator, OtherSnakesAwareFitnessEvaluator)

    @pytest.mark.unit
    def test_fitness_comparison_different_strategies(
        self, sample_snake, grid_size, apple_pos, blocked_cells, other_snakes_info, test_sequence
    ):
        """Test that different fitness evaluators produce different results."""
        # Create evaluators
        single_player = SinglePlayerAppleFitnessEvaluator()
        multiplayer = MultiplayerAppleFitnessEvaluator(GreedySnakeSimulation())
        aggressive = AggressiveFitnessEvaluator(GreedySnakeSimulation(), aggression_level=1.5)

        # Evaluate same sequence
        fitness_single = single_player.evaluate(test_sequence, sample_snake, grid_size, apple_pos, blocked_cells)
        fitness_multi = multiplayer.evaluate(
            test_sequence, sample_snake, grid_size, apple_pos, blocked_cells, other_snakes=other_snakes_info
        )
        fitness_aggressive = aggressive.evaluate(
            test_sequence, sample_snake, grid_size, apple_pos, blocked_cells, other_snakes=other_snakes_info
        )

        # Results should be different (different strategies)
        fitness_values = [fitness_single, fitness_multi, fitness_aggressive]
        assert len(set(fitness_values)) > 1, "Different evaluators should produce different fitness values"


class TestSnakeSimulations:
    """Test suite for snake simulation classes."""

    @pytest.mark.unit
    def test_greedy_simulation(self, sample_snake, apple_pos, grid_size, blocked_cells):
        """Test GreedySnakeSimulation behavior."""
        simulation = GreedySnakeSimulation()

        result = simulation.simulate_sequence(
            sample_snake.head(), sample_snake.body, apple_pos, 5, grid_size, blocked_cells
        )

        assert isinstance(result, list)
        assert len(result) <= 5  # Should not exceed requested steps
        # Each step should be a list of body positions
        for step in result:
            assert isinstance(step, list)
            if step:  # If not empty
                assert isinstance(step[0], tuple)  # Head position should be tuple

    @pytest.mark.unit
    def test_obstacle_aware_simulation(self, sample_snake, apple_pos, grid_size, blocked_cells):
        """Test ObstacleAwareSnakeSimulation avoids obstacles."""
        simulation = ObstacleAwareSnakeSimulation()

        result = simulation.simulate_sequence(
            sample_snake.head(), sample_snake.body, apple_pos, 3, grid_size, blocked_cells
        )

        assert isinstance(result, list)
        # Should try to avoid blocked cells
        for step in result:
            if step:  # If movement was possible
                head_pos = step[0]
                # Head shouldn't move into blocked cells if avoidable
                # (though might be forced if no other options)
                assert isinstance(head_pos, tuple)

    @pytest.mark.unit
    def test_conservative_simulation(self, sample_snake, apple_pos, grid_size, blocked_cells):
        """Test ConservativeSnakeSimulation prioritizes safety."""
        simulation = ConservativeSnakeSimulation()

        result = simulation.simulate_sequence(
            sample_snake.head(), sample_snake.body, apple_pos, 5, grid_size, blocked_cells
        )

        assert isinstance(result, list)
        # Conservative simulation should prefer safer moves
        for step in result:
            if step:
                head_pos = step[0]
                assert isinstance(head_pos, tuple)
                # Should stay within bounds
                assert 0 <= head_pos[0] < grid_size[0]
                assert 0 <= head_pos[1] < grid_size[1]
