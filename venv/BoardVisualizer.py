import pygame
import time
import random
from Board import Board
from SearchNode import SearchNode
from Solver import Solver
from PIL import Image, ImageFilter

"""
--------------Stuff I Still Need to Finish--------------
1. Intro
2. Solver mechanic
3. Pause Sprite
4. Move Counter (Done)
5. Game Over Screen
"""

BLACK = (0, 0, 0)
RED = (255,0,0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
EMERALD_GREEN = (80, 220, 100)
DARK_EMERALD_GREEN = (8, 101, 34)
ROW = 3
COLUMN = 3
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
OFFSET = 200
TEST_PUZZLE = [[1,2,3],[4,5,6],[7,8,0]]
trophy_img = pygame.image.load("trophy2.png")

def main():
    global SCREEN, GAME_OVER, NUM_MOVES
    NUM_MOVES = 0
    TEMP_NUM_MOVES = float('inf')
    GAME_OVER = False
    #board_list = shuffle_a_solvable_board(Board(TEST_PUZZLE)).board
    board_list = TEST_PUZZLE
    temp_board_list = board_list.copy()
    print(board_list)
    pygame.init()
    pygame.display.set_caption("8 Puzzle Visualizer")
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    SCREEN.fill(WHITE)
    # draw_grid2(ROW, COLUMN, board_list)

    while True:
        while GAME_OVER == True:
            SCREEN.fill(WHITE)
            win_txt_box_size = WINDOW_HEIGHT//2
            win_text_box_border = 10
            win_txt_box_center_x = int(WINDOW_WIDTH/2 - win_txt_box_size/2)
            win_txt_box_center_y = int(WINDOW_HEIGHT/2 - win_txt_box_size/2)
            win_text_box = pygame.Rect(win_txt_box_center_x, win_txt_box_center_y,
                               win_txt_box_size, win_txt_box_size)
            pygame.draw.rect(SCREEN, BLACK, win_text_box, win_text_box_border)

            trophy_img_size = trophy_img.get_rect().size[0]
            trophy_img_center_x = int(WINDOW_WIDTH / 2 - trophy_img_size / 2)
            trophy_img_center_y = int(WINDOW_HEIGHT / 2 - trophy_img_size / 2) - 65
            trophy_text_box = pygame.Rect(trophy_img_center_x, trophy_img_center_y,
                                          trophy_img_size, trophy_img_size)

            SCREEN.blit(trophy_img, (trophy_img_center_x, trophy_img_center_y))
            '''
            trophy_txt_box_size = trophy_img_size + 20
            trophy_text_box_border = 1
            trophy_txt_box_center_x = int(WINDOW_WIDTH/2 - trophy_txt_box_size/2)
            trophy_txt_box_center_y = int(WINDOW_HEIGHT/2 - trophy_txt_box_size/2) - 45
            trophy_text_box = pygame.Rect(trophy_txt_box_center_x, trophy_txt_box_center_y,
                                       trophy_txt_box_size, trophy_txt_box_size + 10)
            pygame.draw.rect(SCREEN, RED, trophy_text_box, trophy_text_box_border)
            '''

            congrats_msg_font_size = 17
            congrats_msg_box = write_centered_message('freesansbold.ttf', congrats_msg_font_size, "Nice Job!", BLACK, int(trophy_img_center_x + trophy_img_size/2), int(trophy_img_center_y + trophy_img_size + congrats_msg_font_size))

            num_moves_msg_font_size = 15
            offset = 5
            num_moves_box = write_centered_message('freesansbold.ttf', num_moves_msg_font_size, "Total Moves Made: " + str(NUM_MOVES), BLACK, int(trophy_img_center_x + trophy_img_size/2), int(trophy_img_center_y + trophy_img_size + congrats_msg_font_size + num_moves_msg_font_size + offset))

            timer_msg_font_size = 15
            timer_box = write_centered_message('freesansbold.ttf', timer_msg_font_size, "Time Finished: 60 seconds", BLACK, int(trophy_img_center_x + trophy_img_size/2), int(trophy_img_center_y + trophy_img_size + congrats_msg_font_size + num_moves_msg_font_size + + timer_msg_font_size + offset))


            record_offset = 8
            record_num_moves_msg_font_size = 15

            if NUM_MOVES < TEMP_NUM_MOVES:
                TEMP_NUM_MOVES = NUM_MOVES

            record_num_moves_box = write_centered_message('freesansbold.ttf', num_moves_msg_font_size, "Best Moves Made: " + str(TEMP_NUM_MOVES), RED, int(trophy_img_center_x + trophy_img_size/2), timer_box[1] + timer_box[3] + record_offset)

            record_timer_msg_font_size = 15
            record_timer_box = write_centered_message('freesansbold.ttf', record_timer_msg_font_size, "Best Time Finished: 60 seconds", RED, int(trophy_img_center_x + trophy_img_size/2), record_num_moves_box[1] + record_num_moves_box[3] + offset)


            reset_rect_offset = 5
            reset_rect_width = record_timer_box[2]//2
            reset_rect_height = (win_txt_box_size - trophy_img_size - congrats_msg_box[3] - num_moves_box[3] - timer_box[3] - record_num_moves_box[3] - record_timer_box[3])//2
            reset_rect_border = 1
            reset_rect_center_x = record_timer_box[0]
            reset_rect_center_y = record_timer_box[1] + record_timer_box[3] + reset_rect_offset
            reset_rect = pygame.Rect(reset_rect_center_x, reset_rect_center_y,
                                          reset_rect_width, reset_rect_height)
            pygame.draw.rect(SCREEN, DARK_EMERALD_GREEN, reset_rect, reset_rect_border)
            SCREEN.fill(DARK_EMERALD_GREEN, reset_rect)

            diff_rect_offset = 5
            diff_rect_width = record_timer_box[2]//2
            diff_rect_height = (win_txt_box_size - trophy_img_size - congrats_msg_box[3] - num_moves_box[3] - timer_box[3] - record_num_moves_box[3] - record_timer_box[3])//2
            diff_rect_border = 1
            diff_rect_center_x = record_timer_box[0] + record_timer_box[2]//2 + diff_rect_offset
            diff_rect_center_y = record_timer_box[1] + record_timer_box[3] + diff_rect_offset
            diff_rect = pygame.Rect(diff_rect_center_x, diff_rect_center_y,
                                          diff_rect_width, diff_rect_height)
            pygame.draw.rect(SCREEN, DARK_EMERALD_GREEN, diff_rect, diff_rect_border)
            SCREEN.fill(DARK_EMERALD_GREEN, diff_rect)

            mouse = pygame.mouse.get_pos()

            if reset_rect[0] <= mouse[0] <= reset_rect[0] + reset_rect[2] and reset_rect[1] <= mouse[1] <= reset_rect[1] + reset_rect[3]:
                SCREEN.fill(EMERALD_GREEN, reset_rect)
            elif diff_rect[0] <= mouse[0] <= diff_rect[0] + diff_rect[2] and diff_rect[1] <= mouse[1] <= diff_rect[1] + diff_rect[3]:
                SCREEN.fill(EMERALD_GREEN, diff_rect)

            reset_text_size = 10
            write_centered_message('freesansbold.ttf', reset_text_size, "Replay same puzzle", BLACK, reset_rect[0] + reset_rect[2]//2, reset_rect[1] + reset_rect[3]//2)

            diff_text_size = 10
            write_centered_message('freesansbold.ttf', diff_text_size, "Play new puzzle", BLACK, diff_rect[0] + diff_rect[2]//2 , diff_rect[1] + diff_rect[3]//2)



            pygame.display.update()

            print("The current board list is: " + str(temp_board_list))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_rect[0] <= mouse[0] <= reset_rect[0] + reset_rect[2] and reset_rect[1] <= mouse[1] <= \
                            reset_rect[1] + reset_rect[3]:
                        GAME_OVER = False
                        board_list = temp_board_list.copy()
                        print("temp board list is: " + str(temp_board_list))
                    elif diff_rect[0] <= mouse[0] <= diff_rect[0] + diff_rect[2] and diff_rect[1] <= mouse[1] <= \
                            diff_rect[1] + diff_rect[3]:
                        GAME_OVER = False
                        TEMP_NUM_MOVES = float('inf')
                        board_list = shuffle_a_solvable_board(Board(TEST_PUZZLE)).board
                        temp_board_list = board_list.copy()
                        print("temp board list2 is: " + str(temp_board_list))

                    NUM_MOVES = 0

        SCREEN.fill(WHITE)
        score(NUM_MOVES)
        draw_grid2(ROW, COLUMN, board_list)

        if Board(board_list).isGoal() == True:
            print(board_list)
            GAME_OVER = True

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
                        NUM_MOVES = NUM_MOVES + 1
                        print("Number of moves made: " + str(NUM_MOVES))

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
    solvable_board = Solver(temp_board)
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

def score(score):
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render("Moves Made: " + str(score), True, BLACK)
    SCREEN.blit(text, [0,0])

def write_centered_message(font_type, font_size, message, color, x_coor, y_coor):
    font = pygame.font.Font(font_type, font_size)
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x_coor, y_coor)
    SCREEN.blit(text, text_rect)
    return text_rect


def blurSurf(surface, amt):
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf




if __name__ == "__main__":
    main()