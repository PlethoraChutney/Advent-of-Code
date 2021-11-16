import numpy as np

east = np.array([1,0])
west = np.array([-1,0])
north = np.array([0,1])
south = np.array([0,-1])

class Ship:
    def __init__(self) -> None:
        self.location = np.array([0,0])
        self.rotation = 0
        self.waypoint = np.array([10,1])

    def execute_instruction_one(self, instruction):
        dir = instruction[0]
        value = int(instruction[1:])

        if dir == 'N':
            self.location += value * north
        elif dir == 'S':
            self.location += value * south
        elif dir == 'E':
            self.location += value * east
        elif dir == 'W':
            self.location += value * west
        elif dir == 'L':
            self.rotation += value
            self.rotation = self.rotation % 360
        elif dir == 'R':
            self.rotation -= value
            self.rotation = self.rotation % 360
        elif dir == 'F':
            if self.rotation == 0:
                facing = east
            elif self.rotation == 90:
                facing = north
            elif self.rotation == 180:
                facing = west
            elif self.rotation == 270:
                facing = south
            
            self.location += value * facing

    def execute_instruction_two(self, instruction):
        dir = instruction[0]
        value = int(instruction[1:])

        if dir == 'N':
            self.waypoint += value * north
        elif dir == 'S':
            self.waypoint += value * south
        elif dir == 'E':
            self.waypoint += value * east
        elif dir == 'W':
            self.waypoint += value * west
        elif dir == 'R':
            times = int(value / 90)
            for i in range(times):
                self.waypoint = np.matmul(
                    self.waypoint, np.array([[0,-1],[1,0]])
                    )
        elif dir == 'L':
            times = int(value/90)
            for i in range(times):
                self.waypoint = np.matmul(
                    self.waypoint, np.array([[0,1],[-1,0]])
                    )
        elif dir == 'F':
            self.location += value * self.waypoint


    def manh_dist(self):
        return np.abs(self.location).sum()

ship = Ship()
new_ship = Ship()

with open('input.txt', 'r') as f:
    for line in f:
        ship.execute_instruction_one(line.rstrip())
        new_ship.execute_instruction_two(line.rstrip())

print(ship.manh_dist())
print(new_ship.manh_dist())