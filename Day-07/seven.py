def rule_parser(rule) -> list:
    container, contents = rule.split(' contain ')

    container = container.replace(' bags', '')

    contents = contents.split(', ')

    # since the list of contents will be truthy, this makes
    # it easy to find terminal bags
    if contents[0] == 'no other bags':
        bag_types = False
    else:
        bag_types = {}
        # contents will become a list of [number, bag type]
        for bag in contents:
            bag = bag.replace(' bags', '')
            bag = bag.replace(' bag', '')
            bag_types[bag[1:].strip()] = int(bag[0])


    return [container, bag_types]

# base_rules gives us a dict of the base-level bag: contents info
base_rules = {}

with open('input.txt', 'r') as f:
    for line in f:
        bag, contents = rule_parser(line.rstrip().replace('.', ''))
        base_rules[bag] = contents


# Bag class, which based on its color can tell us what it could contain

class Bag:
    def __init__(self, color) -> None:
        self.color = color
        self.contents = base_rules[color]

    def all_possible_colors(self) -> list:
        if not self.contents:
            return [None]

        possible_colors = list(self.contents.keys())
        current_level = possible_colors
        current_contents = []
        for color in current_level:
            if base_rules[color]:
                current_contents.extend(base_rules[color].keys())

        possible_colors.extend(current_contents)

        i = 0
        while any(current_contents):
            i += 1

            current_level = current_contents
            current_contents = []
            for color in current_level:
                if base_rules[color]:
                    current_contents.extend(base_rules[color].keys())

            possible_colors.extend(current_contents)

            if i == 1e6:
                print('Infinite loop')
                break

        return possible_colors
    
    # next_level_down() gives us how many bags each bag represents
    #
    # a bottom-level bag represents 1, because it has no contents
    #
    # a bag containing two bags which each contain two bags represents
    # 1 + (2 * (1 + 2 * (1))) = 7 bags
    def next_level_down(self, level) -> int:
        bags = 1

        if not self.contents:
            print('│ ' * level + f'A {self.color} bag contains no bags.')
        else:
            for color in self.contents.keys():
                print('│ ' * (level - 1) + '┌ ' + f'A {self.color} bag contains {self.contents[color]} {color} bags.')
                bags += self.contents[color] * Bag(color).next_level_down(level + 1)

        print('│ ' * (level - 1) + '└ ' + f'Thus, a {self.color} bag represents {bags} bags.')
        return bags
            

could_have_gold = 0
for color in base_rules.keys():
    if 'shiny gold' in Bag(color).all_possible_colors():
        could_have_gold += 1

print(could_have_gold)

# subtract one because the question does not include the gold bag itself
print(Bag('shiny gold').next_level_down(1) - 1)