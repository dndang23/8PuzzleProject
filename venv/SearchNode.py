class SearchNode:
    parent = None
    node = None
    priority = 0
    manhattan = 0
    numMoves = 0

    def __init__(self, board):
        INTEGERMAX = 2147483647
        self.parent = None
        self.node = board
        self.priority = INTEGERMAX
        self.manhattan = INTEGERMAX
        self.numMoves = INTEGERMAX

    def __lt__(self, other):
        return self.priority < other.priority

    def __le__(self, other):
        if self.__eq__(other):
            return self.manhattan < other.manhattan
        else:
            return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return other.__lt__(self)

    def __ge__(self, other):
        return other.__le__(self)


    def giveBoard(self):
        return self.node