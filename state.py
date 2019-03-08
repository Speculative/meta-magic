import enemies
import spells

enemy_id = 0

# Normal mode
def normal_handle_key(key, game_state):
    if key in MOVES:
        move_player(key, game_state)
        tick_forward(game_state)
    elif key == "c":
        game_state["mode"] = "cast"
        game_state["target"] = game_state["player_pos"]
        game_state["spell"] = ("", "")
    elif key == "s":
        spawn_enemy(game_state, (2, 2), "zombie")
    elif key == "q":
        game_state["quit"] = True


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


def try_move(key, pos, terrain):
    curr_row, curr_col = pos
    move_row, move_col = MOVES[key]
    target_row = curr_row + move_row
    target_col = curr_col + move_col

    if (
        0 <= target_row < len(terrain)
        and 0 <= target_col < len(terrain[0])
        and not terrain[target_row][target_col]
    ):
        return (target_row, target_col)


def move_player(key, game_state):
    game_state["player_pos"] = try_move(
        key, game_state["player_pos"], game_state["level"]
    )


def spawn_enemy(game_state, position, enemy_type):
    global enemy_id
    game_state["enemies"][enemy_id] = (
        enemy_id,
        enemy_type,
        enemies.ENEMY_TYPES[enemy_type]["init_health"],
        position,
    )
    enemy_id += 1


# Casting mode
def cast_handle_key(key, game_state):
    if key == "\n" and spells.valid_spell(game_state):
        game_state["mode"] = "target"
        game_state["target"] = game_state["player_pos"]
    elif key == "\x1b":
        game_state["mode"] = "normal"
        game_state["spell"] = ("", "")
    elif key == "\t":
        game_state["focused_slot"] = (game_state["focused_slot"] + 1) % 2
    elif key == "\x7f":
        payload, transport = game_state["spell"]
        if game_state["focused_slot"] == 0:
            payload = payload[:-1]
        else:
            transport = transport[:-1]
        game_state["spell"] = (payload, transport)
    elif key.isalpha():
        payload, transport = game_state["spell"]
        if game_state["focused_slot"] == 0:
            game_state["spell"] = (payload + key, transport)
        else:
            game_state["spell"] = (payload, transport + key)


# Targeting mode
def target_handle_key(key, game_state):
    if key in MOVES:
        move_target(key, game_state)
    elif key == "\n" and spells.valid_target(game_state):
        # where the spell would do something
        game_state["spell"] = ("", "")
        game_state["mode"] = "normal"
        tick_forward(game_state)


def move_target(key, game_state):
    game_state["target"] = try_move(key, game_state["target"], game_state["level"])


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
MODE_HANDLERS = {
    "normal": normal_handle_key,
    "cast": cast_handle_key,
    "target": target_handle_key,
}


def handle_key(key, game_state):
    MODE_HANDLERS[game_state["mode"]](key, game_state)

