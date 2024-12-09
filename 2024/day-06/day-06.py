#!/usr/bin/env python
import sys
import numpy as np

with open(sys.argv[1], "r") as f:
    lines = [list(x.rstrip()) for x in f]

class Grid:

    movement = {
        # (i, j) indexing, not (x, y)
        "up": np.array([-1, 0]),
        "right": np.array([0, 1]),
        "down": np.array([1, 0]),
        "left": np.array([0, -1])
    }

    def __init__(
            self,
            grid:np.ndarray,
            guard_position:list[int, int],
            direction:str,
            movement_record:dict[str, np.ndarray],
            time_travel = False
            ) -> None:
        self.grid = grid
        self.guard_position = guard_position
        self.direction = direction
        self.movement_record = movement_record
        self.in_loop = False
        self.time_travel = time_travel

    @classmethod
    def base_grid(self, base_grid:np.ndarray) -> None:
        grid = np.zeros(base_grid.shape, dtype = int)
        gx, gy = np.nonzero(base_grid == "^")
        guard_position = [gx[0], gy[0]]
        grid[*guard_position] = 1
        grid[base_grid == "#"] = -1
        direction = "up"

        movement_record = {
            k: np.zeros_like(grid)
            for k in self.movement.keys()
        }

        return Grid(grid, guard_position, direction, movement_record, time_travel = True)
    
    def copy_self(self) -> "Grid":
        return Grid(
            self.grid.copy(),
            self.guard_position[:],
            self.direction,
            {k: v.copy() for k, v in self.movement_record.items()}
        )

    @property
    def gx(self) -> int:
        return self.guard_position[0]
    
    @property
    def gy(self) -> int:
        return self.guard_position[1]

    def coord_in_grid(self, coord) -> bool:
        x, y = coord
        xlim, ylim = self.grid.shape
        return x < xlim and x >= 0 and y < ylim and y >= 0
    
    def turn_guard(self) -> None:
        directions = list(self.movement.keys())
        cur_dir = directions.index(self.direction)
        self.direction = directions[(cur_dir + 1) % len(directions)]

    def show_grid(self) -> None:
        for i, row in enumerate(self.grid):
            printstr = []
            for j, cell in enumerate(row):
                if i == self.guard_position[0] and j == self.guard_position[1]:
                    printstr.append("^")
                elif cell == 0:
                    printstr.append("\u2591")
                elif cell == -1:
                    printstr.append("\u2588")
                elif cell == 1:
                    movements = {
                        d: self.movement_record[d][i, j]
                        for d in self.movement.keys()
                    }
                    if movements["up"]:
                        printstr.append("\u2191")
                    elif movements["right"]:
                        printstr.append("\u2192")
                    elif movements["down"]:
                        printstr.append("\u2193")
                    elif movements["left"]:
                        printstr.append("\u2190")
                    else:
                        printstr.append("\u2593")
            print("".join(printstr))

    def is_obstacle(self, coord:np.ndarray) -> bool:
        try:
            return self.grid[coord] == -1
        except IndexError:
            # let the guard leave the grid
            return False
        
    def check_for_loop(self) -> bool:
        if self.movement_record[self.direction][*self.guard_position] == 1:
            self.in_loop = True
            return True

    def move_guard(self) -> tuple[int, int]:
        next_coord = self.guard_position + self.movement[self.direction]
        next_coord = (next_coord[0], next_coord[1])
        subloop = False
        if self.coord_in_grid(next_coord):
            if self.check_for_loop():
                return
            
            if self.is_obstacle(next_coord):
                self.turn_guard()
                return self.move_guard()
            elif self.time_travel and self.grid[next_coord] != 1:
                subgrid = self.copy_self()
                subgrid.time_travel = False
                subgrid.grid[next_coord] = -1
                subloop, _, _ = subgrid.simulate_guard()
            
            self.movement_record[self.direction][self.guard_position[0], self.guard_position[1]] = 1
            self.guard_position = next_coord
            self.grid[next_coord] = 1
        else:
            self.guard_position = next_coord

        return next_coord if subloop else False


    def simulate_guard(self, debug = False) -> tuple[bool, int]:
        loop_obstacle_coords = set()
        steps = 0

        while self.coord_in_grid(self.guard_position) and not self.in_loop:
            if debug:
                steps += 1
                if self.time_travel:
                    print(f"Steps: {steps:0>4}", end = "\r")
            subloop = self.move_guard()
            if self.time_travel and subloop:
                loop_obstacle_coords.add(subloop)

        if self.time_travel and debug:
            print("")
        return (self.in_loop, np.sum(self.grid == 1), loop_obstacle_coords)

grid = Grid.base_grid(np.array(lines))
grid.time_travel = False
_, moves, _ = grid.simulate_guard()
grid.show_grid()
print(f"Part one: {np.sum(grid.grid == 1)}")

grid = Grid.base_grid(np.array(lines))
loop, moves, tt_coords = grid.simulate_guard()
print(f"Part two: {len(tt_coords)}")
