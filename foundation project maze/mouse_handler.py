from cell import Cell

class MouseHandler:

    def __init__(self, grid, cell_size):
        self.grid = grid
        self.cell_size = cell_size
        self.mouse_pressed = False
        self.mode = "wall"

    def set_mode(self, mode):
        self.mode = mode

    def mouse_to_cell(self, x, y):
        col = x // self.cell_size
        row = y // self.cell_size
        return row, col


    def handle_click(self, x, y):
        row, col = self.mouse_to_cell(x, y)
        if row < 0 or row >= self.grid.rows:
            return
        if col < 0 or col >= self.grid.cols:
            return
        cell = self.grid.get_cell(row, col)
        if self.mode == "wall":
            self.toggle_wall(cell)
        elif self.mode == "start":
            self.set_start(cell)
        elif self.mode == "target":
            self.set_target(cell)

    def toggle_wall(self, cell):
        if cell.state == Cell.EMPTY:
            cell.state = Cell.WALL
        elif cell.state == Cell.WALL:
            cell.state = Cell.EMPTY


    def set_start(self, cell):
        if self.grid.start is not None:
            self.grid.start.state = Cell.EMPTY
        self.grid.start = cell
        cell.state = Cell.START


    def set_target(self, cell):
        if self.grid.target is not None:
            self.grid.target.state = Cell.EMPTY
        self.grid.target = cell
        cell.state = Cell.TARGET