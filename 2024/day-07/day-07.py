#!/usr/bin/env python
import sys
import re
from collections import Counter
from itertools import product

line_pattern = r"^(\d+): (.+)$"

with open(sys.argv[1], "r") as f:
    lines = [x.rstrip() for x in f]

lines = [
    re.search(line_pattern, line) for line in lines
]
lines = [
    (int(l.group(1)), [int(x) for x in l.group(2).split(" ")]) for l in lines
]

# from https://stackoverflow.com/questions/66148587/function-that-prints-prime-factorization-of-any-number-python
# brute force algo obviously slow lol
def prime_factors(N):
    p,i = 2,1
    while p*p<=N:
        while N%p == 0:
            yield p
            N //= p
        p,i = p+i,2
    if N>1: yield N

# doesn't work
def proper_math_process_line(l:tuple[int,list[int]]) -> bool:
    target = l[0]
    values = l[1]
    operators = []
    primes = Counter(prime_factors(target))
    
    products_found = []
    curr_sum = 0
    while values:
        curr_sum += values.pop(0)
        curr_sum_primes = Counter(prime_factors(curr_sum))
        if all(primes[k] >= v for k, v in curr_sum_primes.items()):
            for k, v in curr_sum_primes.items():
                primes[k] -= v
            products_found.append(curr_sum)
            curr_sum = 0
            operators.append("*")
        else:
            operators.append("+")

    total_value = 1
    for p in products_found:
        total_value = total_value * p

    return total_value == target

def apply_operators(values:list[int], operators:list[str]) -> int:
    total = values.pop(0)
    for i, val in enumerate(values):
        op = operators[i]
        if op == "+":
            total += val
        elif op == "*":
            total *= val
        elif op == "|":
            total = int(str(total) + str(val))
    return total

def process_line(l:tuple[int,list[int]], ops = "*+") -> bool:
    target = l[0]
    values = l[1]
    op_combs = product(ops, repeat = len(values) - 1)
    for oc in op_combs:
        result = apply_operators(values.copy(), oc)
        if result == target:
            return True
    return False

val_sum = 0
for line in lines:
    if process_line(line):
        val_sum += line[0]

print(f"Part one: {val_sum}")

# two brute forces in a row...embarrassing!
val_sum = 0
for line in lines:
    if process_line(line, ops = "*+|"):
        val_sum += line[0]

print(f"Part two: {val_sum}")