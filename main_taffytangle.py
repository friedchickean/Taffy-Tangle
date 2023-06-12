"""
Taffy Tangle
by Kean Arguelles
WINNING CONDITIONS: The game has 3 modes, get n number of points, timed (2 mins), or endless
"""

from draw_taffytangle import *

game_mode = 0


def is_inside_board(mouse_x, mouse_y):
    """
    Checks if the mouse click is inside the board
    :param mouse_x: x pos
    :param mouse_y: y pos
    :return: bool, True if inside, False if outside
    """
    inside = [False, False]
    if gap < mouse_x < board_width + gap:
        inside[0] = True
    if gap < mouse_y < board_height + gap:
        inside[1] = True

    if False in inside:
        return False
    else:
        return True


def which_game_mode(mouse_x, mouse_y):
    """
    listens to users mouse click in the main menu screen
    :param mouse_x: mouse x pos
    :param mouse_y: mouse y pos
    :return: the chosen game mode
    """
    selection = 0
    if 100 <= mouse_x <= 350:
        if 250 <= mouse_y <= 310:  # button y + 60
            selection = 1
        elif 150 <= mouse_y <= 210:
            selection = 2
        elif 50 <= mouse_y <= 110:
            selection = 3

    return selection


def done_relaxing(mouse_x, mouse_y):
    """
    checks if the quit button in endless game mode has been pressed
    :return true if user clicks the button
    """
    not_done = True
    if 700 <= mouse_x <= 800:
        if 100 <= mouse_y <= 160:
            not_done = False
    return not_done


def play_game(mode):
    """
    Plays the game. The game has 3 different game modes:
    1 - Score 3,000 to win
    2 - get as much as you can within 2 mins
    3 - endless, until you hit the done button
    :param mode: chosen game mode
    """
    # x and y pos of mouse mouse clicks
    new_game()
    x, y = [0, 0], [0, 0]
    highlight = False
    clicks = 0

    condition = True

    while condition:  # main game screen, runs til condition is met. condition varies from game modes
        condition = is_not_over(mode)

        clear()
        draw_gems()
        draw_score_box()
        draw_goal_or_timer(mode)

        if highlight:
            draw_highlight(x[0], y[0])

        if mousePressed():
            if is_inside_board(mouseX(), mouseY()):
                clicks += 1
                if clicks == 1:
                    x[0], y[0] = get_tile_index(mouseX(), mouseY())
                    highlight = True
                    mixer.music.load('bleep.wav')  # pygame.mixer is imported in draw_taffytangle.py
                    mixer.music.play()
                elif clicks == 2:
                    x[1], y[1] = get_tile_index(mouseX(), mouseY())
                    if is_valid(x, y):
                        highlight = False
                        switch_gems(x, y)
                        clicks = 0
                    else:
                        clicks -= 1
                        mixer.music.load('invalid.wav')
                        mixer.music.play()
            elif mode == 3:
                condition = done_relaxing(mouseX(), mouseY())

        check_for_lines()
        drop_down()
        show(0)


# program shows until user terminates the window
while True:
    # MAIN MENU
    while game_mode == 0:
        clear()
        main_menu()
        if mousePressed():
            game_mode = which_game_mode(mouseX(), mouseY())
        show(0)

    # GAME SCREEN
    play_game(game_mode)

    # GAME-OVER SCREEN
    while not mousePressed():
        clear()
        game_over()
        show(0)

    game_mode = 0  # reset game mode when user goes back to the main menu
