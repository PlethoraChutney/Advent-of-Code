import numpy as np
import re
import sys

def list_to_bin(list):
    b = 0
    for i in list:
        b = b << 1 | i

    return b

class Tile:
    def __init__(self, id, tile) -> None:
        self.id = id
        self.tile = np.array(tile)

    @property
    def edges(self):
        # edges should always be read left to right or top to bottom
        # since rotating *does* change the edge.

        right = self.tile[:,-1]
        top = self.tile[0,:]
        left = self.tile[::-1,0]
        bottom = self.tile[-1,::-1]

        # return a decimal just to make it easier for me to grok
        return [list_to_bin(x) for x in [right, top, left, bottom]]

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
        return str(self.edges)

    def rotate(self):
        self.tile = np.rot90(self.tile)

    # don't actually need to check both axes. Flipping
    # about x is the same as flipping y and rotating 180
    def flip(self, axis):
        self.tile = np.flip(self.tile, axis=axis)

tiles = []

with open(sys.argv[1], 'r') as f:
    for line in f:
        if line != '\n':
            line = line.rstrip()
            tile_match = re.match('Tile ([0-9]{4}):', line)
            if tile_match:
                try:
                    tiles.append(Tile(curr_tile_id, curr_tile))
                except NameError:
                    pass
                curr_tile_id = tile_match.group(1)
                curr_tile = []

            else:
                curr_tile.append([
                    x == '#' for x in line
                ])


