# -------------------------------
# Read in

with open('input.txt', 'r') as f:
    block = 'crates'
    starting_crates = {}
    instructions = []

    for line in f:
        
        if line[1] == '1':
            block = 'instructions'
            # skip the blank line after crate numbers
            f.readline()

            for stack in starting_crates.values():
                # since we read in from the top down,
                # have to reverse them once done reading
                stack.reverse()
        elif block == 'crates':
            i = 0
            
            # the ith crate has a letter at i * 4 + 1
            while i < len(line) / 4:
                letter = line[4 * i + 1]
                if letter not in [' ', '\n']:
                    try:
                        starting_crates[i + 1].append(letter)
                    except KeyError:
                        starting_crates[i + 1] = [letter]

                i += 1
        elif block == 'instructions':
            line = line.split(' ')
            
            instructions.append({
                'num': int(line[1]),
                'source': int(line[3]),
                'target': int(line[5])
            })

# -------------------------------
# Part one

# need to make a deep copy, so .copy() doesn't work
crates = {x: starting_crates[x][:] for x in starting_crates.keys()}

for inst in instructions:
    for _ in range(inst['num']):
        crates[inst['target']].append(crates[inst['source']].pop())

# my dict keys aren't sorted...took me a while to figure
# out how that was messing me up haha

num_crates = max(crates.keys())

print(''.join(crates[x][-1] for x in range(1, num_crates + 1)))

# -------------------------------
# Part two
crates = {x: starting_crates[x][:] for x in starting_crates.keys()}
crane = []

for inst in instructions:
    for _ in range(inst['num']):
        crane.append(crates[inst['source']].pop())

    while len(crane) > 0:
        crates[inst['target']].append(crane.pop())

print(''.join(crates[x][-1] for x in range(1, num_crates + 1)))