import sys
import numpy as np
import re
from collections import defaultdict
from itertools import product

from numpy.lib.ufunclike import fix

tile_dict = {}

with open(sys.argv[1], 'r') as f:
    for line in f:
        line = line.rstrip()
        if line != '':
            tile_match = re.match('Tile ([0-9]{4}):', line)
            if tile_match:
                curr_tile = tile_match.group(1)
                tile_dict[curr_tile] = []

            else:
                tile_dict[curr_tile].append(line.replace('#', '1').replace('.', '0'))

class Tile:
    def __init__(self, id_num, tile) -> None:
        self.id = int(id_num)
        
        tile = [list(x) for x in tile]
        self.tile = np.array(tile)
        self.locked = False

    @property
    def edges(self):
        # edges should always be read left to right or top to bottom
        # since rotating *does* change the edge.

        right = self.tile[:,-1]
        top = self.tile[0,:]
        left = self.tile[:,0]
        bottom = self.tile[-1,:]

        # return a decimal just to make it easier for me to grok
        return [int(''.join(x), 2) for x in [right, top, left, bottom]]

    # ease of use
    @property
    def right(self):
        return self.edges[0]
    @property
    def top(self):
        return self.edges[1]
    @property
    def left(self):
        return self.edges[2]
    @property
    def bottom(self):
        return self.edges[3]

    def __repr__(self) -> str:
        mid = f'{self.left} | {self.id:04} | {self.right}'
        top = '{edge:^{width}}'.format(edge = self.top, width = len(mid))
        bottom = '{edge:^{width}}'.format(edge = self.bottom, width = len(mid))
        return '\n'.join([top, mid, bottom])

    def rotate(self):
        if self.locked:
            raise ValueError('Cannot rotate a locked tile.')
        self.tile = np.rot90(self.tile)

    def flip(self, axis):
        if self.locked:
            raise ValueError('Cannot flip a locked tile.')
        self.tile = np.flip(self.tile, axis=axis)

tiles = []

for id_num, tile in tile_dict.items():
    tiles.append(Tile(id_num, tile))

print(len(tiles))

all_zeros = ['0'*10]*20

class Grid:
    def __init__(self, tiles) -> None:
        self.grid = defaultdict(lambda: Tile(0, all_zeros))
        self.loose_tiles = tiles

    @property
    def size(self):
        try:
            x_ind = [x[0] for x in self.grid.keys()]
            y_ind = [x[1] for x in self.grid.keys()]

            min_x = min(x_ind)
            max_x = max(x_ind)
            min_y = min(y_ind)
            max_y = max(y_ind)

            return ((min_x, max_x), (min_y, max_y))
        except ValueError:
            return ((0,0), (0,0))

    def __repr__(self) -> str:
        grid = []
        # mess with ranges to ignore the very edge columns/rows, which
        # should all be empty (i.e., zero tiles)
        for y in range(self.size[1][1] - 1, self.size[1][0], -1):
            row = []
            for x in range(self.size[0][0] + 1, self.size[0][1]):
                row.append('{id:04}'.format(id = self.grid[(x,y)].id))
            grid.append(' | '.join(row))

        return '\n'.join(grid)

    def is_empty(self, index):
        return self.grid[index].id == 0

    def get_neighbor_edges(self, index) -> tuple:
        right = self.grid[(index[0] + 1, index[1])].left
        up = self.grid[(index[0], index[1]+1)].bottom
        left = self.grid[(index[0] - 1, index[1])].right
        down = self.grid[(index[0], index[1] -1)].top

        return (right, up, left, down)

    def validate_edges(self, tile, index) -> bool:
        neighbor_edges = self.get_neighbor_edges(index)

        try:
            for i in range(4):
                if neighbor_edges[i] != 0:
                    assert tile.edges[i] == neighbor_edges[i]
            return True
        except AssertionError:
            return False


    def add_tile(self, tile, index):
        if self.grid[index].id != 0:
            self.loose_tiles.append(tile)
            raise ValueError(f'Tried to place tile over existing tile at {index}.')            

        if not self.validate_edges(tile, index):
            self.loose_tiles.append(tile)
            return False
        else:
            self.grid[index] = tile

    def look_for_matches(self, index):
        needed_edges = self.get_neighbor_edges(index)
        possible_tiles = []
        for tile in self.loose_tiles:
            for _ in range(3):
                if self.validate_edges(tile, index):
                    possible_tiles.append(tile)
                    break

                if all((needed_edges[0], needed_edges[2])) == 0:
                    tile.flip(1)
                    if self.validate_edges(tile, index):
                        possible_tiles.append(tile)
                        break

                if all((needed_edges[1], needed_edges[3])) == 0:
                    tile.flip(0)
                    if self.validate_edges(tile, index):
                        possible_tiles.append(tile)
                        break

                tile.rotate()

        if len(possible_tiles) == 1:
            self.add_tile(self.loose_tiles.pop(self.loose_tiles.index(possible_tiles[0])), index)
            return True
        else:
            return False

def neighboring_indecies(i):
    return (
        (i[0], i[1] + 1),
        (i[0] - 1, i[1]), (i[0] + 1, i[1]),
        (i[0], i[1] - 1)
    )

grid = Grid(tiles)

# pick a random tile to be (0,0)
grid.add_tile(tiles.pop(0), (0,0))
print(grid)
print('Matching:')

tiles_changed = True
while len(grid.loose_tiles) > 0 and tiles_changed:
    tiles_changed = False
    for fixed_index in list(grid.grid.keys()):
        if not grid.is_empty(fixed_index):
            for index in neighboring_indecies(fixed_index):
                    tiles_changed = tiles_changed or grid.look_for_matches(index)
        
print(grid)
print([x.id for x in grid.loose_tiles])
