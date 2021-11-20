from collections import defaultdict
import sys

class Number:
    def __init__(self) -> None:
        self.spoken = []
    
    def __repr__(self) -> str:
        return f'Last spoken at {self.spoken[-1]}'

    def speak(self, turn):
        self.spoken.append(turn)

    def what_to_say(self) -> int:
        if len(self.spoken) == 1:
            return 0
        else:
            return self.spoken[-1] - self.spoken[-2]

number_list = defaultdict(lambda: Number())

starting_list = [x.split(',') for x in open(sys.argv[1])]
starting_list = [int(x) for x in starting_list[0]]

turn = 1
while turn <= 30000000:
    if turn % 100000 == 0:
        print(f'On turn {turn}')
    if turn <= len(starting_list):
        _ = number_list[starting_list[turn - 1]].speak(turn)
        last_spoken = starting_list[turn - 1]
    else:
        last_spoken = number_list[last_spoken].what_to_say()
        number_list[last_spoken].speak(turn)

    turn += 1

print(last_spoken)