import level

# Payloads
def do_damage(damage, enemy):
    enemy_id, enemy_type, enemy_health, position = enemy
    return (enemy_id, enemy_type, enemy_health - damage, position)


# Transports
def single_target(game_state, size, payload):
    target = game_state["target"]
    for enemy in game_state["enemies"].values():
        enemy_id, _, _, position = enemy
        if position == game_state["target"]:
            game_state["enemies"][enemy_id] = payload(enemy)


# Payload -> Effect function
PAYLOADS = {"fire": lambda e: do_damage(10, e)}

# Transport => Transport function, Range, Size
TRANSPORTS = {"bolt": (single_target, 5, 0)}


def valid_spell(game_state):
    payload, transport = game_state["spell"]
    return payload in PAYLOADS and transport in TRANSPORTS


def valid_target(game_state):
    _, transport = game_state["spell"]
    target = game_state["target"]
    distances = level.diagonal_distance_map(
        game_state["level"], game_state["player_pos"]
    )
    _, cast_range, _ = TRANSPORTS[transport]
    return level.level_get(distances, target) <= cast_range


def cast_spell(game_state):
    payload, transport = game_state["spell"]
    target = game_state["target"]
    target_direction = game_state["target_direction"]
    transport_function, _, size = TRANSPORTS[transport]
    payload = PAYLOADS[payload]
    transport_function(game_state, size, payload)
