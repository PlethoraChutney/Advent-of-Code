import sys
import numpy as np
import re
from collections import defaultdict

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
        # locked will tell us if we need to worry about anything while flipping
        # tiles that are already in the board. For instance, if we have a tile that
        # is attached only at the bottom, we may want to flip it horizontally. However,
        # if we do that, we need to rotate it twice as well.
        #
        # [locked_horiz, locked_vert]
        self.locked = [False, False]

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

    def rotate(self, force = False):
        if any(self.locked) and not force:
            raise ValueError('Cannot rotate a locked tile.')
        self.tile = np.rot90(self.tile)

    def flip(self, axis):
        if not any(self.locked):
            self.tile = np.flip(self.tile, axis=axis)
        # `axis - 1` always checks the other axis, since 0 - 1 = -1,
        # which is the last (i.e., second) value
        elif self.locked[axis-1] and not self.locked[axis]:
            print('Flipping and rotating')
            self.tile = np.flip(self.tile, axis = axis)
            self.rotate(True)
            self.rotate(True)
        else:
            raise ValueError(f'Tried to flip a locked tile on axis {axis}')

tiles = []

for id_num, tile in tile_dict.items():
    tiles.append(Tile(id_num, tile))

print(tiles[0])
tiles[0].locked[0] = True
tiles[0].flip(1)
print(tiles[0])

all_zeros = ['0'*10]*20

class Grid:
    def __init__(self) -> None:
        self.grid = defaultdict(lambda: Tile(0, all_zeros))

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
        for y in range(self.size[1][0], self.size[1][1]):
            row = []
            for x in range(self.size[0][0], self.size[0][1]):
                row.append(self.grid[(x,y)].id_num)
            grid.append(row)

        return str(grid)

    def add_tile(self, tile):
        pass


grid = Grid()

# pick a random tile to be (0,0)