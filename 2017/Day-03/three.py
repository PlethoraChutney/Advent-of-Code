import sys

target = int(sys.argv[1])
position = 1
x = 0
y = 0
ring = 0

grid = {}
grid[(0, 0)] = 1

def get_value(grid, position):
    x = position[0]
    y = position[1]

    adjacents = [
        (x - 1, y + 1), (x + 0, y + 1), (x + 1, y + 1),
        (x - 1, y + 0), (x + 0, y + 0), (x + 1, y + 0),
        (x - 1, y - 1), (x + 0, y - 1), (x + 1, y - 1)
    ]

    total = 0
    for adj in adjacents:
        position_val = grid.get(adj)
        if position_val is None:
            position_val = 0
        total += position_val

    return total

while True:
    if position == target:
        print('Part one:', abs(x) + abs(y))
    
    if x == ring and y == -ring:
        ring += 1
        x += 1
    elif x == ring:
        if y == ring:
            x -= 1
        else:
            y += 1
    elif y == ring:
        if x == -ring:
            y -= 1
        else:
            x -= 1
    elif x == -ring:
        if y == -ring:
            x += 1
        else:
            y -= 1
    elif y == -ring:
        x += 1
    
    new_position_val = get_value(grid, (x, y))
    grid[(x, y)] = new_position_val
    if new_position_val > target:
        print('Part two:', new_position_val)
        break
    
    position += 1