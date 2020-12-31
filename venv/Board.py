#Board class
class Board:
    #Variables
    dimensions = 0
    board = []
    manhattanCounter = 0
    hammingCounter = 0
    manhattan = 0
    hamming_var = 0

    #Creates 2d array board
    def __init__(self, tiles):
        self.dimensions = len(tiles)
        counter = 1
        self.board = [[0 for i in range(self.dimensions)] for j in range(self.dimensions)]
        for row in range (0, self.dimensions):
            for column in range (0, self.dimensions):
                self.board[row][column] = tiles[row][column]
            counter = counter + self.dimensions

    #Prints out the board
    def __str__(self):
        string = ""
        for row in range(self.dimensions):
            for column in range(self.dimensions):
                string = string + str(self.board[row][column]) + " "
            string = string + "\n"
        return string

    #Converts number into x coordinate
    def __getX(self, num):
        counter = 0
        while num > self.dimensions:
            counter = counter + 1
            num = num - self.dimensions
        return counter

    #Converts number into y coordinate
    def __getY(self, num):
        while num > self.dimensions:
            num = num - self.dimensions
        return num - 1

    #Returns board
    def __getBoard(self):
        return self.board

    #Returns dimension of board
    def dimension(self):
        return self.dimensions

    #Calculates hamming of board
    def hamming(self):
        if self.hammingCounter == 0:
            counter = 0
            numTracker = 1
            for row in range(self.dimensions):
                for column in range(self.dimensions):
                    if self.board[row][column] != numTracker and self.board[row][column] != 0:
                        counter = counter + 1
                    numTracker = numTracker + 1;
            self.hamming_var = counter;
        return self.hamming_var

    #Calculates manhattan of board
    def manhattan(self):
        if self.manhattanCounter == 0:
            sum = 0
            for row in range(self.dimensions):
                for column in range(self.dimensions):
                    if self.board[row][column] != 0:
                        sum = sum + abs(row - self.__getX(self.board[row][column])) + abs(column - self.__getY(self.board[row][column]))
            self.manhattan = sum
        return self.manhattan

    #Checks if board is at its goal state, which is numerical ascending order
    def isGoal(self):
        if self.hamming() == 0:
            return True
        return False

    #Given another board, checks if the two boards are the same
    def equals(self, y):
        if y == self:
            return True
        if y == None:
            return False
        if y.__class__ != self.__class__:
            return False

        thatBoard = y.__getBoard()

        if self.dimensions == y.dimensions:
            for i in range(self.dimensions):
                for j in range(self.dimensions):
                    if self.board[i][j] != thatBoard[i][j]:
                        return False
            return True
        return False

    #Returns the neighbors of the board
    def neighbors(self):
        list = []
        x0 = 0
        y0 = 0
        tempX0 = 0
        tempY0 = 0

        for i in range(self.dimensions):
            for j in range(self.dimensions):
                if self.board[i][j] == 0:
                    tempX0 = i
                    tempY0 = j
                    break
        x0 = tempX0
        y0 = tempY0

        if x0 - 1 >= 0:
            copyBoard = Board(self.board)
            doubleBoard = copyBoard.__getBoard()
            temp = doubleBoard[x0][y0]
            doubleBoard[x0][y0] = doubleBoard[x0 - 1][y0]
            doubleBoard[x0 - 1][y0] = temp
            list.append(copyBoard)

        if x0 + 1 <= self.dimensions - 1:
            copyBoard = Board(self.board)
            doubleBoard = copyBoard.__getBoard()
            temp = doubleBoard[x0][y0]
            doubleBoard[x0][y0] = doubleBoard[x0 + 1][y0]
            doubleBoard[x0 + 1][y0] = temp
            list.append(copyBoard)

        if y0 - 1 >= 0:
            copyBoard = Board(self.board)
            doubleBoard = copyBoard.__getBoard()
            temp = doubleBoard[x0][y0]
            doubleBoard[x0][y0] = doubleBoard[x0][y0 - 1]
            doubleBoard[x0][y0 - 1] = temp
            list.append(copyBoard)

        if y0 + 1 <= self.dimensions - 1:
            copyBoard = Board(self.board)
            doubleBoard = copyBoard.__getBoard()
            temp = doubleBoard[x0][y0]
            doubleBoard[x0][y0] = doubleBoard[x0][y0 + 1]
            doubleBoard[x0][y0 + 1] = temp
            list.append(copyBoard)

        return list

    #Swaps values in board array at board[0][0] and noard[1][1]
    def twin(self):
        temp = Board(self.board)
        copyBoard = temp.__getBoard()
        x0 = 0
        y0 = 0
        x1 = 1
        y1 = 1

        if copyBoard[x0][y0] == 0:
            x0 = 0
            y0 = 1

        if copyBoard[x1][y1] == 0:
            x1 = 1
            y1 = 0

        t = copyBoard[x0][y0]
        copyBoard[x0][y0] = copyBoard[x1][y1]
        copyBoard[x1][y1] = t

        return temp

#Main method
def main():
    tiles = [[1,2,3],[4,5,6],[7,0,8]]
    tiles2 = [[1,2,3],[4,5,6],[7,8,0]]

    board = Board(tiles)
    board2 = Board(tiles2)
    print(str(board.equals(board2)))
    print(str(board2.isGoal()))
    for i in board2.neighbors():
        print(i)
        print(str(i.equals(board)))

#Calls main method
if __name__ == "__main__":
    main()




