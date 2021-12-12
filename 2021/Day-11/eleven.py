import numpy as np
from scipy import signal
import sys

octos = np.array([
    [int(x) for x in y.rstrip()]
    for y in open(sys.argv[1])
])

def iter_days(octos):
    # A classic application for a kernel
    #
    # this kernel is convolved at each point in octos. The zero
    # in the center prevents the flashing octo from adding 1 to
    # itself.
    octo_flash_kernel = [[1,1,1],[1,0,1],[1,1,1]]
    day = 0
    flashes = 0

    while True:
        day += 1

        # on each day, the octos regain the ability to flash
        fired = np.zeros_like(octos).astype(bool)

        octos += 1

        # if any octos have charged
        while (octos > 9).any():
            # first, mark them as ready to fire. add them to the total number of flashes
            # we're tracking for part one
            to_fire = np.logical_and(octos > 9, np.logical_not(fired)).astype(int)
            flashes += sum(to_fire.flatten())
            # mark them as fired so that they don't try to flash again today
            fired += to_fire.astype(bool)
            # if everybody has flashed, return for part two
            if (fired).all():
                return (flashes_to_return, day)

            # convolve our flash kernel with the to_flash to get the number of adjacent
            # flashes at each position
            flashed = signal.convolve2d(
                to_fire,
                octo_flash_kernel,
                mode = 'same',
                boundary = 'fill',
                fillvalue=0
            )

            # add the adjacent flashes to the octos
            octos += flashed
            # reset all fired octos to 0
            octos = np.where(fired, 0, octos)

            # repeating the loop checks if any octos were charged by their adjacent flashes
            # Even the worst arrangement:
            # 888
            # 898
            # 888
            # doesn't loop indefinitely here because the octos have to be > 9

        if day == 100:
            flashes_to_return = flashes        

print(iter_days(octos))