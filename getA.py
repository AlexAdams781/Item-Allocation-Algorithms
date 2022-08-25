# getAlloc (non-balanced)
# By Alex Adams


import EFandPO_Algorithms.getAlloc as a
import copy


def appendAll(i, partitions):
    newP = copy.copy(partitions)
    for p in newP:
        p.append(i)

    return newP


def getPartitions(n, teams):
    if teams == 1:
        return [[n]]
    
    if n == 0:
        return [[0 for i in range(teams)]]

    res = []
    for i in range(0, n+1):
        res.extend(appendAll(i, getPartitions(n-i, teams-1)))
    return res


def flatten(L):
    LL = []
    for i in L:
        for j in i:
            LL.append(j)

    return LL


def getA(n, teams):
    L = getPartitions(n, teams)
    As = []
    for p in L:
        As.append(a.getAllocs(p, n))

    sum = 0
    for A in As:
        sum += len(A)

    As = flatten(As)

    return As