import pygame as pg
from grid import Grid
from mouse_handler import MouseHandler
from cell import Cell
from maze_gen import MazeGenerator
from aigen_note import ControlsNote
from assetsloader import AssetLoader
import bfs 
from DFS import dfs
from dijkstra import dijkstra
from Astar import astar

# VVVVVVVVVVVVVVV
# Setting/Cài đặt
# VVVVVVVVVVVVVVV

ROWS = 20
COLS = 30
CELL_SIZE = 30
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE


# VVVVVVVVVVVVVVV
# INITIALIZE
# VVVVVVVVVVVVVV

asset_loader = AssetLoader(CELL_SIZE)
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Maze Solving & Pathfinding Visualizer")
clock = pg.time.Clock()
grid = Grid(ROWS, COLS)

# Animation settings
SIMULATION_DELAY = 50  # Milliseconds between cell updates
MIN_DELAY = 10
MAX_DELAY = 300
DELAY_STEP = 10

# Animation state
animation_active = False
animation_visited = []
animation_path = []
animation_index = 0
animation_path_index = 0
animation_phase = "visited"
last_animation_update = 0


mouse_handler = MouseHandler(
    grid,
    CELL_SIZE
)
path=[]


maze_gen = MazeGenerator(grid)


#initiate controls note at pos(x,y)
controls_note = ControlsNote(x=10, y=10)
# VVVVVVVVVVVVVVV
# DRAW
# VVVVVVVVVVVVVVV

def start_animation(visited_order, found_path):
    global path
    global animation_active
    global animation_visited, animation_path
    global animation_index, animation_path_index
    global animation_phase, last_animation_update

    # Clear the previous visualization
    grid.clear_path()
    path = []

    # Store the results of the algorithm
    animation_visited = visited_order
    animation_path = found_path

    # Reset animation progress
    animation_index = 0
    animation_path_index = 0
    animation_phase = "visited"

    # Record the animation start time
    last_animation_update = pg.time.get_ticks()

    animation_active = bool(animation_visited or animation_path)


def update_animation():
    global path
    global animation_active
    global animation_index, animation_path_index
    global animation_phase, last_animation_update

    if not animation_active:
        return

    current_time = pg.time.get_ticks()

    # Wait until the next update is due
    if current_time - last_animation_update < SIMULATION_DELAY:
        return

    last_animation_update = current_time

    # Phase 1: Show visited cells one by one
    if animation_phase == "visited":

        if animation_index < len(animation_visited):
            cell = animation_visited[animation_index]

            if cell != grid.start and cell != grid.target:
                cell.state = Cell.VISITED

            animation_index += 1

        else:
            animation_phase = "path"

    # Phase 2: Show the final path one cell at a time
    elif animation_phase == "path":

        if animation_path_index < len(animation_path):
            cell = animation_path[animation_path_index]

            if cell != grid.start and cell != grid.target:
                cell.state = Cell.PATH
                path.append(cell)

            animation_path_index += 1

        else:
            animation_active = False

def draw_grid():
    for r in range(grid.rows):
        for c in range(grid.cols):
            cell = grid.get_cell(r, c)
            x = c * CELL_SIZE
            y = r * CELL_SIZE

            drawn_by_asset = asset_loader.draw_cell(screen, cell, x, y)

            if not drawn_by_asset:
                if cell in path:
                    color = (255, 255, 0)
                elif cell.state == Cell.EMPTY:
                    color = (240, 240, 240)
                elif cell.state == Cell.WALL:
                    color = (30, 30, 30)
                elif cell.state == Cell.START:
                    color = (0, 200, 0)
                else:
                    color = (200, 0, 0)

                pg.draw.rect(
                    screen,
                    color,
                    (x, y, CELL_SIZE, CELL_SIZE)
                )

                pg.draw.rect(
                    screen,
                    (100, 100, 100),
                    (x, y, CELL_SIZE, CELL_SIZE),
                    1
                )
# VVVVVVVVVVVVVVV
# MAIN LOOP
# VVVVVVVVVVVVVVV

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Mouse button pressed
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_handler.mouse_pressed = True
                x,y = pg.mouse.get_pos()
                mouse_handler.handle_click(
                    x, y, is_initial_press = True
                )

        # Mouse button released
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_handler.mouse_pressed = False

        # Keyboard
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                mouse_handler.set_mode("wall")

            elif event.key == pg.K_s:
                mouse_handler.set_mode("start")

            elif event.key == pg.K_t:
                mouse_handler.set_mode("target")

            # Press M to generate a random maze
            elif event.key == pg.K_m:
                maze_gen.generate_maze()

            
            # Press B to run BFS
            elif event.key == pg.K_b:
                visited_order, found_path = bfs.bfs(grid)
                start_animation(visited_order, found_path)

            # Press D to run DFS
            elif event.key == pg.K_d:
                start, target = mouse_handler.find_start_target()

                if start is not None and target is not None:
                    visited_order, found_path = dfs(grid, start, target)
                    start_animation(visited_order, found_path)

            # Press J to run Dijkstra
            elif event.key == pg.K_j:
                start, target = mouse_handler.find_start_target()

                if start is not None and target is not None:
                    visited_order, found_path = dijkstra(
                        grid, start, target
                    )
                    start_animation(visited_order, found_path)

            # Press A to run A*
            elif event.key == pg.K_a:
                start, target = mouse_handler.find_start_target()

                if start is not None and target is not None:
                    visited_order, found_path = astar(
                        grid, start, target
                    )
                    start_animation(visited_order, found_path)

            
            # Press UP to speed up
            elif event.key == pg.K_UP:
                SIMULATION_DELAY = max(
                    MIN_DELAY,
                    SIMULATION_DELAY - DELAY_STEP
                )

            # Press DOWN to slow down
            elif event.key == pg.K_DOWN:
                SIMULATION_DELAY = min(
                    MAX_DELAY,
                    SIMULATION_DELAY + DELAY_STEP
                )

            # Press C to clear the visualization
            elif event.key == pg.K_c:
                animation_active = False
                grid.clear_path()
                path = []

  

    # Handle mouse
    if mouse_handler.mouse_pressed:
        x, y = pg.mouse.get_pos()
        mouse_handler.handle_click(x, y)

    # Update the animation without blocking the game loop
    update_animation()

    # Draw
    screen.fill((255, 255, 255))
    draw_grid()

    controls_note.draw(screen)

    pg.display.update()
    clock.tick(60)

pg.quit()
