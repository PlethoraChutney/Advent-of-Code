import sys
import re
import numpy as np

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

print(tiles)

# we'd like the Tile to be able to store rotations that are allowable
# for it under the current construction. For instance, if edge A matches
# something right now, you could also allow a flip along the A-C axis and 
# then a 180 rotation.

class Tile:
    def __init__(self, index, tile_list) -> None:
        self.index = index
        tile_list = [list(x) for x in tile_list]

        
        # Let's represent #/. as 1/0 instead to gain acess to matrix multiplication
        tile_list = [[int(x) for x in y] for y in tile_list]
        self.tile = np.matrix(tile_list)

    def __repr__(self) -> str:
        return str(self.tile)
    
for index, tile in tiles.items():
    tiles[index] = Tile(index, tile)

for tile in tiles:
    print(tiles[tile])