from abc import ABC, abstractmethod

class GridItem(ABC):
    @abstractmethod
    def blocked_cells(self) -> set:
        """Returns all blocked cells."""
        pass

    @abstractmethod
    def position_cells(self) -> set:
        """Returns all occupied cells (even if not blocked)."""
        pass

    @abstractmethod
    def draw(self, screen, cell_size):
        """Draws the item on the given screen."""
        pass
