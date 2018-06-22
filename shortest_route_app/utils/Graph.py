from collections import defaultdict


class Graph():
    def __init__(self):
        """
        create a structure that list all the possibles next steps for each point(edge) and their distance. for being bidirectional it does for the going and turning back
        e.g. {'A': ['B', 'C', 'E'], ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # first from_node -> to_node, after : to_node -> from_node
        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight
        self.edges[to_node].append(from_node)
        self.weights[(to_node, from_node)] = weight
