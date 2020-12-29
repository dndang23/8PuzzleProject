import heapq
from Board import Board
from SearchNode import SearchNode

class Solver:

    list = []
    minMoves = 0
    isSol = False

    def __init__(self, initial):
        if initial is None:
            raise ValueError("initial must be not None")
        current = SearchNode(initial)
        current.numMoves = 0
        current.manhattan = initial.manhattan()
        current.priority = current.numMoves + current.manhattan
        pqList = []
        pq = heapq

        twin = initial.twin()
        twinCurrent = SearchNode(twin)
        twinCurrent.numMoves = 0
        twinCurrent.manhattan = twin.manhattan()
        twinCurrent.priority = twinCurrent.numMoves + twinCurrent.manhattan
        twinPQList = []
        twinPQ = heapq

        pq.heappush(pqList, (current.priority, current))
        twinPQ.heappush(twinPQList, (twinCurrent.priority, twinCurrent))

        self.list = []

        tempSol = False
        tempMinMoves = -1

        while len(pqList) != 0 and len(twinPQList) != 0:
            if pqList[0][1].giveBoard().isGoal():
                current = pq.heappop(pqList)
                current = current[1]
                tempSol = True
                tempMinMoves = current.numMoves
                while current is not None:
                    self.list.insert(0, current.giveBoard())
                    current = current.parent
                break

            current = pq.heappop(pqList)
            current = current[1]

            for i in current.giveBoard().neighbors():
                neighbor = SearchNode(i)

                gScore = current.numMoves + 1
                tentativeScore = neighbor.numMoves

                if gScore < tentativeScore:
                    neighbor.numMoves = gScore
                    neighbor.manhattan = neighbor.giveBoard().manhattan()
                    neighbor.priority = neighbor.numMoves + neighbor.manhattan
                    neighbor.parent = current

                    if current.giveBoard() == initial:
                        pq.heappush(pqList, (neighbor.priority, neighbor))
                    else:
                        if current.parent.giveBoard().equals(neighbor.giveBoard()) == False:
                            pq.heappush(pqList, (neighbor.priority, neighbor))

            if twinPQList[0][1].giveBoard().isGoal():
                tempSol = False
                tempMinMoves = -1
                break;

            twinCurrent = twinPQ.heappop(twinPQList)
            twinCurrent = twinCurrent[1]

            for w in twinCurrent.giveBoard().neighbors():
                twinNeighbor = SearchNode(w)
                twinGScore = twinCurrent.numMoves + 1
                twinTentativeScore = twinNeighbor.numMoves

                if twinGScore < twinTentativeScore:
                    twinNeighbor.numMoves = twinGScore
                    twinNeighbor.manhattan = twinNeighbor.giveBoard().manhattan()
                    twinNeighbor.priority = twinNeighbor.numMoves + twinNeighbor.manhattan
                    twinNeighbor.parent = twinCurrent

                    if twinCurrent.giveBoard() == twin:
                        twinPQ.heappush(twinPQList, (twinNeighbor.priority, twinNeighbor))
                    else:
                        if twinCurrent.parent.giveBoard().equals(twinNeighbor.giveBoard()) == False:
                            twinPQ.heappush(twinPQList, (twinNeighbor.priority, twinNeighbor))

        self.isSol = tempSol
        self.minMoves = tempMinMoves

    def isSolvable(self):
        return self.isSol

    def moves(self):
        if isSol == False:
            return -1
        return self.minMoves

    def solution(self):
        if self.isSol == False:
            return None
        else:
            return self.list









def main():
    tiles = [[8, 6, 7], [2, 5, 4], [3, 0, 1]]
    tiles2 = [[5, 1, 3, 2], [10, 6, 15, 7], [9, 8, 11, 4], [0, 13, 14, 12]]
    tiles3 = [[1, 2, 3], [4, 6, 5], [7, 8, 0]]
    tiles4 = [[4, 2, 1], [8, 5, 6], [3, 7, 0]]
    tiles5 = [[12,6,5,10],[15,11,7,1],[3,14,13,2],[9,4,8,0]]
    tiles6 = [[4,6,1,7],[3,8,10,5],[2,11,9,0]]
    board = Board(tiles6)
    sol = Solver(board)
    print("The board is solvable? " + str(sol.isSolvable()))
    for i in sol.solution():
        print(i)

if __name__ == "__main__":
    main()