#!/usr/bin/env python
with open("input.txt", "r") as f:
    lines = [x.rstrip() for x in f]

# Part One
import re


def process_digits(lines):
    sum = 0
    for line in lines:
        digits = re.search(r".*?([0-9]).*([0-9])", line)
        if digits is None:
            digits = re.search("[0-9]", line)
            line_val = int(digits.group(0) + digits.group(0))
        else:
            line_val = int(digits.group(1) + digits.group(2))
        sum += line_val
    return sum


print(f"Part one: {process_digits(lines)}")

# Part Two
# Note that letters can overlap

converter = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "f4r",
    "five": "f5e",
    "six": "s6x",
    "seven": "s7n",
    "eight": "e8t",
    "nine": "n9e",
}


def convert_to_digits(line):
    # if we always add the first and last letters back to the string,
    # we won't hurt anything and won't have to be smart
    for word, digit in converter.items():
        line = line.replace(word, digit)

    return line


digitized_lines = [convert_to_digits(x) for x in lines]
print(f"Part two: {process_digits(digitized_lines)}")
