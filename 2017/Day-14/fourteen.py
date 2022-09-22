def knot_hash(key_string) -> str:
    string = list(range(256))

    lengths = [ord(x) for x in key_string]
    lengths.extend([17, 31, 73, 47, 23])

    position = 0
    skip_size = 0

    for iteration in range(64):
        for length in lengths:
            digits = []
            for i in range(length):
                digits.append(string[(position + i) % len(string)])
            digits = digits[::-1]

            for i in range(len(digits)):
                string[(position + i) % len(string)] = digits[i]

            position = (position + length + skip_size) % len(string)
            skip_size += 1

    outputs = []

    i = 0
    while i < len(string):
        output = string[i]
        for j in range(i+1, i + 16):
            output = output ^ string[j]
        outputs.append(output)

        i += 16

    hash_string = [str(hex(x))[2:] for x in outputs]
    for i in range(len(hash_string)):
        if len(hash_string[i]) != 2:
            hash_string[i] = '0' + hash_string[i]
    return(''.join(hash_string))

import sys
import numpy as np

memory = []
on_bits = 0
for i in range(128):
    key_string = sys.argv[1] + '-' + str(i)
    hash_string = knot_hash(key_string)
    hash_bin = str(bin(int(hash_string, 16))[2:])
    while len(hash_bin) < 128:
        hash_bin = '0' + hash_bin
    memory.append([int(x) for x in hash_bin])

memory = np.array(memory)

def get_neighbors(coords):
    x = coords[0]
    y = coords[1]

    neighbors = [
                        (x + 0, y + 1),
        (x - 1, y + 0),                 (x + 1, y + 0),
                        (x + 0, y - 1)
    ]

    return [x for x in neighbors if x[0] >= 0 and x[0] <= 127 and x[1] >= 0 and x[1] <= 127]

groups = {}
curr_group = 2
coords_checked = []

print(memory[0:8,0:8])

for row in range(128):
    for col in range(128):
        if memory[row, col] != 1:
            continue
        
        groups[curr_group] = {(row, col)}
        memory[row, col] = curr_group
        coords_to_check = get_neighbors((row, col))

        while coords_to_check:
            coord = coords_to_check.pop()
            if memory[coord] != 0:
                groups[curr_group].add(coord)
                memory[coord] = curr_group
                coords_to_check.extend(
                    [x for x in get_neighbors(coord) if memory[x] == 1]
                )
                coords_to_check = list(set(coords_to_check))
        curr_group += 1

print(memory[0:8,0:8])
print(len(groups.keys()))