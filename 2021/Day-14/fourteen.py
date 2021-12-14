import sys
from collections import Counter

with open(sys.argv[1], 'r') as f:
    polymer = f.readline().rstrip()

    f.readline()

    insertions = {}

    for line in f:
        pair, insert = line.rstrip().split(' -> ')
        insertions[pair] = insert

# part one
for _ in range(10):
    working_polymer = []
    for i in range(len(polymer) - 1):
        insert = insertions[polymer[i:i+2]]
        working_polymer.extend(
            # for every pair, add the first and inserted letter
            #
            # don't add final character because it will be
            # added by the next loop
            (polymer[i], insert)
        )

    # no next loop, so the final final character gets added here
    working_polymer.append(polymer[-1])

    polymer = ''.join(working_polymer)

counts = list(Counter(list(polymer)).values())
counts.sort()
print(counts[-1] - counts[0])

# part two
# same as the other puzzle where you can't just be dumb with part two

pairs = {}

# helper function to add to a value, or create it if it doesn't exist
def mod_or_create(dict, key, change):
    try:
        dict[key] += change
    except KeyError:
        dict[key] = change

# count the number of each type of pair
for i in range(len(polymer)-1):
    mod_or_create(pairs, polymer[i:i+2], 1)


def extend_polymer(pairs, insertions):
    changes = {}
    # for each type of pair
    for pair, insert in insertions.items():
        try:
            # find how many of that pair we had before this iteration
            num_found = pairs[pair]
        except KeyError:
            num_found = 0
        # remove that number of that pair
        mod_or_create(changes, pair, -num_found)
        # add new of the pairs of first letter/insert and insert/second letter
        # equal to the number of original pairs.
        mod_or_create(changes, pair[0] + insert, num_found)
        mod_or_create(changes, insert + pair[1], num_found)
    for pair, change in changes.items():
        # make all the changes at once
        mod_or_create(pairs, pair, change)
    if any(x<0 for x in pairs.values()):
        # can't really have negative number of char pairs in a string
        raise ValueError

# only need to do it thirty more times
for i in range(30):
    extend_polymer(pairs, insertions)

counts = {}
for pair, count in pairs.items():
    # count only the first letter to avoid counting twice, and to preserve
    # the order of overlap
    mod_or_create(counts, pair[0], count)

# add the last letter for the same reason as in part one. Luckily it never changes.
counts[polymer[-1]] += 1

# part two answer
counts = list(counts.values())
counts.sort()
print(counts[-1] - counts[0])