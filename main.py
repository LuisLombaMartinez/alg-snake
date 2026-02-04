"""
Main entry point for alg-snake game.
Supports both interactive CLI configuration and YAML file configuration.

Usage:
    python main.py                                 # Interactive CLI with YAML presets
    python main.py --config configs/default.yaml   # Load from YAML directly
"""

import argparse
import sys
from pathlib import Path

from config.cli_configurator import CLIConfigurator
from config.configurator import Configurator
from config.yaml_configurator import YAMLConfigurator
from game.game import Game


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Play Snake with various algorithms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
                python main.py                                      # Interactive with YAML presets
                python main.py --config configs/default.yaml        # A* vs Dijkstra
                python main.py -c configs/human_vs_ai.yaml          # Play against AI
                python main.py -c configs/algorithm_comparison.yaml # Compare algorithms
            """,
    )

    parser.add_argument("-c", "--config", type=str, help="Path to YAML configuration file", metavar="FILE")

    parser.add_argument("--list-configs", action="store_true", help="List available example configurations")

    return parser.parse_args()


def list_example_configs():
    """List available example configuration files."""
    configs_dir = Path("configs")
    if not configs_dir.exists():
        print("No configs directory found.")
        return

    yaml_files = list(configs_dir.glob("*.yaml"))

    if not yaml_files:
        print("No example configurations found in configs/")
        return

    print("\n📁 Available Example Configurations:\n")
    for config_file in sorted(yaml_files):
        print(f"  • {config_file.name}")

        # Try to read first comment line as description
        try:
            with open(config_file) as f:
                first_line = f.readline().strip()
                if first_line.startswith("#"):
                    print(f"    {first_line[1:].strip()}")
        except Exception:
            pass

    print("\nUsage: python main.py --config configs/<filename>")
    print()


def main():
    """Main entry point."""
    args = parse_args()

    # Handle --list-configs
    if args.list_configs:
        list_example_configs()
        return

    # Determine configurator to use
    configurator: Configurator
    if args.config:
        # Direct YAML loading (skip menu)
        config_path = Path(args.config)

        if not config_path.exists():
            print(f"❌ Error: Configuration file not found: {args.config}")
            print("\nTip: Use --list-configs to see available examples")
            sys.exit(1)

        print(f"📄 Loading configuration from: {args.config}")
        try:
            configurator = YAMLConfigurator(config_path)
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            sys.exit(1)
    else:
        # Interactive menu mode (shows YAML configs + custom option)
        configurator = CLIConfigurator()

    # Create and run game
    try:
        game = Game.from_configurator(configurator)
        game.run()
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
