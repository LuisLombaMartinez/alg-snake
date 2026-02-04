# alg-snake Development Plan

Quick reference for development phases. Work on these in order, in your free time.

---

## Phase 1: Python 3.13 + Modern Tooling ✅ COMPLETE

### Goals
- Update to Python 3.13 (latest LTS)
- Add modern development tools (linting, formatting, type checking)
- Professional development workflow

### Completed Tasks
- [x] Add Pydantic for YAML validation ✅
- [x] Simplify Configurator interface (9+ methods → 1) ✅
- [x] Fix all type errors ✅
- [x] Update all type hints to use modern syntax (`| None`, `list[]`, `dict[]`, `tuple[]`) ✅
- [x] Create `.python-version` file: `3.13` ✅
- [x] Remove old `typing` imports (`Tuple`, `Optional`, `List`, `Dict`) ✅
- [x] Update `requirements.txt` for Python 3.13 ✅
- [x] Create `pyproject.toml` with project metadata and tool configs ✅
- [x] Add `ruff` for linting and formatting (replaces flake8 + black) ✅
- [x] Add `mypy` for strict type checking ✅
- [x] Consolidate dependencies in `pyproject.toml` ✅
- [x] Version consistency across all files (3.13+) ✅

### How to Use Modern Tooling

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run linter and auto-fix issues
ruff check --fix .

# Format code
ruff format .

# Type checking
mypy .

# Run all checks together
ruff check . && ruff format --check . && mypy .
```

### Notes
- Project targets Python 3.13+ (latest LTS for future-proofing)
- Code remains compatible with Python 3.12+
- `requirements.txt` and `requirements-dev.txt` kept for backward compatibility
- `ruff` replaces both `flake8` and `black` (faster, more modern, all-in-one)
- All modern Python 3.10+ syntax features are used throughout

---

## Phase 2: Expand Test Coverage ⏳ CURRENT

### Goals
- Increase coverage from ~0% to 70%+
- Test all major components
- Discover bugs through testing

### New Test Files Needed
```
tests/unit/
  - test_algorithms.py        (A*, Dijkstra, BFS correctness)
  - test_heuristics.py        (Manhattan, Euclidean distances)
  - test_controllers.py       (algorithmic, human, random, replay)
  - test_configuration.py     (YAML loading, validation)
  - test_snake.py             (movement, collision basics)
  - test_grid.py              (bounds checking, cell tracking)

tests/integration/
  - test_full_game.py         (end-to-end scenarios)
  - test_algorithm_comparison.py
  - test_collision_scenarios.py  (comprehensive collision testing)
```

### Key Testing Areas
1. **Algorithm Correctness**
   - Do algorithms find valid paths?
   - Do they handle blocked cells correctly?
   - Edge cases: no path available, surrounded snake

2. **Configuration Validation**
   - Valid YAML loads correctly
   - Invalid YAML raises proper errors
   - Pydantic catches bad values

3. **Game Logic**
   - Apple spawning
   - Score tracking
   - Game over conditions

4. **Collision Detection** (will expose bugs to fix in Phase 3)
   - Wall collisions
   - Self-collisions
   - Snake-to-snake collisions
   - Head-to-head collisions

### Estimated Time
6-8 hours (testing often reveals bugs that need investigation)

---

## Phase 3: Bug Fixes from Testing 🐛 NEW

### Goals
- Fix issues discovered during test writing
- Ensure collision detection works correctly
- Address any other bugs found

### Known Issues
1. **Collision Detection Timing** ⚠️
   - Current: Collisions checked AFTER all snakes move
   - Problem: One-frame delay in collision detection
   - Impact: Head-to-head collisions may not work correctly
   - Solution: Check collisions using `next_positions` BEFORE moving

2. **To Be Discovered**
   - Additional issues will be added as tests reveal them
   - May include edge cases in algorithms
   - Configuration edge cases
   - Game state management issues

### Implementation Notes
```python
# Current (buggy) approach in game.py:
# 1. Get all next moves -> next_positions
# 2. Move all snakes
# 3. Check collisions  # ❌ Too late!

# Better approach:
# 1. Get all next moves -> next_positions
# 2. Check collisions using next_positions  # ✅ Before moving
# 3. Mark dead snakes
# 4. Move surviving snakes
```

### Estimated Time
3-4 hours (depends on number of bugs found)

---

## Phase 4: CI/CD

### Goals
- Automate testing on every push
- Catch issues early

### Tasks
1. Create `.github/workflows/test.yml`
2. Run tests on push/PR
3. Run linting (ruff)
4. Run type checking (mypy)
5. Generate coverage report
6. Add status badges to README

### Estimated Time
1-2 hours

---

## Phase 5: Algorithm Visualization

### Goals
- Show how algorithms explore the grid
- Educational value for students

### Features
- Color-coded cells: explored, frontier, final path
- Metrics overlay: nodes explored, path length, time
- Step-by-step mode (press space to advance)
- `--visualize` CLI flag

### New Files
```
algorithms/
  - visualization.py         (AlgorithmVisualizer class)

