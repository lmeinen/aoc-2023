import importlib
import logging
import time


def solve(year: int, day: int, data: str):
    mod_name = f"advent_of_code.y_{year:04}_d_{day:02}"
    mod = importlib.import_module(mod_name)
    start = time.time_ns()
    a = mod.part_a(data)
    mid = time.time_ns()
    b = mod.part_b(data)
    end = time.time_ns()
    logging.info("")
    logging.info(f"{year}-{day} part a took {(mid - start) // 1e6} ms")
    logging.info(f"{year}-{day} part b took {(end - mid) // 1e6} ms")
    return a, b
