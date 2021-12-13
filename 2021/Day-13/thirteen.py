import sys
import numpy as np

coords = []
instructions = []

with open(sys.argv[1], 'r') as f:
    for line in f:
        if ',' in line:
            coords.append(tuple([
                # because numpy is row, column indexing, it's backward
                # of the x, y indexing used in this puzzle.
                int(x) for x in line.rstrip().split(',')[::-1]
            ]))
        elif 'along' in line:
            if 'y' in line:
                instructions.append((
                    'u', 
                    int(line.strip().split('=')[1])
                    ))
            else:
                instructions.append((
                    'l', 
                    int(line.strip().split('=')[1])
                    ))

max_coord = (max(x[0] for x in coords) + 1, max(x[1] for x in coords) + 1)
manual = np.zeros(max_coord, dtype = int)

coords = np.array(coords).transpose()
manual[np.index_exp[tuple(coords)]] = 1

def fold_manual(direction, index):
    if direction == 'u':
        top = manual[:index,:]
        bottom = manual[:index:-1,:]
        if top.shape == bottom.shape:
            return np.bitwise_or(top, bottom)
        else:
            raise IndexError
    if direction == 'l':
        left = manual[:,:index]
        right = manual[:,:index:-1]
        if left.shape == right.shape:
            return np.bitwise_or(left, right)
        else:
            raise IndexError

manual = fold_manual(*instructions[0])

print(sum(manual.flatten()))

for i in range(1, len(instructions)):
    manual = fold_manual(*instructions[i])

def print_man(manual):
    for row in manual:
        print(str(row).replace('0', '.').replace('1', '#').replace('\n', ''))

print_man(manual)