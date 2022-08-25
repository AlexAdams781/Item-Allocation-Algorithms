# EF-1 Graph Generator
# Also outputs num. of envy free agents
# By Alex Adams

import numpy as np
import copy

# greates blank adjacency matrix
def newGraph(n):
    return [[0 for i in range(n)] for j in range(n)]


def createValGraph(A, V, length):
    ng = newGraph(length)

    for i in range(length):
        newA = A[i]
        for j in range(length):
            for k in newA:
                ng[j][i] += V[j][k]
    
    return ng


# returns a graph of the maximum value of an item in agent i's valuation of agent j's bundle
def createMaxValGraph(A, V, length):
    ng = newGraph(length)

    for i in range(length):
        newA = A[i]
        for j in range(length):
            currMax = 0
            for k in newA:
                currMax = max(currMax, V[j][k])
            ng[j][i] += currMax
    
    return ng


# subtracts two matrices (leaves the diagonal column alone)
def subMatrices(A, B, length):
    C = copy.deepcopy(A)

    for i in range(length):
        for j in range(length):
            if i != j:
                C[i][j] = A[i][j] - B[i][j]

    return C


# makes envy graph
def egAlgo(alloc, valFun):  
    length = len(alloc)
    ng = newGraph(length)

    valGraph = createValGraph(alloc, valFun, length)

    maxValGraph = createMaxValGraph(alloc, valFun, length)

    valGraph = subMatrices(valGraph, maxValGraph, length)

    for i in range(length):
        for j in range(length):
            if i != j:  # for each non-diagonal entry . . .
                envy = valGraph[i][j] - valGraph[i][i]
                if envy > 0:    # adds envy iff envy value is greater than 0
                    ng[i][j] = envy

    return ng


def getEnvyFree(G):
    agents = set()
    for i in range(len(G)):
        agents.add(i+1)
        for x in G[i]:
            if x != 0:
                agents.remove(i+1)
                break
    
    return agents


def main():
    alloc = [[0,3], [1,4], [2]] # fix me
    valFun = [[1,11,13,14,13], [11,17,17,8,4], [12,17,19,2,8]]
    envyGraph = egAlgo(alloc, valFun)
    L = getEnvyFree(envyGraph)
    print(np.array(envyGraph))
    print()
    print("Envy free agents:", L, " # of them:", len(L))


def program(alloc, valFun):
    return egAlgo(alloc, valFun)