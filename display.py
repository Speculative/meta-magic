import curses
import curses.panel
from math import floor, ceil
import enemies

debug_window = None
main_window = None


def init_display(stdscr):
    global main_window, debug_window
    main_window = stdscr
    curses.curs_set(0)
    main_window.resize(20, 80)
    blank_window(main_window)

    debug_window = curses.newwin(20, 20, 0, 80)
    debug_panel = curses.panel.new_panel(debug_window)
    debug_panel.top()
    curses.panel.update_panels()
    blank_window(debug_window)


def show_debug(row, *args):
    debug_window.addstr(row + 1, 1, " ".join(map(lambda a: str(a), list(args))))
    debug_window.refresh()


def blank_window(window):
    window.clear()
    window.border()
    window.refresh()


def begin_render():
    global main_window, debug_window
    blank_window(main_window)
    blank_window(debug_window)


def show_modal(rows, cols, parent_window):
    parent_rows, parent_cols = parent_window.getmaxyx()
    modal_window = curses.newwin(
        rows, cols, int((parent_rows - rows) / 2), int((parent_cols - cols) / 2)
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
    anc_row_max = anc_row + ceil(win_rows / 2)
    anc_col_max = anc_col + ceil(win_cols / 2)
    anc_row_min = anc_row - floor(win_rows / 2)
    anc_col_min = anc_col - floor(win_cols / 2)

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

    # Transform from level coordinates to window coordinates
    return (win_row_off - row_min, win_col_off - col_min)


def show_player(window, window_transform, player_pos):
    p_row, p_col = player_pos
    row_off, col_off = window_transform
    row = p_row + row_off
    col = p_col + col_off
    window.addch(row + 1, col + 1, "@")


def show_visible_enemies(window, window_transform, spawned_enemies):
    max_row, max_col = window.getmaxyx()
    for enemy in spawned_enemies:
        _, enemy_type, _, enemy_pos = enemy
        e_row, e_col = enemy_pos
        row_off, col_off = window_transform
        row = e_row + row_off
        col = e_col + col_off
        if (0 <= row + 1 < max_row) and (0 <= col + 1 < max_col):
            window.addch(row + 1, col + 1, enemies.ENEMY_TYPES[enemy_type]["icon"])
