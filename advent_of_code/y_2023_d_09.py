import logging
import re
from math import lcm


def parse(data: str) -> list[list[int]]:
    return [[int(x) for x in l.split()] for l in data.splitlines()]


def diff(seq: list[int]) -> list[int]:
    return [v2 - v1 for v1, v2 in zip(seq, seq[1:])]


def solve(sequences: list[int]) -> (int, int):
    backward = 0
    forward = 0
    for seq in sequences:
        diffs = [diff(seq)]
        while not all([d == 0 for d in diffs[-1]]):
            diffs.append(diff(diffs[-1]))
        prev_value = 0
        next_value = 0
        while d := diffs.pop() if len(diffs) > 0 else None:
            prev_value = d[0] - prev_value
            next_value = d[-1] + next_value
        backward += seq[0] - prev_value
        forward += seq[-1] + next_value
    return forward, backward


def part_a(data: str):
    sequences = parse(data)
    forward, _ = solve(sequences)
    return forward


def part_b(data: str):
    sequences = parse(data)
    _, backward = solve(sequences)
    return backward
