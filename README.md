# Maze Solving and Pathfinding 2D Visualizer

A Python/Pygame desktop app for creating mazes and watching classic search algorithms explore them. It visualizes visited cells and the route found, records run statistics, and can generate both solvable and unsolvable random mazes.

## Features

- **Pathfinding algorithms:** A*, Dijkstra, breadth-first search (BFS), and depth-first search (DFS).
- **Maze generators:**
  - Recursive Backtracking
  - Randomized Prim
  - Binary Tree
  - **Random (Loops / No Path):** generates random layouts with multiple possible routes, or sometimes walls off the target so a route cannot be found.
- **Map sizes:** 20 × 20, 20 × 30, and 50 × 50.
- **Animated search:** watch exploration and the final path, adjust the animation speed, pause, or skip to the end.
- **Editable grid:** place walls and choose start and target cells.
- **Statistics and rankings:** review runtime, visited cells, path length, and comparisons between algorithms.
- **No-path notification:** if the search exhausts all reachable cells without finding the target, the app displays a notification after the exploration animation finishes.

## Run from Python

### Requirements

- Windows
- Python 3.10 or later
- Pygame (listed in [`foundation project maze/requirements.txt`](./foundation%20project%20maze/requirements.txt))

### Install and launch

Open PowerShell in the repository folder and run:

```powershell
cd "foundation project maze"
py -3 -m pip install -r requirements.txt
py -3 main.py
```

The window opens with a 20 × 30 grid. No start or target is selected initially; use the **Start** and **Target** tools to place them before running a search.

## Using the application

1. Select **Start** or **Target**, then click a grid cell to place the marker.
2. Select **Wall** and click or drag on the grid to add walls. Click **Clear** to clear the visualization and reset the current grid.
3. Choose a search algorithm from the left-hand dropdown.
4. Choose a maze generator from the **Maze** dropdown to replace the current layout. The random generator can produce mazes with multiple routes and, on some generations, no route.
5. Press **Run** to animate the selected search.
6. Use the speed slider, **Pause**, and **Skip** while an animation is running.
7. Change the map size using the **Map** dropdown. This resets the grid.
8. Use the **Stats** and **Ranking** tabs in the right-hand panel to review results. Rankings become available after algorithm runs have been recorded.

The **Clear** button clears the current visualization and statistics shown in the panel; it does not erase the saved CSV history.

## Build the Windows executable

The repository includes a Windows build script at [`foundation project maze/build_exe.bat`](./foundation%20project%20maze/build_exe.bat). It builds a single-windowed executable and bundles the image assets. The Python source remains in the repository; building does not remove or replace it.

From PowerShell:

```powershell
cd "foundation project maze"
py -3 -m pip install -r requirements.txt
py -3 -m pip install pyinstaller
.\build_exe.bat
```

The executable is written to:

```text
foundation project maze\dist\MazeVisualizer.exe
```

Run `MazeVisualizer.exe` directly; Python does not need to be installed on the computer running the executable. The `assets` folder is bundled inside the executable. The build is specific to Windows and to the Python architecture used to create it.

## Files and project layout

The application source and assets are in [`foundation project maze/`](./foundation%20project%20maze/).

| File or folder | Purpose |
| --- | --- |
| `main.py` | Pygame setup, controls, event loop, and application display |
| `grid.py`, `cell.py` | Grid and cell state |
| `Astar.py`, `dijkstra.py`, `bfs.py`, `DFS.py` | Pathfinding implementations |
| `maze_gen.py` | Maze generation algorithms |
| `animation.py`, `ui.py`, `mouse_handler.py` | Search animation, widgets, and grid interaction |
| `assets/` | Cell images bundled with the executable |
| `stats_manager.py`, `stats_history.csv` | Search statistics and saved run history |
| `requirements.txt` | Python runtime dependency |
| `build_exe.bat` | Windows one-file executable build |

## Statistics and generated files

When run from Python, statistics are read from and written to `stats_history.csv` in the current working directory. When run as the packaged executable, statistics are stored in `stats_history.csv` beside `MazeVisualizer.exe`. The CSV is created on first launch if it does not exist.

PyInstaller's intermediate build files are placed in `foundation project maze\build\`; the finished executable is placed in `foundation project maze\dist\`.
