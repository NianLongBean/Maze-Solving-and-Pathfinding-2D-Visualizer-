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

        # Kiểm tra có nằm trong Grid không
        if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols:

            neighbor = grid.get_cell(new_row, new_col)

            # Không đi xuyên qua tường
            if neighbor.state != Cell.WALL:
                neighbors.append(neighbor)

    return neighbors


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
        for neighbor in get_neighbors(grid, current):

            if neighbor not in visited:

                parent[neighbor] = current

                stack.append(neighbor)

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