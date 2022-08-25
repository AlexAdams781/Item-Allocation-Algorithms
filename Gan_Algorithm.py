# Gan Algorithm
# By Alex Adams

import networkx as nx
from networkx.algorithms import bipartite


def createMatching(P, H):
    B = nx.Graph()
    B.add_nodes_from([i for i in range(1, len(P)+1)], bipartite=0)
    B.add_nodes_from([-i for i in range(1, len(H)+1)], bipartite=1)
    edges = []
    for key in P:
        for i in P[key]:
            edges.append((key, -i))
    B.add_edges_from(edges)

    genMatching = bipartite.maximum_matching(B, [i for i in range(1, len(P)+1)])

    matching = {k: v for k, v in genMatching.items() if k > 0}
    matching = {k: (-v) for k, v in matching.items()}

    invMatching = {k: v for k, v in genMatching.items() if k < 0}
    invMatching = {(-k): v for k, v in invMatching.items()}
    return matching, invMatching


def getUnmatched(M, H):
    U = set()
    for i in H:
        if i not in M:
            return i
        
    return None


def DFS(house, found, M, P):
    print("found", house)
    found.add(house)
    for p in P[M[house]]:
        print("p", p)
        if p not in found:
            DFS(p, found, M, P)
        
    return found


def findHallSet(M, invM, P, H):
    players = {i for i in range(1, len(P)+1)}
    unmatched = getUnmatched(M, players)

    hallSet = set()
    for p in P[unmatched]:
        if p in hallSet:
            continue

        hazmat = DFS(p, set(), invM, P)
        hallSet = hallSet | hazmat
        hallSet.add(p)

    return hallSet


def getTopPref(P):
    topPref = dict()
    for i in range(len(P)):
        topPref[i+1] = P[i][0]
    
    return topPref


def updatePref(P, hSet):
    newP = []

    for V in P:
        newV = []
        for elem in V:
            newS = elem - hSet
            if len(newS) > 0:
                newV.append(newS)

        newP.append(newV)
    
    return newP


def algo(P, H):
    topPref = getTopPref(P)

    while len(H) >= len(topPref):
        M, invM = createMatching(topPref, H)
        if len(M) == len(topPref):
            return M
        
        hSet = findHallSet(M, invM, topPref, H)
        print(hSet)
        H = H - hSet

        P = updatePref(P, hSet)
        topPref = getTopPref(P)

    return None


def program(agentPref, houses):
    H = {i for i in range(1, houses+1)}
    matching = algo(agentPref, H)
    return matching

#print(program([[{2}, {1}, {3}, {4}, {5}], [{1}, {2,3,4,5}], [{2}, {3,4,5}, {1}], [{1,5}, {3}, {2,4}]], 5))
print(program([[{2}, {1}, {3}, {4}, {5}], [{1}, {2,3,4,5}], [{2}, {3,4,5}, {1}], [{1,5}, {3}, {2,4}]], 5))