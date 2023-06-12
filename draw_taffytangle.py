"""
Draw module of Taffy Tangle
by Kean Arguelles
"""

from lib.stddraw import *
from lib.picture import *
from pygame import mixer
import random
import timer_taffytangle

mixer.init()  # used for audio, stdaudio freezes the program when a music is playing
width = 900
height = 670
gap = 20
size_of_tile = 70  # 70x70
board_width = 490
board_height = 630

setCanvasSize(width, height)
setXscale(0, width)
setYscale(0, height)
setFontFamily('Courier')

# tiles: array for the gem number inside each tiles, gem number is used as an index for gems[]
# I made it start with values of 7 because using 0 would make the program think the board is filled with gem #0 which
# causes it to not generate any gem #0. So a 7 means a blank tile in the code
# there are 10 rows, but only the first 9 is shown. 10th row is used to fill empty lines
tiles = [[7 for i in range(10)] for j in range(7)]
x_pos_tiles = []  # position of columns
y_pos_tiles = []  # position of rows
score = 0
goal = 3000

timer = timer_taffytangle.Timer()
seconds = 0
minutes = 0
gm = 0  # equals to the param passed to draw_goal_or_timer. but need to make it a local var so goal/timer box
# don't disappear during animation

# GEMS: 0 = circle, 1 = diamond, 2 = hexagon, 3 = pentagon, 4 = square, 5 = triangle
gems = [Picture('circle.png'), Picture('diamond.png'), Picture('hexagon.png'), Picture('pentagon.png'),
        Picture('square.png'), Picture('triangle.png')]
# Background pictures
backgrounds = [Picture('background.png'), Picture('boardbg.png'), Picture('main menu.png'), Picture('game over.png')]
# All pictures were made by me EXCEPT the astronaut which I traced from a picture I found on google. Sadly I lost the
# link of the original picture


def main_menu():
    """
    The main menu, render the background and 3 buttons
    """
    game_modes = ['> Target: 3,000 pts ', '> Timed: 2 minutes   ', '> Endless            ']  # ignore long spaces ty
    picture(backgrounds[2], width / 2, height / 2)

    setFontSize(19)
    button_x = 100
    button_y = 250

    for i in range(3):
        setPenColor(BLACK)
        filledRectangle(button_x, button_y, 250, 60)
        setPenColor(LIGHT_GRAY)
        setPenRadius(0.008)
        rectangle(button_x, button_y, 250, 60)
        setPenColor(GREEN)
        text(button_x + 130, button_y + 30, game_modes[i])
        button_y -= 100


def game_over():
    """
    Game over screen, shows the final results
    """
    picture(backgrounds[3], width/2, height/2)
    x = 205
    for i in range(2):
        setPenColor(BLACK)
        filledRectangle(x, 100, 200, 100)
        setPenColor(GRAY)
        setPenRadius(0.008)
        rectangle(x, 100, 200, 100)
        setFontSize(22)
        x += 300

    setPenColor(GREEN)
    setFontSize(22)
    text(305, 175, 'TOTAL SCORE')
    if gm != 2:
        text(605, 175, 'Time elapsed')
    else:
        text(605, 150, 'Out of time!')
    text(width / 2, 30, 'Click anywhere to go back to main menu')

    setFontSize(38)
    text(305, 140, str(score))
    if gm != 2:
        text(580, 140, str(minutes))
        text(605, 140, ':')
        text(640, 140, str(seconds))


def new_game():
    """
    Resets all the variable for a new game
    """
    global score, tiles, goal, gm, seconds, minutes

    timer.start_timer()
    goal = 3000
    seconds = 0
    minutes = 0
    gm = 0
    score = 0
    tiles = [[7 for i in range(10)] for j in range(7)]
    generate_gems()


def is_not_over(game_mode):   # for some reason, score doesnt update in the main module, so i need this function
    """
    Tells the program when to stop the code
    :param game_mode: current game mode
    :return: bool, False if game is over
    """
    not_over = True
    if game_mode == 1:
        not_over = score < goal
    elif game_mode == 2:
        not_over = minutes != 2
    return not_over


def generate_gems():
    """
    Generate gems at the start of the game, makes sure that there wont be lines of 3+
    Also stores the x and y positions of each tile in the board
    """
    y_already_stored = False

    for i in range(7):
        x = gap + (490 * i / 7)
        x_pos_tiles.append(x)  # store x positions so we can place gem pictures there later
        for j in range(9):
            y = gap + (630 * j / 9)  # store y positions
            if not y_already_stored:
                y_pos_tiles.append(y)

            no_line = False
            # check if placing the gem would create a line of 3+
            while not no_line:
                gem_number = random.randrange(0, len(gems))

                if check_horizontally(i, j, gem_number, True) >= 3 or check_vertically(i, j, gem_number, True) >= 3:
                    no_line = False
                else:
                    no_line = True

            tiles[i][j] = gem_number
        y_already_stored = True  # so it only saves the y positions once


