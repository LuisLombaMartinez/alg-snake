from abc import ABC, abstractmethod
from copy import deepcopy

from utils.move_utils import DIRECTION_DELTAS
from game.snake import SnakeInfo
from genetics.snake_simulation import GreedySnakeSimulation


class FitnessEvaluator(ABC):
    # Class attribute indicating if this evaluator needs opponent simulation
    NEEDS_OPPONENT_SIMULATION = False

    @abstractmethod
    def evaluate(self, sequence, snake, grid_size, apple_pos, blocked_cells, **kwargs) -> float:
        pass


class OtherSnakesAwareFitnessEvaluator(FitnessEvaluator):
    # Override to indicate this class needs opponent simulation
    NEEDS_OPPONENT_SIMULATION = True

    @abstractmethod
    def evaluate(
        self,
        sequence,
        snake,
        grid_size,
        apple_pos,
        blocked_cells,
        other_snakes: list[SnakeInfo] = None,
        **kwargs,
    ) -> float:
        pass


class SinglePlayerAppleFitnessEvaluator(FitnessEvaluator):
    def evaluate(self, sequence, snake, grid_size, apple_pos, blocked_cells, **kwargs) -> float:
        sim_snake = deepcopy(snake)
        width, height = grid_size
        apples_eaten = 0
        steps_survived = 0

        for move in sequence:
            dx, dy = DIRECTION_DELTAS[move]
            head_x, head_y = sim_snake.head()
            new_head = (head_x + dx, head_y + dy)

            # Check wall or self collision
            if not (0 <= new_head[0] < width and 0 <= new_head[1] < height):
                break
            if new_head in sim_snake.body:
                break
            if blocked_cells and new_head in blocked_cells:
                break

            sim_snake.body.insert(0, new_head)
            if new_head == apple_pos:
                apples_eaten += 1
                # Optionally respawn apple or break; here we break for simplicity
                break
            else:
                sim_snake.body.pop()
            steps_survived += 1

        # Fitness: prioritize apples, then survival
        return apples_eaten * 1000 + steps_survived


class SinglePlayerTimeFitnessEvaluator(FitnessEvaluator):
    """
    Fitness evaluator that prioritizes survival time while avoiding obstacles.
    Does not consider other snakes' movements, but respects static blocked cells.
    """

    def evaluate(self, sequence, snake, grid_size, apple_pos, blocked_cells, **kwargs) -> float:
        sim_snake = deepcopy(snake)
        width, height = grid_size
        fitness = 0
        steps_survived = 0

        for step_idx, move in enumerate(sequence):
            dx, dy = DIRECTION_DELTAS[move]
            head_x, head_y = sim_snake.head()
            new_head = (head_x + dx, head_y + dy)

            # Check wall collision
            if not (0 <= new_head[0] < width and 0 <= new_head[1] < height):
                break

            # Check self collision
            if new_head in sim_snake.body:
                break

            # Check collision with static blocked cells (obstacles)
            if blocked_cells and new_head in blocked_cells:
                break

            # Move snake
            sim_snake.body.insert(0, new_head)

            # Reaching apple gives bonus but isn't the primary goal
            if new_head == apple_pos:
                fitness += 500  # Moderate apple bonus
                break
            else:
                sim_snake.body.pop()

            steps_survived += 1

            # Primary fitness: survival time with bonuses for safe positioning
            fitness += 10  # Base survival points

            # Bonus for staying away from walls (safety margin)
            wall_distance = min(new_head[0], width - 1 - new_head[0], new_head[1], height - 1 - new_head[1])
            if wall_distance >= 3:
                fitness += 5  # Bonus for safe distance from walls
            elif wall_distance == 1:
                fitness -= 2  # Penalty for being too close to walls

            # Bonus for not cornering yourself (avoid tight spaces)
            free_neighbors = 0
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (new_head[0] + dx, new_head[1] + dy)
                if (
                    0 <= neighbor[0] < width
                    and 0 <= neighbor[1] < height
                    and neighbor not in sim_snake.body
                    and (not blocked_cells or neighbor not in blocked_cells)
                ):
                    free_neighbors += 1

            if free_neighbors >= 3:
                fitness += 3  # Bonus for having escape routes
            elif free_neighbors <= 1:
                fitness -= 5  # Penalty for being in tight spots

        # Extra bonus for long survival
        if steps_survived > len(sequence) * 0.8:  # Survived most of the sequence
            fitness += steps_survived * 5

        return max(0, fitness)


