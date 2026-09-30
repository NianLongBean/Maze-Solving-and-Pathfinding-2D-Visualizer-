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

        # Kiểm tra có nằm trong Grid không
        if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols:

            neighbour = grid.get_cell(new_row, new_col)

            # Không đi xuyên qua tường
            if neighbour.state != Cell.WALL:
                neighbours.append(neighbour)

    return neighbours


def dfs(grid, start, target):

    stack = [start]
    visited = set()
    parent = {}

    while stack:

        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        # Đã tìm thấy Target
        if current == target:
            break

        # Tìm các ô có thể đi tới
        for neighbour in get_neighbours(grid, current):

            if neighbour not in visited:

                parent[neighbour] = current

                stack.append(neighbour)

    # Không tìm thấy đường
    if target not in visited:
        return []

    # Tạo path
    path = []
    current = target

    while current != start:

        path.append(current)

        current = parent[current]

    path.append(start)

    # Đảo ngược
    path.reverse()

    return path