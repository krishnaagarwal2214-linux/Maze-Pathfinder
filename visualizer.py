"""
MODULE 3: VISUALIZATION
--------------------------------------------------------------------------
Draws the maze, animates generation and solving, and highlights the
final path. This is the ONLY module that imports pygame.

INPUT  : live state from Module 1 (the maze) and Module 2 (the solver)
OUTPUT : the rendered window, redrawn every frame

Run this file to start the program: python visualizer.py
--------------------------------------------------------------------------
"""

import pygame
from maze_generator import build_grid, generate_step
from maze_solver import start_bfs, solve_step

WIDTH, HEIGHT = 800, 800
TILE = 50
COLS, ROWS = WIDTH // TILE, HEIGHT // TILE
FPS = 30


def draw_cell(sc, cell):
    x, y = cell.x * TILE, cell.y * TILE
    if cell.visited:
        pygame.draw.rect(sc, pygame.Color("#f4efef"), (x, y, TILE, TILE))
    if cell.solve_visited:
        pygame.draw.rect(sc, pygame.Color("#4C6EF5"), (x + TILE // 4, y + TILE // 4, TILE // 2, TILE // 2))
    if cell.on_path:
        pygame.draw.rect(sc, pygame.Color("#FFD43B"), (x + 1, y + 1, TILE - 2, TILE - 2))
    if cell.walls["top"]:
        pygame.draw.line(sc, (0, 0, 255), (x, y), (x + TILE, y), 3)
    if cell.walls["right"]:
        pygame.draw.line(sc, (0, 0, 255), (x + TILE, y), (x + TILE, y + TILE), 3)
    if cell.walls["bottom"]:
        pygame.draw.line(sc, (0, 0, 255), (x + TILE, y + TILE), (x, y + TILE), 3)
    if cell.walls["left"]:
        pygame.draw.line(sc, (0, 0, 255), (x, y + TILE), (x, y), 3)


def draw_current_cell(sc, cell):
    x, y = cell.x * TILE, cell.y * TILE
    pygame.draw.rect(sc, pygame.Color("#f70067"), (x + 2, y + 2, TILE - 2, TILE - 2), border_radius=20)


def main():
    pygame.init()
    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DFS Maze Generator + BFS Solver")
    clock = pygame.time.Clock()

    # ---- ask Module 1 for an empty grid ----
    grid_cells = build_grid(COLS, ROWS)
    current_cell = grid_cells[0]
    current_cell.visited = True
    stack = []

    state = "generating"
    start_cell = grid_cells[0]
    end_cell = grid_cells[-1]
    queue = None
    path, path_index = [], 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        sc.fill(pygame.Color("#0606ED"))
        for cell in grid_cells:
            draw_cell(sc, cell)

        if state == "generating":
            draw_current_cell(sc, current_cell)
            current_cell, finished = generate_step(current_cell, stack, grid_cells, COLS, ROWS)
            if finished:
                state = "solving"
                queue = start_bfs(start_cell)          # ---- hand off to Module 2 ----

        elif state == "solving":
            status, result = solve_step(queue, end_cell, grid_cells, COLS, ROWS)
            if status == "found":
                path = result
                state = "revealing_path"
            elif status == "no_path":
                state = "done"

        elif state == "revealing_path":
            if path_index < len(path):
                path[path_index].on_path = True
                path_index += 1
            else:
                state = "done"

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
