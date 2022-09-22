seq = [int(x.rstrip()) for x in '4	10	4	1	8	4	9	14	5	1	14	15	0	15	3	5'.split()]

prev_seen = {}

def redistribute(seq):
    i = 0

    while True:
        if seq[i] == max(seq):
            break
        else:
            i += 1

    mem_blocks = seq[i]
    seq[i] = 0

    cycle = 0
    while mem_blocks > 0:
        i = (i + 1) % len(seq)
        cycle += 1
        seq[i] += 1
        mem_blocks -= 1

    return seq

cycles = 0

while True:
    if tuple(seq) in prev_seen:
        print(cycles)
        print(cycles - prev_seen[tuple(seq)])
        break
    else:
        prev_seen[tuple(seq)] = cycles
        cycles += 1
        seq = redistribute(seq)
