from functools import cache
import logging
import re
import string


def parse(data: str) -> (dict[str, int], dict[str, str]):
    lines = data.splitlines()
    template_elements = list(lines[0])
    template = {
        (a, b): 0 for a in string.ascii_uppercase for b in string.ascii_uppercase
    }
    for a, b in zip(template_elements, template_elements[1:]):
        s = a + b
        template[s] += 1
    rules = {}
    for line in lines[2:]:
        m = re.match(r"^(?P<old>[A-Z]{2}) -> (?P<new>[A-Z])$", line)
        rules[m.group("old")] = m.group("new")
    return template, rules


def part_a(data: str):
    logging.debug("")
    polymer, rules = parse(data)
    logging.debug(f"parsed: {polymer}")
    logging.debug(f"parsed: {rules}")
    for t in range(10):
        logging.debug(f"polymer at step {t}: {polymer}")
        additions = dict(polymer)
        for p, num in polymer.items():
            if p in rules:
                [a, b] = p.split("")
                additions[a + rules[p]] += num
                additions[rules[p] + b] += num
        polymer = additions

    elements = {e: 0 for e in string.ascii_uppercase}
    for pair, num in polymer.items():
        for a in pair.split(""):
            elements[a] += num

    return max(elements, key=elements.get) - min(elements, key=elements.get)


def part_b(data: str):
    logging.debug("")
    return 0
