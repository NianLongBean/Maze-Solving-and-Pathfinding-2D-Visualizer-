def get_path_coordinates(path):
    coordinates = []

    for cell in path:
        x = cell.col
        y = cell.row
        coordinates.append((x, y))

    return coordinates