def draw_gems():
    """
    draws the gem pictures on the board
    :return:
    """
    # Background image
    picture(backgrounds[0], width/2, height/2)
    # Board
    setPenRadius(0.0085)
    picture(backgrounds[1], gap + (board_width/2) + 1, gap + (board_height/2))
    setPenColor(WHITE)
    rectangle(gap, gap, board_width, board_height)
    setPenColor(BLACK)

    for column in range(7):
        x = gap + (size_of_tile / 2) + (board_width * column / 7)
        for row in range(9):
            y = gap + (size_of_tile / 2) + (board_height * row / 9)
            if tiles[column][row] != 7:
                picture(gems[tiles[column][row]], x, y)


def draw_highlight(x, y):
    """
    Draws a red square on the selected gem
    :param x: column
    :param y: row
    """
    middle = size_of_tile/2

    setPenColor(RED)
    setPenRadius(0.004)
    square(x_pos_tiles[x] + middle, y_pos_tiles[y] + middle, (size_of_tile/2)-4)


def get_tile_index(mouse_x, mouse_y):
    """
    Gets the row # and column # of the mouse click
    :param mouse_x: mouse x position
    :param mouse_y: mouse y position
    :return: column and row
    """
    for column in range(7):
        if column == 6:
            x = column
        elif x_pos_tiles[column] <= mouse_x < x_pos_tiles[column+1]:
            x = column
            break

    for row in range(9):
        if row == 8:
            y = row
        elif y_pos_tiles[row] <= mouse_y < y_pos_tiles[row+1]:
            y = row
            break

    return x, y


def switch_gems(x_list, y_list):
    """
    Switches the gems
    :param x_list: column of selections
    :param y_list: row of selections
    """
    gem_1 = tiles[x_list[0]][y_list[0]]
    gem_2 = tiles[x_list[1]][y_list[1]]

    tiles[x_list[0]][y_list[0]] = gem_2
    tiles[x_list[1]][y_list[1]] = gem_1

    if x_list[0] == x_list[1] and y_list[0] == y_list[1]:
        mixer.music.load('cancel.wav')  # deselect selection
        mixer.music.play()

    else:
        # if all changes to true, means there's no line and use this to switch back the gems
        no_matches = [False, False, False, False]
        if check_vertically(x_list[1], y_list[1], gem_1, True) < 3:
            no_matches[0] = True

        if check_horizontally(x_list[1], y_list[1], gem_1, True) < 3:
            no_matches[1] = True

        if check_vertically(x_list[0], y_list[0], gem_2, True) < 3:
            no_matches[2] = True

        if check_horizontally(x_list[0], y_list[0], gem_2, True) < 3:
            no_matches[3] = True

        draw_gems()
        draw_score_box()
        draw_goal_or_timer(gm)
        mixer.music.load('switch 1.wav')
        mixer.music.play()
        show(600)

        if False not in no_matches:  # revert if no lines
            tiles[x_list[0]][y_list[0]] = gem_1
            tiles[x_list[1]][y_list[1]] = gem_2
            mixer.music.load('switch 2.wav')  # deselect selection
            mixer.music.play()


def is_valid(x_list, y_list):
    """
    Checks if second selection is valid
    :param x_list: column of selections
    :param y_list: row of selections
    :return: bool = if move is valid or not
    """
    x1, y1, x2, y2 = x_list[0], y_list[0], x_list[1], y_list[1]

    if abs(x2-x1) == 1 or abs(y2-y1) == 1:
        if x2 == x1 or y2 == y1:
            return True
    elif x2 == x1 and y2 == y1:  # deselect
        return True
    else:
        return False


def check_for_lines():
    """
    Checks EACH gems for lines, if line is found increase score
    """
    global score

    for column in range(7):
        for row in range(9):
            current_gem = tiles[column][row]

            if current_gem != 7:  # if not a blank, check gem
                vertical_matches = check_vertically(column, row, current_gem, False)
                if vertical_matches >= 3:
                    score += vertical_matches * 100
                    mixer.music.load('pew.wav')
                    mixer.music.play()

                horizontal_matches = check_horizontally(column, row, current_gem, False)
                if horizontal_matches >= 3:
                    score += horizontal_matches * 100
                    mixer.music.load('pew.wav')
                    mixer.music.play()


def check_vertically(column, row, gem, is_pre_check):
    """
    Check for lines (vertically)
    :param column: column of gem
    :param row: row of gem
    :param gem: gem being checked
    :param is_pre_check: True when we only need to check for lines, False to check for lines AND remove the lines
    :return the length of the line
    """
    line_length = 1
    n = 1
    matched_rows = [row]
    while row+n <= 8:  # check up
        if tiles[column][row+n] == gem:
            line_length += 1
            matched_rows.append(row + n)
        else:
            break
        n += 1

    n = 1
    while row-n >= 0:  # check down
        if tiles[column][row-n] == gem:
            line_length += 1
            matched_rows.append(row - n)
        else:
            break
        n += 1

    if line_length >= 3 and not is_pre_check:  # clear lines if its not a pre check
        for i in range(len(matched_rows)):
            tiles[column][matched_rows[i]] = 7

    return line_length


