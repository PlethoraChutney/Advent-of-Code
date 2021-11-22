import sys
import re

expressions = [x.rstrip() for x in open(sys.argv[1])]

# Capture group surrounded by parens. Group cannot have "(" or ")"
paren_pattern = re.compile('\(([^(^)]*?)\)')

# g0: expression
# g1: first num
# g2: operator
# g3: second num
math_pattern = re.compile('([0-9]*) ([\*|\+]) ([0-9]*)')
add_pattern = re.compile('([0-9]*) \+ ([0-9]*)')
mult_pattern = re.compile('([0-9]*) \* ([0-9]*)')

def solve_expression_one(expression):

    paren_match = re.search(paren_pattern, expression)
    math_match = re.match(math_pattern, expression)

    if paren_match:
        expression = expression.replace(
            paren_match.group(0),
            str(solve_expression_one(paren_match.group(1)))
        )

    elif math_match:
        if math_match.group(2) == '+':
            result = int(math_match.group(1)) + int(math_match.group(3))
        else:
            result = int(math_match.group(1)) * int(math_match.group(3))
        # using str.replace here replaces all instances of that pattern with the
        # result. Can give too high a number
        expression = re.sub(
            math_pattern,
            str(result),
            expression,
            count=1
        )

    else:
        print(f'No match for {expression}')

    try:
        return int(expression)
    except ValueError:
        return solve_expression_one(expression)


solutions = [solve_expression_one(x) for x in expressions]
print(solutions)
print(sum(solutions))


def solve_expression_one(expression):

    paren_match = re.search(paren_pattern, expression)
    add_match = re.search(add_pattern, expression)
    mult_match = re.match(mult_pattern, expression)

    if paren_match:
        expression = expression.replace(
            paren_match.group(0),
            str(solve_expression_one(paren_match.group(1)))
        )

    else:
        if add_match:
            result = int(add_match.group(1)) + int(add_match.group(2))
            expression = re.sub(
                add_pattern,
                str(result),
                expression,
                count=1
            )
        elif mult_match:
            result = int(mult_match.group(1)) * int(mult_match.group(2))
            expression = re.sub(
                mult_pattern,
                str(result),
                expression,
                count=1
            )

    try:
        return int(expression)
    except ValueError:
        return solve_expression_one(expression)


solutions = [solve_expression_one(x) for x in expressions]
print(sum(solutions))