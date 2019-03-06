CARDINAL = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}


def make_room(rows, cols):
    level = [[False for col in range(cols)] for row in range(rows)]
    level[0] = [True for col in range(cols)]
    level[rows - 1] = [True for col in range(cols)]
    for row in range(1, rows - 1):
        level[row][0] = True
        level[row][cols - 1] = True
    return level


def add_coord(c1, c2):
    return (c1[0] + c2[0], c1[1] + c2[1])


def dimensions(level):
    return (len(level), len(level[0]))


def level_get(level, loc):
    row, col = loc
    return level[row][col]


def level_set(level, loc, val):
    row, col = loc
    level[row][col] = val


def in_bounds(level, loc):
    rows, cols = dimensions(level)
    row, col = loc
    return 0 <= row < rows and 0 <= col < cols


def neighbor_values(level, loc):
    return list(map(lambda n: level_get(level, n), neighbors(level, loc)))


def neighbors(level, loc):
    return list(
        filter(
            lambda n: in_bounds(level, n),
            [add_coord(loc, dir) for dir in CARDINAL.values()],
        )
    )


def distance_map(level, goal):
    goal_row, goal_col = goal
    rows, cols = dimensions(level)
    weights = [[-1 for col in range(cols)] for row in range(rows)]
    weights[goal_row][goal_col] = 0
    frontier = neighbors(level, goal)
    while len(frontier) > 0:
        node = frontier.pop(0)
        node_weight = level_get(weights, node)
        node_terrain = level_get(level, node)
        # skip wall tiles
        if not node_terrain:
            lowest = sorted(filter(lambda n: n != -1, neighbor_values(weights, node)))[
                0
            ]
            if node_weight == -1 or node_weight > lowest + 1:
                level_set(weights, node, lowest + 1)
                frontier.extend(neighbors(level, node))

    return weights


# Debug stuff
def print_room(room):
    room = map(lambda row: map(lambda cell: "#" if cell else ".", row), room)
    for line in room:
        print("".join(line))


def print_weights(weights):
    weights = map(
        lambda row: map(
            lambda cell: "#" if cell == -1 else 9 if cell > 9 else cell, row
        ),
        weights,
    )
    for line in weights:
        print("".join(map(str, line)))

