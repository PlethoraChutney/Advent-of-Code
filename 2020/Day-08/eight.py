def run_boot_code(input):
    part_one = False
    accumulator = 0
    flip_tracker = [False] * len(input)

    visited = []
    i = 0
    while True:
        if i in visited:
            # reset everything except flip_tracker
            if not part_one:
                part_one = accumulator
            i = 0
            visited = []
            accumulator = 0
            continue
        visited.append(i)

        try:
            operation, argument = input[i].split(' ')
        # here's the return. we succeed if we go past the end of the list
        except IndexError:
            return(part_one, accumulator)
        
        argument = int(argument)

        if operation == 'acc':
            accumulator += argument
            i += 1
        elif operation == 'jmp':
            if (i + argument in visited) and not flip_tracker[i]: # If we haven't tried flipping this one, perform a nop instead
                print('Flipping ' + str(i))
                i += 1
                flip_tracker[i] = True
                continue
            i += argument
        elif operation == 'nop':
            if (i + 1 in visited) and not flip_tracker[i]:
                print('Flipping ' + str(i))
                i += argument
                flip_tracker[i] = True
                continue

            i += 1


instructions = [x.rstrip() for x in open('input.txt')]
print(run_boot_code(instructions))
