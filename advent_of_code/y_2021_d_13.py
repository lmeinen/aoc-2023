from functools import cache
import logging
import re


def parse(data: str) -> (set[tuple[int, int]], list[tuple[int, int]]):
    dots = set()
    folds = list()
    dots_p = r"^(?P<x>\d+),(?P<y>\d+)$"
    fold_p = r"^fold along (?P<dir>[x|y])=(?P<coord>\d+)$"
    lines = data.splitlines()
    parsing_dots = True
    for line in lines:
        if not line:
            parsing_dots = False
            continue
        if parsing_dots:
            m = re.match(dots_p, line)
            dots.add((int(m.group("x")), int(m.group("y"))))
        else:
            m = re.match(fold_p, line)
            coord = int(m.group("coord"))
            folds.append((coord, 0) if m.group("dir") == "x" else (0, coord))
    return dots, folds


sub = lambda t1, t2: (t1[0] - t2[0], t1[1] - t2[1])
mul = lambda v, t: (v * t[0], v * t[1])


def fold(dots: set[tuple[int, int]], f: tuple[int, int]) -> set[tuple[int, int]]:
    reduce = lambda t: (t[0], 0) if f[0] > 0 else (0, t[1])
    return {(d if reduce(d) < f else (sub(d, mul(2, sub(reduce(d), f))))) for d in dots}


def part_a(data: str):
    dots, folds = parse(data)
    return len(fold(dots, folds[0]))


def part_b(data: str):
    print("")
    dots, folds = parse(data)
    for f in folds:
        print(f"{dots_to_string(dots)}")
        print("")
        print(f"------ folding along {f} -------")
        print("")
        dots = fold(dots, f)
    print(f"{dots_to_string(dots)}")

    return 0


def dots_to_string(dots) -> str:
    curr_row = 0
    curr_col = 0
    txt = ""
    width = max([d[0] for d in dots]) + 1
    l = sorted(dots, key=lambda d: (d[1], d[0]))
    txt += f"dots: {l}\n"
    txt += f"width {width}\n"
    txt += f"line {curr_row:03}: "
    for d in l:
        while d[1] > curr_row:
            txt += "." * (width - curr_col) + "\n"
            curr_row += 1
            curr_col = 0
            if txt[-1] == "\n":
                txt += f"line {curr_row:03}: "
        while d[0] > curr_col:
            txt += "."
            curr_col += 1
        txt += "#"
        curr_col += 1
    return txt
