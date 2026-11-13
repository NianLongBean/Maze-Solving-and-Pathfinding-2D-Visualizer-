
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
from stats_manager import StatsManager
from dataset_exporter import export_comparison_dataset


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
PANEL_HEIGHT = 230
MAP_PRESETS = {"20x20": (20, 20), "20x30": (20, 30), "50x50": (50, 50)}

SCREEN_WIDTH = MAZE_WIDTH + STATS_WIDTH
SCREEN_HEIGHT = MAZE_HEIGHT + PANEL_HEIGHT

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Maze Solving & Pathfinding Visualizer")

clock = pg.time.Clock()

font = pg.font.SysFont("Arial", 14, bold=True)
title_font = pg.font.SysFont("Arial", 16, bold=True)
pause_font = pg.font.SysFont("Arial", 56, bold=True)


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
stats_manager = StatsManager()
active_stats_tab = "Stats"
comparison_session_data = []

# ==================================================
# 5. CREATE UI COMPONENTS
# ==================================================

# Algorithm dropdown and speed slider
algo_dropdown = Dropdown(
    15,
    MAZE_HEIGHT + 15,
    180,
    32,
    ["Astar", "Dijkstra", "BFS", "DFS"],
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

maze_dropdown = Dropdown(
    225,
    MAZE_HEIGHT + 60,
    235,
    32,
    ["Recursive Backtracking", "Randomized Prim", "Binary Tree"],
    open_direction="down",
    label="Maze",
)

map_size_dropdown = Dropdown(
    15,
    MAZE_HEIGHT + 100,
    180,
    30,
    list(MAP_PRESETS),
    open_direction="down",
    label="Map",
)
map_size_dropdown.selected_index = 1

ranking_dropdown = Dropdown(
    MAZE_WIDTH + 15,
    68,
    150,
    28,
    ["Runtime", "Success rate", "Path length", "Visited"],
    open_direction="down",
    label="Rank by",
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

btn_pause = Button(
    470, MAZE_HEIGHT + 15, 36, 32, ""
)
btn_skip = Button(
    514, MAZE_HEIGHT + 15, 64, 32, ""
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
btn_export = Button(
    MAZE_WIDTH + 15,
    MAZE_HEIGHT + 105,
    150,
    35,
    "Export Dataset"
)
tab_stats = Button(0, 0, 70, 30, "Stats")
tab_ranking = Button(0, 0, 90, 30, "Ranking")
tab_stats.selected = True


def layout_controls():
    bottom_y = MAZE_HEIGHT
    middle_x = 220
    middle_width = max(0, MAZE_WIDTH - middle_x - 15)

    algo_dropdown.set_position(15, bottom_y + 15, 180, 32)
    speed_slider.rect.y = bottom_y + 65
    speed_slider.handle_y = speed_slider.rect.y + 3
    map_size_dropdown.set_position(15, bottom_y + 105, 180, 30)
    maze_dropdown.set_position(
        middle_x,
        bottom_y + 60,
        min(235, middle_width),
        32,
    )

    base_widths = [75, 75, 75, 36, 64]
    gap = 4
    scale = min(1, middle_width / (sum(base_widths) + gap * 4))
    widths = [max(28, int(width * scale)) for width in base_widths]
    buttons = [btn_wall, btn_start, btn_target, btn_pause, btn_skip]
    x = middle_x
    for button, width in zip(buttons, widths):
        button.rect.update(x, bottom_y + 15, width, 32)
        x += width + gap

    for button, y_offset in (
        (btn_run, 15),
        (btn_clear, 60),
        (btn_export, 105),
    ):
        button.rect.topleft = (
            MAZE_WIDTH + 15,
            bottom_y + y_offset
        )

    tab_stats.rect.topleft = (MAZE_WIDTH + 10, 10)
    tab_ranking.rect.topleft = (MAZE_WIDTH + 85, 10)
    ranking_dropdown.set_position(MAZE_WIDTH + 15, 55, 150, 28)


def set_map_size(size_name):
    global ROWS, COLS, CELL_SIZE
    global MAZE_WIDTH, MAZE_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, screen
    global grid, mouse_handler, maze_gen, animation, asset_loader

    ROWS, COLS = MAP_PRESETS[size_name]
    map_size_dropdown.selected_index = list(MAP_PRESETS).index(size_name)
    CELL_SIZE = min(25, 750 // COLS, 600 // ROWS)
    MAZE_WIDTH = COLS * CELL_SIZE
    MAZE_HEIGHT = ROWS * CELL_SIZE
    SCREEN_WIDTH = MAZE_WIDTH + STATS_WIDTH
    SCREEN_HEIGHT = MAZE_HEIGHT + PANEL_HEIGHT

    grid = Grid(ROWS, COLS)
    mouse_handler = MouseHandler(grid, CELL_SIZE)
    maze_gen = MazeGenerator(grid)
    animation = AnimationController(grid)
    asset_loader = AssetLoader(CELL_SIZE)
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    layout_controls()


layout_controls()


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
    
    maze_id = stats_manager.generate_maze_id(
        grid, start, target
    )

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

    # Save statistics only once
    stats_manager.record(stats, maze_id=maze_id)
    # Save result for the current session's dataset
    comparison_session_data.append({
        **stats,
        "algorithm": selected,
        "maze_id": maze_id,
    })

    # Start the animation only once
    animation.delay = speed_slider.val
    animation.start(visited_order, found_path)


def generate_selected_maze():
    clear_visualization()
    maze_gen.generate_maze(maze_dropdown.get_selected())
    generation_cells = [
        cell
        for row in grid.cells
        for cell in row
        if cell.state == Cell.EMPTY
    ]

    for row in grid.cells:
        for cell in row:
            cell.state = Cell.WALL
    if grid.start is not None:
        grid.start.state = Cell.START
    if grid.target is not None:
        grid.target.state = Cell.TARGET

    animation.delay = speed_slider.val
    animation.start_generation(generation_cells)


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

def get_current_ranking():
    start, target = mouse_handler.find_start_target()
    if start is None or target is None:
        return []

    maze_id = stats_manager.generate_maze_id(grid, start, target)
    results = stats_manager.compare_algorithms(maze_id)
    criterion = ranking_dropdown.get_selected()
    fields = {
        "Runtime": "avg_runtime_ms",
        "Success rate": "success_rate",
        "Path length": "avg_path_length",
        "Visited": "avg_visited_count",
    }
    field = fields[criterion]

    def ranking_key(result):
        value = result[field]
        if value is None:
            value = float("inf")
        if criterion == "Success rate":
            value = -value
        return value, -result["success_rate"], result["algorithm"]

    return sorted(results, key=ranking_key)


def draw_ui_panels():
    stats_rect = pg.Rect(MAZE_WIDTH, 0, STATS_WIDTH, MAZE_HEIGHT)
    pg.draw.rect(screen, (255, 255, 255), stats_rect)
    pg.draw.rect(screen, (0, 0, 0), stats_rect, 2)

    tab_stats.draw(screen, font)
    tab_ranking.draw(screen, font)
    if active_stats_tab == "Stats":
        for text, y in (
            (f"runtime: {runtime_ms:.3f} ms", 55),
            (f"visited: {visited_count}", 85),
            (f"path_length: {path_length}", 115),
        ):
            screen.blit(font.render(text, True, (0, 0, 0)), (MAZE_WIDTH + 15, y))
    else:
        rankings = get_current_ranking()
        ranking_dropdown.draw(screen, font)
        ranking_start_y = (
            ranking_dropdown.option_rects[-1].bottom + 8
            if ranking_dropdown.is_open
            else ranking_dropdown.rect.bottom + 12
        )
        if not rankings:
            screen.blit(font.render("Run an algorithm", True, (70, 70, 70)), (MAZE_WIDTH + 15, ranking_start_y))
            screen.blit(font.render("to build rankings.", True, (70, 70, 70)), (MAZE_WIDTH + 15, ranking_start_y + 20))
        else:
            for index, result in enumerate(rankings):
                value = result[{
                    "Runtime": "avg_runtime_ms",
                    "Success rate": "success_rate",
                    "Path length": "avg_path_length",
                    "Visited": "avg_visited_count",
                }[ranking_dropdown.get_selected()]]
                if value is None:
                    value_text = "N/A"
                elif ranking_dropdown.get_selected() == "Success rate":
                    value_text = f"{value:.1f}%"
                elif ranking_dropdown.get_selected() == "Runtime":
                    value_text = f"{value:.3f} ms"
                else:
                    value_text = f"{value:.1f}"
                line = f"{index + 1}. {result['algorithm']}: {value_text}"
                screen.blit(font.render(line, True, (0, 0, 0)), (MAZE_WIDTH + 15, ranking_start_y + index * 28))

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
    map_size_dropdown.draw(screen, font)

    btn_wall.draw(screen, font)
    btn_start.draw(screen, font)
    btn_target.draw(screen, font)
    btn_pause.draw(screen, font)
    btn_skip.draw(screen, font)
    center_x, center_y = btn_pause.rect.center
    if animation.paused:
        pg.draw.polygon(
            screen,
            (0, 0, 0),
            [(center_x - 4, center_y - 8), (center_x + 8, center_y), (center_x - 4, center_y + 8)],
        )
    else:
        pg.draw.rect(screen, (0, 0, 0), (center_x - 6, center_y - 7, 4, 14))
        pg.draw.rect(screen, (0, 0, 0), (center_x + 2, center_y - 7, 4, 14))
    skip_center = btn_skip.rect.center
    pg.draw.circle(screen, (0, 0, 0), skip_center, 12, width=2)
    pg.draw.polygon(
        screen,
        (0, 0, 0),
        [
            (skip_center[0] - 6, skip_center[1] - 7),
            (skip_center[0] + 3, skip_center[1]),
            (skip_center[0] - 6, skip_center[1] + 7),
        ],
    )
    pg.draw.line(
        screen,
        (0, 0, 0),
        (skip_center[0] + 6, skip_center[1] - 8),
        (skip_center[0] + 6, skip_center[1] + 8),
        3,
    )

    btn_run.draw(screen, font)
    btn_clear.draw(screen, font)
    btn_export.draw(screen, font)

    # Draw dropdowns last so their menus stay visible
    algo_dropdown.draw(screen, font)
    maze_dropdown.draw(screen, font)


def draw_pause_overlay():
    if not animation.paused:
        return

    overlay = pg.Surface((MAZE_WIDTH, MAZE_HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 115))
    screen.blit(overlay, (0, 0))

    center = (MAZE_WIDTH // 2, MAZE_HEIGHT // 2 - 20)
    pg.draw.circle(screen, (25, 25, 25), center, 72)
    pg.draw.circle(screen, (255, 255, 255), center, 72, width=5)
    pg.draw.rect(screen, (255, 255, 255), (center[0] - 25, center[1] - 34, 16, 68), border_radius=5)
    pg.draw.rect(screen, (255, 255, 255), (center[0] + 9, center[1] - 34, 16, 68), border_radius=5)

    text = pause_font.render("PAUSED", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=(MAZE_WIDTH // 2, center[1] + 108)))


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
        map_option_clicked = (
            event.type == pg.MOUSEBUTTONDOWN
            and event.button == 1
            and any(rect.collidepoint(event.pos) for rect in map_size_dropdown.option_rects)
        )
        if map_size_dropdown.handle_event(event):
            if map_option_clicked:
                clear_visualization()
                set_map_size(map_size_dropdown.get_selected())
            continue
        maze_option_clicked = (
            event.type == pg.MOUSEBUTTONDOWN
            and event.button == 1
            and any(rect.collidepoint(event.pos) for rect in maze_dropdown.option_rects)
        )
        if maze_dropdown.handle_event(event):
            if maze_option_clicked:
                generate_selected_maze()
            continue
        if active_stats_tab == "Ranking" and ranking_dropdown.handle_event(event):
            continue

        # Mouse pressed
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if tab_stats.is_clicked((mx, my)):
                active_stats_tab = "Stats"
                tab_stats.selected = True
                tab_ranking.selected = False

            elif tab_ranking.is_clicked((mx, my)):
                active_stats_tab = "Ranking"
                tab_stats.selected = False
                tab_ranking.selected = True

            # Click on the maze
            elif mx < MAZE_WIDTH and my < MAZE_HEIGHT:
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

            # Pause or resume the current animation
            elif btn_pause.is_clicked((mx, my)):
                animation.toggle_pause()

            # Complete the active search or maze generation immediately
            elif btn_skip.is_clicked((mx, my)):
                animation.skip()

            # Run selected algorithm
            elif btn_run.is_clicked((mx, my)):
                execute_selected_algorithm()

            
            # Clear the visualization
            elif btn_clear.is_clicked((mx, my)):
                clear_visualization()

            
            # Export results for the current maze only
            elif btn_export.is_clicked((mx, my)):
                start, target = mouse_handler.find_start_target()

                if start is None or target is None:
                    print("Please set Start and Target first.")

                else:
                    current_maze_id = stats_manager.generate_maze_id(
                        grid, start, target
                    )

                    current_results = [
                        record
                        for record in comparison_session_data
                        if record["maze_id"] == current_maze_id
                    ]

                    output_path = export_comparison_dataset(
                        current_results
                    )

                    if output_path is None:
                        print(
                            "No comparison data for this maze. "
                            "Run an algorithm first."
                        )
                    else:
                        print(
                            f"Dataset exported successfully: {output_path}"
                        )



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
    draw_pause_overlay()
    draw_ui_panels()

    pg.display.update()
    clock.tick(60)


# ==================================================
# 11. SHUTDOWN
# ==================================================

pg.quit()
