# EFM Algorithm
# By Alex Adams

import EFandPO_Algorithms.EFM_Partition as m
import networkx as nx
from networkx.algorithms import bipartite


def getEFMatching(PL, HL, P):
    # creates subgraph
    B = nx.Graph()
    B.add_nodes_from(list(PL), bipartite=0)
    B.add_nodes_from(list(HL), bipartite=1)
    edges = []
    for key in P:
        if key not in PL:
            continue

        for i in P[key]:
            if i in HL:
                edges.append((key, -i))



    B.add_edges_from(edges)
    return bipartite.maximum_matching(B, list(PL)) # calls on EFM_Partition file


def program(playerPref, teams):
    PL, HL = m.program(playerPref, teams) # partitions the node and returns the subgraph that contains all EF matchings
    matching = getEFMatching(PL, HL, playerPref) # finds the maximal matching
    matching = {k: v for k, v in matching.items() if k > 0} # gets rid of double counting matches that the networkx function outputs
    return matching