#!/usr/bin/env python

with open('input.txt', 'r') as f:
    reports = [[int(y) for y in x.split()] for x in f]

def report_safe(report):
    diffs = [
        a - b for a, b in zip(report[:-1], report[1:])
    ]
    increasing = all(x > 0 for x in diffs)
    decreasing = all(x < 0 for x in diffs)
    size_ok = all(abs(x) <= 3 and abs(x) >= 1 for x in diffs)
    return (increasing or decreasing) and size_ok

num_safe = sum(report_safe(r) for r in reports)

print(
    f"Part One: {num_safe}"
)

unsafe_reports = [r for r in reports if not report_safe(r)]

reports_made_safe = 0

# probably a smarter way to do this than checking, but I'm dumb!
for report in unsafe_reports:
    safe_with_drop = False
    for i in range(len(report)):
        local_report = report[:]
        local_report.pop(i)
        if report_safe(local_report):
            safe_with_drop = True
            break
    
    if safe_with_drop:
        reports_made_safe += 1

print(num_safe + reports_made_safe)