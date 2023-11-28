import importlib


def solve(year: int, day: int, data: str):
    mod_name = f"aoc_2023.day_{day:02}"
    mod = importlib.import_module(mod_name)
    a = mod.part_a(data)
    b = mod.part_b(data)
    return a, b
