#!/usr/bin/env python

with open("input.txt", "r") as f:
    lines = [x.rstrip() for x in f]


def limit_generator(dest, src, r):
    def new_limit(input_num):
        if input_num < src or input_num >= src + r:
            return input_num
        else:
            return dest + (input_num - src)

    return new_limit


mapped_values = {}
maps = {}
for line in lines:
    if len(line) == 0:
        continue

    if "seeds" in line:
        mapped_values["seed"] = [int(x) for x in line.split(": ")[1].split()]
    elif "map" in line:
        curr_map = line.split()[0]
        maps[curr_map] = []
    else:
        dest, src, r = [int(x) for x in line.split()]
        maps[curr_map].append(limit_generator(dest, src, r))


def convert_format(start, end):
    print(f"Converting {start} to {end}")
    src_values = mapped_values[start]
    mapping = maps[f"{start}-to-{end}"]
    dest = []
    for src in src_values:
        mapped_value = [x(src) for x in mapping if x(src) != src]
        if mapped_value:
            dest.append(mapped_value[0])
        else:
            dest.append(src)

    mapped_values[end] = dest


def seeds_to_location():
    convert_format("seed", "soil")
    convert_format("soil", "fertilizer")
    convert_format("fertilizer", "water")
    convert_format("water", "light")
    convert_format("light", "temperature")
    convert_format("temperature", "humidity")
    convert_format("humidity", "location")


seeds_to_location()
print(f"Part one: {min(mapped_values['location'])}")

seed_ranges = mapped_values["seed"]
part_two_seeds = []
for i in range(0, len(seed_ranges) - 1, 2):
    part_two_seeds.extend(
        list(range(seed_ranges[i], seed_ranges[i] + seed_ranges[i + 1]))
    )

mapped_values["seed"] = part_two_seeds
seeds_to_location()

print(f"Part two: {min(mapped_values['location'])}")
