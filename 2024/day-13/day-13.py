#!/usr/bin/env python
import sys
import numpy as np
import re

with open(sys.argv[1], "r") as f:
    lines = [x.rstrip() for x in f]

machines = []

class Machine:
    def __init__(self):
        self._a = None
        self._b = None
        self._prize = None
    
    def __repr__(self) -> str:
        return f"A: {self.a}, B: {self.b}, Prize: {self.prize}"
    
    @property
    def a(self):
        return self._a
    
    @a.setter
    def a(self, val):
        self._a = np.array(val)

    @property
    def b(self):
        return self._b
    @b.setter
    def b(self, val):
        self._b = np.array(val)

    @property
    def prize(self):
        return self._prize
    @prize.setter
    def prize(self, val):
        self._prize = np.array(val)
    
    def solve_machine_pt_one(self):        
        coeffs = np.array([[self.a[0], self.b[0]], [self.a[1], self.b[1]]])
        deps = np.array(self.prize)
        coords = np.linalg.solve(coeffs, deps)
        fractional_part, _ = np.modf(coords)

        if any(x > 100 for x in coords) or not np.allclose(fractional_part, 0):
            return (False, False)
            
        return tuple(int(x) for x in coords)
    
    def get_prize(self, pt_one = True) -> tuple[int]:
        if pt_one:
            a_presses, b_presses = self.solve_machine_pt_one()
        else:
            a_presses, b_presses = self.solve_machine_pt_two()

        if not (a_presses or b_presses):
            return (0, 0)
        
        return (1, 3 * a_presses + b_presses)
        
    def solve_machine_pt_two(self):
        prize = np.array(tuple(x + 10000000000000 for x in self.prize))
        coeffs = np.array([[self.a[0], self.b[0]], [self.a[1], self.b[1]]])
        d_coeffs = np.linalg.det(coeffs)
        amat = coeffs.copy()
        amat[:,0] = prize.T
        bmat = coeffs.copy()
        bmat[:,1] = prize.T
        
        coords = (np.linalg.det(amat), np.linalg.det(bmat))
        coords = tuple(x / d_coeffs for x in coords)
        
        int_coords = np.round(coords)
        diff = int_coords - coords
        int_values_okay = all(np.isclose(diff[k], 0, atol = 1e-4) or np.isclose(diff[k], 1, atol = 1e-4) for k in [0,1])

        if int_values_okay:
            print('s')
            return tuple(int(x) for x in int_coords)

        print('f')
        return (False, False)
            


line_pattern = r"(Button [AB]|Prize): X[+=](\d+), Y[+=](\d+)"
for line in lines:
    match = re.match(line_pattern, line)
    if match is None:
        continue
    linetype, x, y = match.groups()
    if linetype == "Button A":
        curr_machine = Machine()
        curr_machine.a = tuple(int(c) for c in (x, y))
    elif linetype == "Button B":
        curr_machine.b = tuple(int(c) for c in (x, y))
    elif linetype == "Prize":
        curr_machine.prize = tuple(int(c) for c in (x, y))
        machines.append(curr_machine)

tokens_pt_one = 0
tokens_pt_two = 0
for m in machines:
    tokens_pt_one += m.get_prize()[1]
    tokens_pt_two += m.get_prize(pt_one = False)[1]

print(f"Part one: {tokens_pt_one}")
print(f"Part two: {tokens_pt_two}")