#!/usr/bin/env python
import sys
import numpy as np
from uuid import uuid4

with open(sys.argv[1], "r") as f:
    lines = [x.rstrip() for x in f]

mountain = np.array([[int(y) for y in x] for x in lines])

class Hiker:
    def __init__(self, coordinate:tuple[int], uid = None, height = 0) -> None:
        self.coordinate = coordinate
        self.height = height
        self.uid = uuid4() if uid is None else uid

    def __repr__(self) -> str:
        return f"Hiker at ({self.coordinate[0]}, {self.coordinate[1]})"

    @property
    def neighbor_coords(self) -> list[tuple[int, int]]:
        potential_coords = [
            (self.coordinate[0], self.coordinate[1] + 1),
            (self.coordinate[0], self.coordinate[1] - 1),
            (self.coordinate[0] + 1, self.coordinate[1]),
            (self.coordinate[0] - 1, self.coordinate[1]),
        ]
        return [
            x for x in potential_coords
            if x[0] >= 0 and x[1] >= 0
        ]
    
    def take_step(self) -> list["Hiker"]:
        if self.height == 9:
            return [self]
        new_hikers = []
        for neighbor in self.neighbor_coords:
            try:
                if mountain[neighbor] == self.height + 1:
                    new_hikers.append(Hiker(neighbor, self.uid, self.height + 1))
            except IndexError:
                continue
        return new_hikers

trailheads = {}
initial_coords = zip(*np.where(mountain == 0))
for coord in initial_coords:
    hiker = Hiker(coord)
    trailheads[hiker.uid] = [hiker]

for height in range(9):
    for trail, hikers in trailheads.items():
        new_hikers = []
        for hiker in hikers:
            new_hikers.extend(hiker.take_step())
        trailheads[trail] = new_hikers

part_one = 0
for hikers in trailheads.values():
    part_one += len(set(h.coordinate for h in hikers))

print(f"Part one: {part_one}")

part_two = 0
for hikers in trailheads.values():
    part_two += len(hikers)

print(f"Part two: {part_two}")