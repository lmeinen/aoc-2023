import json
import logging
import re
from itertools import product, tee


def parse(data: str) -> list[tuple[str, int]]:
    return [(l[0], int(l[1])) for l in [line.split() for line in data.splitlines()]]


def order(hand: str, has_joker: bool) -> list[int]:
    card_val = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 1 if has_joker else 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }
    cards = {c: 0 for c, _ in card_val.items()}
    for card in hand:
        cards[card] += 1
    num_jokers = cards["J"] if has_joker else 0
    counts = [count for card, count in cards.items() if not (has_joker and card == "J")]
    idx, _ = max(enumerate(counts), key=lambda p: p[1])
    counts[idx] += num_jokers
    score = sum([10**c for c in counts])
    return [score] + list(map(lambda s: int(card_val[s]), [card for card in hand]))


def part_a(data: str):
    hands = parse(data)
    hands.sort(key=lambda h: order(h[0], False))
    return sum([(i + 1) * h[1] for i, h in enumerate(hands)])


def part_b(data: str):
    hands = parse(data)
    hands.sort(key=lambda h: order(h[0], True))
    return sum([(i + 1) * h[1] for i, h in enumerate(hands)])
