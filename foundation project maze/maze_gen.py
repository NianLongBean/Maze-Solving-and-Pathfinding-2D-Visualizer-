class MazeGenerator:

    def __init__(self, grid):
        self.grid = grid
    def get_one_off_neighbours(self, cell):
        neighbours = []
        row = cell.row
        col = cell.col

        if row > 1:
            neighbours.append(self.grid.get_cell(row - 2, col))
            
        if row < self.grid.rows - 2:
            neighbours.append(self.grid.get_cell(row + 2, col))

        if col > 1:
            neighbours.append(self.grid.get_cell(row, col - 2))

        if col < self.grid.cols - 2:
            neighbours.append(self.grid.get_cell(row, col + 2))

        return neighbours