import logging
import numpy as np


def parse(data: str):
    return np.array([[t for t in l] for l in data.splitlines()])


tiles = {
    "|": [(1, 0), (-1, 0)],
    "-": [(0, 1), (0, -1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(0, -1), (1, 0)],
    "F": [(1, 0), (0, 1)],
    ".": [],
}


ident = lambda t: t
neg = lambda t: (-t[0], -t[1])
add = lambda t1, t2: (t1[0] + t2[0], t1[1] + t2[1])
in_range = (
    lambda t, min, max: min[0] <= t[0]
    and min[1] <= t[1]
    and t[0] < max[0]
    and t[1] < max[1]
)

rotations = {
    "|": lambda t: t,
    "-": lambda t: t,
    "L": lambda t: (0, 1) if t == (1, 0) else (-1, 0),
    "J": lambda t: (0, -1) if t == (1, 0) else (-1, 0),
    "7": lambda t: (1, 0) if t == (0, 1) else (0, -1),
    "F": lambda t: (0, 1) if t == (-1, 0) else (1, 0),
}


def loop(grid) -> list[tuple[int, int]]:
    prev_pos = None
    pos = tuple(np.argwhere(grid == "S")[0])
    loop = []
    while (t := grid[pos]) != "S" or prev_pos is None:
        tmp = pos
        if t == "S":
            for neigbour in [add(pos, d) for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]]:
                neighbour_dirs = tiles[grid[neigbour]]
                if pos == add(neigbour, neighbour_dirs[0]) or pos == add(
                    neigbour, neighbour_dirs[1]
                ):
                    pos = neigbour
                    break
        elif prev_pos == add(pos, tiles[t][0]):
            pos = add(pos, tiles[t][1])
        else:
            pos = add(pos, tiles[t][0])
        prev_pos = tmp
        loop.append(tuple(prev_pos))
    return loop


def part_a(data: str):
    grid = parse(data)
    return len(loop(grid)) // 2


def visit(
    loop: list[tuple[int, int]],
    interior: set[tuple[int, int]],
    curr: tuple[int, int],
    walking_dir: tuple[int, int],
) -> set[tuple[int, int]]:
    logging.debug(f"checking interior from node {curr} walking in dir {walking_dir}")
    start_node = add(curr, (walking_dir[1], -walking_dir[0]))
    to_visit = (
        {start_node} if start_node not in loop and start_node not in interior else set()
    )
    visited = set()
    while len(to_visit) > 0:
        n = to_visit.pop()
        for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neigh = add(n, d)
            if neigh not in loop and neigh not in to_visit and neigh not in visited:
                to_visit.add(neigh)
        visited.add(n)
    if len(visited) > 0:
        logging.debug(f"newly discovered interior: {visited}")
    return interior | visited


def part_b(data: str):
    grid = parse(data)
    l = loop(grid)
    s_idx = l[0]
    s_neighs = {l[-1], l[1]}
    for tile, dirs in tiles.items():
        if (
            tile != "."
            and add(s_idx, dirs[0]) in s_neighs
            and add(s_idx, dirs[1]) in s_neighs
        ):
            grid[s_idx] = tile
    interior = set()
    top_left = min(l)
    curr = add(top_left, (0, 1))
    walking_dir = (0, 1)
    # walk loop in clockwise direction remembering which side is in
    while curr != top_left:
        interior = visit(l, interior, curr, walking_dir)
        walking_dir = rotations[grid[curr]](walking_dir)
        interior = visit(l, interior, curr, walking_dir)
        curr = add(curr, walking_dir)
    return len(interior)
