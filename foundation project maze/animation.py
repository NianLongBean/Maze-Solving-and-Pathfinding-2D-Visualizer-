
import pygame as pg
from cell import Cell


class AnimationController:
    def __init__(
        self,
        grid,
        delay=50,
        min_delay=10,
        max_delay=300,
        delay_step=10
    ):
        self.grid = grid

        # Animation settings
        self.delay = delay
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.delay_step = delay_step

        # Animation state
        self.active = False
        self.visited = []
        self.path_cells = []

        self.visited_index = 0
        self.path_index = 0
        self.phase = "visited"
        self.last_update = 0

    def start(self, visited_order, found_path):
        # Clear the previous visualization
        self.clear()

        # Store algorithm results
        self.visited = list(visited_order)
        self.path_cells = list(found_path)

        # Reset animation progress
        self.visited_index = 0
        self.path_index = 0
        self.phase = "visited"
        self.last_update = pg.time.get_ticks()

        self.active = bool(self.visited or self.path_cells)

    def update(self):
        if not self.active:
            return

        current_time = pg.time.get_ticks()

        # Wait until the next update is due
        if current_time - self.last_update < self.delay:
            return

        self.last_update = current_time

        # Phase 1: Animate visited cells
        if self.phase == "visited":
            if self.visited_index < len(self.visited):
                cell = self.visited[self.visited_index]

                if cell != self.grid.start and cell != self.grid.target:
                    cell.state = Cell.VISITED

                self.visited_index += 1
            else:
                self.phase = "path"

        # Phase 2: Animate the final path
        elif self.phase == "path":
            if self.path_index < len(self.path_cells):
                cell = self.path_cells[self.path_index]

                if cell != self.grid.start and cell != self.grid.target:
                    cell.state = Cell.PATH

                self.path_index += 1
            else:
                self.active = False

    def speed_up(self):
        self.delay = max(
            self.min_delay,
            self.delay - self.delay_step
        )

    def slow_down(self):
        self.delay = min(
            self.max_delay,
            self.delay + self.delay_step
        )

    def clear(self):
        self.active = False
        self.grid.clear_path()

        if self.grid.start is not None:
            self.grid.start.state = Cell.START

        if self.grid.target is not None:
            self.grid.target.state = Cell.TARGET
