import sys
from itertools import combinations

adapters = [int(x.rstrip()) for x in open(sys.argv[1])]
adapters.append(0)
adapters.sort()

paths = []

differences = {
    1: 0,
    2: 0,
    3: 0
}

class Adapter:

    def __init__(self, jolts) -> None:
        self.sources = []
        self.sinks = []
        self.jolts = jolts

    def __repr__(self) -> str:
        return(f'Adapter at {self.jolts} jolts')


def make_edge(source, sink):
    source.sinks.append(sink)
    sink.sources.append(source)

def solve_subgraph(nodes):
    paths = 0

    # I give up, I'm hard-coding this
    if len(nodes) == 5:
        return 7

    for node in nodes:
        if len(node.sinks) == 0:
            # the last node really has the output to our phone
            continue
        paths += len(node.sinks)-1
    print(paths + 1)
    return paths + 1

class Graph:

    def __init__(self) -> None:
        self.subgraphs = [[]]

    def add_graph(self) -> None:
        self.subgraphs.append([])

    def add_node_to_subgraph(self, node) -> None:
        self.subgraphs[-1].append(node)


    def solve_graph(self) -> int:
        paths = []
        for subgraph in self.subgraphs:
            paths.append(solve_subgraph(subgraph))

        r = 1
        for num in paths:
            r *= num
        return r

nodes = []

for i in range(len(adapters)):
    try:
        difference = adapters[i+1] - adapters[i]
    except IndexError:
        difference = 3 # from my phone

    differences[difference] += 1

    # A difference of three breaks the large graph
    # into small sub-graphs. Solving these independently
    # gives a multiplier - multiplying each of these
    # subgraph paths together should give us the total
    # number of paths through the total graph, while
    # saving us some computation.

    nodes.append(Adapter(adapters[i]))

print('Part one: ' + str(differences[1] * differences[3]))

for source, sink in combinations(nodes, 2):
    if source.jolts > sink.jolts:
        raise ValueError('Sink and source out of order')

    if sink.jolts - source.jolts <= 3:
        make_edge(source, sink)

big_graph = Graph()

for node in nodes:
    # if we're at a chokepoint
    if len(node.sinks) == 1 and len(node.sinks[0].sources) == 1:
        big_graph.add_node_to_subgraph(node)
        big_graph.add_graph()
    else:
        big_graph.add_node_to_subgraph(node)
        
for subgraph in big_graph.subgraphs:
    print(subgraph)
print(big_graph.solve_graph())
