import sys

caves = {}

def add_cave(cave, link):
    if link != 'start':
        try:
            caves[cave].append(link)
        except KeyError:
            caves[cave] = [link]

    if cave != 'start':
        try:
            caves[link].append(cave)
        except KeyError:
            caves[link] = [cave]

with open(sys.argv[1], 'r') as f:
    for line in f:
        add_cave(*line.rstrip().split('-'))

# ugh it's this fucking problem again
# part one
def paths_to_exit(node, count, part):

    # only keep track of visited nodes if they're lowercase
    if node.lower() == node and not node in ['start', 'end']:
        visited[node] += 1

    # if the node is the end, we increment the count
    if node == 'end':
        count[0] += 1
    
    else:
        for adj_node in caves[node]:
            # if the node is at the end or we haven't visited it, find its paths to end
            if adj_node == 'end' or visited[adj_node] < 1 and part == 1:
                paths_to_exit(adj_node, count, part)
            # disgusting. I fucking hate these.
            # for part two, same as above except we check if any visited values are greater
            # than two
            elif adj_node == 'end' or visited[adj_node] < 1 or (
                visited[adj_node] == 1 and not any([x > 1 for x in visited.values()])) \
                    and part == 2:
                    paths_to_exit(adj_node, count, part)

    # if we marked a node as visited, unvisit it for the next iteration
    if visited[node] > 0:
        visited[node] -= 1

count = [0]
visited = {}
for cave in caves.keys():
    visited[cave] = 0
paths_to_exit('start', count, 1)
print(count[0])

count = [0]
visited = {}
for cave in caves.keys():
    visited[cave] = 0
paths_to_exit('start', count, 2)
print(count[0])