import sys
import numpy as np
from collections import Counter
from itertools import chain

heightmap = np.array(
    [[int(x) for x in y.rstrip()] for y in open(sys.argv[1])]
)

# part one
# pad with 10 because we always want the inside to be lower than the edge
padded_heightmap = np.pad(
    heightmap, pad_width = 1,
    mode = 'constant', constant_values = 10
)

# find elements that are lower than the four shifted directions
low_mask = np.logical_and(
    heightmap < padded_heightmap[:-2,1:-1], # down
    heightmap < padded_heightmap[2:, 1:-1] # up
)
low_mask = np.logical_and(
    low_mask,
    heightmap < padded_heightmap[1:-1, :-2] # right
)
low_mask = np.logical_and(
    low_mask,
    heightmap < padded_heightmap[1:-1, 2:] # left
)

# print the sum of one more than each low point (answer)
print(sum(heightmap[low_mask] + 1))


# ---------------------------------------------------------------
#
# part two
# basically just wrote my own implementation of watershed fill
# 
# https://en.wikipedia.org/wiki/Watershed_(image_processing)

# give each low point a unique value based on its index. Any non
# low point is set to 1.
#
# start the range at 2 just in case one of the low points is the
# first element in the array, in which case it would try to fill
# with 1, but 1 is our empty value
fill_map = np.where(
    low_mask,
    np.arange(2,np.size(heightmap)+2).reshape(heightmap.shape),
    np.ones_like(heightmap)
)

# set all walls to zero
fill_map = fill_map * (heightmap != 9)

# while anything hasn't been filled yet:
while (fill_map == 1).any():
    # create an array padded with -1 (so the max at the edge is the inside value)
    padded_fillmap = np.pad(
        fill_map, pad_width = 1,
        mode = 'constant', constant_values = -1
    )

    # make shifted maps, as we used in part one, of the new map
    down = padded_fillmap[:-2,1:-1]
    up = padded_fillmap[2:, 1:-1]
    right = padded_fillmap[1:-1, :-2]
    left = padded_fillmap[1:-1, 2:]

    # set each element to the maximum value of its neighbors
    for shifted_array in [down, up, right, left]:
        fill_map = np.maximum(fill_map, shifted_array)

    # reset walls to zero before next iteration
    fill_map = fill_map * (heightmap != 9)

# count number of cells flowing to each unique basin number
basins = Counter(chain(*fill_map.tolist()))
# delete walls
del basins[0]

# print the product of the number of cells in the three largest
# basins (the answer)
values = list(basins.values())
values.sort()
print(np.prod(values[-3:]))
