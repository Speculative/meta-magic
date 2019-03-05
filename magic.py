import curses
import curses.panel
import time
from math import floor, ceil
import display

MOVES = {
    "h": (0, -1),
    "j": (1, 0),
    "k": (-1, 0),
    "l": (0, 1),
    "y": (-1, -1),
    "u": (-1, 1),
    "n": (1, -1),
    "m": (1, 1),
}


def move_player(key, game_state):
    level = game_state["level"]

    curr_row, curr_col = game_state["player_pos"]
    move_row, move_col = MOVES[key]
    next_row = curr_row + move_row
    next_col = curr_col + move_col

    if (
        0 <= next_row < len(level)
        and 0 <= next_col < len(level[0])
        and not level[next_row][next_col]
    ):
        game_state["player_pos"] = (next_row, next_col)


def handle_key(key, game_state):
    if key in MOVES:
        move_player(key, game_state)
    elif key == "q":
        game_state["quit"] = True


def make_room(rows, cols):
    level = [[False for col in range(cols)] for row in range(rows)]
    level[0] = [True for col in range(cols)]
    level[rows - 1] = [True for col in range(cols)]
    for row in range(1, rows - 1):
        level[row][0] = True
        level[row][cols - 1] = True
    return level


def main(stdscr):
    display.init_display(stdscr)

    level = make_room(20, 80)
    game_state = {"level": level, "player_pos": (1, 1), "quit": False}

    next_key = None
    while True:
        handle_key(next_key, game_state)
        if game_state["quit"]:
            break

        display.begin_render()

        level_off, window_off = display.show_level(
            stdscr, game_state["level"], game_state["player_pos"]
        )
        display.show_player(stdscr, level_off, window_off, game_state["player_pos"])

        next_key = stdscr.getkey()


curses.wrapper(main)
