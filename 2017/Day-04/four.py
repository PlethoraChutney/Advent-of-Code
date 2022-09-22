with open('input.txt', 'r') as f:
    lines = [x.rstrip().split() for x in f]

print('Part one:', sum(
    [1 for x in lines if len(set(x)) == len(x)]
))

from itertools import combinations

good_passes = 0
for line in lines:
    bad_line = False
    for a, b in combinations(line, 2):
        if set(a) == set(b):
            bad_line = True
            break
    if not bad_line:
        good_passes += 1

print('Part two:', good_passes)