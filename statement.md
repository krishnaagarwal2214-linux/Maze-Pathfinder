# Problem Statement

Manually solving a maze, or brute-forcing a route through one, doesn't scale
and doesn't demonstrate *why* one algorithm might be preferable to another.
This project treats a maze as a graph — each cell is a node, and each open
passage between cells is an edge — so that classical graph-search
algorithms can be applied to it directly and their behavior compared on
identical ground. The generation side of the project (building a random,
guaranteed-solvable maze) and the solving side (finding a route through it)
are deliberately built as independent components, so the solver has no way
of "cheating" using knowledge of how the maze was constructed.

## Scope

**In scope:**
- Procedural generation of solvable, rectangular grid mazes using
  Randomized DFS (recursive backtracker)
- Graph-based shortest-path solving using BFS, with the codebase structured
  so DFS, Dijkstra, and A\* can be added as additional solver algorithms
  without changing the generation module
- Real-time animated visualization of both generation and solving

**Out of scope (for now):**
- Weighted terrain or variable movement cost between cells
- Diagonal movement
- 3D or non-rectangular mazes
- Multiplayer or networked features

## Target Users
- Students learning graph traversal algorithms (BFS, DFS, Dijkstra, A\*)
  who want to see the algorithms run rather than only read about them
- Anyone wanting an intuitive, visual comparison of how different
  pathfinding strategies behave on the exact same maze

## High-Level Features
- Procedural maze generation (Randomized DFS / recursive backtracker)
- Graph-based shortest-path solving (BFS implemented; more algorithms planned)
- Real-time animated visualization built with Pygame
- A modular codebase split into independently testable generation, solving,
  and visualization components, connected only through a clearly defined
  `Cell` data structure
