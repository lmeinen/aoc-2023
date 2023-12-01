import regex as re
from functools import cache
from typing import Callable


def solve(data: str, pre: Callable[[str], str]):
    val = 0
    for line in data.splitlines():
        digits = re.findall(r"\d", pre(line))
        val += int(digits[0]) * 10 + int(digits[-1])
    return val


def part_a(data: str):
    return solve(data, lambda s: s)


def part_b(data: str):
    m = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    p = "|".join("({})".format(key) for key, _ in m.items())

    def pre(s: str) -> str:
        matches = re.finditer(p, s, overlapped=True)
        r = ""
        idx = 0
        for match in matches:
            r += s[idx : match.start()] + m[match.group(0)]
            idx = match.end()
        r += s[idx:]
        return r

    return solve(
        data,
        pre,
    )
