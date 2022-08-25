# Algo 1
# By Alex Adams
# the 

import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.matching as nxs
import time


# creates the weight graph
def genGraph(teamPref, length):
    lenT = len(teamPref)
    lenP = length
    edges = []

    for i in range(1, lenP+1):
        m = i % lenT

        for j in range(1, lenP+1):
            edges.append((i, j+lenP, teamPref[m-1][j-1]))

    return edges


# finds who is the player in a matching
def findPlayer(matching, turn):
    for card in matching:
        if card[0] == turn:
            return card[1]
        if card[1] == turn:
            return card[0]
    return 0


# gets the maximum weight of each team pick
# recursive tail function
def getMaxWeight(E, maxWeight, turn, lenP, lenT, teamPref):
    #print(maxWeight)
    if turn > lenP:
        return maxWeight # returns when last turn reached

    else:
        # updates maxweight dict and call function again with next turn
        tempE = list(filter(lambda edge: (edge[0] == turn) or (edge[0] < turn and edge[2] == maxWeight[edge[0]]), E))

        G = nx.Graph()
        G.add_weighted_edges_from(tempE)
        matching = nxs.max_weight_matching(G, maxcardinality=True)
        player = findPlayer(matching, turn) - lenP
        #print(turn, player)
        maxWeight[turn] = teamPref[(turn-1) % lenT][player-1]

        return getMaxWeight(E, maxWeight, turn+1, lenP, lenT, teamPref)


# resolves tiebreakers by finding minimum weight matching for player's priorities
def getMatching(maxWeight, E, playerPref, lenT, lenP):
    E = list(filter(lambda edge: edge[2] == maxWeight[edge[0]], E))

    newE = []

    for edge in E:
        newE.append((edge[0], edge[1], playerPref[edge[1]-lenP-1][(edge[0] - 1) % lenT])) #changed playerPref

    
    G = nx.Graph()
    G.add_weighted_edges_from(newE)
    matching = nxs.min_weight_matching(G, maxcardinality=True)

    return matching

# fixes ordering of matching so that the team is first
def orderMatching(M):
    newM = set()
    for m in M:
        if m[0] > m[1]:
            newM.add((m[1], m[0]))
        else:
            newM.add((m[0], m[1]))
        
    return newM


# modifies result into printable
def polishMatching(M, lenT, lenP):
    D = dict()
    for i in range(1, lenT+1):
        D[i] = set()

    for match in M:
        D[((match[0]-1) % lenT) + 1].add(match[1] - lenP)

    return D


# runs Algorithm 1 from paper
def algo(teamPref, playerPref):
    lenT = len(teamPref)
    lenP = len(playerPref)

    E = genGraph(teamPref, lenP)
    
    maxWeight = dict()
    maxWeight[1] = max(teamPref[0])
    maxWeight = getMaxWeight(E, maxWeight, 2, lenP, lenT, teamPref)

    matching = getMatching(maxWeight, E, playerPref, lenT, lenP)

    return polishMatching(orderMatching(matching), lenT, lenP)


def program(teamPref, playerPref):
    playerPref_ = modPlayerPref(playerPref, len(teamPref))
    G = algo(teamPref, playerPref_)
    return G


def modPlayerPref(P, teams):
    length = len(P[0])
    newP = []
    for V in P:
        newV = [0 for i in range(teams)]
        counter = 0
        for set in V:
            val = counter
            counter += len(set)
            for p in set:
                newV[p-1] = val
        newP.append(newV)

    return newP

#print(modPlayerPref([[{2}, {1}, {3}], [{2}, {3}, {1}], [{3}, {2}, {1}], [{3}, {1}, {2}], [{1}, {2}, {3}], [{3}, {2}, {1}]], 3))


def main():
    teamPref = [[1,1,1,1,1,0], [0,0,0,0,0,1], [0,1,0,1,0,1]]
    playerPref = [[{2,1}, {3}], [{2,3,1}], [{3}, {2}, {1}], [{3}, {1}, {2}], [{1}, {2}, {3}], [{3}, {2}, {1}]] # for each preference list, assigns value to team based on its index
    return program(teamPref, playerPref)

#print(main())