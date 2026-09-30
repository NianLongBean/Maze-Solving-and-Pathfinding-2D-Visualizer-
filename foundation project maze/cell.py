class Cell:
    EMPTY = 0
    WALL = 1
    START = 2
    TARGET = 3
    VISITED = 4  # Visited Cell
    PATH = 5  # Cell that belongs to the shortest path

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = Cell.EMPTY
        self.parent = None  # Path Tracking