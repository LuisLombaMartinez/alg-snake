# 🐍 alg-snake

> **An Interactive Educational Platform for Learning Python, Algorithms, and Software Design**

A well-architected Snake game implementation designed for computer science education. Perfect for students from introductory programming through advanced algorithms courses.

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎓 Educational Goals

This project serves as a **multi-level learning resource** suitable for:

### **Year 1-2: Python Fundamentals**
- Object-oriented programming (inheritance, abstract classes)
- Type hints and static typing
- Module organization and imports
- Data structures (lists, sets, dictionaries)
- Game loop patterns and event handling

### **Year 2-3: Algorithms & Data Structures**
- **Pathfinding algorithms**: A*, Dijkstra, BFS
- **Heuristic functions**: Manhattan, Euclidean distances
- **Algorithm complexity**: Time/space tradeoffs
- **Graph traversal**: Representing grids as graphs
- Priority queues and efficient data structures

### **Year 3-4: Software Engineering**
- **Design patterns**: Strategy, Factory, Abstract Factory
- **SOLID principles**: especially Open/Closed, Dependency Inversion
- **Separation of concerns**: MVC-like architecture
- **Configuration management**: YAML configs, CLI design
- **Testing**: Unit tests, integration tests, pytest fixtures

### **Advanced Topics**
- Performance optimization and profiling
- Real-time decision making under constraints
- Multi-agent systems and collision resolution
- Visualization of algorithm internals
- *(Future)* Reinforcement learning integration

---

## ✨ Features

### **Multiple Control Strategies**
- 🤖 **Algorithmic Controllers**: A*, Dijkstra, BFS with various heuristics
- 🎮 **Human Control**: Play with arrow keys
- 🎲 **Random Movement**: Baseline comparison
- 📼 **Replay System**: Record and replay games

### **Flexible Configuration**
- 📝 **YAML Configuration Files**: Quick testing and iteration
- 🖥️ **Interactive CLI**: Guided setup with auto-discovered presets
- 🎨 **Customizable**: Grid size, colors, speed, multiple snakes

