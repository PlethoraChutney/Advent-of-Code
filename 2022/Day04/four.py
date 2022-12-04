with open('input.txt', 'r') as f:
    lines = [x.rstrip() for x in f]

# part one
count_inclusion = 0
count_overlap = 0


for line in lines:
    elf_1, elf_2 = line.split(',')
    elf_1 = [int(x) for x in elf_1.split('-')]
    elf_2 = [int(x) for x in elf_2.split('-')]

    if elf_1[0] >= elf_2[0] and elf_1[1] <= elf_2[1]:
        count_inclusion += 1
    elif elf_1[0] <= elf_2[0] and elf_1[1] >= elf_2[1]:
        count_inclusion += 1

    if elf_1[0] <= elf_2[1] and elf_1[0] >= elf_2[0]:
        count_overlap += 1
    elif elf_2[0] <= elf_1[1] and elf_2[0] >= elf_1[0]:
        count_overlap += 1

print(count_inclusion)
print(count_overlap)
