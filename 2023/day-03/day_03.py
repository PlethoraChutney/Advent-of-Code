#!/usr/bin/env python
with open("input.txt", "r") as f:
    lines = [list(x.rstrip()) for x in f]

part_positions = []
gears = {}


def expand_position(pos):
    x = pos[0]
    y = pos[1]
    coords = (
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
        (x - 1, y),
        (x + 1, y),
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
    )

    return coords


for rownum, row in enumerate(lines):
    for colnum, val in enumerate(row):
        if val not in "01234567890.":
            coords = expand_position((rownum, colnum))
            part_positions.extend(coords)

            if val == "*":
                for coord in coords:
                    gears[coord] = (rownum, colnum)

part_sum = 0
part_positions = set(part_positions)

gear_adjacent = {}

curr_num = None
near_symb = False
near_gear = None


def complete_num():
    global near_symb
    global part_sum
    global curr_num
    global near_gear
    if near_symb:
        part_sum += int(curr_num)

    if near_gear is not None:
        if near_gear not in gear_adjacent:
            gear_adjacent[near_gear] = [int(curr_num)]
        else:
            gear_adjacent[near_gear].append(int(curr_num))

    curr_num = None
    near_symb = False
    near_gear = None


for rownum, row in enumerate(lines):
    for colnum, val in enumerate(row):
        if val in "01234567890":
            if curr_num is None:
                curr_num = val
            else:
                curr_num += val

            if (rownum, colnum) in part_positions:
                near_symb = True

            if (rownum, colnum) in gears:
                near_gear = gears[(rownum, colnum)]

        else:
            complete_num()
    complete_num()

print(f"Part one: {part_sum}")

gear_ratio_sum = 0
for gearset in gear_adjacent.values():
    if len(gearset) == 2:
        gear_ratio_sum += gearset[0] * gearset[1]

print(f"Part two: {gear_ratio_sum}")
