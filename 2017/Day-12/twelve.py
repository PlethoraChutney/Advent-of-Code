with open('input.txt', 'r') as f:
    lines = [x.rstrip().split(' <-> ') for x in f]

pipes = {x[0]: set(x[1].split(', ')) for x in lines}
for pipe in pipes:
    pipes[pipe].add(pipe)

groups = {}

for outer_pipe, outer_connections in pipes.items():
    if outer_pipe not in groups and not any(outer_pipe in x for x in groups.values()):
        groups[outer_pipe] = outer_connections
    else:
        continue

    modified = True
    while modified:
        modified = False

        for pipe, connections in pipes.items():
            if any(x in connections for x in groups[outer_pipe]) and pipe not in groups[outer_pipe]:
                groups[outer_pipe].add(pipe)
                modified = True

print(len(groups['0']))
print(len(groups))
