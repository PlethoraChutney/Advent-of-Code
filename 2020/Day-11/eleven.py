from itertools import chain
import sys

class Seat():
    def __init__(self, state) -> None:
        if state == '#':
            self.states = [False]
            self.is_floor = False
        elif state == 'L':
            self.states = [True]
            self.is_floor = False
        elif state == '.':
            self.states = [True]
            self.is_floor = True
        self.adjacent = []

    # we want to use a list so that as we iterate through
    # the cabin, seats a row down are looking at the same time
    # state as the first seats were. Basically, we don't want
    # seat [1,2] to see what seat [0,1] looks like *after* the
    # latter has already evolved states
    def get_empty(self, timestamp):
        return self.states[timestamp]

    def __repr__(self) -> str:
        if self.is_floor:
            return '.'
        elif self.get_empty(-1):
            return 'L'
        else:
            return "#"

    def set_adjacent(self, seat):
        self.adjacent.append(seat)

    def evolve_state(self, timestamp) -> None:
        if self.is_floor:
            self.states.append(True)
            return

        neighbors_empty = [x.get_empty(timestamp) for x in self.adjacent]
        empty = self.get_empty(timestamp)
        if empty and all(neighbors_empty):
            self.states.append(False)
        elif not empty and len([x for x in neighbors_empty if not x]) >= 5:
            self.states.append(True)
        else:
            self.states.append(empty)

    def get_stable(self, timestamp) -> bool:
        if timestamp == 0:
            return False
        else:
            return self.states[timestamp] == self.states[timestamp-1]

seats = []
with open('input.txt', 'r') as f:
    for line in f:
        row = []
        for char in line.rstrip():
            row.append(Seat(char))
        seats.append(row)

for row in range(len(seats)):
    for col in range(len(seats[row])):
        # I realize now I didn't arrange these right. Whatever.
        potential_adjacents = (
            (-1, -1), (-1, 0), (-1, +1),
            (0, -1),           (0, +1),
            (+1, -1), (+1, 0), (+1, +1)
        )
        for x, y in potential_adjacents:
            try:
                u = row + x
                v = col + y
                while True:
                    assert u >= 0 and v >= 0
                    if not seats[u][v].is_floor:
                        seats[row][col].set_adjacent(seats[u][v])
                        break
                    else:
                        u += x
                        v += y
            except (IndexError, AssertionError):
                continue

# flatten seats

all_stable = False
i = 0
while not all_stable:
    all_stable = all([x.get_stable(i) for x in chain(*seats)])
    for row in seats:
        for seat in row:
            seat.evolve_state(i)
    i += 1

for x in seats:
    print(list(len(y.adjacent) for y in x))
print()
for x in seats:
    print(list(y for y in x))

print(sum(1 for x in chain(*seats) if not x.get_empty(-1)))
