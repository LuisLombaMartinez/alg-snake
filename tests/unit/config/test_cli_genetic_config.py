"""
Unit tests for CLI genetic controller configuration.
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


class TestCLIGeneticConfiguration:
    """Test suite for CLI genetic controller configuration."""

    @pytest.mark.unit
    def test_class_attributes_for_simulation_needs(self):
        """Test NEEDS_OPPONENT_SIMULATION class attributes are correctly set."""
        # Single player evaluators should not need simulation
        assert not SinglePlayerAppleFitnessEvaluator.NEEDS_OPPONENT_SIMULATION
        assert not SinglePlayerTimeFitnessEvaluator.NEEDS_OPPONENT_SIMULATION

        # Multi-snake aware evaluators should need simulation
        assert MultiplayerAppleFitnessEvaluator.NEEDS_OPPONENT_SIMULATION
        assert AggressiveFitnessEvaluator.NEEDS_OPPONENT_SIMULATION
        assert BalancedFitnessEvaluator.NEEDS_OPPONENT_SIMULATION

    @pytest.mark.unit
    def test_isinstance_check_inheritance(self):
        """Test isinstance() correctly identifies inheritance relationships."""
        # Test SinglePlayerAppleFitnessEvaluator
        single_player = SinglePlayerAppleFitnessEvaluator()
        needs_simulation = isinstance(single_player, OtherSnakesAwareFitnessEvaluator)
        assert not needs_simulation

        # Test MultiplayerAppleFitnessEvaluator
        multiplayer = MultiplayerAppleFitnessEvaluator()
        needs_simulation = isinstance(multiplayer, OtherSnakesAwareFitnessEvaluator)
        assert needs_simulation

        # Test AggressiveFitnessEvaluator
        aggressive = AggressiveFitnessEvaluator()
        needs_simulation = isinstance(aggressive, OtherSnakesAwareFitnessEvaluator)
        assert needs_simulation

        # Test BalancedFitnessEvaluator
        balanced = BalancedFitnessEvaluator()
        needs_simulation = isinstance(balanced, OtherSnakesAwareFitnessEvaluator)
        assert needs_simulation

    @pytest.mark.unit
    def test_fitness_evaluator_class_attributes_exist(self):
        """Test that all fitness evaluators have NEEDS_OPPONENT_SIMULATION attribute."""
        evaluator_classes = [
            SinglePlayerAppleFitnessEvaluator,
            SinglePlayerTimeFitnessEvaluator,
            MultiplayerAppleFitnessEvaluator,
            AggressiveFitnessEvaluator,
            BalancedFitnessEvaluator,
        ]

        for evaluator_class in evaluator_classes:
            assert hasattr(evaluator_class, "NEEDS_OPPONENT_SIMULATION")
            assert isinstance(evaluator_class.NEEDS_OPPONENT_SIMULATION, bool)

    @pytest.mark.unit
    def test_cli_configuration_logic_simulation(self):
        """Test the CLI configuration logic for determining when to ask for simulation."""
        # Simulate the CLI logic using class attributes
        evaluator_classes = {
            "1": SinglePlayerAppleFitnessEvaluator,
            "2": SinglePlayerTimeFitnessEvaluator,
            "3": MultiplayerAppleFitnessEvaluator,
            "4": AggressiveFitnessEvaluator,
            "5": BalancedFitnessEvaluator,
        }

        for choice, evaluator_class in evaluator_classes.items():
            needs_sim = evaluator_class.NEEDS_OPPONENT_SIMULATION

            if choice in ["1", "2"]:  # Single player evaluators
                assert not needs_sim, f"Choice {choice} should not need simulation"
            else:  # Multi-snake aware evaluators
                assert needs_sim, f"Choice {choice} should need simulation"
