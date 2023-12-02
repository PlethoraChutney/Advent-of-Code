with open('input.txt', 'r') as f:
    lines = [x.rstrip() for x in f]

class Dir(object):
    def __init__(self, name):
        self.name = name
        self.children = []
        self.filesize = None
        self.parent = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    @property
    def size(self):
        if self.filesize is None:
            size = 0
            for child in self.children:
                size += child.size
            self.filesize = size
        return self.filesize

class File(object):
    def __init__(self, name, size):
        self.name = name
        self.size = size

class Terminal(object):
    def __init__(self):
        self.root = Dir('/')
        self.all_dirs = [self.root]

    def cd(self, loc):
        if loc == '/':
            self.curr_dir = self.root
        elif loc == '..':
            self.curr_dir = self.curr_dir.parent
        else:
            if loc not in self.all_dirs:
                new_dir = Dir(loc)
                self.curr_dir.add_child(new_dir)
                self.all_dirs.append(new_dir)
            
            self.curr_dir = new_dir

    def make_file(self, size, name):
        new_file = File(name, int(size))
        self.curr_dir.add_child(new_file)

terminal = Terminal()

for line in lines:
    if line[0] == '$':
        if line[2] == 'c':
            _, _, loc = line.split(' ')
            terminal.cd(loc)
    elif line[0] != 'd':
        terminal.make_file(*line.split(' '))

# part one

tot_size = 0
for directory in terminal.all_dirs:
    if directory.size < 100000:
        tot_size += directory.size

print(tot_size)

# part two

size_currently_empty = 70000000 - terminal.root.size
size_to_delete = 30000000 - size_currently_empty

potential_deletions = []
for directory in terminal.all_dirs:
    if directory.size >= size_to_delete:
        potential_deletions.append(directory.size)

print(min(potential_deletions))