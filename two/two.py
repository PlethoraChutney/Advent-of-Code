old_valid = 0
new_valid = 0

with open('input.txt', 'r') as f:
    for line in f:
        split_line = line.strip().split(' ')
        
        low_lim, high_lim = [int(x) for x in split_line[0].split('-')]

        req_letter = split_line[1].replace(':', '')

        occurances = split_line[2].count(req_letter)

        if occurances >= low_lim and occurances <= high_lim:
            old_valid += 1

        new_count = int(split_line[2][low_lim-1] == req_letter) + \
            int(split_line[2][high_lim-1] == req_letter)
        if new_count == 1:
            new_valid += 1

print('Old way: ' + str(old_valid))
print('New way: ' + str(new_valid))
