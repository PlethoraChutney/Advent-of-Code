import numpy as np
import sys
from itertools import chain
from collections import Counter


vent_lines = [x.rstrip().split(' -> ') for x in open(sys.argv[1])]


# convert list of comma separated values to array of np
# arrays, first row start, second row end of line.
vent_lines = [
    np.array([[int(x) for x in y.split(',')] for y in z])
     for z in vent_lines]

def get_grid_points(endpoints, part_one = True):
    run, rise = endpoints[1] - endpoints[0]

    # if rise or run is 0, set the other to 1 (or -1)
    if run == 0:
        rise = int(rise/abs(rise))
        # Get the range from start to end, iterating by + or - 1.
        #
        # Add rise instead of 1 because the endpoints might be less
        # than the start point (i.e., rise might be negative)
        y = np.arange(endpoints[0,1], endpoints[1,1] + rise, rise)
        # x should just be the start point
        x = np.full_like(y, endpoints[0,0], dtype=int)

    elif rise == 0:
        run = int(run/abs(run))
        x = np.arange(endpoints[0,0], endpoints[1,0] + run, run)
        y = np.full_like(x, endpoints[0,1], dtype=int)
    else:
        # Since we know that the slope will always be exactly diagonal,
        # we do not need to worry about finding the greatest common factor.
        if part_one:
            return np.array([])
        run = int(run/abs(run))
        rise = int(rise/abs(rise))
        
        x = np.arange(endpoints[0,0], endpoints[1,0] + run, run)
        y = np.arange(endpoints[0,1], endpoints[1,1] + rise, rise)

    # return a list of lists instead of the numpy array of two columns
    return np.array([x,y]).transpose().tolist()

# iterate through list once
points_visited = map(get_grid_points, vent_lines)
# flatten out the list of list of lists into a list of lists lol
# make the lists strings so Counter can count them
points_visited = [str(x) for x in chain(*points_visited)]
# count number of times each coord in list
counted = Counter(points_visited)
# print the number of coords visited more than once
print(len([x for x in counted if counted[x] > 1]))

# same, but include the diagonal
points_visited = map(lambda x: get_grid_points(x, False), vent_lines)
points_visited = [str(x) for x in chain(*points_visited)]
counted = Counter(points_visited)
print(len([x for x in counted if counted[x] > 1]))