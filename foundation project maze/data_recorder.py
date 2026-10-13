
from time import perf_counter


def calculate_path_length(path, start, target):
    if not path:
        return 0
    
    path_length = len(path)
    if path[0] != start:
        path_length += 0
    else:
        path_length -= 1
    if path[-1] != target:
        path_length += 1
    return path_length

def run_and_record(name, algorithm, *args, start, target):
    #execution time 
    start_time = perf_counter()
    visited_order, path = algorithm(*args)
    end_time = perf_counter()
    runtime_ms = (end_time - start_time) * 1000

    #record explored cells
    visited_count = len(visited_order)

    # recỏd moves in the path
    path_length = calculate_path_length(path, start, target)

    stats = {
        "algorithm": name,
        "runtime_ms": round(runtime_ms, 3),
        "visited_count": visited_count,
        "path_length": path_length
    }

    return visited_order, path, stats
