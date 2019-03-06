import curses
import curses.panel
import time
from math import floor, ceil
import display
import level
import state


def main(stdscr):
    display.init_display(stdscr)

    game_state = {
        "level": level.make_room(20, 80),
        "player_pos": (1, 1),
        "mode": "normal",
        "enemies": {},
        "quit": False,
    }

    next_key = None
    while True:
        state.handle_key(next_key, game_state)
        if game_state["quit"]:
            break

        display.begin_render()

        window_transform = display.show_level(
            stdscr, game_state["level"], game_state["player_pos"]
        )
        display.show_player(stdscr, window_transform, game_state["player_pos"])
        display.show_visible_enemies(
            stdscr, window_transform, game_state["enemies"].values()
        )

        next_key = stdscr.getkey()


curses.wrapper(main)
