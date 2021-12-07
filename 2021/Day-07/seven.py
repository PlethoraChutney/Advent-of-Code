import numpy as np
import sys

# read in the crabs as ints
crab_positions = np.loadtxt(
    sys.argv[1], dtype = int,
    delimiter=',')

# get range of all positions between the crabs
#
# anything beyond the terminal crabs will only
# add fuel
min_crab = np.min(crab_positions)
max_crab = np.max(crab_positions)
potential_positions = np.arange(min_crab, max_crab)

# np.meshgred makes two 2D grids, one for each array, meaning
# we can just subtract one from the other for our differences.
# doing it this way means the cols are each test position
crabs, positions = np.meshgrid(
    crab_positions, potential_positions
    )


# part one
differences = np.abs(crabs - positions)

sums = np.apply_along_axis(sum, 1, differences)
print(np.min(sums))

# part two

# rather than calculate sum fresh for every element,
# instead calculate all the fuel consumptions per
# movement and return that

min_diff = np.min(differences)
max_diff = np.max(differences)

memo_fuel = [
    np.sum(np.arange(x+1)) for 
    x in range(min_diff, max_diff + 1)
    ]
# np.take takes the value from the first array
# at the index matching the value from the second array
# to generate an array of the same shape as the second.
differences = np.take(memo_fuel, differences)
sums = np.apply_along_axis(sum, 1, differences)
print(np.min(sums))