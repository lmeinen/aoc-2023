import json
import logging
import re
from itertools import product, tee


def parse(
    data: str,
) -> (list[int], list[list[tuple[int, int, int]]]):
    seeds = []
    maps = []
    re_seeds = r"^seeds: ([\s\d]+)$"
    re_map = r"^[a-z]+-to-[a-z]+ map:"
    for line in data.splitlines():
        if m := re.match(re_seeds, line):
            seeds = [int(s) for s in m.group(1).split(" ")]
        elif re.match(re_map, line):
            maps.append([])
        elif line != "":
            [dst, src, len] = map(lambda s: int(s), line.split(" "))
            maps[-1].append((dst, src, len))
    return seeds, maps


def part_a(data: str):
    seeds, maps = parse(data)
    for m in maps:
        for idx, s in enumerate(seeds):
            for dst, src, len in m:
                if src <= s < src + len:
                    seeds[idx] = dst + s - src
    return min(seeds)


def part_b(data: str):
    seeds, maps = parse(data)
    ranges = list(zip(*([iter(seeds)] * 2)))
    for m in maps:
        handled_ranges = []
        for dst, src, l1 in m:
            unhandled_ranges = []
            for start, l2 in ranges:
                if src < start + l2 and start < src + l1:
                    o_start = max(src, start)  # inclusive
                    o_end = min(src + l1, start + l2)  # exclusive
                    overlap = (o_start, o_end - o_start)
                    handled_ranges.append((dst + overlap[0] - src, overlap[1]))
                    if overlap[0] - start > 0:
                        unhandled_ranges.append((start, overlap[0] - start))
                    if o_end < start + l2:
                        unhandled_ranges.append(
                            (
                                o_end,
                                start + l2 - (o_end),
                            )
                        )
                else:
                    unhandled_ranges.append((start, l2))
            ranges = unhandled_ranges
        ranges = handled_ranges + unhandled_ranges
    return min([r[0] for r in ranges])
