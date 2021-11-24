import sys
import re
import numpy as np
from itertools import combinations
from collections import defaultdict

tiles = {}
with open(sys.argv[1], 'r') as f:
    for line in f:
        line = line.rstrip()
        tile_match = re.match('Tile ([0-9]+):', line)
        if tile_match:
            curr_tile = tile_match.group(1)
            tiles[curr_tile] = []
        elif line != '':
            tiles[curr_tile].append(line.replace('#', '1').replace('.', '0'))

class Tile:
    def __init__(self, index, tile_list) -> None:
        self.index = index

        self.rotation = 0
        self.yflip = False
        self.xflip = False

        tile_list = [list(x) for x in tile_list]        
        # Let's represent #/. as 1/0 instead to gain acess to matrix multiplication
        tile_list = [[int(x) for x in y] for y in tile_list]
        self.__tile = np.array(tile_list)

        self.position = None

    def __repr__(self) -> str:
        return str(self.tile)

    def rotate(self, times = 1):
        self.rotation += times
        self.rotation = self.rotation % 4
        return self

    def flip_y(self):
        self.yflip = not self.yflip
        return self

    def flip_x(self):
        self.xflip = not self.xflip
        return self

    @property
    def tile(self):
        if self.xflip:
            trans_tile = np.fliplr(self.__tile)
        else:
            trans_tile = self.__tile

        if self.yflip:
            trans_tile = np.flipud(trans_tile)
        
        trans_tile = np.rot90(trans_tile, k = self.rotation)

        return trans_tile

    @property
    def edges(self):
        # top, right, bottom, left
        tile = self.tile
        return [tile[0,:], tile[:,-1], tile[-1,::-1], tile[-1::-1,0]]

    def log_edges(self, edge_dict):
        for y in [False, True]:
            self.yflip = y
            for x in [False, True]:
                self.xflip = x
                for i in range(4):
                    edge_dict[str(self.edges[i])].append((self.index, x, y, i))

for index, tile in tiles.items():
    tiles[index] = Tile(index, tile)

edge_dict = defaultdict(lambda: [])

for tile in tiles.values(): 
    tile.log_edges(edge_dict)

print(tiles['2311'])

for edge, directions in edge_dict.items():
    print(edge)
    for d in directions:
        print(d)