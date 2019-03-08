import level

# Payload -> Damage
PAYLOADS = {"fire": 5}

# Transport => Type, Range, Size
TRANSPORTS = {"ball": ("aoe", 5, 5), "spray": ("cone", 0, 3)}


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
