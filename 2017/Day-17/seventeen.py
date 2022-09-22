steps = 367

buffer = [0]
insert_target = 1
position = 0

while insert_target <= 2017:
    position += steps
    position = position % len(buffer)
    buffer.insert(position + 1, insert_target)
    insert_target += 1
    position += 1

print(buffer[buffer.index(2017) + 1])

# the length before adding will always be iter
# which means that we change the number at position 1
# iff (position + steps) % (iteration) == 0

position = 0
after_zero = 0
for iteration in range(1,50000000):
    position = (position + steps) % (iteration)
    if position == 0:
        after_zero = iteration
    position += 1

print(after_zero)
