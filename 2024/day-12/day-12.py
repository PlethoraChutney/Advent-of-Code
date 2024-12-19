#!/usr/bin/env python
import sys
import numpy as np

with open(sys.argv[1], "r") as f:
    lines = [x.rstrip() for x in f]

farm = np.array(list([ord(x) for x in y] for y in lines))
have_measured = np.zeros_like(farm).astype(bool)
farm_x, farm_y = farm.shape

def in_grid(coord:tuple[int]) -> bool:
    return coord[0] >= 0 and coord[1] >= 0 and coord[0] < farm_x and coord[1] < farm_y

def n_coords(coord:tuple[int]) -> list[tuple[int]]:
    x, y = coord
    return [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)
    ]

def get_neighbors(coord:tuple[int], known_coords:set = set()) -> set[tuple[int]]:
    crop_type = farm[coord]
    potential_neighbors = n_coords(coord)

    neighbors = []
    for neighbor in potential_neighbors:
        if (in_grid(neighbor) and neighbor not in known_coords and farm[neighbor] == crop_type):
            neighbors.append(neighbor)

    return set(neighbors)

def find_region(coord:tuple[int]) -> set[tuple[int]]:

    if have_measured[coord]:
        raise ValueError
    region = set([coord])

    new_neighbors = get_neighbors(coord, region)
    region.update(new_neighbors)

    while new_neighbors:
        additional_new_neighbors = set()
        for n in new_neighbors:
            additional_new_neighbors.update(get_neighbors(n, region))
        region.update(additional_new_neighbors)
        new_neighbors = additional_new_neighbors

    for coord in region:
        have_measured[coord] = True

    return region

region_id = 0
regions = {}
for x in range(farm_x):
    for y in range(farm_y):
        if have_measured[(x, y)]:
            continue
        regions[region_id] = find_region((x, y))
        region_id += 1

def get_region_cost(region_coords:set[tuple[int]]) -> int:
    area = len(region_coords)
    perim = 0
    for square in region_coords:
        perim += 4
        for neighbor in n_coords(square):
            if neighbor in region_coords:
                perim -= 1

    return area * perim

total_cost = 0
for region in regions.values():
    total_cost += get_region_cost(region)

print(f"Part one: {total_cost}")


# part two

class Farmplot:
    def __init__(self, coord:tuple[int]):
        self.coord = coord
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False
        self.find_fences()

    def find_fences(self):
        right, left, top, bottom = n_coords(self.coord)
        direction = {
            "right": {"coord": right},
            "left": {"coord": left},
            "top": {"coord": top},
            "bottom": {"coord": bottom}
        }
        


def cost_by_sides(region_coords:set[tuple[int]]) -> int:
    area = len(region_coords)
    num_segments = 0
    min_x_coord = min(c[0] for c in region_coords) - 1
    max_x_coord = max(c[0] for c in region_coords) + 1
    min_y_coord = min(c[1] for c in region_coords) - 1
    max_y_coord = max(c[1] for c in region_coords) + 1
    
    for x in range(min_x_coord, max_x_coord):
        for y in range(min_y_coord, max_y_coord):
            array = np.array([
                [(x, y) in region_coords, (x + 1, y) in region_coords],
                [(x, y + 1) in region_coords, (x + 1, y + 1) in region_coords]
            ])


    return num_segments

print(cost_by_sides(regions[0]))

print(f"Part two: {total_cost}")