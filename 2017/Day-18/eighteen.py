from collections import defaultdict

with open('input.txt', 'r') as f:
    instructions = [x.rstrip() for x in f]

last_played = 0
registers = defaultdict(lambda: 0)
i = 0

while i < len(instructions) and i >= 0:
    operation = instructions[i][:3]
    inputs = instructions[i].split()[1:]
    if operation == 'snd':
        print('send')
        try:
            inputs[0] = int(inputs[0])
        except ValueError:
            inputs[0] = registers.get(inputs[0])

        last_played = int(inputs[0])
    elif operation == 'set':
        print('set')
        try:
            inputs[1] = int(inputs[1])
        except ValueError:
            inputs[1] = registers.get(inputs[1])

        registers[inputs[0]] = int(inputs[1])
    elif operation == 'add':
        print('add')
        try:
            inputs[1] = int(inputs[1])
        except ValueError:
            inputs[1] = registers.get(inputs[1])

        registers[inputs[0]] += int(inputs[1])
    elif operation == 'mul':
        print('multiply')
        try:
            inputs[1] = int(inputs[1])
        except ValueError:
            inputs[1] = registers.get(inputs[1])

        registers[inputs[0]] = registers[inputs[0]] * inputs[1]

    elif operation == 'mod':
        print('modulo')
        try:
            inputs[1] = int(inputs[1])
        except ValueError:
            inputs[1] = registers.get(inputs[1])

        registers[inputs[0]] = registers[inputs[0]] % inputs[1]

    elif operation == 'rcv':
        print('rcv')
        try:
            inputs[0] = int(inputs[0])
        except ValueError:
            inputs[0] = registers.get(inputs[0])

        if inputs[0] != 0:
            break

    elif operation == 'jgz':
        print('jump')
        try:
            inputs[0] = int(inputs[0])
        except ValueError:
            inputs[0] = registers.get(inputs[0])
        try:
            inputs[1] = int(inputs[1])
        except ValueError:
            inputs[1] = registers.get(inputs[1])

        if inputs[0] > 0:
            i += inputs[1]
            continue

    i += 1

print(last_played)
