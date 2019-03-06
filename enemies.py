import level


def approach_player(game_state, own_state):
    terrain_map = game_state["level"]
    distances = level.distance_map(terrain_map, game_state["player_pos"])
    own_id, own_type, own_health, own_pos = own_state

    # find the step that is closest to the player
    candidate_steps = [
        (n, level.level_get(distances, n))
        for n in level.neighbors(terrain_map, own_pos)
    ]
    best_step, best_step_distance = sorted(candidate_steps, key=lambda c: c[1])[0]

    # move only if it takes us closer to the player
    if best_step_distance < level.level_get(distances, own_pos):
        game_state["enemies"][own_id] = (own_id, own_type, own_health, best_step)
        return True
    return False


# Type -> Starting health, behaviors
ENEMY_TYPES = {
    "zombie": {"init_health": 10, "behaviors": [approach_player], "icon": "z"}
}

