import sys
import numpy as np
from queue import Queue

risk_array = np.array([
    [int(x) for x in y.rstrip()] for y in open(sys.argv[1])
])


# use dijkstra's algorithm to traverse a weighted graph:
# https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html

class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    def construct_graph(self, nodes, init_graph):
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value

        return graph

    def get_outgoing_edges(self, node):
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        return self.graph[node1][node2]


def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.nodes)
    shortest_path = {}
    previous_nodes = {}

    for node in unvisited_nodes:
        shortest_path[node] = np.inf

    shortest_path[start_node] = 0

    while unvisited_nodes:
        dists = [shortest_path[x] for x in unvisited_nodes]
        current_min_node = unvisited_nodes[dists.index(min(dists))]
        for node in unvisited_nodes:
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                previous_nodes[neighbor] = current_min_node

        unvisited_nodes.remove(current_min_node)


    return previous_nodes, shortest_path

def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # don't add start node b/c we only care about nodes we "enter"

    print(shortest_path[target_node])

if sys.argv[2] == '1':

    init_graph = {}
    nodes = []
    for node, _ in np.ndenumerate(risk_array):
        init_graph[node] = {}
        nodes.append(node)
        
        neighbors = [
            (node[0] + 1, node[1]),
            (node[0] - 1, node[1]),
            (node[0], node[1] + 1),
            (node[0], node[1] - 1)
        ]
        neighbors = [
            x for x in neighbors if \
                0 <= x[0] < risk_array.shape[0] and \
                0 <= x[1] < risk_array.shape[1]
        ]

        for neighbor in neighbors:
            init_graph[node][neighbor] = risk_array[neighbor]

    graph = Graph(nodes, init_graph)

    previous_nodes, shortest_path = dijkstra_algorithm(graph, (0,0))

    print_result(
        previous_nodes,
        shortest_path,
        (0,0),
        tuple(np.array(risk_array.shape) - (1,1))
    )

else:

    # haha this is going to be slow as fuck

    def make_row(risk_array):
        row = [risk_array]
        for _ in range(1, 5):
            row.append((row[-1] % 9) + 1)
            
        return row
        
    left_column = make_row(risk_array)
    big_grid = []
    for grid in left_column:
        big_grid.append(np.concatenate(make_row(grid), axis = 1))
    big_grid = np.concatenate(big_grid, axis = 0)


    init_graph = {}
    nodes = []
    for node, _ in np.ndenumerate(big_grid):
        init_graph[node] = {}
        nodes.append(node)
        
        neighbors = [
            (node[0] + 1, node[1]),
            (node[0] - 1, node[1]),
            (node[0], node[1] + 1),
            (node[0], node[1] - 1)
        ]
        neighbors = [
            x for x in neighbors if \
                0 <= x[0] < big_grid.shape[0] and \
                0 <= x[1] < big_grid.shape[1]
        ]

        for neighbor in neighbors:
            init_graph[node][neighbor] = big_grid[neighbor]

    graph = Graph(nodes, init_graph)

    previous_nodes, shortest_path = dijkstra_algorithm(graph, (0,0))

    print_result(
        previous_nodes,
        shortest_path,
        (0,0),
        tuple(np.array(big_grid.shape) - (1,1))
    )