### **Educational Features**
- 📊 Algorithm comparison in real-time
- 🏆 Multiplayer scenarios (snake vs snake)
- 📈 Performance metrics and statistics
- 🎯 Clean, documented, educational code

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.14+** ([Download](https://www.python.org/downloads/))
- pygame library

### Installation

```bash
# Clone the repository
git clone https://github.com/LuisLombaMartinez/alg-snake.git
cd alg-snake

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Your First Game

**Option 1: Interactive Menu**
```bash
python main.py
```
You'll see a menu with all available configurations. Just pick one!

**Option 2: Direct YAML Loading**
```bash
# See available configurations
python main.py --list-configs

# Run a specific configuration
python main.py --config configs/default.yaml
python main.py -c configs/human_vs_ai.yaml
```

---

## 📖 Learning Path

### **Beginner: Understanding the Basics**

1. **Start by playing**: `python main.py -c configs/human_vs_ai.yaml`
2. **Read the core game logic**: `game/snake.py`, `game/apple.py`, `game/grid.py`
3. **Understand the game loop**: `game/game.py`
4. **Explore the controller pattern**: `controllers/controller.py`

**Learning Objectives:**
- How object-oriented design structures a game
- Event-driven programming with pygame
- Basic collision detection logic

### **Intermediate: Algorithm Implementation**

1. **Study pathfinding basics**: `algorithms/algorithm.py` (abstract base class)
2. **Implement BFS**: Read `algorithms/bfs.py`
3. **Compare with Dijkstra**: Read `algorithms/dijkstra.py`
4. **Understand A***: Read `algorithms/a_star.py` and `algorithms/heuristics.py`
5. **Run comparisons**: `python main.py -c configs/algorithm_comparison.yaml`

**Learning Objectives:**
- Graph search algorithms on grids
- Heuristic functions and their impact
- Performance tradeoffs between algorithms
- When to use which algorithm

### **Advanced: Software Design**

1. **Analyze the architecture**:
   ```
   ├── algorithms/     # Strategy pattern for pathfinding
   ├── config/         # Configuration abstraction
   ├── controllers/    # Strategy pattern for snake behavior
   ├── game/           # Core game entities
   └── utils/          # Shared utilities
   ```

2. **Study design patterns**:
   - **Strategy Pattern**: `Controller` and `PathAlgorithm` hierarchies
   - **Factory Pattern**: Configuration builders
   - **Dependency Injection**: Controllers receive algorithm instances

3. **Explore configuration system**: `config/yaml_configurator.py`

**Learning Objectives:**
- How to structure medium-sized projects
- Dependency management and loose coupling
- Making code extensible and testable
- Configuration as code

### **Expert: Extensions & Projects**

**Suggested Projects:**

1. **Implement a new algorithm**: Greedy Best-First Search, Jump Point Search
2. **Create a new heuristic**: Octile distance, Chebyshev distance
3. **Add visualization**: Show explored nodes, open/closed sets
4. **Performance optimization**: Profile and optimize critical paths
5. **Add AI**: Implement reinforcement learning (DQN, PPO)
6. **Extend to 3D**: Adapt the architecture for 3D grid navigation

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
│                   (Entry Point & CLI)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ├─── Configurator (Abstract)
                         │    ├─── CLIConfigurator
                         │    └─── YAMLConfigurator
                         │
                         ▼
                    ┌─────────┐
                    │  Game   │
                    └────┬────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
     ┌───────┐      ┌────────┐     ┌────────┐
     │ Snake │      │ Apple  │     │  Grid  │
     └───┬───┘      └────────┘     └────────┘
         │
         │ uses
         ▼
    ┌────────────────┐
    │   Controller   │ (Abstract Strategy)
    └────────────────┘
         │
         ├─── AlgorithmicController ──uses──> PathAlgorithm
         │                                     ├─── AStar
         │                                     ├─── Dijkstra
         │                                     └─── BFS
         │
         ├─── HumanController
         ├─── RandomController
         └─── ReplayController
```

**Key Design Principles:**

- **Separation of Concerns**: Game logic, rendering, and AI are separate
- **Dependency Inversion**: Game depends on abstract `Controller`, not concrete implementations
- **Open/Closed**: Add new algorithms/controllers without modifying existing code
- **Single Responsibility**: Each class has one clear purpose

---

## 🎮 Example Configurations

### A* vs Dijkstra Comparison
```bash
python main.py -c configs/default.yaml
```
Watch two classic algorithms compete!

### Human vs AI
```bash
python main.py -c configs/human_vs_ai.yaml
```
Test your skills against an A* opponent. Arrow keys to move.

### Algorithm Showdown
```bash
python main.py -c configs/algorithm_comparison.yaml
```
Four algorithms, one arena: BFS, Dijkstra, A* (Manhattan), A* (Euclidean)

---

## 🔧 Creating Custom Configurations

YAML files let you create custom scenarios quickly. See `configs/README.md` for full documentation.

**Basic Template:**
```yaml
game:
  width: 50
  height: 50
  cell_size: 15
  fps: 20
  background_color: [0, 0, 0]
  grid_color: [255, 255, 255]

snakes:
  - name: "A* Snake"
    start_position: [10, 10]
    color: [0, 255, 0]
    controller:
      type: "algorithmic"
      algorithm: "astar"
      heuristic: "manhattan"
      max_steps: 1000
```

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/unit/test_algorithms.py -v
```

View coverage report: `open htmlcov/index.html`

---

## 🤝 Contributing

This project welcomes contributions, especially from students learning! Here's how you can help:

### **Good First Issues:**
- Add new heuristic functions
- Implement additional pathfinding algorithms
- Improve test coverage
- Add algorithm visualization
- Create more example configurations

### **Development Setup:**

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests before committing
pytest

# Format code (when we add it)
ruff format .

# Run linting (when we add it)
ruff check .
```

---

## 📚 Further Reading

### **Pathfinding Algorithms:**
- [Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html) - Red Blob Games (excellent visual guide)
- [A* Pathfinding for Beginners](http://www.policyalmanac.org/games/aStarTutorial.htm)
- [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

### **Python Design Patterns:**
- [Refactoring Guru - Strategy Pattern](https://refactoring.guru/design-patterns/strategy/python)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### **Game Development:**
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)

---

## 🗺️ Roadmap

### **In Progress:**
- [ ] Algorithm visualization (show explored nodes)
- [ ] Performance metrics dashboard
- [ ] Enhanced test coverage (target 80%)

### **Planned:**
- [ ] Reinforcement learning integration (DQN/PPO agents)
- [ ] Web-based visualizer (pyodide + canvas)
- [ ] Jupyter notebooks with interactive tutorials
- [ ] Step-by-step debugger mode
- [ ] Tournament mode (round-robin algorithm competition)

### **Future Ideas:**
- [ ] 3D version with modern graphics
- [ ] Online multiplayer
- [ ] Level editor with obstacles and power-ups
- [ ] Machine learning: train your own models

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Created as an educational resource for computer science students. Special thanks to the open-source community and the incredible [Red Blob Games](https://www.redblobgames.com/) tutorials that inspired this project's educational approach.

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/LuisLombaMartinez/alg-snake/issues)
- **Discussions**: [GitHub Discussions](https://github.com/LuisLombaMartinez/alg-snake/discussions)
- **Author**: Luis Lomba Martinez

---

**Happy coding, and may your snakes always find the shortest path! 🐍✨**
