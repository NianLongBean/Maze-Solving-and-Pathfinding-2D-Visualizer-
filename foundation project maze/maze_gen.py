import random
from cell import Cell

#Recursive Backtracking

class MazeGenerator:

    def __init__(self, grid):
        self.grid = grid


    def get_one_off_neighbours(self, cell):
        neighbours = []
        row = cell.row
        col = cell.col

#neighbours 2 steps away for carving passages

        if row > 1:
            neighbours.append(self.grid.get_cell(row - 2, col))
            
        if row < self.grid.rows - 2:
            neighbours.append(self.grid.get_cell(row + 2, col))

        if col > 1:
            neighbours.append(self.grid.get_cell(row, col - 2))

        if col < self.grid.cols - 2:
            neighbours.append(self.grid.get_cell(row, col + 2))

        return neighbours

#maze gen 
    def generate_maze(self):
        #1.Fill entire grid with wall
        for r in range (self.grid.rows):
            for c in range (self.grid.cols):
                cell = self.grid.get_cell(r, c)
                cell.state = Cell.WALL

        #Carve passages from cell(1,1)
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
            else:stack.pop()

    #ensure start node and target node are placed on empty spots
        if self.grid.start:
                    self.grid.start.state = Cell.START
        if self.grid.target:
                    self.grid.target.state = Cell.TARGET
