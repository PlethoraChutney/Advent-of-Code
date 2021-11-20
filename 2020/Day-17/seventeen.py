from itertools import product
import sys

class Cube:
    def __init__(self, coordinates, active = False) -> None:
        self.coordinates = coordinates
        self.active = active
        self.target_state = False

        x = self.coordinates[0]
        y = self.coordinates[1]
        z = self.coordinates[2]

        self.neighbors = list(product(*[
                [x-1, x, x+1],
                [y-1, y, y+1],
                [z-1, z, z+1]
            ]))

        self.neighbors.remove((x,y,z))

    def __repr__(self) -> str:
        if self.active:
            return '#'
        else:
            return '.'

    def prepare_update(self, grid):
        num_active = 0
        for coord in self.neighbors:
            if grid.get_cube(coord).active:
                num_active += 1

        if self.active:
            if num_active in [2,3]:
                self.target_state = True
            else:
                self.target_state = False
        else:
            if num_active == 3:
                self.target_state = True
            else:
                self.target_state = False

    def update_state(self):
        if self.active is None:
            raise ValueError(f'No target state for cube {self.coordinates}')
        else:
            self.active = self.target_state
            self.target_state = None


class Dimension:
    def __init__(self, initial_state) -> None:
        self.grid = {}
        for coord, state in initial_state.items():
            self.grid[coord] = Cube(coord, state)

        self.cycles = 0

    @property
    def shape(self):
        x = [i[0] for i in self.grid.keys()]
        y = [i[1] for i in self.grid.keys()]
        z = [i[2] for i in self.grid.keys()]

        return ((min(x), max(x)), (min(y), max(y)), (min(z), max(z)))

    @property
    def current_active(self):
        active = [x for x in self.grid.values() if x.active]
        return len(active)

    def __repr__(self) -> str:
        xr, yr, zr = self.shape
        zstack = []
        zstack.append(f'After {self.cycles} cycles:')
        for z in range(zr[0], zr[1] + 1):
            zstack.append(f'Z = {z}')
            rows = []
            for y in range(yr[0], yr[1] + 1):
                row = []
                for x in range(xr[0], xr[1] + 1):
                    state = self.get_cube((x,y,z)).active
                    if state:
                        row.append('#')
                    else:
                        row.append('.')
                rows.append(''.join(row))
            zstack.append('\n'.join(rows))

        return "\n".join(zstack)

    def get_cube(self, coordinate):
        try:
            return self.grid[coordinate]
        except KeyError:
            self.grid[coordinate] = Cube(coordinate)
            return self.grid[coordinate]

    def update_cubes(self):
        # do this twice, first to generate the neighboring cubes, then to
        # get the right update state for those neighbors
        for _ in range(2):
            cubes_to_update = []
            for cube in self.grid.values():
                cubes_to_update.append(cube)
            
            for cube in cubes_to_update:
                cube.prepare_update(self)

        for cube in self.grid.values():
            cube.update_state()

        self.cycles += 1


initial_state = {}
states = [x.rstrip() for x in open(sys.argv[1])]

for y, row in enumerate(states):
    for x, val in enumerate(row):
        if val == '#':
            initial_state[(x, y, 0)] = True
        else:
            initial_state[(x, y, 0)] = False

dim = Dimension(initial_state)

while dim.cycles < 6:
    dim.update_cubes()

print(dim.current_active)