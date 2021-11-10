oo = 0 # one, one
to = 0 # three, one
fo = 0 # five, one
so = 0 # seven, one
ot = 0.0 # one, two

trees = {
    'oo': 0,
    'to': 0,
    'fo': 0,
    'so': 0,
    'ot': 0
}

with open('input.txt', 'r') as f:
    for line in f:
        # one, one
        if line[oo] == '#':
            trees['oo'] += 1
        oo += 1
        oo = oo % (len(line)-1)

        if line[to] == '#':
            trees['to'] += 1
        to += 3
        to = to % (len(line)-1)

        if line[fo] == '#':
            trees['fo'] += 1
        fo += 5
        fo = fo % (len(line) - 1)

        if line[so] == '#':
            trees['so'] += 1
        so += 7
        so = so % (len(line) - 1)

        if ot % 1 == 0 and line[int(ot)] == '#':
            trees['ot'] += 1
        ot += 0.5
        ot = ot % (len(line) - 1)

print(trees)

r = 1
for x in trees.values():
    r *= x

print(r)