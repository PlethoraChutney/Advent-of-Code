with open('input.txt', 'r') as f:
    stream = f.readline().rstrip()

score = 0
i = 0
group_depth = 0
in_garbage = False
garb_removed = 0

while i < len(stream):
    if not in_garbage:
        if stream[i] == '{':
            group_depth +=1
        
        elif stream[i] == '}':
            score += group_depth
            group_depth -= 1

        elif stream[i] == '<':
            in_garbage = True

    else:
        if stream[i] == '!':
            i += 1
        elif stream[i] == '>':
            in_garbage = False
        else:
            garb_removed += 1

    i += 1

print(score)
print(garb_removed)