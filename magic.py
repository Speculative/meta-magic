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
                window.addch(row+1, col+1, '#')
            else:
                window.addch(row+1, col+1, '.')


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
    show_level(stdscr, level)

    stdscr.getkey()


curses.wrapper(main)
