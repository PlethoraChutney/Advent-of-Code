adapters = [int(x.rstrip()) for x in open('input.txt')]
adapters.append(0)
adapters.sort()

differences = {
    1: 0,
    2: 0,
    3: 0
}

for i in range(len(adapters)):
    try:
        differences[adapters[i+1] - adapters[i]] += 1
    except IndexError:
        differences[3] += 1 # from my phone

print(differences[1] * differences[3])