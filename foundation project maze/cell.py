class Cell:
    EMPTY = 0
    WALL = 1
    START = 2
    TARGET = 3
    VISITED = 4  
    PATH = 5  
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = Cell.EMPTY
        self.parent = None  