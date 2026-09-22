import pygame as pg

from grid import Grid
from mouse_handler import MouseHandler
from cell import Cell
from maze_gen import MazeGenerator

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

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Grid Project")
clock = pg.time.Clock()
grid = Grid(ROWS, COLS)

mouse_handler = MouseHandler(
    grid,
    CELL_SIZE
)


# VVVVVVVVVVVVVVV
# DRAW
# VVVVVVVVVVVVVVV

def draw_grid():
    for r in range(grid.rows):
        for c in range(grid.cols):
            cell = grid.get_cell(r, c)
            x = c * CELL_SIZE
            y = r * CELL_SIZE
            if cell.state == Cell.EMPTY:
                color = (240, 240, 240)

            elif cell.state == Cell.WALL:
                color = (30, 30, 30)

            elif cell.state == Cell.START:
                color = (0, 200, 0)

            else:
                color = (200, 0, 0)

            pg.draw.rect(screen,color,(x, y, CELL_SIZE, CELL_SIZE))
            pg.draw.rect(screen,(100, 100, 100),(x, y, CELL_SIZE, CELL_SIZE),1)
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
  
# Handle mouse

    if mouse_handler.mouse_pressed:
        x, y = pg.mouse.get_pos()
        mouse_handler.handle_click(x, y)


# Draw
    screen.fill((255, 255, 255))
    draw_grid()
    pg.display.update()
    clock.tick(60)

pg.quit()