import logging
import re
from itertools import product


def parse(
    data: str,
) -> (list[tuple[int, int, str]], set[tuple[int, int]], set[tuple[int, int]]):
    logging.debug(f"parsing data\n{data}")
    ids = []
    symbols = set()
    gears = set()
    re_p = r"(?P<symbol>[^\d\.\s])|(?P<num>\d+)"
    for row, line in enumerate(data.splitlines()):
        for m in re.finditer(re_p, line):
            if "symbol" == m.lastgroup:
                logging.debug(f"found symbol at index {m.start()}")
                symbols.add((row, m.start()))
                if m.group("symbol") == "*":
                    gears.add((row, m.start()))
            else:
                logging.debug(f"found num {m.group('num')} at index {m.start()}")
                ids.append((row, m.start(), m.group("num")))
    logging.debug(f"parsed ids [len {len(ids)}]: {ids}")
    logging.debug(f"parsed symbols [len {len(symbols)}]: {symbols}")
    return ids, symbols, gears


def part_a(data: str):
    logging.debug("")
    ids, symbols, _ = parse(data)
    return sum(
        [
            int(val)
            for (row, col, val) in ids
            if any(
                (i, j) in symbols
                for (i, j) in product(
                    [row - 1, row, row + 1],
                    range(col - 1, col + len(val) + 1),
                )
            )
        ]
    )


def part_b(data: str):
    logging.debug("")
    ids, _, stars = parse(data)
    gears = {star: [] for star in stars}
    for row, col, val in ids:
        for i, j in product(
            [row - 1, row, row + 1],
            range(col - 1, col + len(val) + 1),
        ):
            if (i, j) in gears:
                vals = gears[(i, j)]
                if len(vals) < 2:
                    vals.append(int(val))
                    gears[(i, j)] = vals
                else:
                    del gears[(i, j)]
    return sum([l[0] * l[1] for _, l in gears.items() if len(l) == 2])