class MultiplayerAppleFitnessEvaluator(OtherSnakesAwareFitnessEvaluator):
    def __init__(self, opponent_simulation=None):
        """
        Args:
            opponent_simulation: SnakeSimulation instance to predict opponent behavior.
            Defaults to GreedySnakeSimulation if not provided.
        """
        self.opponent_simulation = opponent_simulation or GreedySnakeSimulation()

    def evaluate(
        self,
        sequence,
        snake,
        grid_size,
        apple_pos,
        blocked_cells,
        other_snakes: list[SnakeInfo] = None,
        **kwargs,
    ) -> float:
        if not other_snakes:
            # Fall back to single player evaluation if no other snakes
            return self._evaluate_single_player(sequence, snake, grid_size, apple_pos, blocked_cells)

        sim_snake = deepcopy(snake)
        width, height = grid_size
        fitness = 0
        steps_survived = 0
        apple_reached = False

        # Predict opponent movements for comparison
        opponent_predictions = {}
        for i, other_snake_info in enumerate(other_snakes):
            # Skip if this is our own snake (compare by head position since we can't compare objects)
            if other_snake_info.head != snake.head():
                predicted_positions = self.opponent_simulation.simulate_sequence(
                    other_snake_info.head,
                    [other_snake_info.head] + other_snake_info.body,  # Reconstruct full body
                    apple_pos,
                    len(sequence),
                    grid_size,
                    blocked_cells,
                )
                opponent_predictions[f"opponent_{i}"] = predicted_positions

        # Simulate our sequence
        for step_idx, move in enumerate(sequence):
            dx, dy = DIRECTION_DELTAS[move]
            head_x, head_y = sim_snake.head()
            new_head = (head_x + dx, head_y + dy)

            # Check wall collision
            if not (0 <= new_head[0] < width and 0 <= new_head[1] < height):
                break

            # Check self collision
            if new_head in sim_snake.body:
                break

            # Check collision with predicted opponent positions
            collision_with_opponent = False
            for opponent, predictions in opponent_predictions.items():
                if step_idx < len(predictions):
                    opponent_body_at_step = predictions[step_idx]
                    if new_head in opponent_body_at_step:
                        collision_with_opponent = True
                        break

            if collision_with_opponent:
                fitness -= 500  # Heavy penalty for predicted collision
                break

            # Move snake
            sim_snake.body.insert(0, new_head)

            # Check if we reached apple
            if new_head == apple_pos:
                apple_reached = True

                # Bonus if we reach apple before opponents
                reached_first = True
                for opponent, predictions in opponent_predictions.items():
                    for pred_step in range(min(step_idx + 1, len(predictions))):
                        if (
                            pred_step < len(predictions)
                            and len(predictions[pred_step]) > 0
                            and predictions[pred_step][0] == apple_pos
                        ):  # Opponent head at apple
                            if pred_step <= step_idx:
                                reached_first = False
                                break
                    if not reached_first:
                        break

                if reached_first:
                    fitness += 2000  # Big bonus for reaching apple first
                else:
                    fitness += 1000  # Still good to reach apple
                break
            else:
                sim_snake.body.pop()

            steps_survived += 1

            # Small bonus for each step survived
            fitness += 1

            # Bonus for maintaining distance from opponents
            min_opponent_distance = float("inf")
            for opponent, predictions in opponent_predictions.items():
                if step_idx < len(predictions) and len(predictions[step_idx]) > 0:
                    opponent_head = predictions[step_idx][0]
                    distance = abs(new_head[0] - opponent_head[0]) + abs(new_head[1] - opponent_head[1])
                    min_opponent_distance = min(min_opponent_distance, distance)

            if min_opponent_distance != float("inf"):
                if min_opponent_distance < 3:
                    fitness -= 10  # Penalty for being too close
                elif min_opponent_distance > 8:
                    fitness -= 5  # Small penalty for being too far (less competitive)

        # Final bonuses/penalties
        if apple_reached:
            fitness += 500

        fitness += steps_survived * 2

        return max(0, fitness)  # Ensure non-negative fitness

    def _evaluate_single_player(self, sequence, snake, grid_size, apple_pos, blocked_cells):
        """Fallback to single player evaluation when no opponents"""
        evaluator = SinglePlayerAppleFitnessEvaluator()
        return evaluator.evaluate(sequence, snake, grid_size, apple_pos, blocked_cells)


