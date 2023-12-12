from functools import cache


def parse(data: str) -> list[tuple[str, str]]:
    return [
        (springs, broken)
        for [springs, broken] in [l.split() for l in data.splitlines()]
    ]


@cache
def solve(springs: str, broken: str) -> int:
    if len(broken) == 0:
        if "#" not in springs:
            return 1
        else:
            return 0
    seqs = broken.split(",")
    seq_len = int(seqs[0])
    broken = ",".join(seqs[1:])
    assignments = []
    for start_idx in range(len(springs)):
        if (
            start_idx + seq_len <= len(springs)
            and "#" not in springs[:start_idx]
            and "." not in springs[start_idx : start_idx + seq_len]
            and (start_idx == 0 or springs[start_idx - 1] != "#")
            and (
                start_idx + seq_len == len(springs)
                or springs[start_idx + seq_len] != "#"
            )
        ):
            if start_idx + seq_len + 1 < len(springs):
                assignments.append(springs[start_idx + seq_len + 1 :])
            else:
                assignments.append("")
    return sum([solve(ass, broken) for ass in assignments])


def part_a(data: str):
    rows = parse(data)
    return sum([solve(springs, broken) for springs, broken in rows])


def part_b(data: str):
    rows = parse(data)
    rows = [
        ("?".join([springs] * 5), ",".join([broken] * 5)) for springs, broken in rows
    ]
    s = 0
    for springs, broken in rows:
        s += solve(springs, broken)
    return s
