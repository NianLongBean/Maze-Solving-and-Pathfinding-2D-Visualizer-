from cell import Cell


def get_neighbors(grid, cell):
    neighbors = []

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
            neighbor = grid.get_cell(new_row, new_col)

            if neighbor.state != Cell.WALL:
                neighbors.append(neighbor)

    return neighbors


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
        visited_order.append(current)

        if current == target:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                parent[neighbor] = current
                stack.append(neighbor)

    # Không tìm thấy Target
    if target not in visited:
        return visited_order, []

    # Tạo đường đi từ Target về Start
    path = []
    current = target

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()

    return visited_order, path