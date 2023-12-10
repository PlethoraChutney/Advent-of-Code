#!/usr/bin/env python
import re

with open("input.txt", "r") as f:
    lines = [x.rstrip() for x in f]

cards = {}

for line in lines:
    card = int(re.match(r"Card +([0-9]+): ", line).group(1))
    line = line.split(": ")[1]
    winning, have = line.split(" | ")
    winning = set(int(x) for x in winning.split())
    have = set(int(x) for x in have.split())
    win_have = winning.intersection(have)

    cards[card] = {"card": card, "winning": winning, "have": have, "win_have": win_have}

# part one

total_score = 0
for card in cards.values():
    total_score += int(2 ** (len(card["win_have"]) - 1))

print(f"Part one: {total_score}")

# part two
# too slow to do it the dumb way

cards_to_score = list(range(1, len(lines) + 1))
num_cards = 0
card_memos = {}


def get_card_extension(card_index):
    card = cards[card_index]
    if len(card["win_have"]) == 0:
        return 1
    else:
        extension = 1
        for card_index in range(
            card["card"] + 1, card["card"] + len(card["win_have"]) + 1
        ):
            extension += get_card_extension(card_index)
        return extension


# work backward since we know that cards will only ever add cards
# after themselves
for card_index in range(len(cards), 0, -1):
    card_memos[card_index] = get_card_extension(card_index)

print(f"Part two: {sum(card_memos.values())}")
