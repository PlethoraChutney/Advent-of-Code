import sys
from itertools import combinations
from math import lcm

timestamp, busses = [x for x in open(sys.argv[1])]

timestamp = int(timestamp.rstrip())
busses = [int(y) for y in busses.rstrip().split(',') if y != 'x']

# part one

bus_to_take = False
times_waited = -1
while not bus_to_take:
    
    times_waited += 1

    for bus in busses:
        if (timestamp + times_waited) % bus == 0:
            bus_to_take = bus

print(times_waited * bus_to_take)

# part two

_, bus_sched = [x for x in open(sys.argv[1])]
bus_sched = [y for y in bus_sched.rstrip().split(',')]

class Bus:
    def __init__(self, frequency, start_at) -> None:
        self.frequency = int(frequency)
        self.start_at = int(start_at)
        self.overlap_with = {}

    def __repr__(self) -> str:
        return f'Bus {self.frequency}: {self.start_at}'

def find_overlap(busses):

    overlaps = []
    ts_0 = busses[0].start_at
    ts_1 = busses[1].start_at

    while len(overlaps) < 2:
        if ts_0 == ts_1:
            overlaps.append(ts_0)
            ts_0 += busses[0].frequency
        elif ts_0 <= ts_1:
            ts_0 += busses[0].frequency
        elif ts_0 > ts_1:
            ts_1 += busses[1].frequency
        else:
            print('Something bad')
            break

    jump = overlaps[1] - overlaps[0]
    combo_bus = Bus(jump, overlaps[0])
    return combo_bus

def all_freq(busses):
    if len(busses) == 2:
        return find_overlap(busses)
    else:
        bus_0 = busses.pop(0)
        bus_1 = busses.pop(0)
        busses.insert(0, find_overlap([bus_0, bus_1]))
        print(busses)
        return all_freq(busses)

def alt_all_freq(busses):
    if len(busses) == 2:
        return find_overlap(busses)
    else:
        bus_0 = busses.pop(0)
        busses = [find_overlap([bus_0, bus]) for bus in busses]
        print(busses)
        return alt_all_freq(busses)


busses = []
for offset, bus in enumerate(bus_sched):
    if bus != 'x':
        busses.append(Bus(bus, -offset))
print(busses)
print(alt_all_freq(busses))
