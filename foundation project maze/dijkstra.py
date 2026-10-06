import heapq
from itertools import count
from cell import Cell

counter = count()

def dijkstra(grid, start, target):
    # Count distances from start to each cell and store them
    distance = {start: 0}
    parent = {}
    
    # (distance, cell)
    priority_queue = [(0, next(counter), start)]
    visited = set()
    visited_order = []

    while priority_queue:
        current_distance, _, current = heapq.heappop(priority_queue)
        
        if current in visited: continue 
        visited.add(current)
        if current != start and current != target:visited_order.append(current)
        if current == target: break

        # Check all valid neighbours (ignore walls and already visited cells)
        for neighbour in grid.get_neighbours(current):
            if neighbour.state == Cell.WALL: continue
            new_distance = current_distance + 1
            if neighbour not in distance or new_distance < distance[neighbour]:
                distance[neighbour] = new_distance
                parent[neighbour] = current
                heapq.heappush(
                    priority_queue,
                    (new_distance, next(counter), neighbour)
                )

    # did not find a path to the target
    if target not in visited: return visited_order, []

    # final path reconstruction
    path = []
    current = target
    while current != start: 
        path.append(current) 
        current = parent[current]

    path.reverse()
    return visited_order, path