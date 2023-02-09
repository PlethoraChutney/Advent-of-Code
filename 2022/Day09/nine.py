#!/usr/bin/env python3
import sys

# part one

with open(sys.argv[1], 'r') as f:
    instructions = [x.rstrip().split() for x in f]

instructions = [(x[0], int(x[1])) for x in instructions]

head = [0,0]
tail = [0,0]
tail_visits = []

def move_tail(head, tail):
    horizontal = abs(head[0] - tail[0])
    vertical = abs(head[1] - tail[1])
    
    if not (horizontal > 1 or vertical > 1):
        return tail
    
    # keep the sign but only move one space
    tail[0] += 0 if horizontal == 0 else int((head[0] - tail[0]) / horizontal)
    tail[1] += 0 if vertical == 0 else int((head[1] - tail[1]) / vertical)

    return tail

def parse_instruction(instruction):
    match instruction:
        case 'U':
            return [0, 1]
        case 'D':
            return [0, -1]
        case 'L':
            return [-1, 0]
        case 'R':
            return [1, 0]

for step in instructions:
    step_dir = parse_instruction(step[0])

    for _ in range(step[1]):
        head[0] += step_dir[0]
        head[1] += step_dir[1]

        tail = move_tail(head, tail)
        tail_visits.append(tuple(tail))

print(len(set(tail_visits)))

# part two

tail_visits = []

knot_positions = [[0,0] for x in range(10)]

for step in instructions:
    step_dir = parse_instruction(step[0])

    for _ in range(step[1]):
        # knot zero is the new head
        knot_positions[0][0] += step_dir[0]
        knot_positions[0][1] += step_dir[1]

        for knot in range(1, 10):
            # move all the other knots
            knot_positions[knot] = move_tail(knot_positions[knot - 1], knot_positions[knot])

        tail_visits.append(tuple(knot_positions[9]))

print(len(set(tail_visits)))