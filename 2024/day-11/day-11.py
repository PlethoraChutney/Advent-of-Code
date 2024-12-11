#!/usr/bin/env python
import sys
from collections import Counter

with open(sys.argv[1], "r") as f:
    lines = [x.rstrip() for x in f]

stones = [int(x) for x in lines[0].split(" ")]
stones = Counter(stones)

def split_stone(s:int) -> list[int]:
    s = str(s)
    halfway = len(s) // 2
    return [int(x) for x in [s[:halfway], s[halfway:]]]

rules = [
    (
        lambda s: s == 0,
        lambda s: [1]
    ),
    (
        lambda s: len(str(s)) % 2 == 0,
        split_stone
    ),
    (
        lambda s: True,
        lambda s: [s * 2024]
    )
]

def apply_rules(stone:int) -> int:
    for rule, result in rules:
        if rule(stone):
            return result(stone)

memos = {}
def blink(stones:Counter) -> Counter:
    new_stones = Counter()

    for stone, count in stones.items():
        new_values = memos.get(stone)
        if new_values is None:
            new_values = apply_rules(stone)
            memos[stone] = new_values
        for v in new_values:
            new_stones[v] += count

    return new_stones

for i in range(25):
    stones = blink(stones)

print(f"Part one: {sum(stones.values())}")

for i in range(50):
    stones = blink(stones)

print(f"Part two: {sum(stones.values())}")