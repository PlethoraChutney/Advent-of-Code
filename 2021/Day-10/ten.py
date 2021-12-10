import re
import sys
from collections import Counter
from math import floor

navs = [x.rstrip() for x in open(sys.argv[1])]

# make it easy to tell if something matches or not
matches = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

# find chunks by looking for any pair of open/close
# symbols with nothing between them. Capture the open
# and close symbols.
chunk_pattern = re.compile('([\(\[\<\{])([\)\]\>\}])')

def find_corrupt(nav):

    while len(nav) > 0:

        chunk = re.search(chunk_pattern, nav)

        try:
            if matches[chunk.group(1)] == chunk.group(2):
                # if the chunk matches, remove it
                #
                # can't use str.replace because we only want
                # to replace the first instance.
                nav = re.sub(
                    chunk_pattern,
                    '',
                    nav,
                    count = 1
                )
            else:
                # otherwise, return the non-matching close character
                # for point calculation for part one answer
                return chunk.group(2)
                
        # if there is no match, that means we've run out of open or
        # close characters. Return the remaining string for use in
        # part two.
        except AttributeError:
            return nav

corrupts = [find_corrupt(x) for x in navs]
# only count closers, which are a sign that it's corrupted and not incomplete
count_corrupts = Counter([x for x in corrupts if x in matches.values()])

point_values = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

# sum points earned by first corrupted closer
total = 0
for key, val in count_corrupts.items():
    total += val * point_values[key]

print(total)

# part two ----------------------------------------------------------------

incompletes = [x for x in corrupts if x not in matches.values()]

# avoid looking up in matches by giving opener instead
point_values = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

def incomplete_score(nav):
    score = 0
    # move backward through string to reconstruct matches
    # and build score. We don't actually need to keep track
    # of what the reconstruction string is.
    for i in range(len(nav)-1, -1, -1):
        score = score * 5
        score += point_values[nav[i]]

    return score

scores = [incomplete_score(x) for x in incompletes]

# want floor not ceil here b/c of zero indexing
scores.sort()
print(scores[floor(len(scores)/2)])