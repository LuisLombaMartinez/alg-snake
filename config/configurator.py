"""
Abstract base class for game configurators.

This module provides a simple, generic interface that any configurator
must implement. Different configurators (CLI, YAML, GUI, etc.) can all
implement this interface, making them completely interchangeable.

Design Philosophy:
- Keep the interface minimal (one method!)
- Each configurator handles its own complexity internally
- Game logic never needs to know which configurator is used
"""

from abc import ABC, abstractmethod

from config.configuration import Configuration


class Configurator(ABC):
    """
    Abstract base for all configuration sources.

    Any configurator (CLI, YAML, GUI, network, etc.) must implement
    just one method: build_configuration().

    This makes configurators completely interchangeable - the game
    only cares about getting a valid Configuration object, not where
    it came from or how it was created.
    """

    @abstractmethod
    def build_configuration(self) -> Configuration:
        """
        Build and return a complete Configuration object.

        Each configurator implements this differently:
        - CLIConfigurator: Asks user questions interactively
        - YAMLConfigurator: Loads and validates from file
        - GUIConfigurator: Shows a graphical dialog
        - NetworkConfigurator: Fetches from API
        - etc.

        Returns:
            Configuration: A complete, ready-to-use game configuration

        Raises:
            Any exceptions specific to the configurator type
            (e.g., FileNotFoundError for YAML, ValidationError, etc.)
        """
        pass
