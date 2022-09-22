with open('input.txt', 'r') as f:
    instructions = [int(x.rstrip()) for x in f]

pointer = 0
steps = 0

while pointer < len(instructions) and pointer >= 0:
    steps += 1
    instruction = instructions[pointer]
    instructions[pointer] += 1
    pointer += instruction

print('Part one:', steps)

with open('input.txt', 'r') as f:
    instructions = [int(x.rstrip()) for x in f]

pointer = 0
steps = 0

while pointer < len(instructions) and pointer >= 0:
    steps += 1
    instruction = instructions[pointer]
    if instruction >= 3:
        instructions[pointer] -= 1
    else:
        instructions[pointer] += 1
    pointer += instruction

print('Part two:', steps)