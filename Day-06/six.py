from string import ascii_lowercase

def part_one(combined_declaration) -> int:
    declaration = 0

    for letter in ascii_lowercase:
        if letter in combined_declaration:
            declaration += 1

    return declaration

def part_two(declaractions) -> int:
    letters = ascii_lowercase
    remaining_letters = []

    for declaration in declaractions:
        for letter in letters:
            if letter in declaration:
                remaining_letters.append(letter)
        letters = remaining_letters
        remaining_letters = []

    return len(letters)

declarations = []
with open('input.txt', 'r') as f:
    curr_dec = []
    for line in f:
        if line != '\n':
            curr_dec.append(line.rstrip())
        else:
            declarations.append(curr_dec)
            curr_dec = []
    
    declarations.append(curr_dec)

part_one = sum([part_one(''.join(x)) for x in declarations])
part_two = sum([part_two(x) for x in declarations])

print(part_one)
print(part_two)
