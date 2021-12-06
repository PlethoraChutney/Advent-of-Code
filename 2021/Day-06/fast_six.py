import sys
import numpy as np
from collections import Counter

fish = np.loadtxt(sys.argv[1], dtype=int, delimiter=',').tolist()
# count the number of fish at each day-til-reproduce in the input
# 
# we don't technically need to convert to a dict but I do it anyway
fish = dict(Counter(fish))

day = 0
new_fish = {}
while day < 80:
    for key, val in fish.items():
        # bump each fish down a day until reproduction
        new_fish[key-1] = val

    # need a try here becuase sometimes there may not be any
    # fish ready to spawn
    try:
        # make baby fish equal to the number of spawning fish
        new_fish[8] = new_fish[-1]
        # this try lets us add to the 6-fish if there are any,
        # or create them if not
        try:
            new_fish[6] += new_fish[-1]
        except KeyError:
            new_fish[6] = new_fish[-1]
        # once we've handled fish spawning, remove the -1 fish or
        # else they propagate backward forever
        del new_fish[-1]
    except KeyError:
        # if there are no spawning fish we don't need to do anything
        pass


    # prepare for next iteration
    fish = new_fish
    new_fish = {}
    day += 1

print(sum(fish.values()))

# part two, same as part one but longer
while day < 256:
    for key, val in fish.items():
        new_fish[key-1] = val

    try:
        new_fish[8] = new_fish[-1]
        try:
            new_fish[6] += new_fish[-1]
        except KeyError:
            new_fish[6] = new_fish[-1]
        del new_fish[-1]
    except KeyError:
        pass


    fish = new_fish
    new_fish = {}
    day += 1

print(sum(fish.values()))