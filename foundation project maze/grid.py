from cell import Cell

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = []

        for r in range(rows):
            row = []
            for c in range(cols): 
                row.append(Cell(r, c))
            self.cells.append(row)
        self.start = None
        self.target = None

    def get_cell(self, row, col):
        return self.cells[row][col]