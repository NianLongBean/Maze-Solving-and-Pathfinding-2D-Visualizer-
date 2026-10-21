import random
from cell import Cell

#Recursive Backtracking

class MazeGenerator:

    def __init__(self, grid):
        self.grid = grid

    def _fill_walls(self):
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                self.grid.get_cell(row, col).state = Cell.WALL

    def _restore_markers(self):
        if self.grid.start:
            self.grid.start.state = Cell.START
        if self.grid.target:
            self.grid.target.state = Cell.TARGET

    def _odd_cell_neighbours(self, cell):
        neighbours = []
        for row, col in (
            (cell.row - 2, cell.col),
            (cell.row + 2, cell.col),
            (cell.row, cell.col - 2),
            (cell.row, cell.col + 2),
        ):
            if 0 < row < self.grid.rows - 1 and 0 < col < self.grid.cols - 1:
                neighbours.append(self.grid.get_cell(row, col))
        return neighbours


    def get_one_off_neighbours(self, cell):
        return self._odd_cell_neighbours(cell)

    def _generate_backtracking(self):
        start_cell = self.grid.get_cell(1, 1)
        start_cell.state= Cell.EMPTY

        stack = [start_cell]
        visited = {start_cell}

        while stack:
            current = stack[-1]
            #unvisited neighbours that are 2 steps away
            unvisited_neighbours = [
                n 
                for n in self.get_one_off_neighbours(current)
                if n not in visited
            ]

            if unvisited_neighbours:
                next_cell=random.choice(unvisited_neighbours)

                #remove the wall between cell and chosen next cell
                wall_row = (current.row + next_cell.row)//2
                wall_col = (current.col + next_cell.col)//2
                wall_cell = self.grid.get_cell(wall_row, wall_col)

                wall_cell.state = Cell.EMPTY
                next_cell.state = Cell.EMPTY

                visited.add(next_cell)
                visited.add(wall_cell)
                stack.append(next_cell)
            else:
                stack.pop()

    def _generate_prim(self):
        start_cell = self.grid.get_cell(1, 1)
        start_cell.state = Cell.EMPTY
        connected = {start_cell}
        frontier = self._odd_cell_neighbours(start_cell)

        while frontier:
            cell = random.choice(frontier)
            frontier.remove(cell)
            if cell in connected:
                continue

            connected_neighbours = [
                neighbour
                for neighbour in self._odd_cell_neighbours(cell)
                if neighbour in connected
            ]
            if not connected_neighbours:
                continue

            neighbour = random.choice(connected_neighbours)
            wall = self.grid.get_cell(
                (cell.row + neighbour.row) // 2,
                (cell.col + neighbour.col) // 2,
            )
            wall.state = Cell.EMPTY
            cell.state = Cell.EMPTY
            connected.add(cell)
            frontier.extend(
                candidate
                for candidate in self._odd_cell_neighbours(cell)
                if candidate not in connected and candidate not in frontier
            )

    def _generate_binary_tree(self):
        for row in range(1, self.grid.rows - 1, 2):
            for col in range(1, self.grid.cols - 1, 2):
                self.grid.get_cell(row, col).state = Cell.EMPTY
                carve_options = []
                if row > 1:
                    carve_options.append((-1, 0))
                if col > 1:
                    carve_options.append((0, -1))

                if carve_options:
                    row_offset, col_offset = random.choice(carve_options)
                    self.grid.get_cell(row + row_offset, col + col_offset).state = Cell.EMPTY

    def generate_maze(self, algorithm="Recursive Backtracking"):
        generators = {
            "Recursive Backtracking": self._generate_backtracking,
            "Randomized Prim": self._generate_prim,
            "Binary Tree": self._generate_binary_tree,
        }
        if algorithm not in generators:
            raise ValueError(f"Unknown maze generation algorithm: {algorithm}")

        self._fill_walls()
        generators[algorithm]()
        self._restore_markers()
