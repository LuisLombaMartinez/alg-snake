# Configuration Files

This directory contains example YAML configuration files for alg-snake.
These files allow you to quickly set up different game scenarios without going through the interactive CLI.

## Available Configurations

### `default.yaml`
**A* vs Dijkstra** - Simple two-snake comparison of pathfinding algorithms
- 50x50 grid
- A* with Manhattan heuristic vs Dijkstra
- Good for understanding basic algorithm differences

### `human_vs_ai.yaml`
**Human vs AI** - Play snake yourself!
- Smaller 30x30 grid for focused gameplay
- Control your snake with arrow keys
- Compete against A* AI opponent

### `algorithm_comparison.yaml`
**Algorithm Comparison** - Compare all pathfinding algorithms
- Four snakes: BFS, Dijkstra, A* Manhattan, A* Euclidean
- Large 60x30 grid for long-term performance testing
- Great for benchmarking

## Usage

### Running a Configuration

```bash
# Using full flag
python main.py --config configs/default.yaml

# Using short flag
python main.py -c configs/default.yaml

# List all available configs
python main.py --list-configs
```

### Creating Custom Configurations

Copy an existing configuration and modify it:

```bash
cp configs/default.yaml configs/my_config.yaml
# Edit my_config.yaml
python main.py -c configs/my_config.yaml
```

## YAML Structure

### Basic Structure

```yaml
game:
  width: 50              # Grid width
  height: 50             # Grid height
  cell_size: 15          # Pixels per cell
  fps: 20                # Game speed
  background_color: [0, 0, 0]     # RGB
  grid_color: [255, 255, 255]     # RGB

snakes:
  - name: "Snake 1"
    start_position: [5, 5]        # [x, y]
    color: [0, 255, 0]             # RGB
    controller:
      type: "algorithmic"
      # Controller-specific options...
```

## Controller Types

### 1. Human Controller
```yaml
controller:
  type: "human"
```

### 2. Random Controller
```yaml
controller:
  type: "random"
```

### 3. Algorithmic Controller
```yaml
controller:
  type: "algorithmic"
  algorithm: "astar"        # Options: astar, dijkstra, bfs
  heuristic: "manhattan"    # Options: manhattan, euclidean, zero (for A* only)
  max_steps: 1000           # Maximum pathfinding steps
```

## Color Reference

Common colors (use RGB values):
- Red: `[255, 0, 0]`
- Green: `[0, 255, 0]`
- Blue: `[0, 0, 255]`
- Yellow: `[255, 255, 0]`
- Magenta: `[255, 0, 255]`
- Cyan: `[0, 255, 255]`
- White: `[255, 255, 255]`
- Black: `[0, 0, 0]`
- Orange: `[255, 165, 0]`
- Purple: `[128, 0, 128]`

## Tips for Good Configurations

1. **Grid Size**: Larger grids (50x50+) allow longer games but may be slower
2. **FPS**: 10-15 for watching AI, 5-8 for analyzing behavior, 20+ for fast games
3. **Cell Size**: 12-20 pixels works well for most screen sizes
4. **Start Positions**: Place snakes far apart to avoid early collisions
5. **Algorithm Mix**: Combine different algorithms to compare performance

## Troubleshooting

### "Configuration file not found"
- Check the path is correct relative to project root
- Use `--list-configs` to see available files

### "Config must have 'game' section"
- Ensure your YAML has both `game:` and `snakes:` sections
- Check YAML syntax (indentation matters!)

### "Unknown controller type"
- Check spelling of `type:` field
- Valid types: human, random, algorithmic

### Snake immediately dies
- Check `start_position` isn't outside grid bounds
- Ensure positions are `[x, y]` format
- Multiple snakes shouldn't start at same position

## Examples

### Fast-paced 4-snake battle:
```yaml
game:
  width: 40
  height: 40
  cell_size: 15
  fps: 25
  background_color: [10, 10, 10]
  grid_color: [50, 50, 50]

snakes:
  - name: "Red"
    start_position: [5, 5]
    color: [255, 0, 0]
    controller: {type: "algorithmic", algorithm: "astar", heuristic: "manhattan"}
  
  - name: "Blue"
    start_position: [35, 5]
    color: [0, 0, 255]
    controller: {type: "algorithmic", algorithm: "dijkstra"}
  
  - name: "Green"
    start_position: [5, 35]
    color: [0, 255, 0]
    controller: {type: "algorithmic", algorithm: "bfs"}
  
  - name: "Yellow"
    start_position: [35, 35]
    color: [255, 255, 0]
    controller: {type: "random"}
```

### Educational slow-mo:
```yaml
game:
  width: 20
  height: 20
  cell_size: 25
  fps: 5                   # Very slow for observation
  background_color: [240, 240, 240]
  grid_color: [100, 100, 100]

snakes:
  - name: "Learning Snake"
    start_position: [10, 10]
    color: [50, 50, 255]
    controller:
      type: "algorithmic"
      algorithm: "astar"
      heuristic: "manhattan"
      max_steps: 200
```

For more details on how to add new controllers or algorithms, see the main project README.
