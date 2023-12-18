import logging
import re
from typing import Callable
from shapely import Polygon, area

add: Callable[[tuple[int, int], tuple[int, int]], tuple[int, int]] = lambda t1, t2: (
    t1[0] + t2[0],
    t1[1] + t2[1],
)

mul: Callable[[int, tuple[int, int]], tuple[int, int]] = lambda s, t: (
    s * t[0],
    s * t[1],
)


def turn(corner: tuple[int, int], travelling: str, turning_to: str) -> int:
    match turning_to:
        case "U" if travelling == "L":
            return (0, 1) if corner[0] == 0 else (1, 0)
        case "U" if travelling == "R":
            return (0, 0) if corner[0] == 0 else (1, 1)
        case "R" if travelling == "U":
            return (0, 0) if corner[1] == 0 else (1, 1)
        case "R" if travelling == "D":
            return (1, 0) if corner[1] == 0 else (0, 1)
        case "D" if travelling == "R":
            return (0, 1) if corner[0] == 0 else (1, 0)
        case "D" if travelling == "L":
            return (0, 0) if corner[0] == 0 else (1, 1)
        case "L" if travelling == "D":
            return (0, 0) if corner[1] == 0 else (1, 1)
        case "L" if travelling == "U":
            return (1, 0) if corner[1] == 0 else (0, 1)


def parse(data: str) -> list[tuple[str, int, tuple[str, int]]]:
    matches = [
        re.match(
            r"^(?P<direction>[URDL]) (?P<distance>\d+) \(#(?P<hex_len>[\da-z]{5})(?P<hex_dir>[0-3])\)$",
            l,
        )
        for l in data.splitlines()
    ]
    return [
        (
            m.group("direction"),
            int(m.group("distance")),
            (
                ["R", "D", "L", "U"][int(m.group("hex_dir"))],
                int(m.group("hex_len"), base=16),
            ),
        )
        for m in matches
    ]


def area(directions):
    orientations = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}
    area = 0
    square = (0, 0)
    corner = (0, 0)
    for i, (direction, dist) in enumerate(directions):
        prev = add(square, corner)
        square = add(square, mul(dist, orientations[direction]))
        turn_to = directions[(i + 1) % len(directions)][0]
        corner = turn(corner, direction, turn_to)
        pos = add(square, corner)
        area += prev[0] * pos[1] - prev[1] * pos[0]  # shoelace formula
    return abs(area) // 2


def part_a(data: str):
    directions = parse(data)
    directions = [(d0, d1) for d0, d1, _ in directions]
    return area(directions)


def part_b(data: str):
    directions = parse(data)
    directions = [(d2, d3) for _, _, (d2, d3) in directions]
    return area(directions)
