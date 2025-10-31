from abc import ABC, abstractmethod
from copy import deepcopy


class SnakeSimulation(ABC):
    @abstractmethod
    def simulate_sequence(self, head, body, apple_pos, sequence_size, grid_size=None, blocked_cells=None):
        """
        Generate a sequence of body positions for each step of the simulation.

        Args:
            head: tuple(int, int) - The current head position of the snake.
            body: list[tuple(int, int)] - The current body positions of the snake.
            apple_pos: tuple(int, int) - The position of the apple.
            sequence_size: int - The number of moves to simulate.
            grid_size: tuple(int, int) - Optional grid dimensions (width, height).
            blocked_cells: set[tuple(int, int)] - Optional set of blocked positions.

        Returns:
            list[list[tuple(int, int)]] - A list where each element is the snake's body
            positions at that step: [[(head_x, head_y), (body1_x, body1_y), ...], ...]
        """
        pass


class GreedySnakeSimulation(SnakeSimulation):
    def simulate_sequence(self, head, body, apple_pos, sequence_size, grid_size=None, blocked_cells=None):
        """
        Simulates a snake that always moves toward the apple, ignoring obstacles.
        """
        positions_per_step = []
        sim_body = deepcopy(body)
        sim_head = head

        for _ in range(sequence_size):
            # Decide move direction - always toward apple
            if sim_head[0] < apple_pos[0]:
                move = (1, 0)  # Move right
            elif sim_head[0] > apple_pos[0]:
                move = (-1, 0)  # Move left
            elif sim_head[1] < apple_pos[1]:
                move = (0, 1)  # Move down
            elif sim_head[1] > apple_pos[1]:
                move = (0, -1)  # Move up
            else:
                move = (0, 0)  # Stay (reached apple)

            # Update head and body
            new_head = (sim_head[0] + move[0], sim_head[1] + move[1])
            sim_body = [new_head] + sim_body[:-1]  # Move forward, no growth assumed
            sim_head = new_head

            # Store a copy of the current body positions
            positions_per_step.append(list(sim_body))

            # Stop if reached apple
            if sim_head == apple_pos:
                break

        return positions_per_step


class ObstacleAwareSnakeSimulation(SnakeSimulation):
    def simulate_sequence(self, head, body, apple_pos, sequence_size, grid_size=None, blocked_cells=None):
        """
        Simulates a snake that moves toward apple but avoids walls, its own body, and blocked cells.
        """
        positions_per_step = []
        sim_body = deepcopy(body)
        sim_head = head
        width, height = grid_size if grid_size else (float("inf"), float("inf"))
        blocked = blocked_cells if blocked_cells else set()

        for _ in range(sequence_size):
            # Get possible moves toward apple
            possible_moves = []

            # Prioritize moves toward apple
            if sim_head[0] < apple_pos[0]:  # Apple is to the right
                possible_moves.append((1, 0))
            elif sim_head[0] > apple_pos[0]:  # Apple is to the left
                possible_moves.append((-1, 0))

            if sim_head[1] < apple_pos[1]:  # Apple is below
                possible_moves.append((0, 1))
            elif sim_head[1] > apple_pos[1]:  # Apple is above
                possible_moves.append((0, -1))

            # If no direct moves toward apple, try all directions
            if not possible_moves:
                possible_moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right

            # Find valid move that doesn't cause collision
            valid_move = None
            for move in possible_moves:
                new_head = (sim_head[0] + move[0], sim_head[1] + move[1])

                # Check bounds
                if grid_size and (new_head[0] < 0 or new_head[0] >= width or new_head[1] < 0 or new_head[1] >= height):
                    continue

                # Check collisions
                if new_head in sim_body or new_head in blocked:
                    continue

                valid_move = move
                break

            # If no valid move found, stop simulation (snake would die)
            if valid_move is None:
                break

            # Apply the move
            new_head = (sim_head[0] + valid_move[0], sim_head[1] + valid_move[1])
            sim_body = [new_head] + sim_body[:-1]  # Move forward, no growth assumed
            sim_head = new_head

            positions_per_step.append(list(sim_body))

            # Stop if reached apple
            if sim_head == apple_pos:
                break

        return positions_per_step


class ConservativeSnakeSimulation(SnakeSimulation):
    def simulate_sequence(self, head, body, apple_pos, sequence_size, grid_size=None, blocked_cells=None):
        """
        Simulates a snake that prioritizes survival over aggressive apple pursuit.
        Avoids risky moves near walls or tight spaces.
        """
        positions_per_step = []
        sim_body = deepcopy(body)
        sim_head = head
        width, height = grid_size if grid_size else (float("inf"), float("inf"))
        blocked = blocked_cells if blocked_cells else set()

        for _ in range(sequence_size):
            # Evaluate all possible moves with safety scoring
            move_scores = []

            for move in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # up, down, left, right
                new_head = (sim_head[0] + move[0], sim_head[1] + move[1])

                # Check if move is valid
                if grid_size and (new_head[0] < 0 or new_head[0] >= width or new_head[1] < 0 or new_head[1] >= height):
                    continue
                if new_head in sim_body or new_head in blocked:
                    continue

                # Calculate safety score for this move
                safety_score = self._calculate_safety_score(new_head, sim_body, apple_pos, grid_size, blocked)
                move_scores.append((move, safety_score))

            # If no valid moves, stop
            if not move_scores:
                break

            # Choose the safest move that still makes progress toward apple
            move_scores.sort(key=lambda x: x[1], reverse=True)
            chosen_move = move_scores[0][0]

            # Apply the move
            new_head = (sim_head[0] + chosen_move[0], sim_head[1] + chosen_move[1])
            sim_body = [new_head] + sim_body[:-1]
            sim_head = new_head

            positions_per_step.append(list(sim_body))

            if sim_head == apple_pos:
                break

        return positions_per_step

    def _calculate_safety_score(self, pos, body, apple_pos, grid_size, blocked_cells):
        """Calculate how safe a position is (higher = safer)"""
        score = 0
        width, height = grid_size if grid_size else (100, 100)

        # Distance from walls (prefer center)
        wall_distance = min(pos[0], width - pos[0] - 1, pos[1], height - pos[1] - 1)
        score += wall_distance * 10

        # Distance from own body (prefer farther)
        if body:
            min_body_distance = min(abs(pos[0] - bx) + abs(pos[1] - by) for bx, by in body)
            score += min_body_distance * 5

        # Progress toward apple (but weighted less than safety)
        apple_distance = abs(pos[0] - apple_pos[0]) + abs(pos[1] - apple_pos[1])
        score -= apple_distance * 2

        return score
