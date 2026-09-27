"""
MODULE 2: PATHFINDING SOLVER
--------------------------------------------------------------------------
Runs Breadth-First Search (BFS) on an ALREADY-BUILT maze to find the
shortest path from a start cell to an end cell.

INPUT  : the finished maze (list of Cell objects with walls already fixed),
         a start cell, an end cell
OUTPUT : the shortest path between them, as an ordered list of Cell objects

This module never imports maze_generator or pygame. It only reads a
cell's `.walls` and writes `.solve_visited` / `.parent` -- that's the
entire contract between this module and the rest of the program. Because
of that, it can be tested completely on its own (see the bottom of this
file for a tiny self-test), and swapping in Dijkstra or A* later only
means adding a new file with the same shape as this one.
--------------------------------------------------------------------------
"""

from collections import deque


def _check_cell(x, y, grid_cells, cols, rows):
    if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
        return False
    return grid_cells[x + y * cols]


def find_solve_neighbors(cell, grid_cells, cols, rows):
    """
    Solver-only neighbour check: returns every neighbour that is BOTH
    reachable (no wall in the way) and not yet explored by the solver.
    This is what makes the solver independent of how the maze was built --
    it trusts only the walls that are actually there right now.
    """
    neighbors = []
    top = _check_cell(cell.x, cell.y - 1, grid_cells, cols, rows)
    right = _check_cell(cell.x + 1, cell.y, grid_cells, cols, rows)
    bottom = _check_cell(cell.x, cell.y + 1, grid_cells, cols, rows)
    left = _check_cell(cell.x - 1, cell.y, grid_cells, cols, rows)
    if top and not cell.walls["top"] and not top.solve_visited:
        neighbors.append(top)
    if right and not cell.walls["right"] and not right.solve_visited:
        neighbors.append(right)
    if bottom and not cell.walls["bottom"] and not bottom.solve_visited:
        neighbors.append(bottom)
    if left and not cell.walls["left"] and not left.solve_visited:
        neighbors.append(left)
    return neighbors


def start_bfs(start_cell):
    """INPUT: the chosen start cell. OUTPUT: a ready-to-run BFS queue."""
    start_cell.solve_visited = True
    queue = deque()
    queue.append(start_cell)
    return queue


def solve_step(queue, end_cell, grid_cells, cols, rows):
    """
    Performs ONE step of BFS. Meant to be called once per frame by the
    visualizer -- this is the module's public entry point.

    INPUT : the live BFS queue, the end cell, the grid
    OUTPUT: (status, path)
        status == "searching" -> path is None,       keep calling this
        status == "found"     -> path is the route,  ordered start -> end
        status == "no_path"   -> path is None,        maze has no solution
    """
    if not queue:
        return "no_path", None

    current = queue.popleft()
    if current is end_cell:
        path = []
        node = end_cell
        while node is not None:
            path.append(node)
            node = node.parent
        path.reverse()
        return "found", path

    for neighbor in find_solve_neighbors(current, grid_cells, cols, rows):
        neighbor.solve_visited = True
        neighbor.parent = current
        queue.append(neighbor)

    return "searching", None


# --------------------------------------------------------------------------
# Self-test: proves this module works with ZERO pygame and ZERO knowledge
# of how the maze was generated. Run directly with: python maze_solver.py
# --------------------------------------------------------------------------
if __name__ == "__main__":
    from maze_generator import build_grid, generate_step

    cols, rows = 10, 10
    grid_cells = build_grid(cols, rows)
    current, stack, finished = grid_cells[0], [], False
    grid_cells[0].visited = True
    while not finished:
        current, finished = generate_step(current, stack, grid_cells, cols, rows)

    start_cell, end_cell = grid_cells[0], grid_cells[-1]
    queue = start_bfs(start_cell)
    status, path = "searching", None
    while status == "searching":
        status, path = solve_step(queue, end_cell, grid_cells, cols, rows)

    print("Solve status:", status)
    print("Path length:", len(path) if path else 0)
    assert status == "found"
    assert path[0] is start_cell and path[-1] is end_cell
    print("Self-test passed: BFS solved a maze it never generated.")
