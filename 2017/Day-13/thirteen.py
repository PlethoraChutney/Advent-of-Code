import sys

def calc_scanner_position(time, scanner_range):
    time = time % (2*scanner_range)
    if time <= scanner_range:
        position = time
    else:
        position = scanner_range - (time - scanner_range)

    return position

severity = 0
with open(sys.argv[1], 'r') as f:
    lines = [x.rstrip().split(': ') for x in f]

lines = tuple((int(x[0]), int(x[1]) - 1) for x in lines)

delay = 0
caught = True
while caught:
    caught = False
    delay += 1
    for line in lines:
        depth, scanner_range = line
        scanner_position = calc_scanner_position(depth + delay, scanner_range)
        if scanner_position == 0:
            caught = True
            break

print(delay)