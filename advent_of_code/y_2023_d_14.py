from collections import Counter


def parse(data: str) -> (list[list[int]], set[tuple[int, int]]):
    marbles = set()
    grid = []
    for line in data.splitlines():
        row = []
        for c in line:
            match c:
                case ".":
                    row.append(0)
                case "#":
                    row.append(1)
                case "O":
                    marbles.add((len(grid), len(row)))
                    row.append(0)
        grid.append(row)
    return grid, marbles


add_t = lambda t0, t1: (t0[0] + t1[0], t0[1] + t1[1])
sub_t = lambda t0, t1: (t0[0] - t1[0], t0[1] - t1[1])
in_range = lambda t, tmin, tmax: tmin[0] <= t[0] < tmax[0] and tmin[1] <= t[1] < tmax[1]
mul = lambda s, t: (s * t[0], s * t[1])


# returns final positions of marbles after tilt
def tilt(
    grid: list[list[int]],
    old_marbles: set[tuple[int, int]],
    direction: tuple[int, int] = (-1, 0),
) -> set[tuple[int, int]]:
    to_visit = old_marbles
    roll_to = Counter()

    while len(to_visit) > 0:
        marble = to_visit.pop()
        (i0, j0) = marble
        while in_range(add_t((i0, j0), direction), (0, 0), (len(grid), len(grid[0]))):
            (i0, j0) = add_t((i0, j0), direction)
            tile = grid[i0][j0]
            if tile == 1:
                (i0, j0) = sub_t((i0, j0), direction)  # whups, one too far
                break
        roll_to[(i0, j0)] += 1

    return {
        sub_t(pos, mul(s, direction))
        for (pos, num) in roll_to.items()
        for s in range(num)
    }


def marbles_id(marbles: set[tuple[int, int]]) -> int:
    hs = sorted([hash(t) for t in marbles])
    return hash("|".join([str(h) for h in hs]))


def part_a(data: str):
    grid, marbles = parse(data)
    tilted = tilt(grid, marbles)
    return sum([len(grid) - i for (i, _) in tilted])


def part_b(data: str):
    grid, marbles = parse(data)
    cycles = {}
    cycles[marbles_id(marbles)] = (0, marbles.copy())
    a_big_number = 1000000000
    for t in range(a_big_number):
        marbles = tilt(grid, marbles, (-1, 0))
        marbles = tilt(grid, marbles, (0, -1))
        marbles = tilt(grid, marbles, (1, 0))
        marbles = tilt(grid, marbles, (0, 1))
        id = marbles_id(marbles)
        if id in cycles:
            cycle_start, _ = cycles[id]
            cycle_len = t - cycle_start + 1
            break
        cycles[id] = (t + 1, marbles.copy())
    final_spot = cycle_start + ((a_big_number - cycle_start) % cycle_len)
    marbles = next(marbles for (i, marbles) in cycles.values() if i == final_spot)
    return sum([len(grid) - i for (i, _) in marbles])
