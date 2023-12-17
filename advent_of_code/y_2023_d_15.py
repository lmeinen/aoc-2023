from collections import Counter
import logging
import re


def parse(data: str) -> list[str]:
    return data.strip().split(",")


# assumes exponent and m are co-prime
def reindeer_hash(step: str, m: int, exp_seq: list[int]) -> int:
    ascii_vals = [ord(s) for s in step]
    n = len(ascii_vals)
    return (
        sum(
            [
                (v * exp_seq[(n - i) % len(exp_seq)]) % m
                for i, v in enumerate(ascii_vals)
            ]
        )
        % m
    )


def part_a(data: str):
    init_seq = parse(data)
    exp_seq = [17**i % 256 for i in range(int(256 * (1 - 1 / 2)))]  # Euler's theorem
    return sum([reindeer_hash(step, 256, exp_seq) for step in init_seq])


def part_b(data: str):
    init_seq = parse(data)
    exp_seq = [17**i % 256 for i in range(int(256 * (1 - 1 / 2)))]  # Euler's theorem
    boxes: dict[int, list[tuple[str, str]]] = {i: [] for i in range(256)}
    re_dash = r"^(?P<label>\S+)-$"
    re_eq = r"^(?P<label>\S+)=(?P<flen>\d)$"
    for step in init_seq:
        if m := re.match(re_dash, step):
            box = reindeer_hash(m.group("label"), 256, exp_seq)
            boxes[box] = [(l, v) for (l, v) in boxes[box] if l != m.group("label")]
        elif m := re.match(re_eq, step):
            box = reindeer_hash(m.group("label"), 256, exp_seq)
            idx = [i for i, (l, _) in enumerate(boxes[box]) if l == m.group("label")]
            if len(idx) > 0:
                boxes[box][idx[0]] = (m.group("label"), m.group("flen"))
            else:
                boxes[box].append((m.group("label"), m.group("flen")))
        else:
            raise AssertionError(f"illegal step {step}")
    logging.debug(f"boxes: {list(filter(lambda i: i[1] != [], boxes.items()))}")
    return sum(
        [
            (1 + k) * (1 + i) * int(v)
            for k, box in boxes.items()
            for i, (_, v) in enumerate(box)
        ]
    )
