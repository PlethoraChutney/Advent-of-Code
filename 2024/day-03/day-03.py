#!/usr/bin/env python
import sys
import re

with open(sys.argv[1], "r") as f:
    lines = [x.rstrip() for x in f]

command = "".join(lines)
mul_pattern = r"mul\((\d{1,3}),(\d{1,3})\)"

def do_mulls(command):
    muls = re.findall(mul_pattern, command)
    return sum(int(x[0]) * int(x[1]) for x in muls)

print(f"Part one: {do_mulls(command)}")

do_pattern = r"(do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\))"
full_commands = re.findall(do_pattern, command)

perform_commands = True
summed_values = 0
for c in full_commands:
    if c[0] == "don't()":
        perform_commands = False
    elif c[0] == "do()":
        perform_commands = True
    elif perform_commands:
        summed_values += int(c[1]) * int(c[2])

print(f"Part two: {summed_values}")