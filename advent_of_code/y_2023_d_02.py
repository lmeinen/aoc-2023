import logging
import re
from itertools import chain


def parse(line: str) -> (int, list[tuple[(int, str)]]):
    game_p = r"^Game (?P<id>\d+): (?P<game>.*$)"
    draw_p = r"(?P<count>\d+) (?P<color>red|green|blue)"
    logging.debug(f"parsing line '{line}'")
    m = re.match(game_p, line)
    game_id = int(m.group("id"))
    game = m.group("game")
    logging.debug(f"game_id: {game_id}")
    logging.debug(f"game: {game}")
    draws = [draw.split(",") for draw in game.split(";")]
    draws = [draw for sublist in draws for draw in sublist]
    matched_draws = [re.search(draw_p, d) for d in draws]
    counts = [
        (int(matched_draw.group("count")), str(matched_draw.group("color")))
        for matched_draw in matched_draws
    ]
    return (game_id, counts)


def part_a(data: str):
    logging.debug("")
    s = 0

    def possible(n: int, c: str) -> bool:
        match c:
            case "red":
                return n <= 12
            case "green":
                return n <= 13
            case "blue":
                return n <= 14

    for line in data.splitlines():
        game_id, counts = parse(line)
        if all(possible(n, c) for (n, c) in counts):
            logging.debug(f"appears possible - increasing count by {game_id}")
            s += game_id
    return s


def part_b(data: str):
    logging.debug("")
    s = 0
    for line in data.splitlines():
        _, counts = parse(line)
        min_red = max([n for (n, c) in counts if c == "red"])
        min_green = max([n for (n, c) in counts if c == "green"])
        min_blue = max([n for (n, c) in counts if c == "blue"])
        s += min_red * min_green * min_blue
    return s
