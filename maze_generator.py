"""
MODULE 1: MAZE GENERATION
--------------------------------------------------------------------------
Builds a solvable maze from an empty grid using Randomized DFS
(the "recursive backtracker" algorithm).

INPUT  : grid dimensions (cols, rows)
OUTPUT : a fully connected, solvable maze -- a list of Cell objects whose
         `.walls` dictionaries record exactly which passages are open.

This module has NO pygame code and NO knowledge of how the maze will
later be solved. Its only job is producing the maze structure.
--------------------------------------------------------------------------
"""

from random import choice


class Cell:
    """
    One cell of the maze grid. This is the shared data object all three
    modules pass around -- but only THIS module's methods (check_neighbors,
    remove_walls) are allowed to decide which walls exist.

    Fields used by other modules (read/write, but logic lives elsewhere):
      solve_visited, parent   -- written by maze_solver.py
      on_path                 -- written by visualizer.py
    """

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {"top": True, "right": True, "left": True, "bottom": True}
        self.visited = False        # used only during generation
        self.solve_visited = False  # used only by the solver module
        self.parent = None          # used only by the solver module
        self.on_path = False        # used only by the visualizer

    def check_cell(self, x, y, grid_cells, cols, rows):
        """INPUT: a grid coordinate. OUTPUT: the Cell there, or False if off-grid."""
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells, cols, rows):
        """
        Generation-only neighbour check. Ignores walls completely (during
        generation, walls haven't been decided yet) and only cares about
        which neighbours haven't been carved into yet.
        OUTPUT: one random unvisited neighbour Cell, or False if none remain.
        """
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, grid_cells, cols, rows)
        right = self.check_cell(self.x + 1, self.y, grid_cells, cols, rows)
        bottom = self.check_cell(self.x, self.y + 1, grid_cells, cols, rows)
        left = self.check_cell(self.x - 1, self.y, grid_cells, cols, rows)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False

    @staticmethod
    def remove_walls(current, next):
        """Knocks down the shared wall between two adjacent cells."""
        dx = current.x - next.x
        if dx == 1:
            current.walls["left"] = False
            next.walls["right"] = False
        elif dx == -1:
            current.walls["right"] = False
            next.walls["left"] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls["top"] = False
            next.walls["bottom"] = False
        elif dy == -1:
            current.walls["bottom"] = False
            next.walls["top"] = False


def build_grid(cols, rows):
    """INPUT: grid size. OUTPUT: a fresh list of Cell objects, all walls up."""
    return [Cell(col, row) for row in range(rows) for col in range(cols)]


def generate_step(current_cell, stack, grid_cells, cols, rows):
    """
    Performs ONE step of maze generation. Meant to be called once per
    frame by the visualizer -- this is the module's public entry point.

    INPUT : current_cell (algorithm's current position), stack (backtracking history)
    OUTPUT: (new_current_cell, is_finished)
            is_finished is True once every reachable cell has been visited.
    """
    next_cell = current_cell.check_neighbors(grid_cells, cols, rows)
    if next_cell:
        stack.append(current_cell)
        next_cell.visited = True
        Cell.remove_walls(current_cell, next_cell)
        return next_cell, False
    elif stack:
        return stack.pop(), False
    else:
        return current_cell, True
