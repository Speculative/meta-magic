import enemies

enemy_id = 0

# Normal mode
def normal_handle_key(key, game_state):
    if key in MOVES:
        move_player(key, game_state)
    if key == "s":
        spawn_enemy(game_state, (2, 2), "zombie")
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


def spawn_enemy(game_state, position, enemy_type):
    global enemy_id
    game_state["enemies"][enemy_id] = (
        enemy_id,
        enemy_type,
        enemies.ENEMY_TYPES[enemy_type]["init_health"],
        position,
    )
    enemy_id += 1


# Move time forward by one turn
def tick_forward(game_state):
    tick_enemies(game_state)


def tick_enemies(game_state):
    for enemy in game_state["enemies"].values():
        enemy_id, enemy_type, _, _ = enemy
        behaviors = enemies.ENEMY_TYPES[enemy_type]["behaviors"]
        for behavior in behaviors:
            if behavior(game_state, enemy):
                break


# Organize everything in one update function
MODE_HANDLERS = {"normal": normal_handle_key}


def handle_key(key, game_state):
    MODE_HANDLERS[game_state["mode"]](key, game_state)

