# Algo 2
# By Alex Adams

import Algo_1
import copy

def partitionPlayers(P):
    minus = set()
    plus = set()
    for i in range(len(P[0])):
        neg = True

        for j in range(len(P)):
            if P[j][i] >= 0:
                neg = False
                break

        if neg:
            minus.add(i+1)
        else:
            plus.add(i+1)

    return plus, minus


def partitionPref(teamPref, playerPref, plus, minus):
    teamPref1, playerPref1, teamPref2, playerPref2 = copy.deepcopy(teamPref), [], copy.deepcopy(teamPref), []

    for i in range(len(playerPref)):
        if (i + 1) in plus:
            playerPref1.append(playerPref[i])
        else:
            playerPref2.append(playerPref[i])

    plus = sorted(list(plus), reverse=True)
    minus = sorted(list(minus), reverse=True)

    for V in teamPref1:
        for i in minus:
            del V[i-1]

    for V in teamPref2:
        for i in plus:
            del V[i-1]

    return teamPref1, playerPref1, teamPref2, playerPref2


def addDummies(plus, minus, teamPref1, playerPref1, teamPref2, playerPref2, lenT):
    plusDummies = (lenT - 1) * len(plus) + lenT
    minusDummies = (lenT - 1) * len(minus) + lenT

    for V in teamPref1:
        V.extend([0 for i in range(plusDummies)])
    
    for V in teamPref2:
        V.extend([0 for i in range(minusDummies)])

    dummyVal = [1 for i in range(lenT)]

    playerPref1.extend([dummyVal for i in range(plusDummies)])
    playerPref2.extend([dummyVal for i in range(minusDummies)])

    pass


def updateAlloc(A, An, count, i):
    index = 0
    for key in An:
        if (i - count) in An[key]:
            index = key
            break
    
    A[index].add(i)
    pass

def zipAlloc(A1, A2, plus, minus, lenT):
    A = dict()
    for i in range(lenT):
        A[i+1] = set()

    count1 = 0
    count2 = 0

    for i in range(1, len(plus) + len(minus) + 1):
        if i in plus:
            updateAlloc(A, A1, count1, i)
            count2 += 1
        else:
            updateAlloc(A, A2, count2, i)
            count1 += 1

    return A


def reverseTeamPref(P):
    length = len(P)
    newP = []

    for i in range(1, length + 1):
        newP.append(P[length - i])

    return newP


def reversePlayerPref(P):
    for V in P:
        V.reverse()
    pass


def reverseAlloc(P):
    length = len(P)
    newP = dict()

    for i in range(1, length + 1):
        print(i, length - i + 1)
        newP[i] = P[length - i + 1]

    return newP


def algo(teamPref, playerPref):
    plus, minus = partitionPlayers(teamPref)

    # partitions the teams and players based on (+) (-) valuations
    teamPref1, playerPref1, teamPref2, playerPref2 = partitionPref(teamPref, playerPref, plus, minus)

    # adds sufficient dummies to each side of the partition
    addDummies(plus, minus, teamPref1, playerPref1, teamPref2, playerPref2, len(teamPref))

    # runs Algo 1 on the positive valuation preference lists
    A1 = Algo_1.program(teamPref1, playerPref1)

    # runs Algo 2 (in reverse order) on the negative valuation preference lists
    teamPref2 = reverseTeamPref(teamPref2)
    reversePlayerPref(playerPref2)
    A2 = Algo_1.program(teamPref2, playerPref2)
    A2 = reverseAlloc(A2)


    # combines both allocations into one
    A = zipAlloc(A1, A2, plus, minus, len(teamPref))
    return A


def modStrictPref(P):
    newP = []
    for i in P:
        new = [0,0,0]
        for j in range(len(P[0])):
            new[i[j]-1] = j+1
        
        newP.append(new)

    return newP


def main():
    teamPref = [[5,5,5,5,5,5,5,5,5], [2,2,2,2,2,2,2,2,2], [1,1,1,1,1,1,1,1,1]]
    playerPref = [[3,2,1], [1,2,3], [2,3,1], [2,3,1], [1,3,2], [3,1,2], [1,3,2], [2,1,3], [3,1,2]]

    playerPref = modStrictPref(playerPref)

    G = algo(teamPref, playerPref)
    print(G)

main()