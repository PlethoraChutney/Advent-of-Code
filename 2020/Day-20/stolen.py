#!/usr/bin/env python3

import sys
from copy import deepcopy


def get_side(tile, side):
    if side == "top":
        return tile[0]
    if side == "bottom":
        return tile[-1][::-1]
    if side == "right":
        return "".join([t[-1] for t in tile])
    if side == "left":
        return "".join([t[0] for t in tile])[::-1]
    raise ValueError


def get_sides(tile):
    return [get_side(tile, "top"), get_side(tile, "right"), get_side(tile, "bottom"), get_side(tile, "left")]


def rotate(tile):
    R = len(tile)
    C = len(tile[0])
    new = [["x" for _ in range(C)] for _ in range(R)]
    for r in range(R):
        for c in range(C):
            new[r][c] = tile[C - c - 1][r]
    return ["".join(r) for r in new]


def flip(tile):
    return tile[::-1]


def add_fullpic(tile, newline=False):
    global fullpic
    if fullpic == []:
        fullpic = deepcopy(tile)
    elif newline:
        for r in tile:
            fullpic.append(r)
    else:
        R = len(fullpic) - len(tile)
        for r in range(len(tile)):
            fullpic[r + R] += tile[r]


with open(sys.argv[1], "r") as f:
    tiles_raw = f.read().strip().split("\n\n")

tiles = {}

for raw_tile in tiles_raw:
    lines = raw_tile.strip("\n").split("\n")
    idn = int(lines[0].split()[1].strip(":"))
    grid = lines[1:]
    sides = get_sides(grid)
    sides += [s[::-1] for s in sides]
    tiles[idn] = {"grid": grid, "sides": sides, "neighbors": {}}

    for i, tile in tiles.items():
        if i == idn:
            continue
        shared = [s for s in tile["sides"] if s in sides[:4]]
        for s in shared:
            tiles[idn]["neighbors"][i] = s
            tiles[i]["neighbors"][idn] = s

corners = list(map(int, [t for t in tiles if len(tiles[t]["neighbors"]) == 2]))
res = 1
for c in corners:
    res *= c

print(f"Part 1: {res}")

r, c = 0, 0
gridmap = {}
fullpic = []

while not len(gridmap) == len(tiles):
    if r == 0 and c == 0:
        idn = corners[0]
        tile = tiles[idn]["grid"]
        neighbors = list(tiles[idn]["neighbors"].values())
        neighbors += [n[::-1] for n in neighbors]
        while True:
            bottom, right = get_side(tile, "bottom"), get_side(tile, "right")
            if bottom in neighbors and right in neighbors:
                break
            tile = rotate(tile)
        gridmap[(r, c)] = idn
        tiles[idn]["grid"] = tile
        add_fullpic(tile)
        c += 1
    elif c == 0:
        p_idn = gridmap[(r - 1, c)]
        p_tile = tiles[p_idn]["grid"]
        side_options = [get_side(p_tile, "bottom"), get_side(p_tile, "bottom")[::-1]]
        idn = [i for i, s in tiles[p_idn]["neighbors"].items() if s in side_options][0]
        tile = tiles[idn]["grid"]
        n_side = get_side(tiles[p_idn]["grid"], "bottom")
        found = False
        for i in range(8):
            if i == 4:
                tile = flip(tile)
            if get_side(tile, "top") == n_side[::-1]:
                found = True
                break
            tile = rotate(tile)
        if not found:
            raise
        gridmap[(r, c)] = idn
        tiles[idn]["grid"] = tile
        add_fullpic(tile, newline=True)
        c += 1
    else:
        p_idn = idn
        p_tile = tiles[p_idn]["grid"]
        side_options = [get_side(p_tile, "right"), get_side(p_tile, "right")[::-1]]
        idn = [i for i, s in tiles[p_idn]["neighbors"].items() if s in side_options]
        if len(idn) == 1:
            idn = idn[0]
            tile = tiles[idn]["grid"]
            n_side = get_side(tiles[p_idn]["grid"], "right")
            found = False
            for i in range(8):
                if i == 4:
                    tile = flip(tile)
                if get_side(tile, "left") == n_side[::-1]:
                    found = True
                    break
                tile = rotate(tile)
            if not found:
                raise
            gridmap[(r, c)] = idn
            tiles[idn]["grid"] = tile
            add_fullpic(tile)
            c += 1
        elif len(idn) == 0:
            r, c = r + 1, 0
        else:
            raise Exception

G = []
for i in range(len(fullpic) // 10):
    G.extend(fullpic[(10 * i) + 1 : (10 * i) + 9])
G = ["".join([r[(10 * c) + 1 : (10 * c) + 9] for c in range(len(r) // 10)]) for r in G]

monster = [(0, 1), (1, 2), (4, 2), (5, 1), (6, 1), (7, 2), (10, 2), (11, 1),
           (12, 1), (13, 2), (16, 2), (17, 1), (18, 0), (18, 1), (19, 1)]

mon = set()
for i in range(8):
    if i == 4:
        G = flip(G)
    for r in range(len(G) - 2):
        for c in range(len(G[0]) - 20):
            if all([G[r + dr][c + dc] == "#" for dc, dr in monster]):
                for dc, dr in monster:
                    mon.add((r + dr, c + dc))
    G = rotate(G)

part2 = len([c for r in G for c in r if c == "#"]) - len(mon)
print(f"Part 2: {part2}")