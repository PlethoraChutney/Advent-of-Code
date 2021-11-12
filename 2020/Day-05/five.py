class Seat:
    def __init__(self, bording) -> None:
        self.bording = bording

        self.possible_rows = list(range(128))
        self.possible_columns = list(range(8))

    def front(self) -> None:
        half = int(len(self.possible_rows)/2)
        self.possible_rows = self.possible_rows[:half]

    def back(self) -> None:
        half = int(len(self.possible_rows)/2)
        self.possible_rows = self.possible_rows[half:]

    def left(self) -> None:
        half = int(len(self.possible_columns)/2)
        self.possible_columns = self.possible_columns[:half]

    def right(self) -> None:
        half = int(len(self.possible_columns)/2)
        self.possible_columns = self.possible_columns[half:]

    def get_id(self) -> int:
        for letter in self.bording:
            if letter == 'F':
                self.front()
            elif letter == 'B':
                self.back()
            elif letter == 'L':
                self.left()
            elif letter == 'R':
                self.right()

        if len(self.possible_rows) == 1 and len(self.possible_columns) == 1:
            return int(self.possible_rows[0] * 8 + self.possible_columns[0])
        else:
            print('Something has gone wrong with bording pass ' + self.bording)

bording_passes = []

with open('input.txt', 'r') as f:
    for line in f:
        bording_passes.append(Seat(line))
seat_ids = [bp.get_id() for bp in bording_passes]
print('Maximum: ' + str(max(seat_ids)))

possible_ids = []
for r in range(128):
    for c in range(8):
        possible_ids.append(r * 8 + c)

missing = set(possible_ids) - set(seat_ids)

for missing_id in missing:
    if missing_id - 1 not in missing and missing_id + 1 not in missing:
        print('Your seat is ' + str(missing_id))