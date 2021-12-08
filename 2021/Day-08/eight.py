import sys
from itertools import chain

# part one
inputs = [x.rstrip().split(' | ') for x in open(sys.argv[1])]
signals = [x[0] for x in inputs]
outputs = [x[1] for x in inputs]


# just get all the output strings into one big list
all_outputs = chain(*[x.split(' ') for x in outputs])

# count the string if it has one of the unique values
all_outputs = sum(1 for x in all_outputs if len(x) in [2, 3, 4, 7])

print(all_outputs)

# part two

# convert a given string into a bitmask with
# the most significant bit representing 'a' and the least
# significant bit representing 'g'. That is, 64 means 'a'
# and 127 means 'abcdefg'
def convert_to_bitmask(signal):
    bitmask = 0
    for letter in 'abcdefg':
        bitmask = (bitmask << 1) | (letter in signal)

    return bitmask

signals = [[convert_to_bitmask(x) for x in y.split(' ')] for y in signals]
outputs = [[convert_to_bitmask(x) for x in y.split(' ')] for y in outputs]

def decode_signals(signals):
    on_counts = [bin(x).count('1') for x in signals]

    # unique values
    one = signals[on_counts.index(2)]
    eight = signals[on_counts.index(7)]
    seven = signals[on_counts.index(3)]
    four = signals[on_counts.index(4)]

    # for non-unique values, we use a set of rules for shared
    # on bits. For instance, the only six segment digit that does
    # not fully overlap with one is six, so if signal | one != signal
    # we know it's six.
    for i in range(len(signals)):
        if on_counts[i] in [2, 3, 4, 7]:
            continue
        elif on_counts[i] == 6:
            if (signals[i] | one) != signals[i]:
                six = signals[i]
            elif (signals[i] | four) == signals[i]:
                nine = signals[i]
            else:
                zero = signals[i]
        elif on_counts[i] == 5:
            if (signals[i] | one) == signals[i]:
                three = signals[i]
            elif (signals[i] | four) == eight:
                two = signals[i]
            else:
                five = signals[i]

    # the return dict uses strings b/c we'll need to join them later
    return {
        one: '1',
        two: '2',
        three: '3',
        four: '4',
        five: '5',
        six: '6',
        seven: '7',
        eight: '8',
        nine: '9',
        zero: '0'
    }

def get_output(inputs, outputs):
    decoder = decode_signals(inputs)
    
    return int(''.join([decoder[x] for x in outputs]))

print(sum([get_output(signals[x], outputs[x]) for x in range(len(signals))]))