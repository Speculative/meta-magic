# Normal mode
def normal_handle_key(key, game_state):
    if key in MOVES:
        move_player(key, game_state)
    elif key == "q":
        game_state["quit"] = True

    tick_forward(game_state)


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


# Move time forward by one turn
def tick_forward(game_state):
    pass


# Organize everything in one update function
MODE_HANDLERS = {"normal": normal_handle_key}


def handle_key(key, game_state):
    MODE_HANDLERS[game_state["mode"]](key, game_state)

