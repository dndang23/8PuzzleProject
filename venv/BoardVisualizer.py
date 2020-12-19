import pygame
import time
import random
from Board import Board
from SearchNode import SearchNode
from Solver import Solver

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
ROW = 3
COLUMN = 3
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
OFFSET = 200
TEST_PUZZLE = [[1,2,3],[4,5,6],[7,8,0]]

def main():
    global SCREEN
    board_list = shuffle_a_solvable_board(Board(TEST_PUZZLE)).board
    pygame.init()
    pygame.display.set_caption("8 Puzzle Visualizer")
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    SCREEN.fill(WHITE)
    while True:
        draw_grid2(ROW, COLUMN, board_list)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos();
                #print("Position = " + str(position))
                row = (position[1] - 200) // 100
                column = (position[0] - 200) // 100
                #print("Row = " + str(row))
                #print("Column = " + str(column))
                if row in range(ROW) and column in range(COLUMN):
                    #print("Grid Value: " + str(board_list[row][column]))
                    checker, new_row, new_column = is_adjacent_to_zero(board_list,row,column)
                    if board_list[row][column] != 0 and checker == True:
                        board_list[row][column], board_list[new_row][new_column] = board_list[new_row][new_column], board_list[row][column]



        pygame.display.update()


    pygame.quit()

def draw_grid(row, column):
    block_size = 100
    rect_thickness = 5
    for x in range(row):
        for y in range(column):
            rect = pygame.Rect((x * block_size) + OFFSET, (y * block_size) + OFFSET,
                               block_size, block_size)
            pygame.draw.rect(SCREEN, BLACK, rect, rect_thickness)
            SCREEN.fill(GRAY, rect)

def draw_grid2(row, column, puzzle):
    block_size = 100
    rect_thickness = 7
    for x in range(row):
        for y in range(column):
            rect_X_coordinate = (x * block_size) + OFFSET
            rect_Y_coordinate = (y * block_size) + OFFSET
            rect = pygame.Rect(rect_X_coordinate, rect_Y_coordinate,
                               block_size, block_size)
            pygame.draw.rect(SCREEN, BLACK, rect, rect_thickness)
            SCREEN.fill(GRAY, rect)
            if (puzzle[y][x] != 0):
                font = pygame.font.Font('freesansbold.ttf', block_size)
                text = font.render(str(puzzle[y][x]), True, BLACK)
                text_rect = text.get_rect()
                text_rect.center = (rect_X_coordinate + block_size//2, rect_Y_coordinate + block_size//2)
                SCREEN.blit(text, text_rect)

def shuffle_board(board):
    shuffle_list = []
    board_list = board.board
    shuffle_to_board_list = []

    for x in range(ROW):
        for y in range(COLUMN):
            shuffle_list.append(board_list[x][y])

    n = len(shuffle_list) - 1
    
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i + 1)
        shuffle_list[i], shuffle_list[j] = shuffle_list[j], shuffle_list[i]

    shuffle_to_board_list = [shuffle_list[r * ROW:(r + 1) * COLUMN] for r in range(0, ROW)]
    new_board = Board(shuffle_to_board_list)
    return new_board

def shuffle_a_solvable_board(board):
    temp_board = shuffle_board(board)
    solvable_board = Solver(board)
    while solvable_board.isSolvable() == False:
        temp_board = shuffle_board(temp_board)
        solvable_board = Solver(temp_board)
    return temp_board

def is_adjacent_to_zero(board_list, row, column):
    if column + 1 < COLUMN and board_list[row][column + 1] == 0:
        return True, row, column + 1
    if column - 1 >= 0 and board_list[row][column - 1] == 0:
        return True, row , column - 1
    if row + 1 < ROW and board_list[row + 1][column] == 0:
        return True, row + 1, column
    if row - 1 >= 0 and board_list[row - 1][column] == 0:
        return True, row - 1, column
    return False, -1, -1

def animate_swap():
    return 0


if __name__ == "__main__":
    main()