#!/usr/bin/env python
with open("input.txt", "r") as f:
    lines = [x.rstrip() for x in f]

import re

cube_pattern = r"([0-9]+ (?:red|blue|green))"

allowed_games = []
power_sum = 0
permissable_cubes = {"red": 12, "green": 13, "blue": 14}


def parse_cubes(line):
    min_cubes = {"red": 0, "blue": 0, "green": 0}
    game_id = int(re.search("Game ([0-9]*):", line).group(1))
    possible = True

    for cube_string in re.finditer(cube_pattern, line):
        cubes, color = cube_string.group(0).split(" ")
        cubes = int(cubes)

        if cubes > permissable_cubes[color]:
            possible = False

        if cubes > min_cubes[color]:
            min_cubes[color] = cubes

    if possible:
        allowed_games.append(game_id)
    power = min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]
    return power


for line in lines:
    power_sum += parse_cubes(line)

print(f"Part one: {sum(allowed_games)}")
print(f"Part two: {power_sum}")
