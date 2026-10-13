import heapq
from cell import Cell


def heuristic(cell, target):
    return abs(cell.row - target.row) + abs(cell.col - target.col)


def astar(grid, start, target):

    open_heap = []

    counter = 0

    g_score = {start: 0}

    f_score = {start: heuristic(start, target)}

    heapq.heappush(
        open_heap,
        (f_score[start], counter, start)
    )

    counter += 1

    parent = {}

    visited_order = []

    while open_heap:

        current_f, _, current = heapq.heappop(open_heap)

        if current != start and current != target:
            visited_order.append(current)

        if current == target:
            break

        for neighbour in grid.get_neighbours(current):

            if neighbour.state == Cell.WALL:
                continue

            tentative_g = g_score[current] + 1

            if neighbour not in g_score or tentative_g < g_score[neighbour]:

                parent[neighbour] = current

                g_score[neighbour] = tentative_g

                f_score[neighbour] = (
                    tentative_g
                    + heuristic(neighbour, target)
                )

                heapq.heappush(
                    open_heap,
                    (f_score[neighbour], counter, neighbour)
                )

                counter += 1

    path = []

    if target in parent or target == start:

        current = target

        while current != start:
            path.append(current)
            current = parent[current]

        path.reverse()

    return visited_order, path