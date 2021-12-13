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
        # select top up to index
        top = manual[:index,:]
        # select bottom up to index, reversing the order of rows to simulate a fold
        bottom = manual[:index:-1,:]
        # it turns out this check isn't necessary, but theoretically I could have had
        # to write a quick catch here to pad the top or bottom with zeros
        if top.shape == bottom.shape:
            return np.bitwise_or(top, bottom)
        else:
            raise IndexError
    if direction == 'l':
        # same thing but left or right
        left = manual[:,:index]
        right = manual[:,:index:-1]
        if left.shape == right.shape:
            return np.bitwise_or(left, right)
        else:
            raise IndexError

# part one answer
manual = fold_manual(*instructions[0])
print(sum(manual.flatten()))

# run the rest of the folds
for i in range(1, len(instructions)):
    manual = fold_manual(*instructions[i])

# need to replace the newlines here because numpy inserts newlines even if you
# set the maximum print width to infinite. Annoying.
def print_man(manual):
    for row in manual:
        print(str(row).replace('0', '.').replace('1', '#').replace('\n', ''))

# part two answer is an image of letters made by the # symbols in the output
print_man(manual)