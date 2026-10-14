import pygame as pg
from grid import Grid
from mouse_handler import MouseHandler
from cell import Cell
from maze_gen import MazeGenerator
from assetsloader import AssetLoader

# Import các thuật toán
import bfs 
from DFS import dfs
from dijkstra import dijkstra
from Astar import astar

# Import helper ghi nhận thông số & UI
from data_recorder import run_and_record
from path_position import get_path_coordinates
from ui import Button, Slider, Dropdown

# VVVVVVVVVVVVVVV
# CẤU HÌNH KÍCH THƯỚC GIAO DIỆN
# VVVVVVVVVVVVVVV

ROWS = 20
COLS = 30
CELL_SIZE = 25

MAZE_WIDTH = COLS * CELL_SIZE   # 750 px
MAZE_HEIGHT = ROWS * CELL_SIZE # 500 px

STATS_WIDTH = 180              # Panel bên phải (Stats)
PANEL_HEIGHT = 110             # Panel điều khiển phía dưới

SCREEN_WIDTH = MAZE_WIDTH + STATS_WIDTH  # 930 px
SCREEN_HEIGHT = MAZE_HEIGHT + PANEL_HEIGHT # 610 px

# VVVVVVVVVVVVVVV
# KHỞI TẠO PYGAME
# VVVVVVVVVVVVVVV

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Maze Solving & Pathfinding Visualizer")
clock = pg.time.Clock()
font = pg.font.SysFont("Arial", 14, bold=True)
title_font = pg.font.SysFont("Arial", 16, bold=True)

asset_loader = AssetLoader(CELL_SIZE)
grid = Grid(ROWS, COLS)
mouse_handler = MouseHandler(grid, CELL_SIZE)
maze_gen = MazeGenerator(grid)

# Animation & Thống kê
animation_active = False
animation_visited = []
animation_path = []
animation_index = 0
animation_path_index = 0
animation_phase = "visited"
last_animation_update = 0

runtime_ms = 0.0
visited_count = 0
path_coords = []

# VVVVVVVVVVVVVVV
# TẠO CÁC NÚT & PANEL THEO BẢN VẼ
# VVVVVVVVVVVVVVV

# 1. Ô Algorithms & Speed Slider (Góc dưới bên trái)
algo_dropdown = Dropdown(15, MAZE_HEIGHT + 15, 180, 32, ["Astar", "Dijkstra", "BFS", "DFS"])
speed_slider = Slider(15, MAZE_HEIGHT + 65, 180, 10, 200, 50, label="speed")

# 2. Ô Blocks (Chế độ đặt vật thể)
btn_wall = Button(225, MAZE_HEIGHT + 15, 75, 32, "Wall")
btn_start = Button(305, MAZE_HEIGHT + 15, 75, 32, "Start")
btn_target = Button(385, MAZE_HEIGHT + 15, 75, 32, "Target")
btn_maze = Button(225, MAZE_HEIGHT + 60, 235, 32, "Generate Maze")

btn_wall.selected = True # Chọn Wall mặc định

# 3. Ô Run & Clear
btn_run = Button(MAZE_WIDTH + 15, MAZE_HEIGHT + 15, 150, 35, "Run", bg_color=(120, 220, 120))
btn_clear = Button(MAZE_WIDTH + 15, MAZE_HEIGHT + 60, 150, 35, "Clear", bg_color=(240, 130, 130))


def start_animation(visited_order, found_path, stats):
    global animation_active, animation_visited, animation_path
    global animation_index, animation_path_index, animation_phase
    global last_animation_update, runtime_ms, visited_count, path_coords

    grid.clear_path()
    animation_visited = visited_order
    animation_path = found_path
    
    # Cập nhật thông số từ data_recorder & path_position
    runtime_ms = stats["runtime_ms"]
    visited_count = stats["visited_count"]
    path_coords = get_path_coordinates(found_path)

    animation_index = 0
    animation_path_index = 0
    animation_phase = "visited"
    last_animation_update = pg.time.get_ticks()
    animation_active = bool(animation_visited or animation_path)


def update_animation():
    global animation_active, animation_index, animation_path_index
    global animation_phase, last_animation_update

    if not animation_active:
        return

    current_time = pg.time.get_ticks()
    if current_time - last_animation_update < speed_slider.val:
        return

    last_animation_update = current_time

    if animation_phase == "visited":
        if animation_index < len(animation_visited):
            cell = animation_visited[animation_index]
            if cell != grid.start and cell != grid.target:
                cell.state = Cell.VISITED
            animation_index += 1
        else:
            animation_phase = "path"

    elif animation_phase == "path":
        if animation_path_index < len(animation_path):
            cell = animation_path[animation_path_index]
            if cell != grid.start and cell != grid.target:
                cell.state = Cell.PATH
            animation_path_index += 1
        else:
            animation_active = False


