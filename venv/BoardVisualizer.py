#BoardVisualizer that creates a slider puzzle game
import pygame
import time
import random
from Board import Board
from SearchNode import SearchNode
from Solver import Solver
import copy

#Colors
BLACK = (0, 0, 0)
RED = (255,0,0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
EMERALD_GREEN = (80, 220, 100)
DARK_EMERALD_GREEN = (8, 101, 34)
JADE = (0, 168, 107)
CARDINAL_RED = (196, 30, 58)
CRIMSON_RED = (153, 0, 0)

#Rows and columns
ROW = 3
COLUMN = 3

#Screen dimensions
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

#Images
trophy_img = pygame.image.load("trophy.png")
pause_img = pygame.image.load("pause.png")
smile_img = pygame.image.load("smile.png")
play_img = pygame.image.load("play.png")
eight_img = pygame.image.load("eight.png")

def main():
    #Global variable is the Screen
    global SCREEN

    #Variables to use in game
    TEST_PUZZLE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    NUM_MOVES = 0
    TEMP_NUM_MOVES = float('inf')
    TEMP_TIMER = float('inf')
    GAME_OVER = False
    NICE_TRY = False
    PAUSE = False

    #Create first puzzle
    board_list = shuffle_a_solvable_board(Board(TEST_PUZZLE)).board
    temp_board_list = copy.deepcopy(board_list)

    #Start pygame module
    pygame.init()

    #Create window
    pygame.display.set_icon(eight_img)
    pygame.display.set_caption("8 Puzzle Visualizer")
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))

    #Start clock
    START = time.time()

    #Game loop
    while True:
        #Loop whenever the player successfully finishes a puzzle
        while GAME_OVER == True:
            SCREEN.fill(WHITE)

            #Create rectangle centered on the screen
            win_txt_box_size = WINDOW_HEIGHT//2
            win_text_box_border = 10
            win_txt_box_x = int(WINDOW_WIDTH/2 - win_txt_box_size/2)
            win_txt_box_y = int(WINDOW_HEIGHT/2 - win_txt_box_size/2)
            win_text_box = pygame.Rect(win_txt_box_x, win_txt_box_y,
                               win_txt_box_size, win_txt_box_size)
            pygame.draw.rect(SCREEN, BLACK, win_text_box, win_text_box_border)

            #Display trophy image onto the screen within the win_txt rectangle
            trophy_img_size = trophy_img.get_rect().size[0]
            trophy_img_x = int(WINDOW_WIDTH / 2 - trophy_img_size / 2)
            trophy_img_y = int(WINDOW_HEIGHT / 2 - trophy_img_size / 2) - 65
            trophy_text_box = pygame.Rect(trophy_img_x, trophy_img_y,
                                          trophy_img_size, trophy_img_size)

            SCREEN.blit(trophy_img, (trophy_img_x, trophy_img_y))

            #Congratulates the player for finishing the puzzle
            congrats_msg_font_size = 17
            congrats_msg_box = write_centered_message("arial", congrats_msg_font_size, "Nice Job!", BLACK, int(trophy_img_x + trophy_img_size/2), int(trophy_img_y + trophy_img_size + congrats_msg_font_size))

            #Display the number of moves the player made to solve the puzzle
            num_moves_msg_font_size = 15
            offset = 5

            num_moves_word_choice = "moves"

            if NUM_MOVES == 1:
                num_moves_word_choice = "move"

            num_moves_box = write_centered_message("arial", num_moves_msg_font_size, "Total Moves Made: " + str(NUM_MOVES) + " " + num_moves_word_choice, BLACK, int(trophy_img_x + trophy_img_size/2), int(trophy_img_y + trophy_img_size + congrats_msg_font_size + num_moves_msg_font_size + offset))

            #Calculates the number of seconds that took the player to solve the puzzle
            seconds = round((END - START),2)

            #Changes the word choice based on the number of seconds
            seconds_word_choice = "seconds"
            if seconds == 1:
                seconds_word_choice = "second"

            #Displays the number of seconds that took the player to solve the puzzle
            timer_msg_font_size = 15
            timer_box = write_centered_message("arial", timer_msg_font_size, "Time Finished: " + str(seconds) + " " + seconds_word_choice, BLACK, int(trophy_img_x + trophy_img_size/2), int(trophy_img_y + trophy_img_size + congrats_msg_font_size + num_moves_msg_font_size + timer_msg_font_size + offset))

            record_offset = 8
            record_num_moves_msg_font_size = 15

            if NUM_MOVES < TEMP_NUM_MOVES:
                TEMP_NUM_MOVES = NUM_MOVES

            temp_word_choice = "moves"

            if TEMP_NUM_MOVES == 1:
                temp_word_choice = "move"

            #Displays the least moves made that a player took to solve the current puzzle
            #Resets whenever the player requests a new puzzle
            record_num_moves_box = write_centered_message("arial", num_moves_msg_font_size, "Least Moves Made: " + str(TEMP_NUM_MOVES) + " " + temp_word_choice, RED, int(trophy_img_x + trophy_img_size/2), timer_box[1] + timer_box[3] + record_offset)

            if seconds < TEMP_TIMER:
                TEMP_TIMER = seconds

            record_word_choice = "seconds"

            if TEMP_TIMER == 1:
                record_word_choice = "second"

            record_timer_msg_font_size = 15

            #Displays the fastest attempt that a player took to solve the current puzzle
            #Resets whenever the player requests a new puzzle
            record_timer_box = write_centered_message("arial", record_timer_msg_font_size, "Best Time Finished: " + str(TEMP_TIMER) + " " + record_word_choice, RED, int(trophy_img_x + trophy_img_size/2), record_num_moves_box[1] + record_num_moves_box[3] + offset)

            #Creates the button to play the same puzzle
            reset_rect_offset = 5
            reset_rect_width = record_timer_box[2]//2 + 2
            reset_rect_height = (win_txt_box_size - trophy_img_size - congrats_msg_box[3] - num_moves_box[3] - timer_box[3] - record_num_moves_box[3] - record_timer_box[3])//2
            reset_rect_border = 1
            reset_rect_x = record_timer_box[0] - 2
            reset_rect_y = record_timer_box[1] + record_timer_box[3] + reset_rect_offset
            reset_rect = pygame.Rect(reset_rect_x, reset_rect_y,
                                          reset_rect_width, reset_rect_height)
            pygame.draw.rect(SCREEN, DARK_EMERALD_GREEN, reset_rect, reset_rect_border)
            SCREEN.fill(DARK_EMERALD_GREEN, reset_rect)
            draw_border_rect(BLACK, reset_rect[0], reset_rect[1], reset_rect[2], reset_rect[3], 3)

            #Creates button to play a new puzzle
            diff_rect_offset = 5
            diff_rect_width = record_timer_box[2]//2 + 2
            diff_rect_height = (win_txt_box_size - trophy_img_size - congrats_msg_box[3] - num_moves_box[3] - timer_box[3] - record_num_moves_box[3] - record_timer_box[3])//2
            diff_rect_border = 1
            diff_rect_x = record_timer_box[0] + record_timer_box[2]//2 + diff_rect_offset + 2
            diff_rect_y = record_timer_box[1] + record_timer_box[3] + diff_rect_offset
            diff_rect = pygame.Rect(diff_rect_x, diff_rect_y,
                                          diff_rect_width, diff_rect_height)
            pygame.draw.rect(SCREEN, DARK_EMERALD_GREEN, diff_rect, diff_rect_border)
            SCREEN.fill(DARK_EMERALD_GREEN, diff_rect)
            draw_border_rect(BLACK, diff_rect[0], diff_rect[1], diff_rect[2], diff_rect[3], 3)

            #Returns (x,y) coordinates of the player's mouse
            mouse = pygame.mouse.get_pos()

            #If the mouse is on the either button then the button will change to a lighter shade of green
            if reset_rect[0] <= mouse[0] <= reset_rect[0] + reset_rect[2] and reset_rect[1] <= mouse[1] <= reset_rect[1] + reset_rect[3]:
                SCREEN.fill(EMERALD_GREEN, reset_rect)
                draw_border_rect(BLACK, reset_rect[0], reset_rect[1], reset_rect[2], reset_rect[3], 3)
            elif diff_rect[0] <= mouse[0] <= diff_rect[0] + diff_rect[2] and diff_rect[1] <= mouse[1] <= diff_rect[1] + diff_rect[3]:
                SCREEN.fill(EMERALD_GREEN, diff_rect)
                draw_border_rect(BLACK, diff_rect[0], diff_rect[1], diff_rect[2], diff_rect[3], 3)

            #Display the text on the button to replay the same puzzle
            reset_text_size = 10
            write_centered_message("arial", reset_text_size, "Replay current puzzle", BLACK, reset_rect[0] + reset_rect[2]//2 + 1, reset_rect[1] + reset_rect[3]//2)

            #Display the text on the button to play a new puzzle
            diff_text_size = 10
            write_centered_message("arial", diff_text_size, "Play new puzzle", BLACK, diff_rect[0] + diff_rect[2]//2 + 2, diff_rect[1] + diff_rect[3]//2)

            #Update the screen
            pygame.display.update()

            #Event handling
            for event in pygame.event.get():
                #If the "X" on the right hand corner is clicked, the window closes and the program stops running
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #If the player clicks the button for the same puzzle
                    if reset_rect[0] <= mouse[0] <= reset_rect[0] + reset_rect[2] and reset_rect[1] <= mouse[1] <= \
                            reset_rect[1] + reset_rect[3]:
                        #Set the array to the previous puzzle and reset variables
                        board_list = copy.deepcopy(temp_board_list)
                        GAME_OVER = False
                        NUM_MOVES = 0
                        START = time.time()
                    #If the player clicks the button for a new puzzle
                    elif diff_rect[0] <= mouse[0] <= diff_rect[0] + diff_rect[2] and diff_rect[1] <= mouse[1] <= \
                            diff_rect[1] + diff_rect[3]:
                        #Processes event handlers internally
                        pygame.event.pump()
                        #Reset variables
                        TEMP_NUM_MOVES = float('inf')
                        TEMP_TIMER = float('inf')
                        #Create new puzzle
                        board_list = shuffle_a_new_solvable_board(Board(board_list), Board(temp_board_list)).board
                        #Copy new puzzle in case player desires to play the same puzzle in the future
                        temp_board_list = copy.deepcopy(board_list)
                        #Reset variables
                        GAME_OVER = False
                        NUM_MOVES = 0
                        START = time.time()

        #Loop whenever the player decides to use the solver
        while NICE_TRY == True:
            SCREEN.fill(WHITE)
            #Displays a rectange that is centered on the screen
            nice_try_box_size = WINDOW_HEIGHT // 2
            nice_try_box_border = 10
            nice_try_box_offset = 10
            nice_try_box_x = int(WINDOW_WIDTH / 2 - nice_try_box_size / 2)
            nice_try_box_y = int(WINDOW_HEIGHT / 2 - nice_try_box_size / 2)
            nice_try_box = pygame.Rect(nice_try_box_x, nice_try_box_y,
                                       nice_try_box_size, nice_try_box_size - nice_try_box_offset)
            pygame.draw.rect(SCREEN, BLACK, nice_try_box, nice_try_box_border)

            #Displays a smile face image in the rectangle centered on the screen
            smile_img_size = smile_img.get_rect().size[0]
            smile_img_x = int(WINDOW_WIDTH / 2 - smile_img_size / 2)
            smile_img_y = int(WINDOW_HEIGHT / 2 - smile_img_size / 2) - 55
            smile_text_box = pygame.Rect(smile_img_x, smile_img_y,
                                          smile_img_size, smile_img_size)

            SCREEN.blit(smile_img, (smile_img_x, smile_img_y))

            #Displays an encouraging message to the player
            nice_try_msg_font_size = 22
            nice_try_offset = smile_img_size//4 + 3
            nice_try_msg_box = write_centered_message("arial", nice_try_msg_font_size, "Good Try!", BLACK, nice_try_box_x + nice_try_box_size//2, nice_try_box_y + nice_try_box_size//2 + nice_try_offset)

            #Dispplays an encouraging message to the player
            encourage_msg_font_size = 22
            encourage_offset = 10
            encourage_box = write_centered_message("arial", encourage_msg_font_size, "You can do it!", BLACK, nice_try_box_x + nice_try_box_size//2, nice_try_msg_box[1] + nice_try_msg_box[3] + encourage_offset)

            #Displays the button to reset the previous puzzle
            reset_rect_offset = 15
            reset_rect_width = int(encourage_box[2]/1.1)
            reset_rect_height = (nice_try_box_size - smile_img_size - nice_try_msg_box[3] - encourage_box[3])//2
            reset_rect_border = 1
            reset_rect_x = encourage_box[0] + encourage_box[2]//2 + 5 - reset_rect_width - 10
            reset_rect_y = encourage_box[1] + encourage_box[3] + 10
            reset_rect = pygame.Rect(reset_rect_x, reset_rect_y,
                                          reset_rect_width, reset_rect_height)
            pygame.draw.rect(SCREEN, DARK_EMERALD_GREEN, reset_rect, reset_rect_border)
            SCREEN.fill(DARK_EMERALD_GREEN, reset_rect)
            draw_border_rect(BLACK, reset_rect[0], reset_rect[1], reset_rect[2], reset_rect[3], 3)

            #Displays the button to play a new puzzle
            diff_rect_offset = 20
            diff_rect_width = int(encourage_box[2]/1.1)
            diff_rect_height = (nice_try_box_size - smile_img_size - nice_try_msg_box[3] - encourage_box[3])//2
            diff_rect_border = 1
            diff_rect_x = encourage_box[0] + encourage_box[2]//2 + 5
            diff_rect_y = encourage_box[1] + encourage_box[3] + 10
            diff_rect = pygame.Rect(diff_rect_x, diff_rect_y,
                                          diff_rect_width, diff_rect_height)
            pygame.draw.rect(SCREEN, DARK_EMERALD_GREEN, diff_rect, diff_rect_border)
            SCREEN.fill(DARK_EMERALD_GREEN, diff_rect)
            draw_border_rect(BLACK, diff_rect[0], diff_rect[1], diff_rect[2], diff_rect[3], 3)

            #Gets (x,y) coordinates of the mouse
            mouse = pygame.mouse.get_pos()

            #If the mouse is on either button then the button has a lighter shade of green
            if reset_rect[0] <= mouse[0] <= reset_rect[0] + reset_rect[2] and reset_rect[1] <= mouse[1] <= reset_rect[1] + reset_rect[3]:
                SCREEN.fill(EMERALD_GREEN, reset_rect)
                draw_border_rect(BLACK, reset_rect[0], reset_rect[1], reset_rect[2], reset_rect[3], 3)
            elif diff_rect[0] <= mouse[0] <= diff_rect[0] + diff_rect[2] and diff_rect[1] <= mouse[1] <= diff_rect[1] + diff_rect[3]:
                SCREEN.fill(EMERALD_GREEN, diff_rect)
                draw_border_rect(BLACK, diff_rect[0], diff_rect[1], diff_rect[2], diff_rect[3], 3)

            #Displays the text that states to replay the same puzzle
            reset_text_size = 10
            write_centered_message("arial", reset_text_size, "Replay current puzzle", BLACK, reset_rect[0] + reset_rect[2]//2, reset_rect[1] + reset_rect[3]//2)

            #Displays the text that states to play a new puzzle
            diff_text_size = 10
            write_centered_message("arial", diff_text_size, "Play new puzzle", BLACK, diff_rect[0] + diff_rect[2]//2 , diff_rect[1] + diff_rect[3]//2)

           #Update the screen
            pygame.display.update()

            #Event handling
            for event in pygame.event.get():
                #If the player clicks the "X" on the right hand corner of the window, the window closes
                #and the program stops running
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #If the player clicks on the reset button
                    if reset_rect[0] <= mouse[0] <= reset_rect[0] + reset_rect[2] and reset_rect[1] <= mouse[1] <= \
                            reset_rect[1] + reset_rect[3]:
                        #Restore puzzle to the previous puzzle
                        board_list = copy.deepcopy(temp_board_list)
                        #Reset variables
                        NICE_TRY = False
                        NUM_MOVES = 0
                        START = time.time()
                    #If the player clicks on the button to play a new puzzle
                    elif diff_rect[0] <= mouse[0] <= diff_rect[0] + diff_rect[2] and diff_rect[1] <= mouse[1] <= \
                            diff_rect[1] + diff_rect[3]:
                        #Process event handlers internally
                        pygame.event.pump()
                        #Reset variables
                        TEMP_NUM_MOVES = float('inf')
                        TEMP_TIMER = float('inf')
                        #Create new puzzle
                        board_list = shuffle_a_new_solvable_board(Board(board_list), Board(temp_board_list)).board
                        #Copy new puzzle in case player desires to play the same puzzle in the future
                        temp_board_list = copy.deepcopy(board_list)
                        #Reset variables
                        NICE_TRY = False
                        NUM_MOVES = 0
                        START = time.time()

        #Loop whenever the player decides to pause the game
        while PAUSE == True:
            SCREEN.fill(WHITE)

            #Displays a play image on the right hand corner of the screen
            play_offset = 1
            play_img_size = play_img.get_rect().size[0]
            play_img_x = WINDOW_WIDTH - play_img_size - play_offset
            play_img_y = 0
            play_text_box = pygame.Rect(play_img_x, play_img_y,
                                        play_img_size, play_img_size)

            SCREEN.blit(play_img, (play_img_x, play_img_y))

            #Displays a rectangle that is centered on the screen
            pause_txt_box_size = int(WINDOW_HEIGHT / 2.3)
            pause_text_box_border = 10
            pause_txt_box_x = WINDOW_WIDTH // 2 - pause_txt_box_size // 2
            pause_txt_box_y = WINDOW_HEIGHT // 2 - pause_txt_box_size // 2
            pause_text_box = pygame.Rect(pause_txt_box_x, pause_txt_box_y,
                                       pause_txt_box_size + 25, pause_txt_box_size - 20)
            pygame.draw.rect(SCREEN, BLACK, pause_text_box, pause_text_box_border)

            #Displays the text "Game Paused" onto the screen
            game_paused_msg_font_size = 60
            game_paused_offset = 20
            game_msg_box = write_centered_message("arial", game_paused_msg_font_size, "Game", BLACK, pause_txt_box_x + pause_txt_box_size//2, pause_txt_box_y + game_paused_msg_font_size - game_paused_offset//2)
            paused_msg_box = write_centered_message("arial", game_paused_msg_font_size, "Paused", BLACK, pause_txt_box_x + pause_txt_box_size//2, game_msg_box[1] + game_msg_box[3] + game_paused_offset)

            #Displays the current moves made solving the puzzle onto the screen while paused
            num_moves_msg_font_size = 18
            num_moves_offset = 32
            num_moves_word_choice = "moves"
            if NUM_MOVES == 1:
                num_moves_word_choice = "move"
            num_moves_box = write_centered_message("arial", num_moves_msg_font_size,
                                                   "Current Moves Made: " + str(NUM_MOVES) + " " + num_moves_word_choice, BLACK,
                                                   pause_txt_box_x + (pause_txt_box_size + 25)//2,
                    paused_msg_box[1] + paused_msg_box[3] + num_moves_offset//2)

            timer_msg_font_size = 18
            timer_box_offset = 10
            seconds = round((time_paused - START),2)

            seconds_word_choice = "seconds"
            if seconds == 1:
                seconds_word_choice = "second"

            #Displays the current seconds solving the puzzle onto the screen while paused
            timer_box = write_centered_message("arial", timer_msg_font_size,
                                               "Current Time: " + str(seconds) + " " + seconds_word_choice, BLACK,
                                               pause_txt_box_x + (pause_txt_box_size + 25)//2, num_moves_box[1] + num_moves_box[3] + timer_box_offset)

            #Displays button used to restart the current puzzle
            reset_rect_offset = 15
            button_offset = 17
            reset_rect_width = timer_box[2] // 2 + reset_rect_offset
            reset_rect_height = (pause_txt_box_size - game_msg_box[3] - paused_msg_box[3] - num_moves_box[3] -
                                 timer_box[3]) // 2
            reset_rect_border = 1
            reset_rect_x = timer_box[0] - reset_rect_offset + 3
            reset_rect_y = timer_box[1] + timer_box[3] + button_offset
            reset_rect = pygame.Rect(reset_rect_x, reset_rect_y,
                                     reset_rect_width, reset_rect_height)
            pygame.draw.rect(SCREEN, DARK_EMERALD_GREEN, reset_rect, reset_rect_border)
            SCREEN.fill(DARK_EMERALD_GREEN, reset_rect)
            draw_border_rect(BLACK, reset_rect[0], reset_rect[1], reset_rect[2], reset_rect[3], 3)

            #Displays button used to play a new puzzle
            diff_rect_offset = 15
            diff_rect_width = timer_box[2] // 2
            diff_rect_height = (pause_txt_box_size - game_msg_box[3] - paused_msg_box[3] - num_moves_box[3] -
                                 timer_box[3]) // 2
            diff_rect_border = 1
            diff_rect_x = timer_box[0] + timer_box[2] // 2 + diff_rect_offset - 2
            diff_rect_y = timer_box[1] + timer_box[3] + button_offset
            diff_rect = pygame.Rect(diff_rect_x, diff_rect_y,
                                    diff_rect_width, diff_rect_height)
            pygame.draw.rect(SCREEN, DARK_EMERALD_GREEN, diff_rect, diff_rect_border)
            SCREEN.fill(DARK_EMERALD_GREEN, diff_rect)
            draw_border_rect(BLACK, diff_rect[0], diff_rect[1], diff_rect[2], diff_rect[3], 3)

            #Returns (x,y) coordinates of the player's mouse
            mouse = pygame.mouse.get_pos()

            #If the mouse is on the either button then the button will change to a lighter shade of green
            if reset_rect[0] <= mouse[0] <= reset_rect[0] + reset_rect[2] and reset_rect[1] <= mouse[1] <= reset_rect[
                1] + reset_rect[3]:
                SCREEN.fill(EMERALD_GREEN, reset_rect)
                draw_border_rect(BLACK, reset_rect[0], reset_rect[1], reset_rect[2], reset_rect[3], 3)
            elif diff_rect[0] <= mouse[0] <= diff_rect[0] + diff_rect[2] and diff_rect[1] <= mouse[1] <= diff_rect[1] + \
                    diff_rect[3]:
                SCREEN.fill(EMERALD_GREEN, diff_rect)
                draw_border_rect(BLACK, diff_rect[0], diff_rect[1], diff_rect[2], diff_rect[3], 3)

            #Displays text that states to the player if they would like to replay the current puzzle
            reset_text_size = 10
            write_centered_message("arial", reset_text_size, "Replay current puzzle", BLACK,
                                   reset_rect[0] + reset_rect[2] // 2, reset_rect[1] + reset_rect[3] // 2)

            #Displays text that states to the player if they would like to play a new puzzle
            diff_text_size = 10
            write_centered_message("arial", diff_text_size, "Play new puzzle", BLACK,
                                   diff_rect[0] + diff_rect[2] // 2, diff_rect[1] + diff_rect[3] // 2)

            #Update the screen
            pygame.display.update()

            #Event handling
            for event in pygame.event.get():
                #If the player clicks "X" on the right hand corner of window, the window will close
                #and program will stop running
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #If the player clicks the play button then the player can play puzzle
                    if play_img_x <= mouse[0] <= play_img_x + play_img_size and play_img_y <= mouse[1] <= play_img_y + play_img_size:
                        PAUSE = False
                        time_unpaused = time.time()
                        duration = time_unpaused - time_paused
                        START = START + duration
                    #If the player clicks the reset button, the puzzle resets to its beginning state
                    elif reset_rect[0] <= mouse[0] <= reset_rect[0] + reset_rect[2] and reset_rect[1] <= mouse[1] <= \
                            reset_rect[1] + reset_rect[3]:
                        board_list = copy.deepcopy(temp_board_list)
                        PAUSE = False
                        NUM_MOVES = 0
                        START = time.time()
                    #If the player clicks the diff button, the player will play a new puzzle
                    elif diff_rect[0] <= mouse[0] <= diff_rect[0] + diff_rect[2] and diff_rect[1] <= mouse[1] <= \
                            diff_rect[1] + diff_rect[3]:
                        pygame.event.pump()
                        TEMP_NUM_MOVES = float('inf')
                        TEMP_TIMER = float('inf')
                        board_list = shuffle_a_new_solvable_board(Board(board_list), Board(temp_board_list)).board
                        temp_board_list = copy.deepcopy(board_list)
                        PAUSE = False
                        NUM_MOVES = 0
                        START = time.time()

        SCREEN.fill(WHITE)

        #Displays the number of moves the players has made
        score(NUM_MOVES)

        #Calculate the number of seconds that have passed as the player attempts to solve puzzle
        end_time = time.time()

        #Display the number of seconds of solving the puzzle
        stopwatch(round(end_time - START, 2))
        #time.sleep(0.01)

        #Draw the 3 by 3 puzzle grid
        draw_grid(ROW, COLUMN, board_list)

        #Display the pause image on the right hand corner of window
        pause_offset = 1
        pause_img_size = pause_img.get_rect().size[0]
        pause_img_x = WINDOW_WIDTH - pause_img_size - pause_offset
        pause_img_y = 0
        pause_text_box = pygame.Rect(pause_img_x, pause_img_y,
                                      pause_img_size, pause_img_size)

        SCREEN.blit(pause_img, (pause_img_x, pause_img_y))

        #Display solver button on the bottom left hand corner of the screen
        solver_rect_width = 150
        solver_rect_height = 50
        solver_rect_offset = 0
        solver_rect_x = 2
        solver_rect_y = WINDOW_HEIGHT - solver_rect_height - 4
        solver_rect = pygame.Rect(solver_rect_x, solver_rect_y,
                                solver_rect_width, solver_rect_height)
        pygame.draw.rect(SCREEN, BLACK, solver_rect)
        SCREEN.fill(CRIMSON_RED, solver_rect)
        draw_border_rect(BLACK, solver_rect[0], solver_rect[1], solver_rect[2], solver_rect[3], 3)

        #Get (x,y) coordinate of the mouse
        mouse_sol = pygame.mouse.get_pos()

        #If the mouse is on the solver button then change the button's color to a lighter shade of red
        if solver_rect[0] <= mouse_sol[0] <= solver_rect[0] + solver_rect[2] and solver_rect[1] <= mouse_sol[1] <= solver_rect[1] + \
                solver_rect[3]:
            SCREEN.fill(CARDINAL_RED, solver_rect)
            draw_border_rect(BLACK, solver_rect[0], solver_rect[1], solver_rect[2], solver_rect[3], 3)

        #Display text on the solver button that asks the player if they want to use the solver button
        #if they are struggling
        solver_text_size = 10
        write_centered_message("arial", solver_text_size, "Struggling?", BLACK,
                               solver_rect[0] + solver_rect[2] // 2, solver_rect[1] + solver_rect[3] // 2 - 5)
        write_centered_message("arial", solver_text_size, "Click for solution", BLACK,
                               solver_rect[0] + solver_rect[2] // 2, solver_rect[1] + solver_rect[3] // 2 + 5)

        #If the numbers on the board are in ascending numerical order then start the game over loop
        if Board(board_list).isGoal() == True:
            GAME_OVER = True
            END = time.time()

        #Event handling
        for event in pygame.event.get():
            #If the player clicks the "X" of the right hand corner of the window, then the window will close
            #and the program will stop running
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Get (x,y) coordinate of mouse
                position = pygame.mouse.get_pos();
                row = (position[1] - 200) // 100
                column = (position[0] - 200) // 100
                #If mouse is on any number of grid and number is next to the slide, then swap places
                #and update move counter
                if row in range(ROW) and column in range(COLUMN):
                    checker, new_row, new_column = is_adjacent_to_zero(board_list,row,column)
                    if board_list[row][column] != 0 and checker == True:
                        board_list[row][column], board_list[new_row][new_column] = board_list[new_row][new_column], board_list[row][column]
                        NUM_MOVES = NUM_MOVES + 1
                #If user clicks the solver button
                elif solver_rect[0] <= position[0] <= solver_rect[0] + solver_rect[2] and solver_rect[1] <= position[1] <= solver_rect[1] + \
                solver_rect[3]:
                    #Make instance of solver class to solve puzzle
                    sol = Solver(Board(board_list))

                    #Creates game clock
                    clock = pygame.time.Clock()

                    #Reduces fps
                    frames_per_second = 3

                    #Loops through the steps of the current puzzle to the goal state
                    for i in sol.solution():
                        #Process internal event handlers
                        pygame.event.pump()
                        #Displays the movements of the puzzle to goal state in 3 frames per second
                        board_list = i.board
                        SCREEN.fill(WHITE)
                        draw_solution(ROW, COLUMN, board_list)
                        clock.tick(frames_per_second)
                        pygame.display.flip()
                    #Starts nice try loop
                    NICE_TRY = True
                    END = time.time()
                #If user clicks pause button then pause game
                elif pause_img_x <= position[0] <= pause_img_x + pause_img_size and pause_img_y <= position[1] <= pause_img_y + pause_img_size:
                    PAUSE = True
                    time_paused = time.time()

        #Update screen
        pygame.display.update()

   #Unintialize all aspects of pygame module
    pygame.quit()

#Draw borders of rectangle using lines
def draw_border_rect(color, x_coor, y_coor, width, height, thickness):
    pygame.draw.line(SCREEN, color, (x_coor, y_coor), (x_coor + width, y_coor), thickness)
    pygame.draw.line(SCREEN, BLACK, (x_coor + width, y_coor), (x_coor + width, y_coor + height), thickness)
    pygame.draw.line(SCREEN, BLACK, (x_coor, y_coor), (x_coor, y_coor + height), thickness)
    pygame.draw.line(SCREEN, BLACK, (x_coor, y_coor + height), (x_coor + width, y_coor + height), thickness)

#Display puzzle onto the screen and change background color of numbers adjacent to the slider to emerald green
def draw_grid(row, column, puzzle):
    block_size = 100
    rect_thickness = 7
    offset = 200
    for x in range(row):
        for y in range(column):
            rect_X_coordinate = (x * block_size) + offset
            rect_Y_coordinate = (y * block_size) + offset
            rect = pygame.Rect(rect_X_coordinate, rect_Y_coordinate,
                               block_size, block_size)
            pygame.draw.rect(SCREEN, BLACK, rect, rect_thickness)
            SCREEN.fill(GRAY, rect)

            mouse = pygame.mouse.get_pos()
            is_adjacent, adjacent_row, adjacent_column = is_adjacent_to_zero(puzzle, y, x)

            if is_adjacent == True and rect[0] <= mouse[0] <= rect[0] + rect[2] and rect[1] <= mouse[1] <= rect[
                1] + rect[3]:
                SCREEN.fill(JADE, rect)

            if (puzzle[y][x] != 0):
                font = pygame.font.Font('freesansbold.ttf', block_size)
                text = font.render(str(puzzle[y][x]), True, BLACK)
                text_rect = text.get_rect()
                text_rect.center = (rect_X_coordinate + block_size//2, rect_Y_coordinate + block_size//2)
                SCREEN.blit(text, text_rect)

#Displays the various grids shown during the solver process
def draw_solution(row, column, puzzle):
    block_size = 100
    rect_thickness = 7
    offset = 200
    for x in range(row):
        for y in range(column):
            rect_X_coordinate = (x * block_size) + offset
            rect_Y_coordinate = (y * block_size) + offset
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

#Shuffles the board using the Fisher–Yates shuffle Algorithm for a solvable/unsolvable state
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

#Shuffles a board into a solvable puzzle that is not the goal state
def shuffle_a_solvable_board(board):
    temp_board = shuffle_board(board)
    solvable_board = Solver(temp_board)
    while solvable_board.isSolvable() == False and temp_board.isGoal() == False:
        temp_board = shuffle_board(temp_board)
        solvable_board = Solver(temp_board)
    return temp_board

#Shuffles a board into a solvable puzzle that is not the goal state and not the "old_board"
def shuffle_a_new_solvable_board(board, old_board):
    temp_board = shuffle_board(board)
    solvable_board = Solver(temp_board)
    while solvable_board.isSolvable() == False and temp_board.isGoal() == False and temp_board.equals(old_board) == False:
        temp_board = shuffle_board(temp_board)
        solvable_board = Solver(temp_board)
    return temp_board

#Determines if the following number on the 2d array is adjacent to the slider and returns
#if the number is next the slider as well as the row, column coordinates of the slider in the 2d array
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

#Displays the number of moves made the player has made onto the screen
def score(score):
    score_font = pygame.font.SysFont("arial", 25)
    score_font.set_bold(True)
    word_choice = "moves"
    if score == 1:
        word_choice = "move"
    text = score_font.render("Moves Made: " + str(score) + " " + word_choice, True, BLACK)
    SCREEN.blit(text, [0,0])

#Displays the time, in seconds, that has passed as the player solves the puzzle onto the screen
def stopwatch(time):
    text_size = 25
    score_font = pygame.font.SysFont("arial", 25)
    score_font.set_bold(True)
    text = score_font.render("Time: " + str(time), True, BLACK)
    SCREEN.blit(text, [0, text_size])

#Displays text that is centered onto the screen
def write_centered_message(font_type, font_size, message, color, x_coor, y_coor):
    font = pygame.font.SysFont(font_type, font_size)
    font.set_bold(True)
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x_coor, y_coor)
    SCREEN.blit(text, text_rect)
    return text_rect

#Calls the main method
if __name__ == "__main__":
    main()