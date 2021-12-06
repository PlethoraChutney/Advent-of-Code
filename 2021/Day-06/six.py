import sys
import numpy as np

#######################
# This is implemented as a literal "keep track of fish".
# It technically works, but it's so slow it may as well
# not work at all. fast_six is the answer.

fish = np.loadtxt(sys.argv[1], dtype=int, delimiter=',')

day = 0
while day < 80:
    fish = fish - 1
    spawning_fish = fish < 0
    fish[spawning_fish] = 6
    if sum(spawning_fish) > 0:
        fish = np.append(fish, [8]*sum(spawning_fish))

    day += 1

print(len(fish))

# I wrote and ran fast_six.py before this finished running

while day < 256:
    fish = fish - 1
    spawning_fish = fish < 0
    fish[spawning_fish] = 6
    if sum(spawning_fish) > 0:
        fish = np.append(fish, [8]*sum(spawning_fish))

    day += 1