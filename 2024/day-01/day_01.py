#!/usr/bin/env python

list_a = []
list_b = []
with open('input.txt', 'r') as f:
    for line in f:
        a, b = (int(x) for x in line.split())
        list_a.append(a)
        list_b.append(b)

list_a.sort()
list_b.sort()

print(f"Part One: {sum(abs(a - b) for a, b in zip(list_a, list_b))}")

from collections import Counter

counted_a = Counter(list_a)
counted_b = Counter(list_b)

part_b_total = 0
for id, count_a in counted_a.items():
    count_b = counted_b[id]
    part_b_total += id * count_a * count_b

print(f"Part Two: {part_b_total}")