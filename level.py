import math

CARDINAL_DIRECTIONS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
ALL_DIRECTIONS = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
    "NE": (-1, 1),
    "NW": (-1, -1),
    "SE": (1, 1),
    "SW": (1, -1),
}


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


def neighbor_values(level, loc, directions):
    return list(map(lambda n: level_get(level, n), neighbors(level, loc, directions)))


def neighbors(level, loc, directions):
    return list(
        filter(
            lambda n: in_bounds(level, n),
            [add_coord(loc, dir) for dir in directions.values()],
        )
    )


def cardinal_distance_map(level, goal):
    return distance_map(level, goal, CARDINAL_DIRECTIONS)


def diagonal_distance_map(level, goal):
    return distance_map(level, goal, ALL_DIRECTIONS)


def distance_map(level, goal, directions):
    goal_row, goal_col = goal
    rows, cols = dimensions(level)
    weights = [[math.inf for col in range(cols)] for row in range(rows)]
    weights[goal_row][goal_col] = 0
    frontier = neighbors(level, goal, directions)
    while len(frontier) > 0:
        node = frontier.pop(0)
        node_weight = level_get(weights, node)
        node_terrain = level_get(level, node)
        # skip wall tiles
        if not node_terrain:
            lowest = sorted(neighbor_values(weights, node, directions))[0]
            if node_weight > lowest + 1:
                level_set(weights, node, lowest + 1)
                frontier.extend(neighbors(level, node, directions))

    return weights


# Debug stuff
def print_room(room):
    room = map(lambda row: map(lambda cell: "#" if cell else ".", row), room)
    for line in room:
        print("".join(line))


def print_weights(weights):
    weights = map(
        lambda row: map(
            lambda cell: "#" if cell == math.inf else 9 if cell > 9 else cell, row
        ),
        weights,
    )
    for line in weights:
        print("".join(map(str, line)))
