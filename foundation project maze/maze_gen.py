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

    def _random_endpoints(self):
        start = self.grid.start or self.grid.get_cell(1, 1)
        target = self.grid.target or self.grid.get_cell(
            self.grid.rows - 2,
            self.grid.cols - 2,
        )
        return start, target

    def _carve_route(self, waypoints):
        for (row, col), (next_row, next_col) in zip(waypoints, waypoints[1:]):
            row_step = (next_row > row) - (next_row < row)
            col_step = (next_col > col) - (next_col < col)
            while (row, col) != (next_row, next_col):
                self.grid.get_cell(row, col).state = Cell.EMPTY
                row += row_step
                col += col_step
            self.grid.get_cell(row, col).state = Cell.EMPTY

    def _generate_random_connected(self, start, target):
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                if random.random() < 0.28:
                    self.grid.get_cell(row, col).state = Cell.EMPTY

        start_pos = (start.row, start.col)
        target_pos = (target.row, target.col)
        start_row, start_col = start_pos
        target_row, target_col = target_pos

        if start_pos == target_pos:
            return

        if start_row != target_row and start_col != target_col:
            self._carve_route([start_pos, (start_row, target_col), target_pos])
            self._carve_route([start_pos, (target_row, start_col), target_pos])
        elif start_row == target_row:
            detour_row = random.choice(
                [row for row in range(self.grid.rows) if row != start_row]
            )
            self._carve_route([start_pos, target_pos])
            self._carve_route([
                start_pos,
                (detour_row, start_col),
                (detour_row, target_col),
                target_pos,
            ])
        else:
            detour_col = random.choice(
                [col for col in range(self.grid.cols) if col != start_col]
            )
            self._carve_route([start_pos, target_pos])
            self._carve_route([
                start_pos,
                (start_row, detour_col),
                (target_row, detour_col),
                target_pos,
            ])

    def _generate_random_disconnected(self, target):
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                if random.random() < 0.28:
                    self.grid.get_cell(row, col).state = Cell.EMPTY

        for neighbour in self.grid.get_neighbours(target):
            neighbour.state = Cell.WALL

    def _generate_random(self):
        start, target = self._random_endpoints()
        start_neighbours = self.grid.get_neighbours(start)
        can_disconnect = start != target and target not in start_neighbours

        if can_disconnect and random.random() < 0.4:
            self._generate_random_disconnected(target)
        else:
            self._generate_random_connected(start, target)

    def generate_maze(self, algorithm="Recursive Backtracking"):
        generators = {
            "Recursive Backtracking": self._generate_backtracking,
            "Randomized Prim": self._generate_prim,
            "Binary Tree": self._generate_binary_tree,
            "Random (Loops / No Path)": self._generate_random,
        }
        if algorithm not in generators:
            raise ValueError(f"Unknown maze generation algorithm: {algorithm}")

        self._fill_walls()
        generators[algorithm]()
        self._restore_markers()
