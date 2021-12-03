import itertools
import sys
import numpy as np
import re
from collections import defaultdict
from itertools import chain

from numpy.core.numeric import full
from numpy.lib.index_tricks import ndindex

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
        self.all_full = False

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

    @property
    def image(self):
        # hard code tile shape b/c lazy
        im = []
        for row in range(1,9):
            im.append([int(x) for x in self.tile[row,1:9]])

        return im

tiles = []

for id_num, tile in tile_dict.items():
    tiles.append(Tile(id_num, tile))

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
        for y in range(self.size[1][1] - 2, self.size[1][0] + 1, -1):
            row = []
            for x in range(self.size[0][0] + 2, self.size[0][1] - 1):
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
        for tile in self.loose_tiles:
            if not any([x in needed_edges for x in tile.edges]):
                continue
            for _ in range(3):
                if self.add_tile(
                        self.loose_tiles.pop(self.loose_tiles.index(tile)),
                        index
                    ):
                    return True

                if all((needed_edges[0], needed_edges[2])) == 0:
                    tile.flip(1)
                    if self.validate_edges(tile, index):
                        self.add_tile(
                            self.loose_tiles.pop(self.loose_tiles.index(tile)),
                            index
                        )
                        return True

                if all((needed_edges[1], needed_edges[3])) == 0:
                    tile.flip(0)
                    if self.validate_edges(tile, index):
                        self.add_tile(
                            self.loose_tiles.pop(self.loose_tiles.index(tile)),
                            index
                        )
                        return True

                tile.rotate()

    @property
    def full_image(self):
        images = []
        full_image = []

        for lat in range(self.size[1][1], self.size[1][0], -1):
            for lon in range(self.size[0][0], self.size[0][1]):
                if self.grid[lon, lat].id == 0:
                    continue
                images.append(self.grid[lon, lat].image)

        side_size = int(len(images)**.5)
        for i in range(side_size):
            working_ims = images[side_size * i: 3+side_size*i]
            for j in range(len(working_ims[0])):
                full_image.append(list(chain(*[x[j] for x in working_ims])))

        return np.array(full_image)

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

if sys.argv[2] != 'noalign':
    tiles_changed = True
    while len(grid.loose_tiles) > 0 and tiles_changed:
        tiles_changed = False
        
        for fixed_index in list(grid.grid.keys()):
            if not grid.is_empty(fixed_index) and not grid.grid[fixed_index].all_full:
                neighbors = neighboring_indecies(fixed_index)
                if not any(grid.is_empty(x) for x in neighbors):
                    grid.grid[fixed_index].all_full = True
                    continue
                for index in neighbors:
                    if grid.is_empty(index):
                        tiles_changed = tiles_changed or grid.look_for_matches(index)
        print('-'*13)
        print(grid)
        print('-'*13)
            
    print(grid)
    print(f'Loose tiles: {[x.id for x in grid.loose_tiles]}')

    # part one

    corners = [
        (grid.size[0][0]+2, grid.size[1][0]+2),
        (grid.size[0][0]+2, grid.size[1][1]-2),
        (grid.size[0][1]-2, grid.size[1][0]+2),
        (grid.size[0][1]-2, grid.size[1][1]-2)
    ]

    r = 1
    for index in corners:
        r *= grid.grid[index].id
    print(f'Corner product: {r}')

# Part two

print('Finding sea monsters')

# monster_test is a binary representation of a sea monster
#
# if we & the test and the sub-region of the np array and get
# the monster back, then we know there are 1s in each relevant section
monster_ind = [
    (0,1), (0,4), (0,7), (0,10), (0,13), (0,16),
    (1,0), (1,5), (1,6), (1,11), (1,12), (1,17), (1,18), (1,19),
    (2,18)
]

def check_for_monster(image):
    monsters = 0
    for row, col in ndindex(image.shape):
        try:
            monster = [image[row + x[0], col + x[1]] for x in monster_ind]
            if all(monster):
                monsters += 1
        except IndexError:
            continue

    return monsters



def check_all_rotations(image):
    monsters = []
    for _ in range(3):
        monsters.append(check_for_monster(image))
        image = np.rot90(image)

    return monsters

def print_image(image):
    image = image.tolist()
    rows = []
    for row in image[::-1]:
        rows.append(''.join((str(x) for x in row)))
    print('\n'.join(rows).replace('0', '.').replace('1', '#'))

if sys.argv[2] == 'noalign':
    with open(sys.argv[1][:-4] + '_image.txt', 'r') as f:
        image = []
        for line in f:
            image.append(list(line.rstrip()))
    full_image = np.array(image, dtype = int)
else:
    full_image = grid.full_image
    with open(sys.argv[1][:-4] + '_image.txt', 'w') as f:
        for row in full_image.tolist():
            f.write(''.join([str(x) for x in row]) + '\n')

monsters = check_all_rotations(full_image)
if monsters == 0:
    full_image = np.fliplr(full_image)
    monsters = check_all_rotations(full_image)
if monsters == 0:
    full_image = np.flipud(full_image)
    monsters = check_all_rotations(full_image)
if monsters == 0:
    full_image = np.fliplr(full_image)
    monsters = check_all_rotations(full_image)

# each monster has 15 1s
print_image(full_image)
print(monsters)
print(sum(sum(full_image)) - 15 * monsters)
