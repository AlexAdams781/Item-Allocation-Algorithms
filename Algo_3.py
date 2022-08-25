# Algorithm 3
# By Alex Adams


def findIndifference(teamPref, playerPref):
    D = {1: set(), 2: set()}
    for i in range(len(teamPref[0])):
        if teamPref[0][i] == 0 and teamPref[1][i] == 0:
            if i in playerPref[1]:
                D[1].add(i)
            else:
                D[2].add(i)

    return D


def getPartitions(teamPref, playerPref):
    P1, P2, PPlus, PMinus = set(), set(), set(), set()

    for i in range(len(teamPref[0])):
        if teamPref[0][i] >= 0 and teamPref[1][i] <= 0:
            P1.add(i+1)
        
        elif teamPref[0][i] <= 0 and teamPref[1][i] >= 0:
            P2.add(i+1)

        elif teamPref[0][i] > 0:
            PPlus.add(i+1)
        
        else:
            PMinus.add(i+1)

    return P1, P2, PPlus, PMinus


def prio(p, P, b):
    if (b and p not in P[1] and p in P[2]) or (not b and p in P[1] and p not in P[2]):
        return 1
    elif p in P[1] and p in P[2]:
        return 2
    else:
        return 3


def getPrioList(S, PPlus, T, P):
    V = set()
    for p in S:
        V.add((p, (T[0][p-1] / T[1][p-1]), prio(p, P, p in PPlus)))
    V = list(V)
    #print(V)
    V.sort(key=lambda k: (k[1], k[2]))
    
    L = []
    for elem in V:
        L.append(elem[0])
    L.reverse()
    return L


def EF1(A1, A2, teamPref):
    maxItem = 0
    otherBundle = 0
    for elem in A1:
        val = teamPref[1][elem-1]
        otherBundle += val
        if val > maxItem:
            maxItem = val
    otherBundle -= maxItem

    myBundle = 0
    for elem in A2:
        myBundle += teamPref[1][elem-1]

    if myBundle >= otherBundle:
        return True
    return False


def algo(teamPref, playerPref):
    indifferentTeamAlloc = findIndifference(teamPref, playerPref)
    P1, P2, PPlus, PMinus = getPartitions(teamPref, playerPref)
    prioList = getPrioList(PPlus.union(PMinus), PPlus, teamPref, playerPref)
    A1, A2 = PPlus.union(P1), PMinus.union(P2)

    while not EF1(A1, A2, teamPref):
        p = prioList.pop()
        if p in PPlus:
            A1.remove(p)
            A2.add(p)
        else:
            A1.add(p)
            A2.remove(p)

    res = {1: A1, 2: A2}
    return res


def modPlayerPref(P):
    D = dict()
    D[1] = set()
    D[2] = set()

    for i in range(1, len(P)+1):
        if 1 in P[i-1][0]:
            D[1].add(i)
        if 2 in P[i-1][0]:
            D[2].add(i)

    return D


def program(teamPref, playerPref):
    playerPref_ = modPlayerPref(playerPref)
    alloc = algo(teamPref, playerPref_)
    return alloc


def main():
    teamPref = [[0,0,0,4,4,2,1,1,4,2,4,2], [4,1,4,1,2,0,3,4,2,3,1,0]]
    playerPref = [[{2},{1}], [{1,2}], [{1,2}], [{1},{2}], [{2},{1}], [{2},{1}], [{1},{2}], [{2},{1}], [{2},{1}], [{2,1}], [{1,2}], [{1},{2}]]
    playerPref_ = modPlayerPref(playerPref)
    alloc = algo(teamPref, playerPref_)

    return alloc