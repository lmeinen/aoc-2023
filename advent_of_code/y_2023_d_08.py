import logging
import re
from math import lcm


def parse(data: str) -> (list[int], dict[str, tuple[str, str]]):
    lines = data.splitlines()
    return [0 if instr == "L" else 1 for instr in lines[0]], {
        m.group("node"): (m.group("node_l"), m.group("node_r"))
        for m in [
            re.match(
                r"^(?P<node>[A-Z]+) = \((?P<node_l>[A-Z]+), (?P<node_r>[A-Z]+)\)$", l
            )
            for l in lines[2:]
        ]
    }


def part_a(data: str):
    path, network = parse(data)
    curr_node = "AAA"
    curr_instr = 0
    num_steps = 0
    while curr_node != "ZZZ":
        curr_node = network[curr_node][path[curr_instr]]
        curr_instr = (curr_instr + 1) % len(path)
        num_steps += 1
    return num_steps


def part_b(data: str):
    logging.debug("")
    path, network = parse(data)
    curr_nodes = {n for n in network.keys() if n[-1] == "A"}
    cycles = []
    for curr_node in curr_nodes:
        # simplifying assumptions made in data: XXA -- S steps -- repeat(XXZ -- S steps -- XXZ)
        curr_instr = 0
        cycle_len = 0
        while curr_node[-1] != "Z":
            curr_node = network[curr_node][path[curr_instr]]
            curr_instr = (curr_instr + 1) % len(path)
            cycle_len += 1
        cycles.append(cycle_len)
    return lcm(*cycles)
