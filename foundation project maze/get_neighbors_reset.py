from cell import Cell

class Grid:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = []

        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(Cell(r,c)) #append adds a single element to the end of a collection
            self.cells.append(row)
            self.start = None
            self.target = None
    def get_cell(self,row,col):
        return self.cells[self.rows][self.cols]

    def get_neighbors(self, cell):
        neighbors=[]
        r, c = cell.row, cell.col
        directions = [(-1, 0),(1, 0),(0, -1),(0, 1)] #phai,trai,tren,duoi

        for dr, dc in directions:
            nr, nc = r + dr, c + dc #n is neighbors, d is direction
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbors.append(self.cells[nr][nc])
        return neighbors

    #clear
    def clear_path(self):
        for r in range(self.rows):
            for c in range (self.cols):
                cell=self.cells[r][c]
                cell.parents= None
                if cell.state in (Cell.VISITED, Cell.PATH):
                    cell.state = Cell.EMPTY