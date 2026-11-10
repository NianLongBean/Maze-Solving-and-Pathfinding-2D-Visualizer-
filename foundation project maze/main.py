
import pygame as pg

from grid import Grid
from mouse_handler import MouseHandler
from cell import Cell
from maze_gen import MazeGenerator
from assetsloader import AssetLoader

import bfs
from DFS import dfs
from dijkstra import dijkstra
from Astar import astar

from comparison_view import ComparisonView
from animation import AnimationController
from data_recorder import run_and_record
from path_position import get_path_coordinates
from ui import Button, Slider, Dropdown
from stats_manager import StatsManager


pg.init()


ROWS = 20
COLS = 30
CELL_SIZE = 25

MAZE_WIDTH = COLS * CELL_SIZE
MAZE_HEIGHT = ROWS * CELL_SIZE

STATS_WIDTH = 180
PANEL_HEIGHT = 150

SCREEN_WIDTH = MAZE_WIDTH + STATS_WIDTH
SCREEN_HEIGHT = MAZE_HEIGHT + PANEL_HEIGHT

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Maze Solving & Pathfinding Visualizer")

clock = pg.time.Clock()

font = pg.font.SysFont("Arial", 14, bold=True)
title_font = pg.font.SysFont("Arial", 16, bold=True)

asset_loader = AssetLoader(CELL_SIZE)

grid = Grid(ROWS, COLS)
mouse_handler = MouseHandler(grid, CELL_SIZE)
maze_gen = MazeGenerator(grid)

animation = AnimationController(grid)

runtime_ms = 0.0
visited_count = 0
path_length = 0
path_coords = []
stats_manager = StatsManager()
comparison_view = ComparisonView()


def test_stats_comparison(maze_id):
    results = stats_manager.compare_algorithms(maze_id)

    if not results:
        print("No statistics found for this maze.")
        return

    print(f"\nComparison for maze: {maze_id}")
    print("-" * 75)

    for result in results:
        print(
            f"Algorithm: {result['algorithm']} | "
            f"Runs: {result['total_runs']} | "
            f"Success: {result['success_rate']:.1f}% | "
            f"Runtime: {result['avg_runtime_ms']:.3f} ms | "
            f"Visited: {result['avg_visited_count']:.1f} | "
            f"Path: {result['avg_path_length']}"
        )


algo_dropdown = Dropdown(
    15,
    MAZE_HEIGHT + 15,
    180,
    32,
    ["Astar", "Dijkstra", "BFS", "DFS"]
)

speed_slider = Slider(
    15,
    MAZE_HEIGHT + 65,
    180,
    10,
    200,
    50,
    label="speed"
)

btn_wall = Button(
    225, MAZE_HEIGHT + 15, 75, 32, "Wall"
)

btn_start = Button(
    305, MAZE_HEIGHT + 15, 75, 32, "Start"
)

btn_target = Button(
    385, MAZE_HEIGHT + 15, 75, 32, "Target"
)

btn_maze = Button(
    225, MAZE_HEIGHT + 60, 235, 32, "Generate Maze"
)

btn_wall.selected = True

btn_run = Button(
    MAZE_WIDTH + 15,
    MAZE_HEIGHT + 15,
    150,
    35,
    "Run",
    bg_color=(120, 220, 120)
)

btn_clear = Button(
    MAZE_WIDTH + 15,
    MAZE_HEIGHT + 60,
    150,
    35,
    "Clear",
    bg_color=(240, 130, 130)
)
btn_compare = Button(
    MAZE_WIDTH + 15,
    MAZE_HEIGHT + 100,
    150,
    35,
    "Compare",
)


def execute_selected_algorithm():
    global runtime_ms
    global visited_count
    global path_length
    global path_coords

    start, target = mouse_handler.find_start_target()

    if start is None or target is None:
        return

    maze_id = stats_manager.generate_maze_id(
        grid, start, target
    )

    selected = algo_dropdown.get_selected()

    animation.clear()

    if selected == "BFS":
        visited_order, found_path, stats = run_and_record(
            "BFS",
            lambda: bfs.bfs(grid),
            start=start,
            target=target
        )

    elif selected == "DFS":
        visited_order, found_path, stats = run_and_record(
            "DFS",
            dfs,
            grid,
            start,
            target,
            start=start,
            target=target
        )

    elif selected == "Dijkstra":
        visited_order, found_path, stats = run_and_record(
            "Dijkstra",
            dijkstra,
            grid,
            start,
            target,
            start=start,
            target=target
        )

    elif selected == "Astar":
        visited_order, found_path, stats = run_and_record(
            "A*",
            astar,
            grid,
            start,
            target,
            start=start,
            target=target
        )

    else:
        return

    runtime_ms = stats["runtime_ms"]
    visited_count = stats["visited_count"]
    path_length = stats["path_length"]
    path_coords = get_path_coordinates(found_path)

    stats_manager.record(stats, maze_id=maze_id)

    test_stats_comparison(maze_id)

    animation.delay = speed_slider.val
    animation.start(visited_order, found_path)


