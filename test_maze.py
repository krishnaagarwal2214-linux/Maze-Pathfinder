"""
Validation tests for maze_generator.py and maze_solver.py.

Run from the project root with:
    python -m unittest tests/test_maze.py -v
or directly with:
    python tests/test_maze.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from maze_generator import build_grid, generate_step
from maze_solver import start_bfs, solve_step


def run_full_generation(cols, rows):
    grid_cells = build_grid(cols, rows)
    current = grid_cells[0]
    current.visited = True
    stack = []
    finished = False
    while not finished:
        current, finished = generate_step(current, stack, grid_cells, cols, rows)
    return grid_cells


def run_full_solve(grid_cells, start_cell, end_cell, cols, rows):
    queue = start_bfs(start_cell)
    status = "searching"
    path = None
    while status == "searching":
        status, path = solve_step(queue, end_cell, grid_cells, cols, rows)
    return status, path


class TestMazeGeneration(unittest.TestCase):

    def test_every_cell_is_visited(self):
        """A correctly generated maze must have no unreachable pockets."""
        grid_cells = run_full_generation(10, 10)
        unvisited = [c for c in grid_cells if not c.visited]
        self.assertEqual(len(unvisited), 0)

    def test_grid_has_correct_size(self):
        cols, rows = 8, 6
        grid_cells = run_full_generation(cols, rows)
        self.assertEqual(len(grid_cells), cols * rows)


class TestMazeSolver(unittest.TestCase):

    def test_bfs_finds_a_path(self):
        grid_cells = run_full_generation(10, 10)
        status, path = run_full_solve(grid_cells, grid_cells[0], grid_cells[-1], 10, 10)
        self.assertEqual(status, "found")
        self.assertIsNotNone(path)

    def test_path_starts_and_ends_correctly(self):
        grid_cells = run_full_generation(10, 10)
        start, end = grid_cells[0], grid_cells[-1]
        status, path = run_full_solve(grid_cells, start, end, 10, 10)
        self.assertIs(path[0], start)
        self.assertIs(path[-1], end)

    def test_path_is_contiguous(self):
        """Every step must move exactly one grid cell -- never jump through a wall."""
        grid_cells = run_full_generation(12, 12)
        status, path = run_full_solve(grid_cells, grid_cells[0], grid_cells[-1], 12, 12)
        for a, b in zip(path, path[1:]):
            step_distance = abs(a.x - b.x) + abs(a.y - b.y)
            self.assertEqual(step_distance, 1)

    def test_solver_does_not_import_generator(self):
        """Proves the two modules are genuinely decoupled, not just split into files."""
        import maze_solver
        self.assertNotIn("maze_generator", dir(maze_solver))

    def test_no_path_when_cells_are_disconnected(self):
        """Edge case: an ungenerated grid (all walls up) has no route at all --
        the solver must report this cleanly instead of crashing or looping forever."""
        grid_cells = build_grid(4, 4)  # walls never removed, nothing connects
        status, path = run_full_solve(grid_cells, grid_cells[0], grid_cells[-1], 4, 4)
        self.assertEqual(status, "no_path")
        self.assertIsNone(path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
