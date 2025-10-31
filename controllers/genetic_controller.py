import random
from controllers.controller import Controller
from utils.move_utils import DIRECTION_DELTAS
from genetics.fitness_evalutor import FitnessEvaluator
from game.snake import SnakeInfo


class GeneticController(Controller):
    def __init__(
        self,
        fitness_evaluator: FitnessEvaluator,
        population_size=20,
        sequence_length=100,
        mutation_rate=0.05,
    ):
        self.fitness_evaluator = fitness_evaluator
        self.population_size = population_size
        self.sequence_length = sequence_length
        self.mutation_rate = mutation_rate
        self.population = [self._random_sequence() for _ in range(population_size)]
        self.fitness = [0] * population_size
        self.generation = 0
        self.current_index = 0
        self.best_sequence = self.population[0]

    def _random_sequence(self):
        return [random.choice(list(DIRECTION_DELTAS.keys())) for _ in range(self.sequence_length)]

    def _evaluate_fitness(
        self,
        sequence,
        snake,
        grid_size,
        apple_pos,
        blocked_cells,
        **kwargs,
    ):
        return self.fitness_evaluator.evaluate(
            sequence,
            snake,
            grid_size,
            apple_pos,
            blocked_cells,
            **kwargs,
        )

    def _select_parents(self):
        # Select two parents using tournament selection
        tournament = random.sample(list(zip(self.population, self.fitness)), k=4)
        tournament.sort(key=lambda x: x[1], reverse=True)
        return tournament[0][0], tournament[1][0]

    def _crossover(self, parent1, parent2):
        # Single-point crossover
        point = random.randint(1, self.sequence_length - 1)
        return parent1[:point] + parent2[point:]

    def _mutate(self, sequence):
        # Randomly mutate the sequence
        return [
            move if random.random() > self.mutation_rate else random.choice(list(DIRECTION_DELTAS.keys()))
            for move in sequence
        ]

    def _evolve_population(
        self,
        snake,
        grid_size,
        apple_pos,
        blocked_cells,
        **kwargs,
    ):
        self.fitness = [
            self._evaluate_fitness(
                seq,
                snake,
                grid_size,
                apple_pos,
                blocked_cells,
                **kwargs,
            )
            for seq in self.population
        ]
        # Keep the best sequence
        best_idx = self.fitness.index(max(self.fitness))
        self.best_sequence = self.population[best_idx]
        # Create new population
        new_population = [self.best_sequence]  # Elitism: keep the best
        while len(new_population) < self.population_size:
            p1, p2 = self._select_parents()
            child = self._crossover(p1, p2)
            child = self._mutate(child)
            new_population.append(child)
        self.population = new_population
        self.generation += 1
        self.current_index = 0

    def get_next_move(self, snake, grid_size, **kwargs):
        apple_pos = kwargs.get("apple_pos")
        blocked_cells = kwargs.get("blocked_cells")
        other_snakes: list[SnakeInfo] = kwargs.get("other_snakes")

        # Evolve every time we finish a sequence
        if self.current_index == 0:
            self._evolve_population(snake, grid_size, apple_pos, blocked_cells, other_snakes=other_snakes)
        # Use the best sequence for this generation
        direction = self.best_sequence[self.current_index]
        dx, dy = DIRECTION_DELTAS[direction]
        head_x, head_y = snake.head()
        self.current_index = (self.current_index + 1) % self.sequence_length
        return (head_x + dx, head_y + dy)

    def get_display_info(self):
        return f"Genetic Controller (Gen {self.generation}, Step {self.current_index})"
