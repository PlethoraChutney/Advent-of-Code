import sys
from itertools import chain

string = list(range(256))

with open(sys.argv[1], 'r') as f:
    lengths = [ord(x) for x in f.readline().rstrip()]
lengths.extend([17, 31, 73, 47, 23])

position = 0
skip_size = 0

for iteration in range(64):
    for length in lengths:
        digits = []
        for i in range(length):
            digits.append(string[(position + i) % len(string)])
        digits = digits[::-1]

        for i in range(len(digits)):
            string[(position + i) % len(string)] = digits[i]

        position = (position + length + skip_size) % len(string)
        skip_size += 1

outputs = []

i = 0
while i < len(string):
    output = string[i]
    for j in range(i+1, i + 16):
        output = output ^ string[j]
    outputs.append(output)

    i += 16

print(outputs)

hash_string = [str(hex(x))[2:] for x in outputs]
print(''.join(hash_string))