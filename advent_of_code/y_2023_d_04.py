import logging
import re
from itertools import product


def parse(
    data: str,
) -> list[tuple[set[int], set[int]]]:
    logging.debug(f"parsing data\n{data}")
    cards = []
    re_p = r"^Card\s+(?P<card>\d+): (?P<winners>[\d\s]+) \| (?P<drawn>[\d\s]+)$"
    for line in data.splitlines():
        cards_m = re.match(re_p, line)
        cards.append(
            [
                {int(s) for s in cards_m.group("winners").split()},
                {int(s) for s in cards_m.group("drawn").split()},
            ]
        )
    return cards


def part_a(data: str):
    logging.debug("")
    cards = parse(data)
    return sum([int(2 ** (len(c[0] & c[1]) - 1)) for c in cards])


def part_b(data: str):
    logging.debug("")
    cards = parse(data)
    instances = [1 for _ in range(len(cards))]
    for card_no, c in enumerate(cards):
        num_matches = len(c[0] & c[1])
        logging.debug(
            f"Card {card_no + 1}: {num_matches} matching numbers and {instances[card_no]} instances"
        )
        f = card_no + 1
        t = min(card_no + 1 + num_matches, len(instances))
        instances[f:t] = [x + instances[card_no] for x in instances[f:t]]
    return sum(instances)
