values = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

win = {
    'A': 'Y',
    'B': 'Z',
    'C': 'X'
}

tie = {
    'A': 'X',
    'B': 'Y',
    'C': 'Z'
}

def process_throw(throw_string):
    score = 0
    opponent, me = throw_string.split(' ')
    if win[opponent] == me:
        score += 6
    elif tie[opponent] == me:
        score += 3

    score += values[me]

    return score

with open('input.txt', 'r') as f:
    lines = [x.rstrip() for x in f]

print(sum([process_throw(x) for x in lines]))

# part two

values = {
    'A': 1,
    'B': 2,
    'C': 3
}

# what luck! this makes the indices work, and
# gets us the throw all in one.
throws = ['C', 'A', 'B', 'C', 'A']

total_score = 0
for line in lines:
    opp, goal = line.split(' ')

    if goal == 'X':
        my_throw = throws[values[opp] - 1]
        score = 0 + values[my_throw]
    if goal == 'Y':
        my_throw = throws[values[opp]]
        score = 3 + values[my_throw]
    if goal == 'Z':
        my_throw = throws[values[opp] + 1]
        score = 6 + values[my_throw]

    total_score += score

print(total_score)