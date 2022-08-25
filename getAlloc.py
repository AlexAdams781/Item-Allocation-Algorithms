# getAllocs
# By Alex Adams

import itertools
import copy


def noCommon(A, B):
    for set in B:
        for i in A:
            if i in set:
                    return False
    return True


def combineLists(S1, S2):
    S = []
    for s1 in S1:
        for s2 in S2:
            if noCommon(s1, s2):
                s3 = copy.copy(s2)
                s3.append(s1)
                S.append(s3)
    return S


def getCombo(players, size):
    L = []
    for i in itertools.combinations(players, size):
        S = set()
        for j in range(size):
            S.add(i[j])
        L.append(S)
    return L



def getAllocs(L, n):
    As = getCombo({j for j in range(1, n+1)}, L.pop(0))
    newAs = []
    for elem in As:
        newAs.append([elem])
    
    for i in L:
        A = getCombo({j for j in range(1, n+1)}, i)
        newAs = combineLists(A, newAs)

    finAs = []
    for A in newAs:
        D = dict()
        count = 1
        for all in A:
            D[count] = all
            count += 1
        finAs.append(D)

    return finAs