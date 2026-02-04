# alg-snake Development Plan

Quick reference for development phases. Work on these in order, in your free time.

---

## Phase 1: Python 3.14 + Modern Tooling ⏳ CURRENT

### Goals
- Update to Python 3.14
- Add modern development tools (linting, formatting, type checking)
- Professional development workflow

### Tasks
- [x] Add Pydantic for YAML validation ✅ **DONE**
- [x] Simplify Configurator interface (9+ methods → 1) ✅ **DONE**
- [x] Fix all type errors ✅ **DONE**
- [x] Update some type hints to use `| None` syntax ✅ **PARTIAL**
- [ ] Remove old `typing` imports (`Tuple`, `Optional`, `List`, `Dict`)
- [ ] Replace with built-in types (`tuple[int, int]`, `X | None`)
- [ ] Create `.python-version` file: `3.14`
- [ ] Update `requirements.txt` for Python 3.14 compatibility
- [ ] Create `pyproject.toml` with project metadata and tool configs
- [ ] Add `ruff` for linting and formatting
- [ ] Add `mypy` for strict type checking
- [ ] Add `.pre-commit-config.yaml` for automated checks
- [ ] Fix any remaining linting/type errors

### Estimated Time
**Original**: 2-4 hours  
**Remaining**: 1-2 hours

### Files to Update (~8-10 remaining)
Files still using old typing imports:
- `game/game.py`
- `game/snake.py`
- `controllers/controller.py`
- `controllers/algorithmic_controller.py`
- `algorithms/path_utils.py`
- `algorithms/bfs.py`
- `algorithms/dijkstra.py`
- `algorithms/a_star.py`

---

## Phase 2: Expand Test Coverage

### Goals
- Increase coverage from ~40% to 70%+
- Test untested components

### New Test Files Needed
```
tests/unit/
  - test_controllers.py       (algorithmic, human, random, replay)
  - test_configuration.py     (YAML loading, validation)
  - test_collision_detection.py

tests/integration/
  - test_full_game.py         (end-to-end scenarios)
  - test_algorithm_comparison.py
```

### Estimated Time
4-6 hours

---

## Phase 3: CI/CD

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

## Phase 4: Algorithm Visualization

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

## Phase 5: Learning Exercises

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

## Phase 6: Jupyter Notebooks (Optional)

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
Phase 1: Python 3.14 + Tooling     [~] 60% Complete
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
✅ **All type errors fixed** (14 issues resolved)  
✅ **Clean codebase** ready for modernization

**Next Steps**: 
1. Finish type hints modernization (remove old `typing` imports)
2. Add development tooling (ruff, mypy, pyproject.toml)
3. Then move to Phase 2 (Test Coverage)