class AggressiveFitnessEvaluator(OtherSnakesAwareFitnessEvaluator):
    def __init__(self, opponent_simulation=None, aggression_level=1.0):
        """
        Args:
            opponent_simulation: SnakeSimulation instance to predict opponent behavior.
            aggression_level: Float controlling how aggressive the behavior is (0.5-2.0 recommended).
        """
        self.opponent_simulation = opponent_simulation or GreedySnakeSimulation()
        self.aggression_level = aggression_level

    def evaluate(
        self,
        sequence,
        snake,
        grid_size,
        apple_pos,
        blocked_cells,
        other_snakes: list[SnakeInfo] = None,
        **kwargs,
    ) -> float:
        if not other_snakes:
            # Fall back to single player with aggressive apple pursuit
            return self._evaluate_aggressive_single_player(sequence, snake, grid_size, apple_pos, blocked_cells)

        sim_snake = deepcopy(snake)
        width, height = grid_size
        fitness = 0
        steps_survived = 0

        # Predict opponent movements
        opponent_predictions = {}
        for i, other_snake_info in enumerate(other_snakes):
            # Skip if this is our own snake (compare by head position)
            if other_snake_info.head != snake.head():
                predicted_positions = self.opponent_simulation.simulate_sequence(
                    other_snake_info.head,
                    [other_snake_info.head] + other_snake_info.body,  # Reconstruct full body
                    apple_pos,
                    len(sequence),
                    grid_size,
                    blocked_cells,
                )
                opponent_predictions[f"opponent_{i}"] = predicted_positions

        # Simulate our sequence with aggressive evaluation
        for step_idx, move in enumerate(sequence):
            dx, dy = DIRECTION_DELTAS[move]
            head_x, head_y = sim_snake.head()
            new_head = (head_x + dx, head_y + dy)

            # Basic survival checks
            if not (0 <= new_head[0] < width and 0 <= new_head[1] < height):
                fitness -= 1000  # Heavy penalty for dying
                break

            if new_head in sim_snake.body:
                fitness -= 1000
                break

            # Check if we're cutting off opponents (aggressive behavior)
            cutoff_bonus = 0
            territory_control_bonus = 0

            for opponent, predictions in opponent_predictions.items():
                if step_idx < len(predictions):
                    opponent_positions = predictions[step_idx]
                    if len(opponent_positions) > 0:
                        opponent_head = opponent_positions[0]

                        # Bonus for being close to opponent (intimidation/cutting off)
                        distance_to_opponent = abs(new_head[0] - opponent_head[0]) + abs(new_head[1] - opponent_head[1])

                        if distance_to_opponent <= 2:
                            cutoff_bonus += 50 * self.aggression_level  # Close combat bonus

                        # Bonus for blocking opponent's path to apple
                        our_blocking_effect = self._calculate_blocking_effect(
                            new_head, opponent_head, apple_pos, opponent_positions
                        )

                        cutoff_bonus += our_blocking_effect * 30 * self.aggression_level

                        # Territory control: bonus for being in "central" or strategic positions
                        center_x, center_y = width // 2, height // 2
                        distance_to_center = abs(new_head[0] - center_x) + abs(new_head[1] - center_y)
                        territory_control_bonus += max(0, (width + height) // 4 - distance_to_center) * 5

            fitness += cutoff_bonus + territory_control_bonus

            # Move snake
            sim_snake.body.insert(0, new_head)

            # Apple reaching (lower priority than aggression)
            if new_head == apple_pos:
                fitness += 800  # Good but not as high as competitive behavior
                # Extra bonus if we denied it from opponents
                for opponent, predictions in opponent_predictions.items():
                    opponent_could_reach = any(
                        len(pred) > 0 and pred[0] == apple_pos for i, pred in enumerate(predictions[: step_idx + 2])
                    )
                    if opponent_could_reach:
                        fitness += 300 * self.aggression_level  # Denial bonus
                break
            else:
                sim_snake.body.pop()

            steps_survived += 1
            fitness += 2  # Basic survival

            # Aggressive positioning: stay near opponents and apple corridor
            apple_distance = abs(new_head[0] - apple_pos[0]) + abs(new_head[1] - apple_pos[1])
            if apple_distance < 10:  # Near apple area
                fitness += 5

        # Final scoring adjustments
        fitness += steps_survived * 3

        # Bonus for overall aggressive positioning
        if opponent_predictions:
            total_distance = 0
            valid_opponents = 0
            for predictions in opponent_predictions.values():
                if predictions and len(predictions) > 0 and len(predictions[-1]) > 0:
                    final_pred = predictions[-1]
                    distance = abs(sim_snake.head()[0] - final_pred[0][0]) + abs(sim_snake.head()[1] - final_pred[0][1])
                    total_distance += distance
                    valid_opponents += 1

            if valid_opponents > 0:
                avg_opponent_distance = total_distance / valid_opponents
                if avg_opponent_distance < 5:
                    fitness += 100 * self.aggression_level  # Staying close to opponents

        return max(0, fitness)

    def _calculate_blocking_effect(self, our_pos, opponent_head, apple_pos, opponent_body):
        """Calculate how much we're blocking opponent's path to apple"""
        # Simple heuristic: if we're between opponent and apple
        if (our_pos[0] - opponent_head[0]) * (apple_pos[0] - opponent_head[0]) > 0 and (
            our_pos[1] - opponent_head[1]
        ) * (apple_pos[1] - opponent_head[1]) > 0:
            # We're in the general direction from opponent to apple
            opponent_apple_dist = abs(opponent_head[0] - apple_pos[0]) + abs(opponent_head[1] - apple_pos[1])
            our_apple_dist = abs(our_pos[0] - apple_pos[0]) + abs(our_pos[1] - apple_pos[1])
            our_opponent_dist = abs(our_pos[0] - opponent_head[0]) + abs(our_pos[1] - opponent_head[1])

            # If we're roughly between them, return blocking effect
            if our_opponent_dist + our_apple_dist <= opponent_apple_dist + 2:
                return min(10, opponent_apple_dist - our_apple_dist)  # Higher when closer to apple

        return 0

    def _evaluate_aggressive_single_player(self, sequence, snake, grid_size, apple_pos, blocked_cells):
        """Aggressive single player: prioritize fast, risky apple pursuit"""
        sim_snake = deepcopy(snake)
        width, height = grid_size
        fitness = 0

        for step_idx, move in enumerate(sequence):
            dx, dy = DIRECTION_DELTAS[move]
            head_x, head_y = sim_snake.head()
            new_head = (head_x + dx, head_y + dy)

            if not (0 <= new_head[0] < width and 0 <= new_head[1] < height):
                break
            if new_head in sim_snake.body:
                break
            if blocked_cells and new_head in blocked_cells:
                break

            sim_snake.body.insert(0, new_head)

            if new_head == apple_pos:
                # Bonus for reaching apple quickly (aggressive pursuit)
                speed_bonus = max(0, len(sequence) - step_idx) * 10
                fitness += 1500 + speed_bonus
                break
            else:
                sim_snake.body.pop()

            # Bonus for making progress toward apple
            apple_distance = abs(new_head[0] - apple_pos[0]) + abs(new_head[1] - apple_pos[1])
            fitness += max(0, (width + height) - apple_distance * 2)  # Aggressive apple pursuit
            fitness += 1  # Survival

        return fitness


class BalancedFitnessEvaluator(OtherSnakesAwareFitnessEvaluator):
    def __init__(self, opponent_simulation=None, aggression_weight=0.3, cooperation_weight=0.7):
        """
        Combines competitive and cooperative strategies.

        Args:
            opponent_simulation: SnakeSimulation for predicting opponents
            aggression_weight: How much to weight aggressive behavior (0.0-1.0)
            cooperation_weight: How much to weight cooperative behavior (0.0-1.0)
        """
        from genetics.snake_simulation import ObstacleAwareSnakeSimulation

        self.opponent_simulation = opponent_simulation or ObstacleAwareSnakeSimulation()
        self.aggression_weight = aggression_weight
        self.cooperation_weight = cooperation_weight

        # Initialize sub-evaluators
        self.aggressive_evaluator = AggressiveFitnessEvaluator(opponent_simulation, aggression_level=0.8)
        self.multiplayer_evaluator = MultiplayerAppleFitnessEvaluator(opponent_simulation)

    def evaluate(
        self,
        sequence,
        snake,
        grid_size,
        apple_pos,
        blocked_cells,
        other_snakes: list[SnakeInfo] = None,
        **kwargs,
    ) -> float:
        # Get fitness from both strategies
        aggressive_fitness = self.aggressive_evaluator.evaluate(
            sequence, snake, grid_size, apple_pos, blocked_cells, other_snakes, **kwargs
        )

        cooperative_fitness = self.multiplayer_evaluator.evaluate(
            sequence, snake, grid_size, apple_pos, blocked_cells, other_snakes, **kwargs
        )

        # Combine with weights
        balanced_fitness = self.aggression_weight * aggressive_fitness + self.cooperation_weight * cooperative_fitness

        return balanced_fitness
