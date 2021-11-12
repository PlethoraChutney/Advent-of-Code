
def run_boot_code(input):
    accumulator = 0

    visited = []
    i = 0
    while True:
        if i in visited:
            raise ValueError('Loop! Accumulator is ' + str(accumulator))
        else:
            visited.append(i)

        operation, argument = input[i].split(' ')
        argument = int(argument)

        if operation == 'acc':
            accumulator += argument
            i += 1
        elif operation == 'jmp':
            i += argument
        elif operation == 'nop':
            i += 1


instructions = [x.rstrip() for x in open('input.txt')]
run_boot_code(instructions)
