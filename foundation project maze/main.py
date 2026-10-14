
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

from animation import AnimationController
from data_recorder import run_and_record
from path_position import get_path_coordinates
from ui import Button, Slider, Dropdown


# ==================================================
# 1. INITIALIZE PYGAME
# ==================================================

pg.init()


# ==================================================
# 2. SETTINGS
# ==================================================

ROWS = 20
COLS = 30
CELL_SIZE = 25

MAZE_WIDTH = COLS * CELL_SIZE
MAZE_HEIGHT = ROWS * CELL_SIZE

STATS_WIDTH = 180
PANEL_HEIGHT = 110

SCREEN_WIDTH = MAZE_WIDTH + STATS_WIDTH
SCREEN_HEIGHT = MAZE_HEIGHT + PANEL_HEIGHT

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Maze Solving & Pathfinding Visualizer")

clock = pg.time.Clock()

font = pg.font.SysFont("Arial", 14, bold=True)
title_font = pg.font.SysFont("Arial", 16, bold=True)


# ==================================================
# 3. CREATE OBJECTS
# ==================================================

asset_loader = AssetLoader(CELL_SIZE)

grid = Grid(ROWS, COLS)
mouse_handler = MouseHandler(grid, CELL_SIZE)
maze_gen = MazeGenerator(grid)

animation = AnimationController(grid)


# ==================================================
# 4. STATISTICS
# ==================================================

runtime_ms = 0.0
visited_count = 0
path_length = 0
path_coords = []


# ==================================================
# 5. CREATE UI COMPONENTS
# ==================================================

# Algorithm dropdown and speed slider
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

# Cell editing buttons
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

# Run and Clear buttons
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


# ==================================================
# 6. RUN SELECTED ALGORITHM
# ==================================================

def execute_selected_algorithm():
    global runtime_ms
    global visited_count
    global path_length
    global path_coords

    start, target = mouse_handler.find_start_target()

    # Start and target must both exist
    if start is None or target is None:
        return

    selected = algo_dropdown.get_selected()

    # Clear the previous animation before a new run
    animation.clear()

    # Run the selected algorithm and record statistics
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

    # Update statistics
    runtime_ms = stats["runtime_ms"]
    visited_count = stats["visited_count"]
    path_length = stats["path_length"]
    path_coords = get_path_coordinates(found_path)

    # Start the animation using the separate controller
    animation.delay = speed_slider.val
    animation.start(visited_order, found_path)


# ==================================================
# 7. DRAW THE MAZE
# ==================================================

def draw_grid():
    for row in range(grid.rows):
        for col in range(grid.cols):
            cell = grid.get_cell(row, col)

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            # Try drawing with the project's asset loader
            drawn_by_asset = asset_loader.draw_cell(
                screen, cell, x, y
            )

            # Fallback colors if no asset was drawn
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

            # Draw the cell border
            # pg.draw.rect(
            #     screen,
            #     (210, 210, 210),
            #     (x, y, CELL_SIZE, CELL_SIZE),
            #     1
            # )


# ==================================================
# 8. DRAW UI PANELS
# ==================================================

def draw_ui_panels():
    # Statistics panel on the right
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

    # Border around the maze
    maze_border = pg.Rect(
        0, 0, MAZE_WIDTH, MAZE_HEIGHT
    )
    pg.draw.rect(screen, (0, 0, 0), maze_border, 2)

    # Bottom control panel
    bottom_rect = pg.Rect(
        0, MAZE_HEIGHT, SCREEN_WIDTH, PANEL_HEIGHT
    )

    pg.draw.rect(screen, (245, 245, 245), bottom_rect)
    pg.draw.rect(screen, (0, 0, 0), bottom_rect, 2)

    # Separators between control areas
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

    # Draw controls
    speed_slider.draw(screen, font)

    btn_wall.draw(screen, font)
    btn_start.draw(screen, font)
    btn_target.draw(screen, font)
    btn_maze.draw(screen, font)

    btn_run.draw(screen, font)
    btn_clear.draw(screen, font)

    # Draw the dropdown last so its menu stays visible
    algo_dropdown.draw(screen, font)


# ==================================================
# 9. CLEAR VISUALIZATION AND STATISTICS
# ==================================================

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


# ==================================================
# 10. MAIN LOOP
# ==================================================

running = True

while running:

    for event in pg.event.get():

        # Close the window
        if event.type == pg.QUIT:
            running = False
            continue

        # Let the slider handle its own events
        speed_slider.handle_event(event)

        # Let the dropdown handle its own events
        if algo_dropdown.handle_event(event):
            continue

        # Mouse pressed
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # Click on the maze
            if mx < MAZE_WIDTH and my < MAZE_HEIGHT:
                mouse_handler.mouse_pressed = True

                mouse_handler.handle_click(
                    mx,
                    my,
                    is_initial_press=True
                )

            # Select Wall mode
            elif btn_wall.is_clicked((mx, my)):
                mouse_handler.set_mode("wall")

                btn_wall.selected = True
                btn_start.selected = False
                btn_target.selected = False

            # Select Start mode
            elif btn_start.is_clicked((mx, my)):
                mouse_handler.set_mode("start")

                btn_wall.selected = False
                btn_start.selected = True
                btn_target.selected = False

            # Select Target mode
            elif btn_target.is_clicked((mx, my)):
                mouse_handler.set_mode("target")

                btn_wall.selected = False
                btn_start.selected = False
                btn_target.selected = True

            # Generate a maze
            elif btn_maze.is_clicked((mx, my)):
                clear_visualization()
                maze_gen.generate_maze()

            # Run selected algorithm
            elif btn_run.is_clicked((mx, my)):
                execute_selected_algorithm()

            # Clear the visualization
            elif btn_clear.is_clicked((mx, my)):
                clear_visualization()

        # Mouse released
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            mouse_handler.mouse_pressed = False

    # Handle mouse dragging to place walls
    if mouse_handler.mouse_pressed:
        mx, my = pg.mouse.get_pos()

        if mx < MAZE_WIDTH and my < MAZE_HEIGHT:
            mouse_handler.handle_click(mx, my)

    # Synchronize animation speed with the slider
    animation.delay = speed_slider.val

    # Update animation
    animation.update()

    # Render the screen
    screen.fill((255, 255, 255))

    draw_grid()
    draw_ui_panels()

    pg.display.update()
    clock.tick(60)


# ==================================================
# 11. SHUTDOWN
# ==================================================

pg.quit()
