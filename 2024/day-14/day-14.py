#!/usr/bin/env python
import sys
import re
import numpy as np

with open(sys.argv[1], "r") as f:
    lines = [x.rstrip() for x in f]

if sys.argv[1] == "test.txt":
    grid_size = np.array([11, 7])
else:
    grid_size = np.array([101, 103])

robots = []
for line in lines:
    if not line:
        continue
    position, velocity = re.match(r"p=([,0-9]+) v=([-0-9,]+)", line).groups()
    position = np.array(list(int(x) for x in position.split(",")))
    velocity = np.array(list(int(x) for x in velocity.split(",")))

    robots.append({"position": position, "velocity": velocity})

def simulate_robot(robot:dict, time:int) -> tuple[int]:
    position = robot["position"]
    velocity = robot["velocity"]
    offset = np.array(velocity) * time
    return tuple(np.mod(position + offset, grid_size))

final_positions = []
for robot in robots:
    final_positions.append(simulate_robot(robot, 100))

grid = np.zeros(grid_size[::1], int)
for coord in final_positions:
    grid[coord[0], coord[1]] += 1

# np does i,j not x, y and counts from top
grid = np.flipud(np.rot90(grid))

half_points = np.array(grid.shape) // 2
def split_lr(grid, hsplit):
    return grid[:hsplit, :], grid[hsplit + 1:, :]
def split_ud(grid, vsplit):
    return grid[:, :vsplit], grid[:, vsplit + 1:]

left, right = split_lr(grid, half_points[0])
ul, bl = split_ud(left, half_points[1])
ur, br = split_ud(right, half_points[1])

pt_one = np.prod([np.sum(ul), np.sum(bl), np.sum(ur), np.sum(br)])
print(f"Part one: {pt_one}")

# looking for cycles I assume...?