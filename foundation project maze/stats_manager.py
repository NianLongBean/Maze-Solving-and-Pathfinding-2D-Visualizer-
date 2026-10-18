import hashlib
import csv
import os
from datetime import datetime


class StatsManager:
    def __init__(self, csv_file="stats_history.csv"):
        self.csv_file = csv_file
        self.history = []

        # Create the CSV file with headers if it does not exist.
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "run_id",
                        "timestamp",
                        "maze_id",
                        "algorithm",
                        "runtime_ms",
                        "visited_count",
                        "path_length",
                        "found_path",
                    ],
                )
                writer.writeheader()
        else:
            with open(self.csv_file, "r", newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    row["run_id"] = int(row["run_id"])
                    row["runtime_ms"] = float(row["runtime_ms"])
                    row["visited_count"] = int(row["visited_count"])
                    row["path_length"] = int(row["path_length"])
                    row["found_path"] = row["found_path"].lower() == "true"

                    self.history.append(row)

    def record(self, stats, maze_id="maze_001"):
        """Save one algorithm run to memory and CSV."""
        record = {
            "run_id": len(self.history) + 1,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "maze_id": maze_id,
            "algorithm": stats["algorithm"],
            "runtime_ms": stats["runtime_ms"],
            "visited_count": stats["visited_count"],
            "path_length": stats["path_length"],
            "found_path": stats.get("found_path", stats["path_length"] > 0),
        }

        self.history.append(record)

        with open(self.csv_file, "a", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=record.keys())
            writer.writerow(record)

        return record

    def get_history(self, algorithm=None, maze_id=None):
        """Return all records, optionally filtered."""
        records = self.history

        if algorithm is not None:
            records = [
                item for item in records
                if item["algorithm"] == algorithm
            ]

        if maze_id is not None:
            records = [
                item for item in records
                if item["maze_id"] == maze_id
            ]

        return list(records)

    def get_average(self, algorithm, maze_id=None):
        """Calculate averages for successful runs of an algorithm."""
        records = [
            item for item in self.get_history(algorithm, maze_id)
            if item["found_path"]
        ]

        if not records:
            return None

        count = len(records)

        return {
            "algorithm": algorithm,
            "runs": count,
            "avg_runtime_ms": sum(
                item["runtime_ms"] for item in records
            ) / count,
            "avg_visited_count": sum(
                item["visited_count"] for item in records
            ) / count,
            "avg_path_length": sum(
                item["path_length"] for item in records
            ) / count,
        }

    def generate_maze_id(self, grid, start, target):
        """Generate an ID from the maze layout and endpoints."""

        layout = []

        for row in range(grid.rows):
            row_data = []

            for col in range(grid.cols):
                cell = grid.get_cell(row, col)
                row_data.append("1" if cell.state == 1 else "0")

            layout.append("".join(row_data))

        maze_data = (
            f"{grid.rows}x{grid.cols}|"
            + "|".join(layout)
            + f"|S:{start.row},{start.col}"
            + f"|T:{target.row},{target.col}"
        )

        return hashlib.sha256(
            maze_data.encode("utf-8")
        ).hexdigest()[:12]

    def compare_algorithms(self, maze_id):
        """Compare algorithms tested on the same maze."""

        records = self.get_history(maze_id=maze_id)

        if not records:
            return []

        algorithms = sorted(set(
            item["algorithm"] for item in records
        ))

        comparison = []

        for algorithm in algorithms:
            runs = [
                item for item in records
                if item["algorithm"] == algorithm
            ]

            successful_runs = [
                item for item in runs
                if item["found_path"]
            ]

            total_runs = len(runs)
            success_count = len(successful_runs)

            result = {
                "algorithm": algorithm,
                "total_runs": total_runs,
                "success_rate": (
                    success_count / total_runs * 100
                ),
                "avg_runtime_ms": (
                    sum(item["runtime_ms"] for item in runs)
                    / total_runs
                ),
                "avg_visited_count": (
                    sum(item["visited_count"] for item in runs)
                    / total_runs
                ),
                "avg_path_length": (
                    sum(item["path_length"] for item in successful_runs)
                    / success_count
                    if success_count > 0 else None
                ),
            }

            comparison.append(result)

        return comparison