from ai.algorithm import PathAlgorithm


class StepLimitedPathfinder:
    def __init__(self, algorithm: PathAlgorithm, max_steps=100):
        """
        Wraps a pathfinding algorithm with a step limit.
        """
        self.algorithm = algorithm
        self.max_steps = max_steps

    def find_path(self, start, goal, blocked, grid_size, prev=None):
        """
        Intercepts the find_path method and injects step limit if supported.
        """
        return self.algorithm.find_path(
            start, goal, blocked, grid_size, max_steps=self.max_steps, prev=prev
        )
