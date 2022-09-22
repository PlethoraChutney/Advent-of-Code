programs = list('abcdefghijklmnop')
iterations = [''.join(programs)]

def spin(programs:list, num:int):
    for _ in range(num):
        programs.insert(0, programs.pop())

    return programs

def exchange(programs:list, positions:list):
    positions = [int(x) for x in positions]
    first_partner = programs[positions[0]]
    programs[positions[0]] = programs[positions[1]]
    programs[positions[1]] = first_partner
    return programs

def partner(programs:list, names:list):
    positions = (programs.index(names[0]), programs.index(names[1]))
    return exchange(programs, positions)

with open('input.txt', 'r') as f:
    instructions = f.readline().split(',')

for instruction in instructions:
    if instruction[0] == 's':
        programs = spin(programs, int(instruction[1:]))
    
    else:
        action = instruction[0]
        args = instruction[1:].split('/')

        if action == 'x':
            programs = exchange(programs, args)
        elif action == 'p':
            programs = partner(programs, args)

print(''.join(programs))

# find a cycle

iters = 1

while ''.join(programs) not in iterations:
    iterations.append(''.join(programs))
    
    for instruction in instructions:
        if instruction[0] == 's':
            programs = spin(programs, int(instruction[1:]))
        
        else:
            action = instruction[0]
            args = instruction[1:].split('/')

            if action == 'x':
                programs = exchange(programs, args)
            elif action == 'p':
                programs = partner(programs, args)
    
    iters += 1

# iters now tells us how many cycles is a loop
# so we can start from abcdef... and apply
# (1e9 % iters) dances to it

num_dances = 1000000000 % iters

programs = list('abcdefghijklmnop')

for _ in range(num_dances):
    for instruction in instructions:
        if instruction[0] == 's':
            programs = spin(programs, int(instruction[1:]))
        
        else:
            action = instruction[0]
            args = instruction[1:].split('/')

            if action == 'x':
                programs = exchange(programs, args)
            elif action == 'p':
                programs = partner(programs, args)

print(''.join(programs))