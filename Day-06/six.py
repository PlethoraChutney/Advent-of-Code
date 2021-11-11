from string import ascii_lowercase

def read_declaration(combined_declaration):
    declaration = 0

    for letter in ascii_lowercase:
        if letter in combined_declaration:
            declaration += 1

    return declaration

declarations = []
with open('input.txt', 'r') as f:
    curr_dec = []
    for line in f:
        if line != '\n':
            curr_dec.append(line.rstrip())
        else:
            declarations.append(read_declaration(''.join(curr_dec)))
            curr_dec = []
    
    declarations.append(read_declaration(''.join(curr_dec)))

print(sum(declarations))