def execute_selected_algorithm():
    start, target = mouse_handler.find_start_target()
    if not start or not target:
        return

    selected = algo_dropdown.get_selected()

    if selected == "BFS":
        algo_func = lambda: bfs.bfs(grid)
        visited_order, found_path, stats = run_and_record("BFS", algo_func, start=start, target=target)
    elif selected == "DFS":
        visited_order, found_path, stats = run_and_record("DFS", dfs, grid, start, target, start=start, target=target)
    elif selected == "Dijkstra":
        visited_order, found_path, stats = run_and_record("Dijkstra", dijkstra, grid, start, target, start=start, target=target)
    elif selected == "Astar":
        visited_order, found_path, stats = run_and_record("A*", astar, grid, start, target, start=start, target=target)
    else:
        return

    start_animation(visited_order, found_path, stats)


def draw_grid():
    for r in range(grid.rows):
        for c in range(grid.cols):
            cell = grid.get_cell(r, c)
            x = c * CELL_SIZE
            y = r * CELL_SIZE

            drawn_by_asset = asset_loader.draw_cell(screen, cell, x, y)
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

                pg.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pg.draw.rect(screen, (210, 210, 210), (x, y, CELL_SIZE, CELL_SIZE), 1)


def draw_ui_panels():
    # 1. Khu vực Stats (Khung bên phải)
    stats_rect = pg.Rect(MAZE_WIDTH, 0, STATS_WIDTH, MAZE_HEIGHT)
    pg.draw.rect(screen, (255, 255, 255), stats_rect)
    pg.draw.rect(screen, (0, 0, 0), stats_rect, 2)

    txt_stats = title_font.render("Stats", True, (0, 0, 0))
    txt_runtime = font.render(f"runtime: {runtime_ms} ms", True, (0, 0, 0))
    txt_visited = font.render(f"visited: {visited_count}", True, (0, 0, 0))

    screen.blit(txt_stats, (MAZE_WIDTH + 15, 15))
    screen.blit(txt_runtime, (MAZE_WIDTH + 15, 50))
    screen.blit(txt_visited, (MAZE_WIDTH + 15, 80))

    # 2. Khung viền lớn chứa Bàn cờ (The maze)
    maze_border = pg.Rect(0, 0, MAZE_WIDTH, MAZE_HEIGHT)
    pg.draw.rect(screen, (0, 0, 0), maze_border, 2)

    # 3. Khu vực Bảng điều khiển phía dưới
    bottom_rect = pg.Rect(0, MAZE_HEIGHT, SCREEN_WIDTH, PANEL_HEIGHT)
    pg.draw.rect(screen, (245, 245, 245), bottom_rect)
    pg.draw.rect(screen, (0, 0, 0), bottom_rect, 2)

    # Đường phân cách các ô điều khiển
    pg.draw.line(screen, (0, 0, 0), (210, MAZE_HEIGHT), (210, SCREEN_HEIGHT), 2)
    pg.draw.line(screen, (0, 0, 0), (MAZE_WIDTH, MAZE_HEIGHT), (MAZE_WIDTH, SCREEN_HEIGHT), 2)

    # Vẽ các linh kiện tương tác
    speed_slider.draw(screen, font)
    btn_wall.draw(screen, font)
    btn_start.draw(screen, font)
    btn_target.draw(screen, font)
    btn_maze.draw(screen, font)

    btn_run.draw(screen, font)
    btn_clear.draw(screen, font)

    # Draw Dropdown sau cùng để danh sách không bị các nút khác đè
    algo_dropdown.draw(screen, font)


# Main Loop
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Tương tác Slider
        speed_slider.handle_event(event)

        # Tương tác Dropdown
        if algo_dropdown.handle_event(event):
            continue

        # Sự kiện click chuột
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # Click vào bàn cờ
            if mx < MAZE_WIDTH and my < MAZE_HEIGHT:
                mouse_handler.mouse_pressed = True
                mouse_handler.handle_click(mx, my, is_initial_press=True)

            # Click nút chuyển chế độ Wall/Start/Target
            elif btn_wall.is_clicked((mx, my)):
                mouse_handler.set_mode("wall")
                btn_wall.selected, btn_start.selected, btn_target.selected = True, False, False

            elif btn_start.is_clicked((mx, my)):
                mouse_handler.set_mode("start")
                btn_wall.selected, btn_start.selected, btn_target.selected = False, True, False

            elif btn_target.is_clicked((mx, my)):
                mouse_handler.set_mode("target")
                btn_wall.selected, btn_start.selected, btn_target.selected = False, False, True

            elif btn_maze.is_clicked((mx, my)):
                maze_gen.generate_maze()

            elif btn_run.is_clicked((mx, my)):
                execute_selected_algorithm()

            elif btn_clear.is_clicked((mx, my)):
                animation_active = False
                grid.clear_path()
                runtime_ms = 0.0
                visited_count = 0
                path_coords = []

        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            mouse_handler.mouse_pressed = False

    # Kéo giữ chuột trên bàn cờ
    if mouse_handler.mouse_pressed:
        mx, my = pg.mouse.get_pos()
        if mx < MAZE_WIDTH and my < MAZE_HEIGHT:
            mouse_handler.handle_click(mx, my)

    update_animation()

    screen.fill((255, 255, 255))
    draw_grid()
    draw_ui_panels()

    pg.display.update()
    clock.tick(60)

pg.quit()