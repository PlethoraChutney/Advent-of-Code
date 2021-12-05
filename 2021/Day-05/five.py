import numpy as np
import sys
from itertools import chain
from math import gcd


vent_lines = [x.rstrip().split(' -> ') for x in open(sys.argv[1])]


# convert list of comma separated values to array of np
# arrays, first row start, second row end of line.
vent_lines = np.array([
    np.array([[int(x) for x in y.split(',')] for y in z])
     for z in vent_lines])

# unnest our entire vent_lines array to find the biggest
# x or y value. This is the grid extent, which we'll use
# to construct the map.
grid_extent = max(chain(*chain(*vent_lines.tolist()))) + 1
vent_map_one = np.zeros(
    shape = (grid_extent, grid_extent),
    dtype = int
)
vent_map_two = vent_map_one.copy()

def map_grid_points(endpoints, vent_map_one, vent_map_two):
    run, rise = endpoints[1] - endpoints[0]



    # if rise or run is 0, set the other to 1 (or -1)
    if run == 0:
        rise = int(rise/abs(rise))
    elif rise == 0:
        run = int(run/abs(run))
    # otherwise, reduce both by their greatest common factor
    #
    # I wrote this before knowing it would only ever be 45 degree
    # lines...oh well...
    else:
        factor = gcd(run, rise)
        run = int(run/factor)
        rise = int(rise/factor)

    curr_point = endpoints[0]
    if any(x == 0 for x in (run, rise)):
        vent_map_one[tuple(curr_point)] += 1
    vent_map_two[tuple(curr_point)] += 1
    # walk along the slope, adding to the map at each point,
    # until you reach the endpoint
    while not np.array_equal(curr_point, endpoints[1]):
        curr_point += (run, rise)
        
        # only add to the first map if line is vert. or horiz.
        if any(x == 0 for x in (run, rise)):
            vent_map_one[tuple(curr_point)] += 1

        # always add to the second map
        vent_map_two[tuple(curr_point)] += 1

# iterate through list once
for vent in vent_lines:
    map_grid_points(vent, vent_map_one, vent_map_two)

print((vent_map_one > 1).sum())
print((vent_map_two > 1).sum())
