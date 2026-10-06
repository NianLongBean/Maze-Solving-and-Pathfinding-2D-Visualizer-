from collections import deque
from cell import Cell


def bfs(grid):
    if not grid.start or not grid.target:
        return [], []

    # grid.clear_path()
    queue = deque([grid.start])
    visited = {grid.start}

    visited_order = []
    found = False

    while queue:
        current = queue.popleft()

        if current != grid.start and current != grid.target:
            visited_order.append(current)

        if current == grid.target:
            found = True
            break

        for neighbour in grid.get_neighbours(current):
            if neighbour.state != Cell.WALL and neighbour not in visited:
                visited.add(neighbour)
                neighbour.parent = current
                queue.append(neighbour)

    # Truy vết đường đi (Shortest Path)[cite: 1]
    path = []
    if found:
        curr = grid.target.parent
        while curr and curr != grid.start:
            path.append(curr)
            curr = curr.parent
        path.reverse()

    return visited_order, path