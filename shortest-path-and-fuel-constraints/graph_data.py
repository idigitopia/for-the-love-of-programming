import os
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import random

# Define Graphs
def defaultGraph(ret_edges= False):
    """
    Defines and returns a graph
    :return:
    Graph is a 1 level deep default Dictionary with default=inf
    Query distance as graph[src][dst] , will be inf if no edges exist.
    """
    edges = [("A", "B", 4), ("E", "B", 3), ("A", "H", 5), ("A", "C", 4), ("C", "E", 10), ("C", "D", 3),
                  ("D", "E", 4), ("F", "B", 4), ("E", "G", 1), ("D", "H", 3), ("G", "H", 1), ("F", "H", 4), ]

    random.shuffle(edges)
    graph = defaultdict( lambda: defaultdict(lambda: float("inf")))
    for s, d, dist in edges:
        graph[s][d], graph[d][s] = dist, dist

    return edges if ret_edges else graph

def longPathGraph(ret_edges= False):
    """
    Defines and returns a graph
    :return:
    Graph is a 1 level deep default Dictionary with default=inf
    Query distance as graph[src][dst] , will be inf if no edges exist.
    """
    edges = [("A", "B", 4), ("E", "B", 3), ("A", "H", 5), ("A", "C", 4), ("C", "E", 10), ("C", "D", 3),
                  ("D", "E", 4), ("F", "B", 4), ("E", "G", 1), ("D", "H", 3), ("G", "H", 1), ("F", "H", 4), ]
    edges += [(f"I{i}", f"I{i + 1}", 1) for i in range(1, 6)]
    edges +=[("A", "I1", 2), ("H", "I6", 3)]

    graph = defaultdict( lambda: defaultdict(lambda: float("inf")))
    for s, d, dist in edges:
        graph[s][d], graph[d][s] = dist, dist

    return edges if ret_edges else graph


def testGraph1(ret_edges= False):
    """
    Defines and returns a graph
    :return:
    Graph is a 1 level deep default Dictionary with default=inf
    Query distance as graph[src][dst] , will be inf if no edges exist.
    """
    edges = [("A", "B", 2), ("B", "D", 9), ("D", "E", 7), ("A", "C", 9), ("C", "D", 3) ]

    graph = defaultdict( lambda: defaultdict(lambda: float("inf")))
    for s, d, dist in edges:
        graph[s][d], graph[d][s] = dist, dist

    return edges if ret_edges else graph


def plotGraph(edges, label):
    if not os.path.exists('graph_plots'):
        os.makedirs('graph_plots')
    plt.figure(figsize=(12,6))
    G=nx.Graph()
    G.add_weighted_edges_from(edges)

    pos =nx.planar_layout(G)
    nx.draw(G,pos, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.savefig(f"graph_plots/{label}.png")  # save as png
    print(f"{label} plotted and saved at graph_plots/{label}.png")


if __name__ == "__main__":
    """ Add a line per graph to plot"""
    plotGraph(defaultGraph(ret_edges=True),label="defaultGraph")
    plotGraph(longPathGraph(ret_edges=True),label="longPathGraph")
    plotGraph(testGraph1(ret_edges=True),label="testGraph1")





