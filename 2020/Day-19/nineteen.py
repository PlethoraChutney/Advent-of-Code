import re
import sys

rule_dict = {}
messages = []
rules = [x.rstrip().replace('"', '') for x in open(sys.argv[1]) if x != '\n']

for rule in rules:
    try:
        num, rule = rule.split(': ')
        rule_dict[num] = rule
    except ValueError:
        messages.append(rule)

compiled_rules = {}

def compile_rule(index, rule):
    try:
        # memoization baby!
        return compiled_rules[index]

    except KeyError:
        if rule in ['a', 'b']:
            return rule
        else:
            rule_list = []
            for subrule in rule.split(' '):
                if subrule in ['a', 'b', '|']:
                    rule_list.append(subrule)
                else:
                    rule_list.append(compile_rule(subrule, rule_dict[subrule]))

            result = ''.join(rule_list)
            result = f'(?:{result})'
            compiled_rules[index] = result

            return result

# part one

rule_zero = re.compile(f'^{compile_rule("0", rule_dict["0"])}$')

matches = [re.match(rule_zero, x) for x in messages]

print(len([x for x in matches if x]))

# part two
# 8: 42 | 42 8 is the same as 8: (42){1,}
#
# 11: 42 31 | 42 11 31 is the same as 11: ((42){1,} (31){1,})
# technically, here, these would have to match the same number
# of times...hopefully the puzzle is kind
# It's not...
#
# Hmm...maybe I should just be lazy...
# 
# so I can first solve 42 and 31, then hardcode the new rules.
# thank god for regex

compiled_rules = {}
compile_rule('31', rule_dict['31'])
compile_rule('42', rule_dict['42'])
ft = compiled_rules['42']
to = compiled_rules['31']

# hacky bullshit. Just make a big group that solves the same-repeat problem.
# basically (aabb|aaaabbbb|aaaaaabbbbbb|aaaaaaaabbbbbbbb|etc). Only goes to eleven.
eleven_list = []
for i in range(10):
    eleven_list.append(ft*(i + 1) + to * (i + 1))

compiled_rules['8'] = compiled_rules['42'] + '{1,}'
compiled_rules['11'] = '(?:' + '|'.join(eleven_list) + ')'


rule_zero = re.compile(f'^{compile_rule("0", rule_dict["0"])}$')

matches = [re.match(rule_zero, x) for x in messages]

print(len([x for x in matches if x]))
