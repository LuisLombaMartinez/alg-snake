# alg-snake

**alg-snake** is an open-source, educational Python implementation of the classic Snake game, designed to help students learn about algorithms, AI, and game development.  
It features modular controllers, multiple pathfinding algorithms (A*, Dijkstra, BFS, and more), and a flexible configuration system.

## Features

- Play Snake with AI or human controllers
- Compare different pathfinding algorithms (A*, Dijkstra, BFS, and more)
- Easily add new algorithms or controllers
- Configurable game settings (speed, colors, grid size, etc.)
- Visualize algorithm steps and snake decisions
- Extensible for research and teaching

## Getting Started

### Prerequisites

- Python 3.8+
- [pygame](https://www.pygame.org/) (`pip install pygame`)

### Installation

Clone the repository:

```bash
git clone https://github.com/luislombamartinez/alg-snake.git
cd alg-snake
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Game

```bash
python main.py
```

You will be prompted to choose configuration options and controllers.

## Project Structure

```
alg-snake/
├── ai/                # Pathfinding algorithms (A*, Dijkstra, BFS, etc.)
├── config/            # Configuration and CLI configurator
├── controllers/       # AI and human controllers
├── game/              # Game logic, grid, snake, apple, etc.
├── main.py            # Entry point
└── README.md
```

## Contributing

Contributions are welcome!  
Feel free to submit pull requests, bug reports, or suggestions.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Inspired by classic Snake and modern AI research
- Special thanks to all contributors and students using this resource

---

**For educators and students:**  
Use this project to experiment with algorithms, visualize decision-making, and extend the game with your own ideas!
