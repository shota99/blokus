import numpy as np


class UCT1:
    """
    Select the child with the highest upper confidence bound,
    estimate the reward by Q_(s,a).
    """
    def __init__(self, c=1.414):
        self.c = c

    def __call__(self, graph, node):
        return max(graph[node], key=lambda action:
                   graph[node][action]['rewards'][node.current_player] +
                   self.c * np.sqrt(2 * np.log(graph.node[node]['plays']) /
                                    graph[node][action]['plays']))


class Best:
    """
    Select the child with the highest reward
    """
    def __call__(self, graph, node):
        return max(graph[node], key=lambda action:
                   graph[node][action]['rewards'][node.current_player])


class Secure:
    """
    Select the child with the highest lower confidence bound
    """
    def __init__(self, c=1.414):
        self.c = c

    def __call__(self, graph, node):
        return max(graph[node], key=lambda action:
                   graph[node][action]['rewards'][node.current_player] -
                   self.c * np.sqrt(2 * np.log(graph.node[node]['plays']) /
                                    graph[node][action]['plays']))


class Robust:
    """
    Select the most visited child
    """
    def __call__(self, graph, node):
        return max(graph[node], key=lambda action:
                   graph[node][action]['plays'])
