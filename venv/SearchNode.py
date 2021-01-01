#SearchNode class used for Solver.py
class SearchNode:
    #Variables
    parent = None
    node = None
    priority = 0
    manhattan = 0
    numMoves = 0

    #Initializes variables using Board instance
    def __init__(self, board):
        INTEGERMAX = 2147483647
        self.parent = None
        self.node = board
        self.priority = INTEGERMAX
        self.manhattan = INTEGERMAX
        self.numMoves = INTEGERMAX

    #Compares priority value of another SearchNode instance
    def __lt__(self, other):
        return self.priority < other.priority

    #Compares manhattan/priority value of two SearchNodes
    def __le__(self, other):
        if self.__eq__(other):
            return self.manhattan < other.manhattan
        else:
            return self.priority < other.priority

    #Checks if priority values of two SearchNodes are equal
    def __eq__(self, other):
        return self.priority == other.priority

    #Check if priority values of two SearchNodes are not equal
    def __ne__(self, other):
        return not self.__eq__(other)

    #Compares priority values of two SearchNodes
    def __gt__(self, other):
        return other.__lt__(self)

    #Compares manhattan/priority values of two SearchNodes
    def __ge__(self, other):
        return other.__le__(self)


    def giveBoard(self):
        return self.node