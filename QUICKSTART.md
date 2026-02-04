# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/luislombamartinez/alg-snake.git
cd alg-snake

# (Optional but recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .           # Installs from pyproject.toml
# OR
pip install -r requirements.txt  # Traditional method
```

## For Development

```bash
# Install with development dependencies
pip install -e ".[dev]"
# This includes: pytest, ruff, mypy, pre-commit, etc.
```

## Running the Game

### 1. Interactive Menu (Easiest - Recommended for First Time)

```bash
# Just run without arguments
python main.py

# You'll see a menu like this:
# ============================================================
# 🐍 Welcome to alg-snake Configuration
# ============================================================
# 
# Choose a configuration option:
# 
# 📁 Preset Configurations:
#   1 - default: Default Configuration - A* vs Dijkstra
#   2 - human_vs_ai: Human vs AI Configuration
#   3 - algorithm_comparison: Algorithm Comparison Test
#   ... more options ...
# 
# 🔧 Built-in Configurations:
#   4 - Default (A* vs Dijkstra)
#   5 - Custom (Configure manually)
# 
# Enter choice [1-5] (default 1):

# Just press Enter for default, or choose a number
```

### 2. Direct YAML Loading (Fastest for Repeat Testing)

```bash
# See all available configurations
python main.py --list-configs

# Run a specific configuration
python main.py --config configs/default.yaml

# Short form
python main.py -c configs/human_vs_ai.yaml
```

## Common Use Cases

### Play Snake Yourself
```bash
python main.py -c configs/human_vs_ai.yaml
# Use arrow keys to control your snake
```

### Watch AI Algorithms Compete
```bash
python main.py -c configs/algorithm_comparison.yaml
# See BFS, Dijkstra, and A* in action
```

### Test Pathfinding Algorithms
```bash
python main.py -c configs/default.yaml
# A* vs Dijkstra head-to-head
```

### Create Custom Configuration
```bash
# Copy an example
cp configs/default.yaml configs/my_experiment.yaml

# Edit with your favorite editor
vim configs/my_experiment.yaml

# Run it
python main.py -c configs/my_experiment.yaml
```

## Quick Reference

### Available Controller Types

**Algorithmic (AI using pathfinding):**
```yaml
controller:
  type: "algorithmic"
  algorithm: "astar"  # or "dijkstra", "bfs"
  heuristic: "manhattan"  # or "euclidean" (for A* only)
  max_steps: 1000
```

**Human:**
```yaml
controller:
  type: "human"
```

**Random:**
```yaml
controller:
  type: "random"
```

**Replay (from recorded file):**
```yaml
controller:
  type: "replay"
  replay_file: "replays/game_01.txt"
```

## Color Options

Available colors (use in `color` field):
- `[255, 0, 0]` - Red
- `[0, 255, 0]` - Green
- `[0, 0, 255]` - Blue
- `[255, 255, 0]` - Yellow
- `[0, 255, 255]` - Cyan
- `[255, 0, 255]` - Magenta
- `[255, 255, 255]` - White
- `[128, 128, 128]` - Gray
- `[255, 165, 0]` - Orange

## Troubleshooting

### Game won't start

**Check Python version:**
```bash
python --version  # Should be 3.13+
```

**Reinstall dependencies:**
```bash
pip install -r requirements.txt --force-reinstall
```

### "pygame not found" error

```bash
pip install pygame
```

### Configuration file not found

```bash
# Make sure you're in the project directory
cd alg-snake

# List available configs
python main.py --list-configs
```

### Snake runs into walls immediately

- The grid might be too small for the starting positions
- Try increasing `width` and `height` in the config
- Or adjust `start_position` to be farther from edges

### Algorithms seem slow

- Increase `fps` in the config for faster gameplay
- Or reduce `max_steps` for quicker decision-making
- Note: Very large grids (100x100+) can be slow

## Next Steps

1. **Read the main README** for architecture overview
2. **Explore `configs/README.md`** for detailed YAML documentation
3. **Check out the code** starting with `game/game.py`
4. **Run the tests**: `pytest`
5. **Try implementing a new algorithm** or heuristic

## Configuration File Structure

Basic template:

```yaml
game:
  width: 50
  height: 50
  cell_size: 15
  fps: 20
  background_color: [0, 0, 0]
  grid_color: [255, 255, 255]

snakes:
  - name: "Snake 1"
    start_position: [10, 10]
    color: [0, 255, 0]
    controller:
      type: "algorithmic"
      algorithm: "astar"
      heuristic: "manhattan"
      max_steps: 1000
      
  - name: "Snake 2"
    start_position: [40, 40]
    color: [255, 0, 0]
    controller:
      type: "algorithmic"
      algorithm: "dijkstra"
      max_steps: 1000
```

## Tips

- **Start simple**: Use small grids (20x20) when testing
- **Use high FPS**: Set `fps: 60` to see algorithms run quickly
- **Compare algorithms**: Run multiple snakes with different algorithms
- **Experiment**: Try different heuristics, grid sizes, speeds
- **Learn by modifying**: Copy configs and tweak one variable at a time

---

**Need more help?** Check the [main README](README.md) or open an issue on GitHub!
