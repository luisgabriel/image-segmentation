class Node:
    def __init__(self, parent, rank=0, size=1):
        self.parent = parent
        self.rank = rank
        self.size = size

    def __repr__(self):
        return '(parent=%s, rank=%s, size=%s)' % (self.parent, self.rank, self.size)

class Forest:
    def __init__(self, num_nodes):
        self.nodes = [Node(i) for i in xrange(num_nodes)]
        self.num_sets = num_nodes

    def size_of(self, i):
        return self.nodes[i].size

    def find(self, n):
        temp = n
        while temp != self.nodes[temp].parent:
            temp = self.nodes[temp].parent

        self.nodes[n].parent = temp
        return temp

    def merge(self, a, b):
        if self.nodes[a].rank > self.nodes[b].rank:
            self.nodes[b].parent = a
            self.nodes[a].size = self.nodes[a].size + self.nodes[b].size
        else:
            self.nodes[a].parent = b
            self.nodes[b].size = self.nodes[b].size + self.nodes[a].size

            if self.nodes[a].rank == self.nodes[b].rank:
                self.nodes[b].rank = self.nodes[b].rank + 1

        self.num_sets = self.num_sets - 1

    def print_nodes(self):
        for node in self.nodes:
            print node

def build_graph(image, diff):
    img = image.load()
    width = image.size[0]
    height = image.size[1]

    graph = []
    for y in xrange(height):
        for x in xrange(width):
            if x < width-1:
                w = diff(img, x, y, x+1, y)
                graph.append([y * width + x, y * width + (x+1), w])

            if y < height-1:
                w = diff(img, x, y, x, y+1)
                graph.append([y * width + x, (y+1) * width + x, w])

            if x < width-1 and y < height-1:
                w = diff(img, x, y, x+1, y+1)
                graph.append([y * width + x, (y+1) * width + (x+1), w])

            if x < width-1 and y > 0:
                w = diff(img, x, y, x+1, y-1)
                graph.append([y * width + x, (y-1) * width + (x+1), w])

    return graph

def remove_small_components(forest, graph, min_size):
    for edge in graph:
        a = forest.find(edge[0])
        b = forest.find(edge[1])

        if a != b and (forest.size_of(a) < min_size or forest.size_of(b) < min_size):
            forest.merge(a, b)

    return  forest

def segment_graph(graph, num_nodes, const, min_size, threshold_func):
    weight = lambda edge: edge[2]

    forest = Forest(num_nodes)
    sorted_graph = sorted(graph, key=weight)
    threshold = [const] * num_nodes

    for edge in sorted_graph:
        parent_a = forest.find(edge[0])
        parent_b = forest.find(edge[1])
        a_condition = weight(edge) <= threshold[parent_a]
        b_condition = weight(edge) <= threshold[parent_b]

        if parent_a != parent_b and a_condition and b_condition:
            forest.merge(parent_a, parent_b)
            a = forest.find(parent_a)
            threshold[a] = weight(edge) + threshold_func(forest.nodes[a].size, const)

    return remove_small_components(forest, sorted_graph, min_size)
