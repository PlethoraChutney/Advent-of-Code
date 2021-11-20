import sys
import re
from collections import defaultdict
from itertools import combinations

def apply_mask(in_val, mask):
    or_mask = int(mask.replace('X', '0'), 2)
    and_mask = int(mask.replace('X', '1'), 2)
    return (int(in_val) | or_mask) & and_mask

def write_two(in_val, address, mask):
    in_val = int(in_val)

    or_mask = int(mask.replace('X', '0'), 2)
    address = int(address) | or_mask
    address = str(f'{address:b}'.zfill(36))

    target_addresses = []
    i_to_replace = []
    for i in range(len(mask)):
        if mask[i] == 'X':
            i_to_replace.append(i)

    for i in i_to_replace:
        zeroed = []
        oned = []
        if len(target_addresses) == 0:
            working_add = list(address)
            working_add[i] = '0'
            zeroed.append(''.join(working_add))
            working_add[i] = '1'
            oned.append(''.join(working_add))
        else:
            for address in target_addresses:
                working_add = list(address)
                working_add[i] = '0'
                zeroed.append(''.join(working_add))
                working_add[i] = '1'
                oned.append(''.join(working_add))
        
        target_addresses = []
        target_addresses.extend(zeroed)
        target_addresses.extend(oned)

    target_addresses = [int(x, 2) for x in target_addresses]

    for add in target_addresses:
        memory_two[add] = in_val



memory_one = defaultdict(lambda: '0'*36)
memory_two = defaultdict(lambda: '0'*36)
mask = 'X'*36

with open(sys.argv[1], 'r') as f:
    for line in f:
        line = line.rstrip()
        address_match = re.match('mem\[([0-9]*)\] = (.*)', line)

        if address_match:
            masked = apply_mask(address_match.group(2), mask)
            memory_one[address_match.group(1)] = masked
            write_two(address_match.group(2), address_match.group(1), mask)
            
        else:
            mask = re.match('mask = (.*)', line).group(1)

print(sum(memory_one.values()))
print(sum(memory_two.values()))

