#!/usr/bin/env python
import sys
import numpy as np
from itertools import combinations

with open(sys.argv[1], "r") as f:
    lines = [list(ord(y) for y in x.rstrip()) for x in f]

grid = np.array(lines)
grid[grid == 46] = 0
signal_freqs = [x for x in np.unique(grid) if x != 0]

def is_in_grid(coord):
    x, y = coord
    xlim, ylim = grid.shape
    return x < xlim and x >= 0 and y < ylim and y >= 0

antennas = {
    freq: list(zip(*np.where(grid == freq)))
    for freq in signal_freqs
}

nodes = set()
for freq, coords in antennas.items():
    combs = combinations(coords, 2)
    for comb in combs:
        a, b = [np.array(x) for x in comb]
        diff = a - b
        n1 = a + diff
        n2 = b - diff
        for n in [n1, n2]:
            if is_in_grid(n):
                nodes.add(tuple(n))

print(f"Part one: {len(nodes)}")

# part two

nodes = set()
for freq, coords in antennas.items():
    combs = combinations(coords, 2)
    for comb in combs:
        a, b = [np.array(x) for x in comb]
        direction = a - b
        starting_pos = a.copy()
        while is_in_grid(starting_pos):
            # this'll go one step too far
            starting_pos += direction
        starting_pos -= direction

        while is_in_grid(starting_pos):
            nodes.add(tuple(starting_pos))
            starting_pos -= direction

print(f"Part two: {len(nodes)}")