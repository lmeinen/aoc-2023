import logging


def solve(data: str, is_b: bool):
    dumbos = []
    for line in data.splitlines():
        row = []
        for d in line:
            row.append(int(d))
        dumbos.append(row)

    logging.debug("")
    logging.debug("initial state")
    logging.debug(pretty(dumbos))
    flashes = 0
    t = 0
    while True:
        t += 1
        logging.debug(f"===== t {t} =====")
        flashed = []
        for i in range(len(dumbos)):
            for j in range(len(dumbos[i])):
                dumbos, flashed, s = flash(dumbos, flashed, i, j)
                flashes += s
        logging.debug(pretty(dumbos))
        logging.debug(f"{len(flashed)} new flashes")
        logging.debug(f"{flashes} flashes total")
        if is_b and len(flashed) == 100:
            return t
        elif not is_b and t == 100:
            return flashes


def part_a(data: str):
    return solve(data, False)


def part_b(data: str):
    return solve(data, True)


def pretty(dumbos: list[list[int]]) -> str:
    s = ""
    for i in range(len(dumbos)):
        s += ",".join(map(lambda x: str(x), dumbos[i])) + "\n"
    return s


def flash(
    dumbos: list[list[int]], flashed: list[(int, int)], i: int, j: int
) -> tuple[list[list[int]], list[(int, int)], int]:
    flashes = 0
    if (i, j) not in flashed:
        dumbos[i][j] += 1
        if dumbos[i][j] == 10:
            flashes = 1
            flashed.append((i, j))
            dumbos[i][j] = 0
            for x, y in [
                (u, v)
                for u in [i - 1, i, i + 1]
                for v in [j - 1, j, j + 1]
                if 0 <= u
                and u < len(dumbos)
                and 0 <= v
                and v < len(dumbos[u])
                and (u, v) != (i, j)
            ]:
                dumbos, flashed, s = flash(dumbos, flashed, x, y)
                flashes += s
    return dumbos, flashed, flashes
