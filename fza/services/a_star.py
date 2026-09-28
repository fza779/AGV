from heapq import heappop, heappush
from math import inf, sqrt
from typing import Dict, List, Optional, Sequence, Tuple


Point = Tuple[int, int]


def a_star(
    grid: Sequence[Sequence[int]],
    start: Sequence[int],
    goal: Sequence[int],
    allow_diagonal: bool = False,
) -> Dict[str, object]:
    """Find a shortest path on a grid where non-zero cells are obstacles."""
    if not grid or not grid[0]:
        return _failure("Grid is empty")

    rows = len(grid)
    cols = len(grid[0])
    if any(len(row) != cols for row in grid):
        return _failure("Grid rows have different lengths")

    start_point = _to_point(start)
    goal_point = _to_point(goal)

    if not _inside(start_point, rows, cols):
        return _failure("Start is outside the grid")
    if not _inside(goal_point, rows, cols):
        return _failure("Goal is outside the grid")
    if _is_blocked(grid, start_point):
        return _failure("Start is an obstacle")
    if _is_blocked(grid, goal_point):
        return _failure("Goal is an obstacle")
    if start_point == goal_point:
        return {
            "success": True,
            "path": [list(start_point)],
            "cost": 0.0,
            "visited_count": 1,
            "message": "Start and goal are the same cell",
        }

    directions = [
        (-1, 0, 1.0),
        (1, 0, 1.0),
        (0, -1, 1.0),
        (0, 1, 1.0),
    ]
    if allow_diagonal:
        diagonal_cost = sqrt(2.0)
        directions.extend(
            [
                (-1, -1, diagonal_cost),
                (-1, 1, diagonal_cost),
                (1, -1, diagonal_cost),
                (1, 1, diagonal_cost),
            ]
        )

    open_heap: List[Tuple[float, float, Point]] = []
    heappush(open_heap, (_heuristic(start_point, goal_point), 0.0, start_point))

    g_score: Dict[Point, float] = {start_point: 0.0}
    parent: Dict[Point, Point] = {}
    closed = set()
    visited_count = 0

    while open_heap:
        _, current_cost, current = heappop(open_heap)
        if current in closed:
            continue

        closed.add(current)
        visited_count += 1

        if current == goal_point:
            path = _build_path(parent, start_point, goal_point)
            return {
                "success": True,
                "path": [list(point) for point in path],
                "cost": round(current_cost, 6),
                "visited_count": visited_count,
                "message": "Path found",
            }

        row, col = current
        for row_offset, col_offset, move_cost in directions:
            neighbor = (row + row_offset, col + col_offset)
            if not _inside(neighbor, rows, cols):
                continue
            if _is_blocked(grid, neighbor):
                continue

            # Prevent diagonal movement through the corner of an obstacle.
            if row_offset != 0 and col_offset != 0:
                side_one = (row + row_offset, col)
                side_two = (row, col + col_offset)
                if _is_blocked(grid, side_one) or _is_blocked(grid, side_two):
                    continue

            tentative_cost = current_cost + move_cost
            if tentative_cost >= g_score.get(neighbor, inf):
                continue

            parent[neighbor] = current
            g_score[neighbor] = tentative_cost
            priority = tentative_cost + _heuristic(neighbor, goal_point)
            heappush(open_heap, (priority, tentative_cost, neighbor))

    return {
        "success": False,
        "path": [],
        "cost": None,
        "visited_count": visited_count,
        "message": "No path found",
    }


def _to_point(value: Sequence[int]) -> Point:
    if len(value) != 2:
        raise ValueError("A point must contain exactly two coordinates")
    return int(value[0]), int(value[1])


def _inside(point: Point, rows: int, cols: int) -> bool:
    row, col = point
    return 0 <= row < rows and 0 <= col < cols


def _is_blocked(grid: Sequence[Sequence[int]], point: Point) -> bool:
    row, col = point
    return grid[row][col] != 0


def _heuristic(point: Point, goal: Point) -> float:
    return float(abs(point[0] - goal[0]) + abs(point[1] - goal[1]))


def _build_path(
    parent: Dict[Point, Point],
    start: Point,
    goal: Point,
) -> List[Point]:
    path: List[Point] = [goal]
    current = goal
    while current != start:
        current = parent[current]
        path.append(current)
    path.reverse()
    return path


def _failure(message: str) -> Dict[str, Optional[object]]:
    return {
        "success": False,
        "path": [],
        "cost": None,
        "visited_count": 0,
        "message": message,
    }
