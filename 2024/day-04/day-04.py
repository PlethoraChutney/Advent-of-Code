#!/usr/bin/env python
import sys
import numpy as np
from scipy.signal import convolve

with open(sys.argv[1], "r") as f:
    lines = [x.rstrip() for x in f]

num_lines = []
# convert letters to prime numbers of alternating sign to avoid
# coincidentally coming up with the right value when we're convolving later
line_replacements = {
    "X": 2,
    "M": -3,
    "A": 5,
    "S": -7
}
for line in lines:
    num_lines.append([line_replacements[x] for x in line])

a = np.array(num_lines)

# part one

horizontal = np.array([
    # horizontal
    [2, -3, 5, -7]
])
diagonal = np.array([
    # diag
    [2, 0, 0, 0],
    [0, -3, 0, 0],
    [0, 0, 5, 0],
    [0, 0, 0, -7]
])

xmas_arrays = [horizontal, diagonal]
for k in range(1, 4):
    xmas_arrays.append(np.rot90(horizontal, k))
    xmas_arrays.append(np.rot90(diagonal, k))

# diagnostic printing of XMAS from numbers (used during development)
replacements = {v: k for k, v in line_replacements.items()}
replacements[0] = " "
def xmas_print(a):
    for r in a:
        for c in r:
            print(replacements[c], end = "")
        print("")
    print("----")
    

def search_for_arrays(a, search_arrays, target_value):
    num_xmas = 0
    for search_array in search_arrays:
        convolved_arrays = convolve(
            a,
            search_array,
            mode = "valid"
        )
        num_xmas += len(np.argwhere(convolved_arrays == target_value))
    return num_xmas

xmas_target = convolve(horizontal, horizontal, mode = "valid")[0][0]
print(f"Part one: {search_for_arrays(a, xmas_arrays, xmas_target)}")

# part two
cross_mas = np.array([
    [-3, 0, -3],
    [0, 5, 0],
    [-7, 0, -7]
])

cross_mas_arrays = [np.rot90(cross_mas, k) for k in range(4)]
cross_mas_target = convolve(cross_mas, cross_mas, mode = "valid")[0][0]
print(f"Part two: {search_for_arrays(a, cross_mas_arrays, cross_mas_target)}")