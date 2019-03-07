import curses
import curses.panel
import time
from math import floor, ceil
import display
import level
import state
import binascii


def main(stdscr):
    display.init_display(stdscr)

    game_state = {
        "level": level.make_room(20, 80),
        "player_pos": (1, 1),
        "mode": "normal",
        "enemies": {},
        "spell": ("", ""),
        "target": None,
        "focused_slot": 0,
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

        payload, transport = game_state["spell"]
        if next_key != None:
            display.show_debug(3, str(binascii.hexlify(next_key.encode())))
        display.show_debug(4, payload, transport)

        next_key = stdscr.getkey()


curses.wrapper(main)
