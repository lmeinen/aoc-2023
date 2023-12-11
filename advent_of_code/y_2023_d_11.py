import logging
import numpy as np
from itertools import combinations


def parse(data: str) -> list[tuple[int, int]]:
    return [
        (i, j)
        for i, l in enumerate(data.splitlines())
        for j, c in enumerate(l)
        if c == "#"
    ]


def expand(galaxies: list[tuple[int, int]], galactic: bool) -> list[tuple[int, int]]:
    num_rows = max([g[0] for g in galaxies]) + 1
    num_cols = max([g[1] for g in galaxies]) + 1
    empty_rows = [
        i
        for i in range(num_rows)
        if not any([(i, j) in galaxies for j in range(num_cols)])
    ]
    empty_cols = [
        j
        for j in range(num_cols)
        if not any([(i, j) in galaxies for i in range(num_rows)])
    ]
    return [
        (
            i + len([x for x in empty_rows if x < i]) * (999999 if galactic else 1),
            j + len([y for y in empty_cols if y < j]) * (999999 if galactic else 1),
        )
        for (i, j) in galaxies
    ]


def shortest_paths(galaxies: list[tuple[int, int]]) -> list[int]:
    return [
        abs(g1[0] - g2[0]) + abs(g1[1] - g2[1]) for g1, g2 in combinations(galaxies, 2)
    ]


def part_a(data: str):
    galaxies = parse(data)
    galaxies = expand(galaxies, galactic=False)
    return sum(shortest_paths(galaxies))


def part_b(data: str):
    logging.debug("")
    galaxies = parse(data)
    galaxies = expand(galaxies, galactic=True)
    return sum(shortest_paths(galaxies))
