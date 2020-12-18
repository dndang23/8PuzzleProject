import pygame
import time
import random
from Board import Board

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
ROW = 3
COLUMN = 3
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
OFFSET = 200
TEST_PUZZLE = [[1,2,3],[4,5,6],[7,8,0]]

def main():
    global SCREEN
    temp = Board(TEST_PUZZLE)
    temp = shuffle_board(temp)
    pygame.init()
    pygame.display.set_caption("8 Puzzle Visualizer")
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    SCREEN.fill(WHITE)
    while True:
        draw_grid2(ROW, COLUMN, temp)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

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

def draw_grid2(row, column, board):
    puzzle = board.board;
    block_size = 100
    rect_thickness = 5
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

if __name__ == "__main__":
    main()