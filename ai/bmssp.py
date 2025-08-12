from ai.algorithm import PathAlgorithm


class BMSSP(PathAlgorithm):
    def find_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        prev: tuple[int, int] | None,
        blocked: set[tuple[int, int]],
        grid_size: tuple[int, int],
        max_steps: int,
    ) -> tuple[list[tuple[int, int]], int]:
        # Placeholder: just return a random move for now
        return [self.get_random_move(start, prev)], 1
