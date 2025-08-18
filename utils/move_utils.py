import random

DIRECTION_DELTAS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}


def get_random_move(
    start: tuple[int, int], prev: tuple[int, int] = None
) -> tuple[int, int]:
    """
    Returns a random move from the start position, excluding the direction it came from.
    - start: current head position
    - prev: previous head position (None for first move)
    """
    x, y = start
    moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    if prev is not None:
        moves = [m for m in moves if m != prev]
    return random.choice(moves) if moves else start
