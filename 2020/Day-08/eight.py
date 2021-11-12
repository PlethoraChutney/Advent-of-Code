def run_boot_code(input, part_one):
    accumulator = 0
    flip_tracker = []

    visited = []
    i = 0
    flipped = False
    while True:

        # if already visited, return for part one, otherwise
        # reset everything except flip_tracker
        if i in visited:
            if part_one:
                return accumulator
            
            print('Resetting')
            
            i = 0
            visited = []
            accumulator = 0
            flipped = False
            continue
        visited.append(i)

        try:
            operation, argument = input[i].split(' ')
        # here's the return for part two. we succeed if we go past the end of the list
        except IndexError:
            return accumulator
        
        argument = int(argument)

        if operation == 'acc':
            accumulator += argument
            i += 1
        elif operation == 'jmp':
            if i not in flip_tracker and not flipped and not part_one: # If we haven't tried flipping this one, perform a nop instead
                print('Flipping ' + str(i))
                flip_tracker.append(i)
                flipped = True
                i += 1
                continue

            i += argument
        elif operation == 'nop':
            if i not in flip_tracker and not flipped and not part_one:
                print('Flipping ' + str(i))
                flip_tracker.append(i)
                flipped = True
                i += argument
                continue

            i += 1


instructions = [x.rstrip() for x in open('input.txt')]
print(run_boot_code(instructions, True))
print(run_boot_code(instructions, False))
