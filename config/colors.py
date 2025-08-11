from typing import Literal


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
VIOLET = (148, 0, 211)

COLOR_CHOICES: dict[str, tuple[Literal[0, 255], Literal[0, 255], Literal[0, 255]]] = {
    "black": BLACK,
    "white": WHITE,
    "red": RED,
    "green": GREEN,
    "blue": BLUE,
    "yellow": YELLOW,
    "cyan": CYAN,
    "magenta": MAGENTA,
    "violet": VIOLET,
    "orange": ORANGE,
}
