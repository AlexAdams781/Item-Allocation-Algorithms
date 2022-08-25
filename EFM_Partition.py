# Find EFM Partition
# By Alex Adams

import networkx as nx
from networkx.algorithms import bipartite
import copy


def findUnmatched(M, S):
    U = set()
    for i in S:
        if i not in M:
            U.add(i)
        
    return U


def getPartition(freePlayers, freeHouses, P, matching, newSet):
    fullPlayers = copy.copy(freePlayers)
    fullHouses = copy.copy(freeHouses)
    freePlayers = freePlayers - newSet

    while True:
        newSet_ = set()
        for p in newSet:
            for house in P[p]:
                if house in freeHouses:
                    newSet_.add(house)
                    freeHouses.remove(house)
            
        if len(newSet_) == 0:
            break

        newSet = set()
        for h in newSet_:
            player = matching[h]
            if player in freePlayers:
                newSet.add(player)
                freePlayers.remove(player)

        if len(newSet) == 0:
            break

    for p in freePlayers:
        fullPlayers.remove(p)
    for h in freeHouses:
        fullHouses.remove(h)

    return fullPlayers, freePlayers, fullHouses, freeHouses


def invMatching(M):
    D = {k: v for k, v in M.items() if k < 0}
    D = {(-k): v for k, v in D.items()}
    return D


def algo(P, H):
    # creates graph and adds in edges that exist in the player preference list
    B = nx.Graph()
    B.add_nodes_from([i for i in range(1, len(P)+1)], bipartite=0)
    B.add_nodes_from([-i for i in range(1, len(H)+1)], bipartite=1)
    edges = []
    for key in P:
        for i in P[key]:
            edges.append((key, -i))
    B.add_edges_from(edges)

    # finds maximal matching in that graph
    matching = bipartite.maximum_matching(B, [i for i in range(1, len(P)+1)])
    


    freePlayers = {i for i in range(1, len(P)+1)}
    freeHouses = {i for i in range(1, len(H)+1)}
    unmatched = findUnmatched(matching, freePlayers)

    matching = invMatching(matching)

    # Runs algorithm to find maximal M-alternating sequence from the set of unmatched players
    # then computes partition
    PM, PL, HM, HL = getPartition(freePlayers, freeHouses, P, matching, unmatched)

    return PM, PL, HM, HL


def program(playerPref, H):
    houses = {i for i in range(1, H+1)}

    PM, PL, HM, HL = algo(playerPref, houses)
    return PL, HL

program({1: {1}, 2: {2,3}, 3: {1,4}, 4: {2,4}, 5: {1,3,4}, 6: {2,3,4}, 7: {3,5}, 8: {4,6,7}}, 7)