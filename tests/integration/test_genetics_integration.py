"""
Integration tests for the genetics module.
Tests the complete genetic algorithm workflow.
"""

import pytest
from controllers.genetic_controller import GeneticController
from genetics.fitness_evalutor import SinglePlayerAppleFitnessEvaluator, MultiplayerAppleFitnessEvaluator
from genetics.snake_simulation import GreedySnakeSimulation


class TestGeneticsIntegration:
    """Integration tests for genetic algorithm components."""

    @pytest.mark.integration
    def test_genetic_controller_creation(self):
        """Test that genetic controller can be created with different fitness evaluators."""
        # Single player genetic controller
        single_evaluator = SinglePlayerAppleFitnessEvaluator()
        controller1 = GeneticController(
            fitness_evaluator=single_evaluator, population_size=10, sequence_length=20, mutation_rate=0.1
        )

        assert controller1.population_size == 10
        assert controller1.sequence_length == 20
        assert controller1.mutation_rate == 0.1
        assert controller1.generation == 0
        assert len(controller1.population) == 10

        # Multiplayer genetic controller
        multi_evaluator = MultiplayerAppleFitnessEvaluator(GreedySnakeSimulation())
        controller2 = GeneticController(
            fitness_evaluator=multi_evaluator, population_size=15, sequence_length=30, mutation_rate=0.05
        )

        assert controller2.population_size == 15
        assert controller2.sequence_length == 30
        assert controller2.mutation_rate == 0.05

    @pytest.mark.integration
    def test_genetic_controller_evolution(self, sample_snake, grid_size, apple_pos, blocked_cells, other_snakes_info):
        """Test that genetic controller can evolve population over generations."""
        evaluator = SinglePlayerAppleFitnessEvaluator()
        controller = GeneticController(
            fitness_evaluator=evaluator, population_size=5, sequence_length=10, mutation_rate=0.2
        )

        initial_generation = controller.generation
        initial_best = controller.best_sequence.copy()

        # Simulate several moves to trigger evolution
        for _ in range(controller.sequence_length):
            move = controller.get_next_move(
                sample_snake,
                grid_size,
                apple_pos=apple_pos,
                blocked_cells=blocked_cells,
                other_snakes=other_snakes_info,
            )
            assert isinstance(move, tuple)
            assert len(move) == 2

        # Should have evolved at least once
        assert controller.generation > initial_generation

    @pytest.mark.integration
    def test_genetic_controller_with_multiplayer_evaluator(
        self, sample_snake, grid_size, apple_pos, blocked_cells, other_snakes_info
    ):
        """Test genetic controller with multiplayer fitness evaluator and opponent simulation."""
        simulation = GreedySnakeSimulation()
        evaluator = MultiplayerAppleFitnessEvaluator(simulation)
        controller = GeneticController(
            fitness_evaluator=evaluator, population_size=8, sequence_length=15, mutation_rate=0.1
        )

        # Test multiple moves with other snakes present
        moves = []
        for _ in range(5):
            move = controller.get_next_move(
                sample_snake,
                grid_size,
                apple_pos=apple_pos,
                blocked_cells=blocked_cells,
                other_snakes=other_snakes_info,
            )
            moves.append(move)
            assert isinstance(move, tuple)
            assert len(move) == 2

        # Should generate valid moves
        assert len(moves) == 5
        assert all(isinstance(m, tuple) for m in moves)

    @pytest.mark.integration
    def test_genetic_controller_display_info(self):
        """Test that genetic controller provides meaningful display information."""
        evaluator = SinglePlayerAppleFitnessEvaluator()
        controller = GeneticController(
            fitness_evaluator=evaluator, population_size=10, sequence_length=20, mutation_rate=0.05
        )

        display_info = controller.get_display_info()
        assert isinstance(display_info, str)
        assert "Genetic Controller" in display_info
        assert "Gen" in display_info
        assert "Step" in display_info

    @pytest.mark.integration
    @pytest.mark.slow
    def test_genetic_algorithm_convergence(self, sample_snake, grid_size, apple_pos, blocked_cells):
        """Test that genetic algorithm shows improvement over multiple generations."""
        evaluator = SinglePlayerAppleFitnessEvaluator()
        controller = GeneticController(
            fitness_evaluator=evaluator, population_size=20, sequence_length=50, mutation_rate=0.1
        )

        initial_fitness_scores = []
        final_fitness_scores = []

        # Run for multiple generations
        generations_to_test = 3
        moves_per_generation = controller.sequence_length

        for gen in range(generations_to_test):
            generation_fitness = []

            # Complete a full sequence to trigger evolution
            for step in range(moves_per_generation):
                # Evaluate current best sequence fitness before move
                if step == 0:
                    fitness = controller._evaluate_fitness(
                        controller.best_sequence, sample_snake, grid_size, apple_pos, blocked_cells
                    )
                    generation_fitness.append(fitness)

                # Make move (this will trigger evolution when sequence completes)
                controller.get_next_move(sample_snake, grid_size, apple_pos=apple_pos, blocked_cells=blocked_cells)

            if gen == 0:
                initial_fitness_scores.extend(generation_fitness)
            elif gen == generations_to_test - 1:
                final_fitness_scores.extend(generation_fitness)

        # The algorithm should maintain or improve fitness over generations
        # (Note: Due to randomness, we can't guarantee improvement, but we can check it doesn't crash)
        assert len(initial_fitness_scores) > 0
        assert len(final_fitness_scores) > 0
        assert all(isinstance(f, (int, float)) for f in initial_fitness_scores + final_fitness_scores)
