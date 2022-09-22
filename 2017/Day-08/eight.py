from collections import defaultdict

with open('input.txt', 'r') as f:
    lines = [x.rstrip() for x in f]

registers = defaultdict(lambda: 0)
max_max = 0

for line in lines:
    line = line.split()
    register = line[0]
    change = int(line[2]) if line[1] == 'inc' else -int(line[2])
    condition_reg = line[4]
    condition_compare = line[5]
    condition_val = int(line[6])

    cond_reg_val = registers[condition_reg]

    if condition_compare == '>':
        condition = cond_reg_val > condition_val
    elif condition_compare == '<':
        condition = cond_reg_val < condition_val
    elif condition_compare == '>=':
        condition = cond_reg_val >= condition_val
    elif condition_compare == '<=':
        condition = cond_reg_val <= condition_val
    elif condition_compare == '==':
        condition = cond_reg_val == condition_val
    elif condition_compare == '!=':
        condition = cond_reg_val != condition_val

    if condition:
        registers[register] = registers[register] + change

    if registers[register] > max_max:
        max_max = registers[register]

print(max(registers.values()))
print(max_max)
