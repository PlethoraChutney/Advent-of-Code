#!/usr/bin/env python
import sys

with open(sys.argv[1], "r") as f:
    disc_spec = [x.rstrip() for x in f][0]

disc_spec = [int(x) for x in disc_spec]

# try the naive way

class File:
    def __init__(self, index:int, position:int, length: int):
        self.index = index
        self.position = position
        self.length = length
        self.id = i // 2
        self.start_filled = index % 2 == 0
        if self.start_filled:
            self.contents = [self.id] * length
        else:
            self.contents = []

    def __repr__(self):
        to_return = []
        for i in range(self.length):
            try:
                to_return.append(str(self.contents[i]))
            except IndexError:
                to_return.append(".")
        return "".join(to_return)
    
    @property
    def is_full(self) -> bool:
        return len(self.contents) == self.length

    @property
    def is_empty(self) -> bool:
        return len(self.contents) == 0
    
    @property
    def empty_space(self) -> int:
        return self.length - len(self.contents)

    def append(self, value):
        self.contents.append(value)

    def pop(self) -> int:
        return self.contents.pop()
    
    def evaluate(self) -> int:
        total = 0
        for i, val in enumerate(self.contents):
            total += (self.position + i) * val
        return total

files = []
position = 0
for i, file_len in enumerate(disc_spec):
    files.append(File(index = i, position = position, length = file_len))
    position += file_len

empty_index = 1
full_index = -1
empty_file = files[empty_index]
full_file = files[full_index]

while True:

    if empty_file.is_full:
        continue

    while not full_file.is_empty and not empty_file.is_full:
        empty_file.append(full_file.pop())

    while empty_file.is_full:
        empty_index += 2
        empty_file = files[empty_index]
    while full_file.is_empty:
        full_index -= 2
        full_file = files[full_index]

    if empty_index > len(files) + full_index:
        break

def eval_files():
    result = 0
    position = 0
    for file in files:
        result += file.evaluate()
        position += file.length
    return result

print(f"Part one: {eval_files()}")

# part two

files = []
position = 0
for i, file_len in enumerate(disc_spec):
    files.append(File(index = i, position = position, length = file_len))
    position += file_len

files_by_empty_space = {}
for f in [x for x in files if not x.start_filled]:
    empty_space = f.empty_space
    try:
        files_by_empty_space[empty_space].append(f)
    except KeyError:
        files_by_empty_space[empty_space] = [f]

non_empties = [f for f in files if f.start_filled]

for file in non_empties[::-1]:

    print(f"Checking file {file}")

    file_strs = [str(file) for file in files]
    print("".join(file_strs))

    if file.is_empty:
        continue
    space_needed = file.length
    file_to_fill = None
    for empty_space, empty_files in files_by_empty_space.items():
        if empty_space < space_needed or not empty_files:
            continue
        earliest_file = empty_files[0]
        if file_to_fill is None or earliest_file.index < file_to_fill.index:
            file_to_fill = earliest_file

    if file_to_fill is None:
        continue
    
    files_by_empty_space[file_to_fill.empty_space].remove(file_to_fill)
    file_to_fill.contents.extend(file.contents)

    file.contents = []
    if file_to_fill.empty_space > 0:
        fs = files_by_empty_space[file_to_fill.empty_space]
        fs.append(file_to_fill)
        files_by_empty_space[file_to_fill.empty_space] = sorted(fs, key = lambda f: f.index)


