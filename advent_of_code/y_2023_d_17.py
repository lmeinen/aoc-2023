import logging
from typing import Callable

add: Callable[[tuple[int, int], tuple[int, int]], tuple[int, int]] = lambda t1, t2: (
    t1[0] + t2[0],
    t1[1] + t2[1],
)

mul: Callable[[int, tuple[int, int]], tuple[int, int]] = lambda s, t: (
    s * t[0],
    s * t[1],
)

in_range: Callable[[tuple[int, int], tuple[int, int], tuple[int, int]], bool] = (
    lambda t, tmin, tmax: tmin[0] <= t[0] < tmax[0] and tmin[1] <= t[1] < tmax[1]
)


def parse(data: str) -> list[list[int]]:
    return [[int(t) for t in l] for l in data.splitlines()]


def sum_tuple_range(grid, t1, t2) -> int:
    step_i = 1 if t1[0] < t2[0] else -1
    step_j = 1 if t1[1] < t2[1] else -1
    return sum(
        [
            grid[i][j]
            for i in range(t1[0], t2[0] + step_i, step_i)
            for j in range(t1[1], t2[1] + step_j, step_j)
        ]
    )


def min_path(grid: list[list[int]], ultra: bool) -> int:
    num_rows = len(grid)
    num_cols = len(grid[0])
    path_lens = {}  # (node, direction_of_entry) -> len
    to_visit = {((0, 0), (1, 0)): 0, ((0, 0), (0, 1)): 0}
    while len(to_visit) > 0:
        curr, direction = min(to_visit, key=to_visit.get)
        dist = to_visit.pop((curr, direction))
        path_lens[(curr, direction)] = dist
        swerve = (direction[1], direction[0])
        start, end = (4, 10) if ultra else (1, 3)
        distances = [m * s for m in range(start, end + 1) for s in [-1, 1]]
        for n in [add(curr, mul(s, swerve)) for s in distances]:
            if (
                in_range(n, (0, 0), (num_rows, num_cols))
                and (n, swerve) not in path_lens
            ):
                new_dist = (
                    dist + sum_tuple_range(grid, curr, n) - grid[curr[0]][curr[1]]
                )
                if (n, swerve) not in to_visit or new_dist < to_visit[(n, swerve)]:
                    to_visit[(n, swerve)] = new_dist
    return min(
        [d for (n, _), d in path_lens.items() if n == (num_rows - 1, num_cols - 1)]
    )


def part_a(data: str):
    grid = parse(data)
    return min_path(grid, False)


def part_b(data: str):
    grid = parse(data)
    return min_path(grid, True)
