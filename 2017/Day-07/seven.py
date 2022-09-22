from statistics import mode
import sys

with open('input.txt', 'r') as f:
    lines = [x.rstrip() for x in f]

# part one

programs = [x.split()[0] for x in lines]

for line in lines:
    if '->' not in line:
        continue
    else:
        children = line.split(' -> ')[1]
        children = children.split(', ')
        for child in children:
            programs.remove(child)

print(programs)
root = programs[0]

# part two

class Program:
    def __init__(self, program_string):
        program_string = program_string.split(' -> ')

        self.name, self.weight = program_string[0].split()
        self.weight = int(self.weight[1:-1])
        
        try:
            self.children = program_string[1].split(', ')
            self.disk_weight = None
            self.leaf = False
        except IndexError:
            self.children = []
            self.leaf = True
            self.disk_weight = self.weight

    def total_weight(self, other_programs):
        if self.disk_weight is None:
            other_weights = [other_programs[x].total_weight(other_programs) for x in self.children]
            
            self.disk_weight = self.weight + sum(other_weights)

            for i in range(len(self.children)):
                if other_weights[i] != mode(other_weights):
                    difference = mode(other_weights) - other_weights[i]
                    print(
                        'Child',
                        self.children[i],
                        'of',
                        self.name,
                        'is unbalanced, should be',
                        mode(other_weights),
                        'but is',
                        other_weights[i],
                        'difference',
                        difference
                    )
                    print(
                        'This child weight is',
                        other_programs[self.children[i]].weight,
                        'so should become',
                        other_programs[self.children[i]].weight + difference,
                        'making weight of',
                        self.name,
                        'into',
                        self.disk_weight + difference
                    )
        
        return self.disk_weight

programs = {x.split()[0]: Program(x) for x in lines}
programs[root].total_weight(programs)