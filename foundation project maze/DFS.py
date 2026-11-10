from cell import Cell


def get_neighbours(grid, cell):
    neighbours = []

    directions = [
        (-1, 0),  # trên
        (1, 0),   # dưới
        (0, -1),  # trái
        (0, 1)    # phải
    ]

    for dr, dc in directions:
        new_row = cell.row + dr
        new_col = cell.col + dc

        if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols:
            neighbour = grid.get_cell(new_row, new_col)

            if neighbour.state != Cell.WALL:
                neighbours.append(neighbour)

    return neighbours


def dfs(grid, start, target):
    stack = [start]

    visited = set()
    visited_order = []
    parent = {}

    while stack:
        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        if current != start and current != target:
            visited_order.append(current)

        if current == target:
            break

        for neighbour in get_neighbours(grid, current):
            if neighbour not in visited:
                parent[neighbour] = current
                stack.append(neighbour)

    if target not in visited:
        return visited_order, []

    path = []
    current = target

    while current != start:
        path.append(current)
        current = parent[current]

    path.reverse()

    return visited_order, path
