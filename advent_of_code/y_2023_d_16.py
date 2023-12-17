from functools import cache
import logging
from typing import Callable


def parse(data: str) -> list[str]:
    return data.splitlines()


add: Callable[[tuple[int, int], tuple[int, int]], tuple[int, int]] = lambda t1, t2: (
    t1[0] + t2[0],
    t1[1] + t2[1],
)
in_range: Callable[[tuple[int, int], tuple[int, int], tuple[int, int]], bool] = (
    lambda t, tmin, tmax: tmin[0] <= t[0] < tmax[0] and tmin[1] <= t[1] < tmax[1]
)


def travel(
    grid: list[str], init_pos: tuple[int, int], init_dir: tuple[int, int]
) -> set[tuple[int, int]]:
    visited = set()
    to_visit = {(init_pos, init_dir)}
    logging.debug(f"starting from {init_pos}, {init_dir}")
    while len(to_visit) > 0:
        pos, dir = to_visit.pop()
        match grid[pos[0]][pos[1]]:
            case "-" if dir[0] != 0:
                reflected = [(0, -1), (0, 1)]
            case "|" if dir[1] != 0:
                reflected = [(-1, 0), (1, 0)]
            case "/":
                reflected = [(-dir[1], -dir[0])]
            case "\\":
                reflected = [(dir[1], dir[0])]
            case _:
                reflected = [dir]
        for d in reflected:
            n = add(pos, d)
            if in_range(n, (0, 0), (len(grid), len(grid[0]))) and (n, d) not in visited:
                to_visit.add((n, d))
        visited.add((pos, dir))
    return {n for n, _ in visited}


def part_a(data: str):
    grid = parse(data)
    visited = travel(grid, (0, 0), (0, 1))
    return len(visited)


def part_b(data: str):
    grid = parse(data)
    configs = [
        ((i, j), d)
        for i, d in [(0, (1, 0)), (len(grid) - 1, (-1, 0))]
        for j in range(len(grid[i]))
    ] + [
        ((i, j), d)
        for i in range(len(grid))
        for j, d in [(0, (0, 1)), (len(grid[i]) - 1, (0, -1))]
    ]
    return max([len(travel(grid, pos, dir)) for pos, dir in configs])
