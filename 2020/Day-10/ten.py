import sys

adapters = [int(x.rstrip()) for x in open(sys.argv[1])]
adapters.append(0)
adapters.sort()

paths = []

differences = {
    1: 0,
    2: 0,
    3: 0
}

for i in range(len(adapters)):
    try:
        difference = adapters[i+1] - adapters[i]
    except IndexError:
        difference = 3 # from my phone

    differences[difference] += 1

    j = i + 1
    path_from_here = 0
    try:
        while adapters[j] - adapters[i] <= 3:
            path_from_here += 1
            j += 1
    except IndexError:
        if path_from_here == 0:
            path_from_here = 1

    paths.append(path_from_here-1)
    print(f'Paths from {adapters[i]}: {path_from_here}')


print(differences)
print('Part one: ' + str(differences[1] * differences[3]))

# add one for the trivial case
print('All arrangements: ' + str(sum(paths) + 1))