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


def main(stdscr):
    curses.curs_set(0)
    stdscr.resize(20, 80)
    stdscr.border()

    left_window = curses.newwin(20, 10, 0, 0)
    left_panel = curses.panel.new_panel(left_window)
    left_panel.top()
    curses.panel.update_panels()
    blank_window(left_window)

    modal = show_modal(8, 3, left_window)
    modal.window().addstr(1, 2, "hello")
    modal.window().refresh()

    stdscr.refresh()
    stdscr.getkey()


curses.wrapper(main)
