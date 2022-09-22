with open('input.txt', 'r') as f:
    steps = f.readline().rstrip().split(',')

print(steps[:5])

def solve_distance(steps):
    modified = True
    while modified:
        modified = False
        while 'ne' in steps:
            if 'sw' in steps:
                steps.remove('ne')
                steps.remove('sw')
                modified = True
            elif 's' in steps:
                steps.remove('ne')
                steps.remove('s')
                steps.append('se')
                modified = True
            elif 'nw' in steps:
                steps.remove('ne')
                steps.remove('nw')
                steps.append('n')
                modified = True
            else:
                break
        while 'n' in steps:
            if 's' in steps:
                steps.remove('n')
                steps.remove('s')
                modified = True
            elif 'se' in steps:
                steps.remove('n')
                steps.remove('se')
                steps.append('ne')
                modified = True
            elif 'sw' in steps:
                steps.remove('n')
                steps.remove('sw')
                steps.append('nw')
                modified = True
            else:
                break
        while 'nw' in steps:
            if 'se' in steps:
                steps.remove('nw')
                steps.remove('se')
                modified = True
            elif 'ne' in steps:
                steps.remove('nw')
                steps.remove('ne')
                steps.append('n')
                modified = True
            elif 's' in steps:
                steps.remove('nw')
                steps.remove('s')
                steps.append('sw')
                modified = True
            else:
                break
        while 'se' in steps:
            if 'sw' in steps:
                steps.remove('se')
                steps.remove('sw')
                steps.append('s')
            else:
                break

    return len(steps)

print(solve_distance(steps[:]))

distances = []
print('Solving path:')
for i in range(len(steps)):
    print(f'Solving step {i} of {len(steps)}', end = '\r')
    distances.append(solve_distance(steps[:i+1]))
print()
print(max(distances))
