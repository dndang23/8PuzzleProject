import pygame
import time
import random
from Board import Board
from SearchNode import SearchNode
from Solver import Solver
import copy
import time

"""
--------------Stuff I Still Need to Finish--------------
1. Intro
2. Solver mechanic (Done)
3. Pause Sprite (Done)
4. Move Counter (Done)
5. Timer (Display Timer)
6. Game Over Screen (Done)
7. Pause Mechanic
8. Other puzzle modes (maybe)
"""

BLACK = (0, 0, 0)
RED = (255,0,0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
EMERALD_GREEN = (80, 220, 100)
DARK_EMERALD_GREEN = (8, 101, 34)
CARDINAL_RED = (196, 30, 58)
CRIMSON_RED = (153, 0, 0)
ROW = 3
COLUMN = 3
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
OFFSET = 200
TEST_PUZZLE = [[1,2,3],[4,5,6],[7,8,0]]
trophy_img = pygame.image.load("trophy2.png")
pause_img = pygame.image.load("pause2.png")
smile_img = pygame.image.load("smile2.png")
play_img = pygame.image.load("play.png")

def main():
    global SCREEN, time_paused
    NUM_MOVES = 0
    TEMP_NUM_MOVES = float('inf')
    TEMP_TIMER = float('inf')
    GAME_OVER = False
    NICE_TRY = False
    PAUSE = False
    board_list = shuffle_a_solvable_board(Board(TEST_PUZZLE)).board
    temp_board_list = copy.deepcopy(board_list)
    pygame.init()
    pygame.display.set_caption("8 Puzzle Visualizer")
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    START = time.time()

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

            congrats_msg_font_size = 17
            congrats_msg_box = write_centered_message('freesansbold.ttf', congrats_msg_font_size, "Nice Job!", BLACK, int(trophy_img_center_x + trophy_img_size/2), int(trophy_img_center_y + trophy_img_size + congrats_msg_font_size))

            num_moves_msg_font_size = 15
            offset = 5
            num_moves_box = write_centered_message('freesansbold.ttf', num_moves_msg_font_size, "Total Moves Made: " + str(NUM_MOVES), BLACK, int(trophy_img_center_x + trophy_img_size/2), int(trophy_img_center_y + trophy_img_size + congrats_msg_font_size + num_moves_msg_font_size + offset))

            seconds = int(END - START)

            timer_msg_font_size = 15
            timer_box = write_centered_message('freesansbold.ttf', timer_msg_font_size, "Time Finished: " + str(seconds) + " seconds", BLACK, int(trophy_img_center_x + trophy_img_size/2), int(trophy_img_center_y + trophy_img_size + congrats_msg_font_size + num_moves_msg_font_size + + timer_msg_font_size + offset))

            record_offset = 8
            record_num_moves_msg_font_size = 15

            if NUM_MOVES < TEMP_NUM_MOVES:
                TEMP_NUM_MOVES = NUM_MOVES

            record_num_moves_box = write_centered_message('freesansbold.ttf', num_moves_msg_font_size, "Least Moves Made: " + str(TEMP_NUM_MOVES), RED, int(trophy_img_center_x + trophy_img_size/2), timer_box[1] + timer_box[3] + record_offset)

            if seconds < TEMP_TIMER:
                TEMP_TIMER = seconds

            record_timer_msg_font_size = 15
            record_timer_box = write_centered_message('freesansbold.ttf', record_timer_msg_font_size, "Best Time Finished: " + str(TEMP_TIMER) + " seconds", RED, int(trophy_img_center_x + trophy_img_size/2), record_num_moves_box[1] + record_num_moves_box[3] + offset)

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_rect[0] <= mouse[0] <= reset_rect[0] + reset_rect[2] and reset_rect[1] <= mouse[1] <= \
                            reset_rect[1] + reset_rect[3]:
                        board_list = copy.deepcopy(temp_board_list)
                        GAME_OVER = False
                        NUM_MOVES = 0
                        START = time.time()
                    elif diff_rect[0] <= mouse[0] <= diff_rect[0] + diff_rect[2] and diff_rect[1] <= mouse[1] <= \
                            diff_rect[1] + diff_rect[3]:
                        TEMP_NUM_MOVES = float('inf')
                        TEMP_TIMER = float('inf')
                        board_list = shuffle_a_solvable_board(Board(board_list)).board
                        temp_board_list = copy.deepcopy(board_list)
                        GAME_OVER = False
                        NUM_MOVES = 0
                        START = time.time()

        while NICE_TRY == True:
            SCREEN.fill(WHITE)
            nice_try_box_size = WINDOW_HEIGHT // 2
            nice_try_box_border = 10
            nice_try_box_offset = 10
            nice_try_box_center_x = int(WINDOW_WIDTH / 2 - nice_try_box_size / 2)
            nice_try_box_center_y = int(WINDOW_HEIGHT / 2 - nice_try_box_size / 2)
            nice_try_box = pygame.Rect(nice_try_box_center_x, nice_try_box_center_y,
                                       nice_try_box_size, nice_try_box_size - nice_try_box_offset)
            pygame.draw.rect(SCREEN, BLACK, nice_try_box, nice_try_box_border)

            smile_img_size = smile_img.get_rect().size[0]
            smile_img_center_x = int(WINDOW_WIDTH / 2 - smile_img_size / 2)
            smile_img_center_y = int(WINDOW_HEIGHT / 2 - smile_img_size / 2) - 55
            smile_text_box = pygame.Rect(smile_img_center_x, smile_img_center_y,
                                          smile_img_size, smile_img_size)

            SCREEN.blit(smile_img, (smile_img_center_x, smile_img_center_y))

            nice_try_msg_font_size = 22
            nice_try_offset = smile_img_size//4 + 3
            nice_try_msg_box = write_centered_message('freesansbold.ttf', nice_try_msg_font_size, "Good Try!", BLACK, nice_try_box_center_x + nice_try_box_size//2, nice_try_box_center_y + nice_try_box_size//2 + nice_try_offset)

            encourage_msg_font_size = 22
            encourage_offset = 10
            encourage_box = write_centered_message('freesansbold.ttf', encourage_msg_font_size, "You can do it!", BLACK, nice_try_box_center_x + nice_try_box_size//2, nice_try_msg_box[1] + nice_try_msg_box[3] + encourage_offset)

            reset_rect_offset = 15
            reset_rect_width = encourage_box[2]//2 + reset_rect_offset
            reset_rect_height = (nice_try_box_size - smile_img_size - nice_try_msg_box[3] - encourage_box[3])//2
            reset_rect_border = 1
            reset_rect_center_x = encourage_box[0] + encourage_box[2]//2 + 5 - reset_rect_width - 10
            reset_rect_center_y = encourage_box[1] + encourage_box[3] + 10
            reset_rect = pygame.Rect(reset_rect_center_x, reset_rect_center_y,
                                          reset_rect_width, reset_rect_height)
            pygame.draw.rect(SCREEN, DARK_EMERALD_GREEN, reset_rect, reset_rect_border)
            SCREEN.fill(DARK_EMERALD_GREEN, reset_rect)

            diff_rect_offset = 20
            diff_rect_width = encourage_box[2]//2 + diff_rect_offset
            diff_rect_height = (nice_try_box_size - smile_img_size - nice_try_msg_box[3] - encourage_box[3])//2
            diff_rect_border = 1
            diff_rect_center_x = encourage_box[0] + encourage_box[2]//2 + 5
            diff_rect_center_y = encourage_box[1] + encourage_box[3] + 10
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
            write_centered_message('freesansbold.ttf', reset_text_size, "Repeat puzzle", BLACK, reset_rect[0] + reset_rect[2]//2, reset_rect[1] + reset_rect[3]//2)

            diff_text_size = 10
            write_centered_message('freesansbold.ttf', diff_text_size, "Play new puzzle", BLACK, diff_rect[0] + diff_rect[2]//2 , diff_rect[1] + diff_rect[3]//2)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_rect[0] <= mouse[0] <= reset_rect[0] + reset_rect[2] and reset_rect[1] <= mouse[1] <= \
                            reset_rect[1] + reset_rect[3]:
                        board_list = copy.deepcopy(temp_board_list)
                        NICE_TRY = False
                        NUM_MOVES = 0
                        START = time.time()
                    elif diff_rect[0] <= mouse[0] <= diff_rect[0] + diff_rect[2] and diff_rect[1] <= mouse[1] <= \
                            diff_rect[1] + diff_rect[3]:
                        TEMP_NUM_MOVES = float('inf')
                        TEMP_TIMER = float('inf')
                        board_list = shuffle_a_solvable_board(Board(board_list)).board
                        temp_board_list = copy.deepcopy(board_list)
                        NICE_TRY = False
                        NUM_MOVES = 0
                        START = time.time()

        while PAUSE == True:
            SCREEN.fill(WHITE)

            play_offset = 1
            play_img_size = play_img.get_rect().size[0]
            play_img_x = WINDOW_WIDTH - play_img_size - play_offset
            play_img_y = 0
            play_text_box = pygame.Rect(play_img_x, play_img_y,
                                        play_img_size, play_img_size)

            SCREEN.blit(play_img, (play_img_x, play_img_y))

            pause_txt_box_size = int(WINDOW_HEIGHT / 2.8)
            pause_text_box_border = 10
            pause_txt_box_x = WINDOW_WIDTH // 2 - pause_txt_box_size // 2
            pause_txt_box_y = WINDOW_HEIGHT // 2 - pause_txt_box_size // 2
            pause_text_box = pygame.Rect(pause_txt_box_x, pause_txt_box_y,
                                       pause_txt_box_size, pause_txt_box_size)
            pygame.draw.rect(SCREEN, BLACK, pause_text_box, pause_text_box_border)

            game_paused_msg_font_size = 60
            game_paused_offset = 20
            game_msg_box = write_centered_message('freesansbold.ttf', game_paused_msg_font_size, "Game", BLACK, pause_txt_box_x + pause_txt_box_size//2, pause_txt_box_y + game_paused_msg_font_size - game_paused_offset//2)
            paused_msg_box = write_centered_message('freesansbold.ttf', game_paused_msg_font_size, "Paused", BLACK, pause_txt_box_x + pause_txt_box_size//2, game_msg_box[1] + game_msg_box[3] + game_paused_offset)

            num_moves_msg_font_size = 18
            num_moves_offset = 30
            num_moves_box = write_centered_message('freesansbold.ttf', num_moves_msg_font_size,
                                                   "Current Moves Made: " + str(NUM_MOVES), BLACK,
                                                   pause_txt_box_x + pause_txt_box_size//2,
                    paused_msg_box[1] + paused_msg_box[3] + num_moves_offset//2)

            timer_msg_font_size = 18
            timer_box_offset = 10
            seconds = int(time_paused - START)
            word_choice = "seconds"
            if seconds == 1:
                word_choice = "second"
            timer_box = write_centered_message('freesansbold.ttf', timer_msg_font_size,
                                               "Current Time: " + str(seconds) + " " + word_choice, BLACK,
                                               pause_txt_box_x + pause_txt_box_size//2, num_moves_box[1] + num_moves_box[3] + timer_box_offset)

            reset_rect_offset = 5
            button_offset = 15
            reset_rect_width = timer_box[2] // 2
            reset_rect_height = (pause_txt_box_size - game_msg_box[3] - paused_msg_box[3] - num_moves_box[3] -
                                 timer_box[3]) // 2
            reset_rect_border = 1
            reset_rect_x = timer_box[0]
            reset_rect_y = timer_box[1] + timer_box[3] + button_offset
            reset_rect = pygame.Rect(reset_rect_x, reset_rect_y,
                                     reset_rect_width, reset_rect_height)
            pygame.draw.rect(SCREEN, DARK_EMERALD_GREEN, reset_rect, reset_rect_border)
            SCREEN.fill(DARK_EMERALD_GREEN, reset_rect)

            diff_rect_offset = 5
            diff_rect_width = timer_box[2] // 2
            diff_rect_height = (pause_txt_box_size - game_msg_box[3] - paused_msg_box[3] - num_moves_box[3] -
                                 timer_box[3]) // 2
            diff_rect_border = 1
            diff_rect_x = timer_box[0] + timer_box[2] // 2 + diff_rect_offset
            diff_rect_y = timer_box[1] + timer_box[3] + button_offset
            diff_rect = pygame.Rect(diff_rect_x, diff_rect_y,
                                    diff_rect_width, diff_rect_height)
            pygame.draw.rect(SCREEN, DARK_EMERALD_GREEN, diff_rect, diff_rect_border)
            SCREEN.fill(DARK_EMERALD_GREEN, diff_rect)


            mouse = pygame.mouse.get_pos()

            if reset_rect[0] <= mouse[0] <= reset_rect[0] + reset_rect[2] and reset_rect[1] <= mouse[1] <= reset_rect[
                1] + reset_rect[3]:
                SCREEN.fill(EMERALD_GREEN, reset_rect)
            elif diff_rect[0] <= mouse[0] <= diff_rect[0] + diff_rect[2] and diff_rect[1] <= mouse[1] <= diff_rect[1] + \
                    diff_rect[3]:
                SCREEN.fill(EMERALD_GREEN, diff_rect)

            reset_text_size = 10
            write_centered_message('freesansbold.ttf', reset_text_size, "Replay same puzzle", BLACK,
                                   reset_rect[0] + reset_rect[2] // 2, reset_rect[1] + reset_rect[3] // 2)

            diff_text_size = 10
            write_centered_message('freesansbold.ttf', diff_text_size, "Play new puzzle", BLACK,
                                   diff_rect[0] + diff_rect[2] // 2, diff_rect[1] + diff_rect[3] // 2)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_img_x <= mouse[0] <= play_img_x + play_img_size and play_img_y <= mouse[1] <= play_img_y + play_img_size:
                        PAUSE = False
                        time_unpaused = time.time()
                        duration = time_unpaused - time_paused
                        START = START + duration
                    elif reset_rect[0] <= mouse[0] <= reset_rect[0] + reset_rect[2] and reset_rect[1] <= mouse[1] <= \
                            reset_rect[1] + reset_rect[3]:
                        board_list = copy.deepcopy(temp_board_list)
                        PAUSE = False
                        NUM_MOVES = 0
                        START = time.time()
                    elif diff_rect[0] <= mouse[0] <= diff_rect[0] + diff_rect[2] and diff_rect[1] <= mouse[1] <= \
                            diff_rect[1] + diff_rect[3]:
                        TEMP_NUM_MOVES = float('inf')
                        TEMP_TIMER = float('inf')
                        board_list = shuffle_a_solvable_board(Board(board_list)).board
                        temp_board_list = copy.deepcopy(board_list)
                        PAUSE = False
                        NUM_MOVES = 0
                        START = time.time()

        SCREEN.fill(WHITE)
        score(NUM_MOVES)

        end_time = time.time()
        stopwatch(int(end_time - START))
        time.sleep(0.01)

        draw_grid2(ROW, COLUMN, board_list)

        pause_offset = 1
        pause_img_size = pause_img.get_rect().size[0]
        pause_img_center_x = WINDOW_WIDTH - pause_img_size - pause_offset
        pause_img_center_y = 0
        pause_text_box = pygame.Rect(pause_img_center_x, pause_img_center_y,
                                      pause_img_size, pause_img_size)

        SCREEN.blit(pause_img, (pause_img_center_x, pause_img_center_y))

        solver_rect_width = 150
        solver_rect_height = 50
        solver_rect_offset = 0
        solver_rect_x = 2
        solver_rect_y = WINDOW_HEIGHT - solver_rect_height - 4
        solver_rect = pygame.Rect(solver_rect_x, solver_rect_y,
                                solver_rect_width, solver_rect_height)
        pygame.draw.rect(SCREEN, BLACK, solver_rect)
        SCREEN.fill(CRIMSON_RED, solver_rect)
        draw_border_rect(BLACK, solver_rect[0], solver_rect[1], solver_rect[2], solver_rect[3], 4)

        mouse_sol = pygame.mouse.get_pos()

        if solver_rect[0] <= mouse_sol[0] <= solver_rect[0] + solver_rect[2] and solver_rect[1] <= mouse_sol[1] <= solver_rect[1] + \
                solver_rect[3]:
            SCREEN.fill(CARDINAL_RED, solver_rect)
            draw_border_rect(BLACK, solver_rect[0], solver_rect[1], solver_rect[2], solver_rect[3], 4)

        solver_text_size = 10
        write_centered_message('freesansbold.ttf', solver_text_size, "Struggling?", BLACK,
                               solver_rect[0] + solver_rect[2] // 2, solver_rect[1] + solver_rect[3] // 2 - 5)
        write_centered_message('freesansbold.ttf', solver_text_size, "Click for solution", BLACK,
                               solver_rect[0] + solver_rect[2] // 2, solver_rect[1] + solver_rect[3] // 2 + 5)

        if Board(board_list).isGoal() == True:
            #print(board_list)
            GAME_OVER = True
            END = time.time()

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
                        #print("Number of moves made: " + str(NUM_MOVES))
                elif solver_rect[0] <= position[0] <= solver_rect[0] + solver_rect[2] and solver_rect[1] <= position[1] <= solver_rect[1] + \
                solver_rect[3]:
                    sol = Solver(Board(board_list))
                    clock = pygame.time.Clock()
                    frames_per_second = 3
                    for i in sol.solution():
                        board_list = i.board
                        SCREEN.fill(WHITE)
                        draw_grid2(ROW, COLUMN, board_list)
                        pygame.display.update()
                        clock.tick(frames_per_second)
                    NICE_TRY = True
                    END = time.time()
                elif pause_img_center_x <= position[0] <= pause_img_center_x + pause_img_size and pause_img_center_y <= position[1] <= pause_img_center_y + pause_img_size:
                    PAUSE = True
                    time_paused = time.time()

        pygame.display.update()

    pygame.quit()

def draw_border_rect(color, x_coor, y_coor, width, height, thickness):
    pygame.draw.line(SCREEN, color, (x_coor, y_coor), (x_coor + width, y_coor), thickness)
    pygame.draw.line(SCREEN, BLACK, (x_coor + width, y_coor), (x_coor + width, y_coor + height), thickness)
    pygame.draw.line(SCREEN, BLACK, (x_coor, y_coor), (x_coor, y_coor + height), thickness)
    pygame.draw.line(SCREEN, BLACK, (x_coor, y_coor + height), (x_coor + width, y_coor + height), thickness)

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

def stopwatch(time):
    text_size = 25
    font = pygame.font.Font('freesansbold.ttf', text_size)
    text = font.render("Time: " + str(time), True, BLACK)
    SCREEN.blit(text, [0, text_size])

def write_centered_message(font_type, font_size, message, color, x_coor, y_coor):
    font = pygame.font.Font(font_type, font_size)
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x_coor, y_coor)
    SCREEN.blit(text, text_rect)
    return text_rect

if __name__ == "__main__":
    main()