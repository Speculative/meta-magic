import curses
import curses.panel
import time


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


def show_level(window, level):
    for row in range(len(level)):
        for col in range(len(level[0])):
            if level[row][col]:
                window.addch(row + 1, col + 1, "#")
            else:
                window.addch(row + 1, col + 1, ".")


def show_player(window, player_pos):
    p_row, p_col = player_pos
    window.addch(p_row + 1, p_col + 1, '@')


MOVES = {
    'h': (0, -1),
    'j': (1, 0),
    'k': (-1, 0),
    'l': (0, 1),
    'y': (-1, -1),
    'u': (-1, 1),
    'n': (1, -1),
    'm': (1, 1),
}

def move_player(key, game_state):
    level = game_state['level']

    curr_row, curr_col = game_state['player_pos']
    move_row, move_col = MOVES[key]
    next_row = curr_row + move_row
    next_col = curr_col + move_col

    if (0 <= next_row < len(level)
        and 0 <= next_col < len(level[0])
        and not level[next_row][next_col]):
        game_state['player_pos'] = (next_row, next_col)

def handle_key(key, game_state):
    if key in MOVES:
        move_player(key, game_state)
    elif key == 'q':
        game_state['quit'] = True


def main(stdscr):
    curses.curs_set(0)
    stdscr.resize(20, 80)
    blank_window(stdscr)

    level = [[False for col in range(78)] for row in range(18)]
    level[0] = [True for col in range(78)]
    level[17] = [True for col in range(78)]
    for row in range(1, 17):
        level[row][0] = True
        level[row][77] = True

    game_state = {
        'level': level,
        'player_pos': (10, 40),
        'quit': False
    }

    next_key = None
    while True:
        handle_key(next_key, game_state)
        if game_state['quit']:
            break
        show_level(stdscr, game_state['level'])
        show_player(stdscr, game_state['player_pos'])
        next_key = stdscr.getkey()


curses.wrapper(main)