def check_horizontally(column, row, gem, is_pre_check):
    """
    Check for lines (horizontally)
    works the same way as check_vertically
    """
    line_length = 1
    n = 1
    matched_columns = [column]
    while column+n <= 6:
        if tiles[column+n][row] == gem:
            line_length += 1
            matched_columns.append(column + n)
        else:
            break
        n += 1

    n = 1
    while column-n >= 0:
        if tiles[column-n][row] == gem:
            line_length += 1
            matched_columns.append(column - n)
        else:
            break
        n += 1

    if line_length >= 3 and not is_pre_check:
        for i in range(len(matched_columns)):
            tiles[matched_columns[i]][row] = 7

    return line_length


def drop_down():
    """
    Drop down animation. Gems drop down when there is a blank space below them. updates every 10 ms
    """
    no_more_drops = False
    # runs until all the gems have dropped all the way down
    while not no_more_drops:
        for row in range(10):  # also drops the hidden row
            for column in range(7):
                if tiles[column][9] == 7:
                    tiles[column][9] = random.randrange(0, len(gems))
                if row != 0 and tiles[column][row] != 7 and tiles[column][row-1] == 7:
                    n = 1
                    no_more_drops = False
                    while row-n >= 0 and tiles[column][row-n] == 7:
                        tiles[column][row-n] = tiles[column][(row - n) + 1]
                        tiles[column][(row - n) + 1] = 7
                        n += 1
                        clear()
                        draw_gems()
                        draw_score_box()
                        draw_goal_or_timer(gm)
                        show(10)
                    continue
                else:
                    no_more_drops = True


# --------- unnecessarily long functions for more creativity points :^) ---------

def draw_goal_or_timer(game_mode):
    """
    Draws 2 boxes that shows the target goal or a timer (for timed or endless mode)
    hope you don't mind that my seconds aren't 2 digits when it's < 10
    :param game_mode: 1 = score, 2 = timed, 3 = zen
    """
    global gm, seconds, minutes
    gm = game_mode

    minutes = int(timer.time_elapsed() / 60)
    seconds = int(timer.time_elapsed() % 60)

    box_x_position = ((gap + board_width + width) / 2) - 120
    box_y_position = (height * 1.2/3) - 55

    setPenColor(BLACK)
    filledRectangle(box_x_position, box_y_position, 240, 110)
    setPenColor(GRAY)
    setPenRadius(0.008)
    rectangle(box_x_position, box_y_position, 240, 110)
    setFontSize(22)

    if game_mode == 1:  # score 3000 to win
        setPenColor(GREEN)
        setFontSize(22)
        text(box_x_position + 120, box_y_position + 85, 'GOAL')
        setFontSize(38)
        text(box_x_position + 120, box_y_position + 40, str(goal))
    elif game_mode == 2:  # timed
        time_left_min = 1 - minutes
        time_left_sec = 60 - seconds

        setPenColor(GREEN)
        setFontSize(22)
        text(box_x_position + 120, box_y_position + 85, 'Time left')
        setFontSize(38)
        text(box_x_position + 95, box_y_position + 40, str(time_left_min))
        text(box_x_position + 120, box_y_position + 40, ':')
        text(box_x_position + 155, box_y_position + 40, str(time_left_sec))
    elif game_mode == 3:
        setPenColor(RED)
        filledRectangle(700, 100, 100, 60)
        setPenColor(BLACK)
        setPenRadius(0.008)
        rectangle(700, 100, 100, 60)
        text(750, 130, 'Done?')
        setPenColor(GREEN)
        setFontSize(22)
        text(box_x_position + 120, box_y_position + 85, 'Time elapsed')
        setFontSize(38)
        text(box_x_position + 95, box_y_position + 40, str(minutes))
        text(box_x_position + 120, box_y_position + 40, ':')
        text(box_x_position + 155, box_y_position + 40, str(seconds))


def draw_score_box():
    """
    Draws a score box that shows the current score
    """
    box_x_position = ((gap + board_width + width) / 2) - 120
    box_y_position = (height * 1.8/3) - 55

    setPenColor(BLACK)
    filledRectangle(box_x_position, box_y_position, 240, 110)
    setPenColor(GRAY)
    setPenRadius(0.008)
    rectangle(box_x_position, box_y_position, 240, 110)
    setPenColor(GREEN)
    setFontSize(22)
    text(box_x_position + 120, box_y_position + 85, 'SCORE')
    setFontSize(38)
    text(box_x_position + 120, box_y_position + 40, str(score))

