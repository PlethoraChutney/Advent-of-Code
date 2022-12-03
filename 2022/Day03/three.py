from string import ascii_letters

letter_list = list(ascii_letters)

with open('input.txt', 'r') as f:
    lines = [x.rstrip() for x in f]

total_priorities = 0
badge_priorities = 0

for i in range(len(lines)):
    sack = lines[i]
    # part one -------------------

    half_split = int(len(sack)/2)
    compartment_one = set(sack[:half_split])
    compartment_two = set(sack[half_split:])

    # have to pop out the string even though there's only one result
    in_both = compartment_one.intersection(compartment_two).pop()

    # score is one-indexed
    total_priorities += letter_list.index(in_both) + 1

    # part two -------------------
    if i % 3 == 0:
        curr_badge_set = set(sack)
    else:
        curr_badge_set = curr_badge_set.intersection(set(sack))

    if i % 3 == 2:
        badge_priorities += letter_list.index(curr_badge_set.pop()) + 1


print(total_priorities)
print(badge_priorities)