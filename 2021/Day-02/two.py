with open('input.txt', 'r') as f:
    depth = 0
    pos = 0
    aim = 0
    aim_depth = 0

    for line in f:
        line = line.rstrip()
        distance = int(line.split(' ')[1])
        if line[0] == 'f':
            pos += distance
            aim_depth += (aim * distance)
        elif line[0] == 'd':
            # part one
            depth += distance
            # part two
            aim += distance
        else:
            depth -= distance
            aim -= distance

print(depth * pos)
print(aim_depth * pos)