import logging
from typing import Optional


def parse(data: str) -> list[list[list[bool]]]:
    return [
        [[tile == "#" for tile in row] for row in grid.splitlines()]
        for grid in data.split("\n\n")
    ]


def solve(
    grid: list[list[bool]], possible_reflections: set[tuple[str, int]]
) -> Optional[tuple[str, int]]:
    num_rows = len(grid)
    num_cols = len(grid[0])
    for i in range(num_rows):
        for j in range(num_cols):
            remaining = set()
            for axis, mirror in possible_reflections:
                i0 = 2 * mirror - i - 1 if axis == "hor" else i
                j0 = 2 * mirror - j - 1 if axis == "ver" else j
                if (
                    axis == "hor"
                    and (mirror <= i or num_rows <= i0 or grid[i][j] == grid[i0][j0])
                ) or (
                    axis == "ver"
                    and (mirror <= j or num_cols <= j0 or grid[i][j] == grid[i0][j0])
                ):
                    remaining.add((axis, mirror))
            possible_reflections = remaining

    if len(possible_reflections) == 1:
        return possible_reflections.pop()
    elif len(possible_reflections) == 0:
        return None
    else:
        raise AssertionError("multiple reflections remaining")


def part_a(data: str):
    grids = parse(data)
    s = 0
    for grid in grids:
        possible_reflections = {("hor", i) for i in range(1, len(grid))} | {
            ("ver", j) for j in range(1, len(grid[0]))
        }
        axis, val = solve(grid, possible_reflections)
        s += val * 100 if axis == "hor" else val
    return s


def part_b(data: str):
    grids = parse(data)
    s = 0
    for grid in grids:
        possible_reflections = {("hor", i) for i in range(1, len(grid))} | {
            ("ver", j) for j in range(1, len(grid[0]))
        }
        original = solve(grid, possible_reflections)
        possible_reflections.remove(original)
        smudged = None
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                grid[i][j] = not grid[i][j]
                res = solve(grid, possible_reflections)
                grid[i][j] = not grid[i][j]
                if res is not None:
                    smudged = res
        s += smudged[1] * 100 if smudged[0] == "hor" else smudged[1]
    return s
