import numpy as np
import sys
import re
import time

t0 = time.time()
diagnostics = [list(x.rstrip()) for x in open(sys.argv[1])]
t_read = time.time()

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

t_one = time.time()

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

t_vid = time.time()

# vectorize

def list_to_int(bit_list):
    out = 0
    for bit in bit_list:
        # bitshift out left 1 (i.e., multiply by 2), then or it with
        # the next bit in the list. Or-ing a zero with a bit just keeps
        # the bit
        out = (out << 1) | bit

    return out


diagnostics = np.array(bit_arrays)
num_bits = len(diagnostics[0])
num_diags = len(diagnostics)

position = 0
working_diag = diagnostics.copy()

while position < num_bits and len(working_diag) > 1:
    pos_array = working_diag[:, position:position+1].flatten()
    # can't use argmax b/c we need to break ties with a 1
    bit_count = np.bincount(pos_array)
    # if 0 is more common, return False (i.e., 0). Else true (i.e., 1)
    mcb = int(bit_count[0] <= bit_count[1])
    # select rows with the most common bit in the current position
    working_diag = working_diag[pos_array == mcb, :]

    position += 1

o_gen = list_to_int(working_diag[0].tolist())

position = 0
working_diag = diagnostics.copy()

while position < num_bits and len(working_diag) > 1:
    pos_array = working_diag[:, position:position+1].flatten()
    bit_count = np.bincount(pos_array)
    # flipped from o_gen, and want the equal case to return 0 now
    mcb = int(bit_count[0] > bit_count[1])
    working_diag = working_diag[pos_array == mcb, :]

    position += 1

c_scrubber = list_to_int(working_diag[0].tolist())

print(o_gen * c_scrubber)

t_np = time.time()

time_read = t_read - t0
time_one = t_one - t_read
time_slow = t_vid - t_one
time_np = t_np - t_vid

# regex solution is actually quite fast :)
print('Time to read data: ', time_read)
print('Time for part one: ', time_one)
print('Time for video solution to part two: ', time_slow)
print('Time for np solution to part two: ', time_np)