from functools import cache
import json
import logging
import re
import string


def parse(data: str) -> (dict[tuple[str, str], int], dict[tuple[str, str], str]):
    lines = data.splitlines()
    template_elements = list(lines[0])
    template = {
        (a, b): 0 for a in string.ascii_uppercase for b in string.ascii_uppercase
    }
    padding = {("Q", template_elements[0]): 1, (template_elements[-1], "Q"): 1}
    for a, b in zip(template_elements, template_elements[1:]):
        template[(a, b)] += 1

    rules = {}
    for line in lines[2:]:
        m = re.match(r"^(?P<old>[A-Z]{2}) -> (?P<new>[A-Z])$", line)
        rules[(m.group("old")[0], m.group("old")[1])] = m.group("new")
    return template | padding, rules


def solve(polymer, rules, steps=10):
    for _ in range(steps):
        new_polymer = {
            (a, b): 0 for a in string.ascii_uppercase for b in string.ascii_uppercase
        }
        for (a, b), num in polymer.items():
            if (a, b) in rules:
                new_polymer[(a, rules[(a, b)])] += num
                new_polymer[(rules[(a, b)], b)] += num
            else:
                new_polymer[(a, b)] = num
        polymer = new_polymer

    elements = {e: 0 for e in string.ascii_uppercase}
    for (a, b), num in polymer.items():
        elements[a] += num
        elements[b] += num
    elements = {k: v / 2 for k, v in elements.items() if v > 0 and k != "Q"}
    vals = list(elements.values())
    return int(max(vals) - min(vals))


def part_a(data: str):
    polymer, rules = parse(data)
    return solve(polymer, rules)


def part_b(data: str):
    polymer, rules = parse(data)
    return solve(polymer, rules, steps=40)
