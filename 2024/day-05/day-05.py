#!/usr/bin/env python
import sys
import re

with open(sys.argv[1], "r") as f:
    lines = [x.rstrip() for x in f]

rule_pattern = "^(\d+)\|(\d+)$"

rules = []
manuals = []
for line in lines:
    if rule_match := re.match(rule_pattern, line):
        rules.append(list(int(x) for x in rule_match.groups()))
    elif line:
        manuals.append(list(int(x) for x in line.split(",")))

must_be_after = {x[0]: [] for x in rules}
for r in rules:
    must_be_after[r[0]].append(r[1])


def check_manual(manual:list) -> bool:
    manual = manual.copy()
    while manual:
        page = manual.pop()
        if any(p in must_be_after.get(page, []) for p in manual):
            return False
        
    return True

middle_page_sum = 0
bad_manuals = []
for manual in manuals:
    if check_manual(manual):
        middle_page_sum += manual[len(manual) // 2]
    else:
        bad_manuals.append(manual)


print(f"Part one: {middle_page_sum}")

def get_relevant_rules(manual:list) -> dict[int, list]:
    relevant_rules = {k: v for k, v in must_be_after.items() if k in manual or any(vi in manual for vi in v)}
    relevant_rules = {k: [r for r in rule if r in manual] for k, rule in relevant_rules.items()}
    return relevant_rules

def sort_manual(manual:list[int]) -> list[int]:
    relevant_rules = get_relevant_rules(manual)
    # this will only work if there is always one additional rule per number
    # but that is equivalent to there being only one correct sort, which I think
    # is true
    num_rules = {k: len(v) for k, v in relevant_rules.items()}
    return sorted(manual, key = lambda k: num_rules.get(k, 0), reverse = True)

part_two_sum = 0
for manual in bad_manuals:
    good_manual = sort_manual(manual)
    part_two_sum += good_manual[len(good_manual) // 2]

print(f"Part two: {part_two_sum}")