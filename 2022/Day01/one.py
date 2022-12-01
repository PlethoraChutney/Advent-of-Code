# read in file

with open('input.txt', 'r') as f:
    lines = [line.rstrip() for line in f]

elves = []
current_pack = []

for snack in lines:
    if not snack:
        elves.append(current_pack)
        current_pack = []
    else:
        current_pack.append(int(snack))

elves.append(current_pack)

total_elf_calories = [sum(elf) for elf in elves]

total_elf_calories.sort(reverse=True)

# part one
print(total_elf_calories[0])

# part two
print(sum(total_elf_calories[0:3]))