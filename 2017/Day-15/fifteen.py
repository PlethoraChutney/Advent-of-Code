a_val = 883
b_val = 879
matches = 0

def generate(a_val, b_val):
    a_val = (a_val * 16807) % 2147483647
    while a_val % 4 != 0:
        a_val = (a_val * 16807) % 2147483647

    b_val = (b_val * 48271) % 2147483647
    while b_val % 8 != 0:
        b_val = (b_val * 48271) % 2147483647

    return (a_val, b_val)

def judge(a_val, b_val):
    a_judge = (2**16 - 1) & a_val
    b_judge = (2**16 - 1) & b_val
    return a_judge == b_judge

for i in range(int(5e6)):
    a_val, b_val = generate(a_val, b_val)
    matches += judge(a_val, b_val)

print(matches)