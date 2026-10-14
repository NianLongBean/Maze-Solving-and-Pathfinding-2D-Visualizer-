import pygame as pg
from grid import *
from cell import Cell
from path_position import *
pg.init()

def start_animation(visited_order, found_path, stats, grid):
    global animation_active, animation_visited, animation_path
    global animation_index, animation_path_index, animation_phase
    global last_animation_update, runtime_ms, visited_count, path_coords, path_length

    grid.clear_path()
    animation_visited = visited_order
    animation_path = found_path
    
    # Cập nhật thông số từ data_recorder & path_position
    runtime_ms = stats["runtime_ms"]
    visited_count = stats["visited_count"]
    path_length = stats["path_length"]
    path_coords = get_path_coordinates(found_path)

    animation_index = 0
    animation_path_index = 0
    animation_phase = "visited"
    last_animation_update = pg.time.get_ticks()
    animation_active = bool(animation_visited or animation_path)

def update_animation(grid, speed_slider):
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