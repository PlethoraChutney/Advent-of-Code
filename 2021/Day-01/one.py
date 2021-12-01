depths = [int(x.rstrip()) for x in open('input.txt')]

# part one
increase = 0
for index in range(len(depths)):
    try:
        if depths[index - 1] < depths[index]:
            increase += 1
    except IndexError:
        continue

print(increase)

# part two
increase = 0
for i in range(len(depths)):
    try:
        if i == 0:
            prev_sum = sum(depths[i:i+3])
            continue
        curr_sum = sum(depths[i:i+3])
        if curr_sum > prev_sum:
            increase += 1
        prev_sum = curr_sum
    except IndexError:
        break

print(increase)