#Solver class that solves a puzzle to its goal state
import heapq
from Board import Board
from SearchNode import SearchNode

class Solver:

    #Variables
    list = []
    minMoves = 0
    isSol = False

    #Given a Board instance, the Solver uses the A* algorithm, implemented by a priority queue, to solve
    #the board
    def __init__(self, initial):
        #If no arguement then raise error
        if initial is None:
            raise ValueError("initial must be not None")
        #Creates a SearchNode instance using Board instance
        current = SearchNode(initial)
        #Sets number of moves, manhattan value, and priority value of SearchNode
        current.numMoves = 0
        current.manhattan = initial.manhattan()
        current.priority = current.numMoves + current.manhattan

        #Creates list and priority queue instance
        pqList = []
        pq = heapq

        #Creates a second board using the twin of the argument board to help determine if a board is solvable
        twin = initial.twin()
        twinCurrent = SearchNode(twin)
        twinCurrent.numMoves = 0
        twinCurrent.manhattan = twin.manhattan()
        twinCurrent.priority = twinCurrent.numMoves + twinCurrent.manhattan
        twinPQList = []
        twinPQ = heapq

        #Pushes the SearchNode and its priority into priority queue
        pq.heappush(pqList, (current.priority, current))

        #Pushes twin SearchNode and its priority into separate priority queue
        twinPQ.heappush(twinPQList, (twinCurrent.priority, twinCurrent))

        #Initializes list that keeps track of correct steps of inital board to its goal state
        self.list = []

        #Temporarily initialize variables
        tempSol = False
        tempMinMoves = -1

        #Loops until either priority queue is empty
        while len(pqList) != 0 and len(twinPQList) != 0:
            #Checks if the first element in priority queue is solved
            if pqList[0][1].giveBoard().isGoal():
                #If first element in priority queue is solved then board has been successfully solved
                current = pq.heappop(pqList)
                current = current[1]
                #Set solvability to true
                tempSol = True
                #Set the number of moves to reach goal state
                tempMinMoves = current.numMoves
                #Loop through current SeachNode to add all correct steps to reach goal state
                while current is not None:
                    self.list.insert(0, current.giveBoard())
                    current = current.parent
                #End the loop
                break

            #If the board has not reach its goal state then pop the SearchNode with the smallest priority
            current = pq.heappop(pqList)
            current = current[1]

            #Look through each neighbor of the popped SearchNode
            for i in current.giveBoard().neighbors():
                #Create a SearchNode object for each neighbor
                neighbor = SearchNode(i)

                #Set value of gScore to the number of moves made to current SearchNode and add one
                gScore = current.numMoves + 1
                #Get the number of moves made to reach neighbor puzzle
                tentativeScore = neighbor.numMoves

                #Check if the number of moves made to reach neighbor through the current SearchNode
                #is less than the number of moves made to reach neighbor through a previous SearchNode
                if gScore < tentativeScore:
                    #If true then update the number of moves, manhattan value, and priority
                    #alone with setting the neighbor's parent to the current SearchNode
                    neighbor.numMoves = gScore
                    neighbor.manhattan = neighbor.giveBoard().manhattan()
                    neighbor.priority = neighbor.numMoves + neighbor.manhattan
                    neighbor.parent = current

                    #--------Conditions below used to limit the number of cases--------
                    #If the current board is the same as the argument then push the neighbor SearchNode into
                    #the priority queue
                    if current.giveBoard() == initial:
                        pq.heappush(pqList, (neighbor.priority, neighbor))
                    else:
                        #Else if the current board and neighbor board are not the same then push the neighbor
                        #SearchNode into the priority queue
                        if current.parent.giveBoard().equals(neighbor.giveBoard()) == False:
                            pq.heappush(pqList, (neighbor.priority, neighbor))

            #Checks if the first element in the twin priority queue has board in its goal state
            if twinPQList[0][1].giveBoard().isGoal():
                #If it does then the board is unsolvable
                tempSol = False
                tempMinMoves = -1
                break;

            #Remove the current SearchNode in the twin priority queue with the lowest priority
            twinCurrent = twinPQ.heappop(twinPQList)
            twinCurrent = twinCurrent[1]

            #Loops through the neighbors of the twinCurrent board
            for w in twinCurrent.giveBoard().neighbors():
                #Creates a SearchNode object with the neighbor board
                twinNeighbor = SearchNode(w)
                #Initializes the numbers of moves made to the twinCurrent SearchNode plus one
                twinGScore = twinCurrent.numMoves + 1
                #Initializes the number of moves made to reach the neighbor from a previous twinSearchNode
                twinTentativeScore = twinNeighbor.numMoves

                #Check if the number of moves made to reach neighbor through the twinCurrent SearchNode
                #is less than the number of moves made to reach neighbor through a previous SearchNode
                if twinGScore < twinTentativeScore:
                    #If true then update the number of moves, manhattan value, and priority value of
                    #the twinNeighbor SearchNode as well as the parent of the twinNeighbor
                    twinNeighbor.numMoves = twinGScore
                    twinNeighbor.manhattan = twinNeighbor.giveBoard().manhattan()
                    twinNeighbor.priority = twinNeighbor.numMoves + twinNeighbor.manhattan
                    twinNeighbor.parent = twinCurrent

                    # --------Conditions below used to limit the number of cases--------
                    #If the twinCurrent board is the same as the argument then push the neighbor SearchNode into
                    #the twin priority queue
                    if twinCurrent.giveBoard() == twin:
                        twinPQ.heappush(twinPQList, (twinNeighbor.priority, twinNeighbor))
                    else:
                        #Else if the twinCurrent board and neighbor board are not the same then push the neighbor
                        #SearchNode into the twin priority queue
                        if twinCurrent.parent.giveBoard().equals(twinNeighbor.giveBoard()) == False:
                            twinPQ.heappush(twinPQList, (twinNeighbor.priority, twinNeighbor))

        #After the loop breaks, set the values of solvability of the board and its number of moves
        #to reach the goal state
        self.isSol = tempSol
        self.minMoves = tempMinMoves

#Returns whether or not the board is solvable
    def isSolvable(self):
        return self.isSol

#Returns the number of moves to reach goal state
    def moves(self):
        if isSol == False:
            return -1
        return self.minMoves

#Returns the list of steps for the board to reach the goal state
    def solution(self):
        if self.isSol == False:
            return None
        else:
            return self.list

#Main method
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

#Used to call main method
if __name__ == "__main__":
    main()