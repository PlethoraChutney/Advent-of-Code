numbers = []

with open('input.txt', 'r') as f:
    for line in f:
        numbers.append(int(line))

for i in range(len(numbers)):
    j = i
    while j < len(numbers):
        k = j
        while k < len(numbers):
            if numbers[i] + numbers[j] + numbers[k] == 2020:
                print(numbers[i] * numbers[j] * numbers[k])
            k += 1
        j += 1