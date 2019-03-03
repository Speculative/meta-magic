import curses
import curses.panel
import time


def blank_window(window):
    window.clear()
    window.border()
    window.refresh()


def show_modal(width, height):
    modal_window = curses.newwin(3, 10, 2, 2)
    modal_panel = curses.panel.new_panel(modal_window)
    modal_panel.top()
    curses.panel.update_panels()

    blank_window(modal_window)
    return modal_panel


def main(stdscr):
    curses.curs_set(0)
    stdscr.resize(20, 80)
    stdscr.border()

    modal = show_modal(3, 10)

    time.sleep(2)
    modal.window().erase()
    curses.doupdate()
    blank_window(stdscr)

    stdscr.refresh()
    stdscr.getkey()


curses.wrapper(main)
