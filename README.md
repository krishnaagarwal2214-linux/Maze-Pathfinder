# Maze Generator & Pathfinder — A DSA Visualization Project

## Overview
A Python + Pygame application that procedurally generates a maze using
**Randomized Depth-First Search** (the recursive backtracker algorithm) and
then finds the shortest path between the start and end cells using
**Breadth-First Search (BFS)**. Both processes are animated in real time.
The project treats a maze as a graph — cells are nodes, open passages are
edges — so classic graph algorithms apply directly.

## Features

**Implemented:**
- Randomized DFS maze generation, animated cell-by-cell
- BFS pathfinding on the completed maze, animated cell-by-cell
- Final shortest path highlighted clearly once found
- Clean 3-module architecture: generation, solving, and visualization are
  fully decoupled — the solver has zero dependency on how the maze was built

**Planned (see `statement.md` and the project report for full scope):**
- Additional solvers: DFS, Dijkstra, A\*
- Interactive start/end cell selection and algorithm switching
- Side-by-side analytics comparing algorithms (nodes explored, path length, time taken)

## Technologies Used
- Python 3.x
- Pygame

## Project Structure
```
maze-pathfinder-dsa/
├── README.md
├── statement.md
├── requirements.txt
├── .gitignore
├── maze_generator.py      # Module 1: builds the maze
├── maze_solver.py         # Module 2: solves the maze (BFS)
├── visualizer.py          # Module 3: Pygame rendering + entry point
├── tests/
│   └── test_maze.py       # unit tests for generation and solving
└── docs/
    ├── architecture_diagram.png
    ├── class_diagram.png
    ├── sequence_diagram.png
    └── use_case_diagram.png
```

## Installation & Setup
1. Clone this repository:
   ```
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```
2. (Optional but recommended) create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate        (Windows)
   source venv/bin/activate     (Mac/Linux)
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## How to Run
```
python visualizer.py
```
A window opens and automatically:
1. Builds an empty grid
2. Generates a maze using randomized DFS (animated)
3. Once generation finishes, solves it using BFS (animated in blue)
4. Reveals the final shortest path in yellow

Press the window's close button or `Esc`/close the window to quit.

## Testing
Run the full unit test suite (7 tests covering generation, solving, path
validity, module independence, and a no-path edge case):
```
python -m unittest tests/test_maze.py -v
```

`maze_solver.py` also includes its own standalone self-test that proves the
solver works correctly with **no Pygame window at all**, on a maze it never
generated:
```
python maze_solver.py
```
Expected output: `Self-test passed: BFS solved a maze it never generated.`

## Design Diagrams
See `docs/` for the full set: architecture diagram, class diagram, sequence
diagram, and use case diagram (the last two mark which features are
implemented vs. still planned). See the project report for maze
generation / solving screenshots.

## Author
[Your Name] — [Registration Number] — [Course Name]
