from functools import cache
import json
import logging
import re

paths: dict[str, list[str]] = dict()


def parse(data: str):
    paths.clear()
    path_re = r"([a-zA-Z]+)-([a-zA-Z]+)"
    for line in data.splitlines():
        logging.debug(f"parsing line {line}")
        path_match = re.match(path_re, line)
        a = path_match.group(1)
        b = path_match.group(2)
        for f, t in [(a, b), (b, a)]:
            if t != "start" and f != "end":
                logging.debug(f"adding path {f}-{t}")
                if f in paths:
                    paths[f].append(t)
                else:
                    paths[f] = [t]


@cache
def visit(curr: str, visit_twice: bool, visited: tuple[str]) -> int:
    logging.debug(f"visiting {curr}")
    if curr in visited and not visit_twice:
        return 0
    elif curr == "end":
        return 1
    else:
        if all(c.islower() for c in curr):
            if curr in visited:
                logging.debug(f"visiting {curr} a second time")
                visit_twice = False
            else:
                logging.debug(f"adding {curr} to visited")
                visited = tuple(sorted([curr, *visited]))
        return sum([visit(next, visit_twice, visited) for next in paths[curr]])


def part_a(data: str):
    logging.debug("")
    parse(data)
    visit.cache_clear()
    return visit("start", False, tuple())


def part_b(data: str):
    logging.debug("")
    parse(data)
    visit.cache_clear()
    return visit("start", True, tuple())
