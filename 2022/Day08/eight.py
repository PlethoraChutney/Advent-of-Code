import numpy as np

with open('input.txt', 'r') as f:
    grid = np.array([[int(x) for x in y.rstrip()] for y in f])

rows, cols = grid.shape

edges = np.ones_like(grid)
edges[1:-1,1:-1] = 0

top_vis = np.ones_like(grid)

top_view = np.ones_like(grid)

top_pad = grid.copy()
for i in range(cols):
    top_pad = np.pad(
        top_pad,
        pad_width = 1,
        mode = 'constant',
        constant_values=-1
    )[:-2,1:-1]

    top_vis = (grid > top_pad) & top_vis

    curr_ind = np.full_like(top_view, i + 1)
    not_set = np.equal(top_view, np.ones_like(top_view)).astype(int)
    ind_for_not_set = np.multiply(curr_ind, not_set)
    is_blocked = np.greater_equal(grid, top_pad)
    adjustment = (ind_for_not_set * is_blocked) - 1
    
    top_view = np.add(
        curr_ind,
        adjustment
    )

bottom_vis = np.ones_like(grid)
bottom_pad = grid.copy()
for i in range(cols):
    bottom_pad = np.pad(
        bottom_pad,
        pad_width = 1,
        mode = 'constant',
        constant_values=-1
    )[2:,1:-1]

    bottom_vis = (grid > bottom_pad) & bottom_vis

left_vis = np.ones_like(grid)
left_pad = grid.copy()
for i in range(cols):
    left_pad = np.pad(
        left_pad,
        pad_width = 1,
        mode = 'constant',
        constant_values=-1
    )[1:-1,:-2]

    left_vis = (grid > left_pad) & left_vis

right_vis = np.ones_like(grid)
right_pad = grid.copy()
for i in range(cols):
    right_pad = np.pad(
        right_pad,
        pad_width = 1,
        mode = 'constant',
        constant_values=-1
    )[1:-1,2:]

    right_vis = (grid > right_pad) & right_vis

all_vis = top_vis | bottom_vis | left_vis | right_vis | edges

print('Part 1:', sum(all_vis.flatten()))

# Part two ------------------------------------------------------

def calc_viewing_distance(grid:np.array, x_coord, y_coord):
    height = grid[x_coord,y_coord]
    cols, rows = grid.shape

    x = x_coord
    left_vis = 0
    while x > 0:
        left_vis += 1
        x -= 1
        if grid[x,y_coord] >= height:
            break
    if left_vis == 0:
        return 0

    x = x_coord
    right_vis = 0
    while x < cols - 1:
        right_vis += 1
        x += 1
        if grid[x, y_coord] >= height:
            break
    if right_vis == 0:
        return 0
    
    y = y_coord
    bottom_vis = 0
    while y > 0:
        bottom_vis += 1
        y -= 1
        if grid[x_coord, y] >= height:
            break
    if bottom_vis == 0:
        return 0
    
    y = y_coord
    top_vis = 0
    while y < rows - 1:
        top_vis += 1
        y += 1
        if grid[x_coord, y] >= height:
            break
    if top_vis == 0:
        return 0

    total_vis = left_vis * right_vis * top_vis * bottom_vis

    return total_vis

max_score = 0

for x in range(0, cols):
    for y in range(0, cols):
        max_score = max(max_score, calc_viewing_distance(grid, x, y))

print('Part two:', max_score)