# Modify algorithms to track exploration
```

### Estimated Time
6-8 hours

---

## Phase 6: Learning Exercises

### Goals
- Structured challenges for different levels
- Reference solutions included

### Directory Structure
```
exercises/
  - README.md                    (overview and instructions)
  - level_1_beginner/
      - 01_add_new_heuristic.py  (implement Chebyshev distance)
      - 02_modify_colors.py
      - 03_grid_obstacles.py
  - level_2_intermediate/
      - 01_greedy_bfs.py         (implement Greedy Best-First)
      - 02_custom_controller.py
      - 03_optimize_astar.py
  - level_3_advanced/
      - 01_jump_point_search.py
      - 02_multiplayer_ai.py     (considers other snakes)
      - 03_performance_tuning.py
  - solutions/                   (reference implementations)
```

### Estimated Time
8-10 hours

---

## Phase 7: Jupyter Notebooks (Optional)

### Goals
- Interactive tutorials
- Code + explanation + visualization in one place

### Notebooks to Create
```
notebooks/
  - 01_introduction.ipynb
  - 02_bfs_explained.ipynb
  - 03_dijkstra.ipynb
  - 04_astar_heuristics.ipynb
  - 05_algorithm_comparison.ipynb
  - 06_custom_algorithm.ipynb    (exercise)
  - 07_software_design.ipynb
```

### Estimated Time
10-12 hours

---

## Phase 7: Advanced Features (For Final Year Students)

### Option A: Multi-Agent Cooperation (Recommended)
Snakes that cooperate to maximize total score
- Communication between snakes
- Shared knowledge about apple locations
- Conflict resolution
- **Time**: 8-10 hours
- **Difficulty**: Advanced but achievable
- **Educational Value**: High (distributed systems, game theory)

### Option B: Performance Optimization Challenge
Maximize performance of existing algorithms
- Profiling tools integration
- Memory optimization
- Algorithm parameter tuning
- **Time**: 6-8 hours
- **Difficulty**: Medium
- **Educational Value**: Very high (practical optimization)

### Option C: Algorithm Hybridization
Dynamically switch between algorithms based on game state
- A* when far from apple, greedy when close
- Learn when to use which algorithm
- **Time**: 8-10 hours
- **Difficulty**: Advanced
- **Educational Value**: High (adaptive systems)

### Option D: Reinforcement Learning (If Time Permits)
Real ML with Stable-Baselines3
- DQN or PPO agent
- Training script
- Comparison with hand-coded algorithms
- **Time**: 20+ hours
- **Difficulty**: Very advanced
- **Educational Value**: Very high but time-intensive

**Recommendation**: Start with Option A or B, add others if time permits.

---

## Phase 8: University Submission Prep

### Tasks
1. Review all documentation
2. Add screenshots/GIFs to README
3. Create architecture diagrams
4. Generate PDF from README
5. Prepare submission package
6. Test on clean machine

### Estimated Time
4-6 hours

---

## Quick Progress Tracking

```
Phase 1: Python 3.13 + Tooling     [~] 60% Complete
  ✅ Pydantic schema validation
  ✅ Configurator interface simplified  
  ✅ Type errors fixed
  ⏳ Type hints modernization (partial)
  ⏳ Tooling setup (ruff, mypy, pyproject.toml)
  
Phase 2: Test Coverage             [ ] Not Started
Phase 3: CI/CD                     [ ] Not Started
Phase 4: Visualization             [ ] Not Started
Phase 5: Exercises                 [ ] Not Started
Phase 6: Notebooks (Optional)      [ ] Not Started
Phase 7: Advanced Features         [ ] Not Started
Phase 8: Submission Prep           [ ] Not Started
```

Mark with `[x]` as you complete each phase, `[~]` for in-progress.

---

## Total Timeline Estimate

**Core Features** (Phases 1-5): 20-30 hours
**Optional Features** (Phases 6-7): +20-30 hours
**University Ready**: 4-6 weeks working in free time

---

## Current Status

✅ **Genetic algorithm removed**  
✅ **Documentation consolidated to 3 files** (README, QUICKSTART, PROJECT_PLAN)  
✅ **Pydantic validation** implemented for YAML configs  
✅ **Configurator interface simplified** (9+ methods → 1 abstract method)  
✅ **All type errors fixed**
✅ **Clean codebase** ready for modernization

**Next Steps**: 
1. Finish type hints modernization (remove old `typing` imports)
2. Add development tooling (ruff, mypy, pyproject.toml)
3. Then move to Phase 2 (Test Coverage)
