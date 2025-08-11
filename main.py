from config.cli_configurator import CLIConfigurator
from game.game import Game

def main():
    configurator = CLIConfigurator()
    game = Game.from_configurator(configurator)
    game.run()

if __name__ == "__main__":
    main()
