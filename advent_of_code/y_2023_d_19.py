from math import prod
import re


def parse_cond(c: str) -> (tuple[str, int, int], str):
    m = re.match(
        r"(?:(?P<cat>[xmas])(?P<op>[<>])(?P<val>\d+):)?(?P<target>[a-zAR]+)", c
    )
    if (op := m.group("op")) is not None:
        category = m.group("cat")
        value = int(m.group("val"))
        if op == ">":
            condition = (category, value + 1, 4000)
        else:
            condition = (category, 1, value - 1)
    else:
        condition = ("x", 1, 4000)
    return condition, m.group("target")


def parse(
    data: str,
) -> (dict[str, list[tuple[tuple[str, int, int], str]]], list[dict[str, int]],):
    [workflows, parts] = data.split("\n\n")
    return {
        m.group("id"): [parse_cond(c) for c in m.group("rules").split(",")]
        for m in [
            re.match(r"^(?P<id>[a-z]+)\{(?P<rules>\S+)\}$", w)
            for w in workflows.splitlines()
        ]
    }, [
        {
            m.group("cat"): int(m.group("val"))
            for m in re.finditer(r"(?P<cat>[xmas])=(?P<val>\d+)", p)
        }
        for p in parts.splitlines()
    ]


def rating(part: dict[str, int], paths: list[dict[str, tuple[int, int]]]) -> int:
    return (
        sum(part.values())
        if any(
            [
                all([path[c][0] <= v <= path[c][1] for c, v in part.items()])
                for path in paths
            ]
        )
        else 0
    )


def collapse(cons: list[tuple[str, int, int]]) -> dict[str, tuple[int, int]]:
    brief = {c: (1, 4000) for c in ["x", "m", "a", "s"]}
    for k, low, high in cons:
        max_low, min_high = brief[k]
        brief[k] = (max(max_low, low), min(min_high, high))
    return brief


def find_paths(
    workflows: dict[str, list[tuple[tuple[str, int, int], str]]]
) -> list[dict[str, tuple[int, int]]]:
    paths = []
    to_visit = [("in", [])]  # current workflow, set of collected constraints
    while len(to_visit) > 0:  # DFS for 'A' paths
        (curr, cs) = to_visit.pop()
        w = workflows[curr]
        for (k, low, high), next in w:
            constraints_and = cs + [(k, low, high)]
            if next == "A":
                paths.append(collapse(constraints_and))
            elif next != "R":
                to_visit.append((next, constraints_and))
            # add complement of rule
            cs = cs + [(k, high + 1, 4000) if high < 4000 else (k, 1, low - 1)]
    return paths


def part_a(data: str):
    workflows, parts = parse(data)
    paths = find_paths(workflows)
    return sum([rating(p, paths) for p in parts])


def part_b(data: str):
    workflows, _ = parse(data)
    paths = find_paths(workflows)
    return sum(
        [prod([max(0, high - low + 1) for (low, high) in p.values()]) for p in paths]
    )
