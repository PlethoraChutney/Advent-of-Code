import sys

rules = []
nearby_tickets = []

with open('input.txt', 'r') as f:
    apply_reader = 0
    line = f.readline()

    while line != 'your ticket:\n':
        if line == '\n':
            line = f.readline()
            continue

        rule, values = [x for x in line.rstrip().split(': ')]
        values = [[int(y) for y in x.split('-')] for x in values.split(' or ')]

        rules.append([rule, values])
        line = f.readline()

    line = f.readline()
    my_ticket = [int(x) for x in line.split(',')]

    line = f.readline()
    line = f.readline()

    while line:
        line = f.readline().rstrip()
        if line == '':
            continue

        nearby_tickets.append([int(x) for x in line.split(',') if x])

def check_rules(ticket):
    possible = []
    invalid = []
    for val in ticket:
        val_poss = []
        for rule in rules:
            # confusing. rule is [name, [[low, high], [low, high]]]
            # so rule[1] is the list of ranges, rule[1][0][0] is the low of the low range
            if rule[1][0][0] <= val <= rule[1][0][1] or rule[1][1][0] <= val <= rule[1][1][1]:
                val_poss.append(rule[0])
        if len(val_poss) == 0:
            invalid.append(val)

        possible.append(val_poss)

    return (invalid, possible)

# part one
invalid = 0
valid_tix = []
for tick in nearby_tickets:
    tick_invalid, tick_valid = check_rules(tick)
    if len(tick_invalid) != 0:
        invalid += sum(tick_invalid)
    else:
        valid_tix.append(tick_valid)

print(invalid)
    
# part two
fields = {}
rule_names = [x[0] for x in rules]
for i in range(len(valid_tix[0])):
    fields[i] = []
    field = [x[i] for x in valid_tix]
    for name in rule_names:
        if all(name in x for x in field):
            fields[i].append(name)

# puzzle is generous. each field has exactly one more possible
# field than the last. I suppose otherwise it would be unsolvable :)

solved_fields = {}
while len(fields.values()) > 0:
    for key, value in fields.items():
        if len(value) == 1:
            solved = value[0]
            solved_fields[key] = solved

            del fields[key]

            for key in fields:
                fields[key].remove(solved)

            # break here because the dict has changed size
            break

r = 1
for key, value in solved_fields.items():
    if 'departure' in value:
        r *= my_ticket[key]

print(r)