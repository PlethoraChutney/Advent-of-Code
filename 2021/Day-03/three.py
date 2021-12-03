import numpy as np
import sys
import re

diagnostics = [list(x.rstrip()) for x in open(sys.argv[1])]

# part one

# list of integer arrays
bit_arrays = [np.array(x, dtype = int) for x in diagnostics]

# add the bits at each position together, getting
# the sum of bits at each possition
sum_array = sum(bit_arrays)

# get the average array value for each bit (i.e., if half
# the bits at position 3 are 1, av_array[3] == 0.5)
av_array = [x/len(diagnostics) for x in sum_array]

# make a string of bits where, for each position, if the average
# is greater than 0.5, the position is 1, otherwise 0
gamma_array = [str(int(x>.5)) for x in av_array]
gamma = int(''.join(gamma_array), 2)

# xor with all 1s just flips all the bits
eps = int('1'*len(gamma_array), 2) ^ gamma

# solution
print(gamma * eps)


# part two    

def oxygen_scrubber(diag, mask):
    # if there's only one diagnostic left, return it as an integer
    if len(diag) == 1:
        return int(diag[0], 2)

    # add a 1 to our working mask
    one_mask = mask + '1'
    ones = [1 for x in diag if re.match(one_mask, x)]

    # if fewer than half our working diagnostics match the one mask, 
    # we need the zero mask instead
    if sum(ones)/len(diag) < 0.5:
        mask = mask + '0'
    # otherwise, the 1 mask is right
    else:
        mask = one_mask

    # our working diagnostics are those that match the mask
    diag = [x for x in diag if re.match(mask, x)]

    # recurse (if there's only one left, it'll get returned at the top
    # of the next call)
    return oxygen_scrubber(diag, mask)

# same as oxygen_scrubber, but reversed bit
def co2_scrubber(diag, mask):
    if len(diag) == 1:
        return int(diag[0], 2)

    one_mask = mask + '1'
    ones = [1 for x in diag if re.match(one_mask, x)]
    if sum(ones)/len(diag) < 0.5:
        mask = mask + '1'
    else:
        mask = mask + '0'

    diag = [x for x in diag if re.match(mask, x)]

    
    return co2_scrubber(diag, mask)
    

    
    
diag_array = [x.rstrip() for x in open(sys.argv[1])]
# solution
print(oxygen_scrubber(diag_array, '^') * co2_scrubber(diag_array, '^'))

