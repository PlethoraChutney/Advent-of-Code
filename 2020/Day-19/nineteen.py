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

# for mess in messages:
#     print(mess)

for num, rule in rule_dict.items():
    print(f'{num}: {rule}')

compiled_rules = {}

def compile_rule(rule):
    try:
        return compiled_rules[rule]

    except KeyError:
        if rule in ['a', 'b']:
            return rule
        elif len(rule) == 1:
            return compile_rule(rule_dict[rule])
        else:
            rule_list = []
            for subrule in rule.split(' '):
                if subrule in ['a', 'b', '|']:
                    rule_list.append(subrule)
                else:
                    rule_list.append(compile_rule(subrule))

            result = ''.join(rule_list)
            result = f'(?:{result})'
            compiled_rules[rule] = result

            return result

rule_zero = re.compile(f'^{compile_rule("0")}$')

matches = [re.match(rule_zero, x) for x in messages]

print(len([x for x in matches if x]))