def draw_grid():
    for row in range(grid.rows):
        for col in range(grid.cols):
            cell = grid.get_cell(row, col)

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            drawn_by_asset = asset_loader.draw_cell(
                screen, cell, x, y
            )

            if not drawn_by_asset:
                if cell.state == Cell.EMPTY:
                    color = (245, 245, 245)

                elif cell.state == Cell.WALL:
                    color = (40, 40, 40)

                elif cell.state == Cell.START:
                    color = (0, 200, 0)

                elif cell.state == Cell.TARGET:
                    color = (220, 0, 0)

                elif cell.state == Cell.VISITED:
                    color = (175, 215, 245)

                elif cell.state == Cell.PATH:
                    color = (255, 215, 0)

                else:
                    color = (200, 200, 200)

                pg.draw.rect(
                    screen,
                    color,
                    (x, y, CELL_SIZE, CELL_SIZE)
                )


def draw_ui_panels():
    stats_rect = pg.Rect(
        MAZE_WIDTH, 0, STATS_WIDTH, MAZE_HEIGHT
    )

    pg.draw.rect(screen, (255, 255, 255), stats_rect)
    pg.draw.rect(screen, (0, 0, 0), stats_rect, 2)

    txt_stats = title_font.render(
        "Stats", True, (0, 0, 0)
    )

    txt_runtime = font.render(
        f"runtime: {runtime_ms:.3f} ms",
        True,
        (0, 0, 0)
    )

    txt_visited = font.render(
        f"visited: {visited_count}",
        True,
        (0, 0, 0)
    )

    txt_length = font.render(
        f"path_length: {path_length}",
        True,
        (0, 0, 0)
    )

    screen.blit(txt_stats, (MAZE_WIDTH + 15, 15))
    screen.blit(txt_runtime, (MAZE_WIDTH + 15, 50))
    screen.blit(txt_visited, (MAZE_WIDTH + 15, 80))
    screen.blit(txt_length, (MAZE_WIDTH + 15, 110))

    maze_border = pg.Rect(
        0, 0, MAZE_WIDTH, MAZE_HEIGHT
    )
    pg.draw.rect(screen, (0, 0, 0), maze_border, 2)

    bottom_rect = pg.Rect(
        0, MAZE_HEIGHT, SCREEN_WIDTH, PANEL_HEIGHT
    )

    pg.draw.rect(screen, (245, 245, 245), bottom_rect)
    pg.draw.rect(screen, (0, 0, 0), bottom_rect, 2)

    pg.draw.line(
        screen,
        (0, 0, 0),
        (210, MAZE_HEIGHT),
        (210, SCREEN_HEIGHT),
        2
    )

    pg.draw.line(
        screen,
        (0, 0, 0),
        (MAZE_WIDTH, MAZE_HEIGHT),
        (MAZE_WIDTH, SCREEN_HEIGHT),
        2
    )

    speed_slider.draw(screen, font)

    btn_wall.draw(screen, font)
    btn_start.draw(screen, font)
    btn_target.draw(screen, font)
    btn_maze.draw(screen, font)

    btn_run.draw(screen, font)
    btn_clear.draw(screen, font)

    algo_dropdown.draw(screen, font)
    btn_compare.draw(screen, font)


def clear_visualization():
    global runtime_ms
    global visited_count
    global path_length
    global path_coords

    animation.clear()

    runtime_ms = 0.0
    visited_count = 0
    path_length = 0
    path_coords = []


running = True

while running:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False
            continue
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            comparison_view.visible = False
        speed_slider.handle_event(event)

        if algo_dropdown.handle_event(event):
            continue

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if mx < MAZE_WIDTH and my < MAZE_HEIGHT:
                mouse_handler.mouse_pressed = True

                mouse_handler.handle_click(
                    mx,
                    my,
                    is_initial_press=True
                )

            elif btn_wall.is_clicked((mx, my)):
                mouse_handler.set_mode("wall")

                btn_wall.selected = True
                btn_start.selected = False
                btn_target.selected = False

            elif btn_start.is_clicked((mx, my)):
                mouse_handler.set_mode("start")

                btn_wall.selected = False
                btn_start.selected = True
                btn_target.selected = False

            elif btn_target.is_clicked((mx, my)):
                mouse_handler.set_mode("target")

                btn_wall.selected = False
                btn_start.selected = False
                btn_target.selected = True

            elif btn_maze.is_clicked((mx, my)):
                clear_visualization()
                maze_gen.generate_maze()

            elif btn_run.is_clicked((mx, my)):
                execute_selected_algorithm()

            elif btn_clear.is_clicked((mx, my)):
                clear_visualization()
            elif btn_compare.is_clicked((mx, my)):
                comparison_view.visible = True

        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            mouse_handler.mouse_pressed = False

    if mouse_handler.mouse_pressed:
        mx, my = pg.mouse.get_pos()

        if mx < MAZE_WIDTH and my < MAZE_HEIGHT:
            mouse_handler.handle_click(mx, my)

    animation.delay = speed_slider.val

    animation.update()

    screen.fill((255, 255, 255))

    draw_grid()
    draw_ui_panels()
    if stats_manager.history:
        latest_maze_id = stats_manager.history[-1]["maze_id"]
        results = stats_manager.compare_algorithms(latest_maze_id)
    else:
        results = []

    comparison_view.draw(screen, results)

    pg.display.update()
    clock.tick(60)

pg.quit()
