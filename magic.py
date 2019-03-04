import curses
import curses.panel
import time
from math import floor, ceil


debug_window = None


def show_debug(row, *args):
    debug_window.addstr(row + 1, 1, " ".join(map(lambda a: str(a), list(args))))
    debug_window.refresh()


def blank_window(window):
    window.clear()
    window.border()
    window.refresh()


def show_modal(width, height, parent_window):
    parent_height, parent_width = parent_window.getmaxyx()
    modal_window = curses.newwin(
        height,
        width,
        int((parent_height / 2) - height / 2),
        int((parent_width / 2) - width / 2),
    )
    modal_panel = curses.panel.new_panel(modal_window)
    modal_panel.top()
    curses.panel.update_panels()

    blank_window(modal_window)
    return modal_panel


def show_level(window, level, anchor):
    anc_row, anc_col = anchor

    win_rows, win_cols = window.getmaxyx()

    # account for border width
    win_rows = win_rows - 2
    win_cols = win_cols - 2

    lvl_rows = len(level)
    lvl_cols = len(level[0])

    # relative to level coordinates, centered on player
    anc_row_max = anc_row + floor(win_rows / 2)
    anc_col_max = anc_col + floor(win_cols / 2)
    anc_row_min = anc_row - ceil(win_rows / 2)
    anc_col_min = anc_col - ceil(win_cols / 2)

    row_min = max(anc_row_min, 0)
    col_min = max(anc_col_min, 0)
    row_max = min(anc_row_max, lvl_rows)
    col_max = min(anc_col_max, lvl_cols)

    if anc_row_min < 0:
        row_max = min(win_rows, lvl_rows)
    if anc_row_max > lvl_rows:
        row_min = max(lvl_rows - win_rows, 0)
    if anc_col_min < 0:
        col_max = min(win_cols, lvl_cols)
    if anc_col_max > lvl_cols:
        col_min = max(lvl_cols - win_cols, 0)

    # we can print this many rows/cols
    rows = row_max - row_min
    cols = col_max - col_min

    # top left corner of window centered on player
    # relative to level coordinates
    win_row_off = floor((win_rows - rows) / 2)
    win_col_off = floor((win_cols - cols) / 2)

    show_debug(0, "win off", win_row_off, win_col_off)
    show_debug(1, "anc    ", anc_row, anc_col)
    show_debug(2, "showing", rows, cols)

    # row and col are relative to the window
    for row in range(rows):
        for col in range(cols):
            # abs_row and abs_col are relative to the level
            lvl_row = row_min + row
            lvl_col = col_min + col
            win_row = win_row_off + row
            win_col = win_col_off + col
            terrain = "."
            if level[lvl_row][lvl_col]:
                terrain = "#"
            window.addch(win_row + 1, win_col + 1, terrain)

    return ((row_min, col_min), (win_row_off, win_col_off))


def show_player(window, level_off, window_off, player_pos):
    p_row, p_col = player_pos
    l_row, l_col = level_off
    w_row, w_col = window_off
    row = p_row - l_row + w_row
    col = p_col - l_col + w_col
    window.addch(row + 1, col + 1, "@")


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
    curses.curs_set(0)
    stdscr.resize(18, 78)
    blank_window(stdscr)

    global debug_window
    debug_window = curses.newwin(20, 20, 0, 80)
    debug_panel = curses.panel.new_panel(debug_window)
    debug_panel.top()
    curses.panel.update_panels()

    level = make_room(5, 5)

    game_state = {"level": level, "player_pos": (1, 1), "quit": False}

    next_key = None
    while True:
        blank_window(stdscr)
        blank_window(debug_window)

        handle_key(next_key, game_state)
        if game_state["quit"]:
            break

        level_off, window_off = show_level(
            stdscr, game_state["level"], game_state["player_pos"]
        )
        show_player(stdscr, level_off, window_off, game_state["player_pos"])

        next_key = stdscr.getkey()


curses.wrapper(main)
