import json
import logging
import re
from itertools import product, tee


def parse(data: str, mini_races: bool) -> list[tuple[int, int]]:
    [ts, rs] = data.splitlines()
    times = [
        t for t in re.match(r"^Time:\s+(?P<times>[\d\s]+)$", ts).group("times").split()
    ]
    records = [
        d
        for d in re.match(r"^Distance:\s+(?P<records>[\d\s]+)$", rs)
        .group("records")
        .split()
    ]
    if not mini_races:
        times = ["".join(times)]
        records = ["".join(records)]
    return list(zip([int(t) for t in times], [int(d) for d in records], strict=True))


def solve(races):
    p = 1
    for t, d in races:
        start, end = None, None

        hold_time = 1
        while start is None:
            if (t - hold_time) * hold_time > d:
                start = hold_time
            hold_time += 1

        hold_time = t - 1
        while end is None:
            if (t - hold_time) * hold_time > d:
                end = hold_time + 1
            hold_time -= 1
        p *= end - start
    return p


def part_a(data: str):
    logging.debug("")
    races = parse(data, True)
    return solve(races)


def part_b(data: str):
    logging.debug("")
    races = parse(data, False)
    return solve(races)
