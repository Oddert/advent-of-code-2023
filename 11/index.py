import sys

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from utils.read_input import read_input, read_input_raw

# raw_text = read_input_raw('./11/example.txt')
# text = read_input('./11/example.txt')
raw_text = read_input_raw('./11/input.txt')
text = read_input('./11/input.txt')

is_part_2 = True

raw_map = []

empty_rows_list = [True for x in range(len(text))]
empty_cols_list = [True for x in range(len(text[0]))]

line_idx = 0
for line in text:
    chars = list(line)
    char_idx = 0
    for char in chars:
        if char == '#':
            empty_rows_list[line_idx] = False
            empty_cols_list[char_idx] = False
        char_idx += 1
    raw_map.append(chars)
    line_idx += 1

# jump_size = 1_000_000 if is_part_2 else 1

# for row_idx, row in enumerate(raw_map):
#     new_row = []
#     warp_jumps_vertical = 0
#     warp_jumps_horizontal = 0
#     for col_idx, col in enumerate(row):
#         if empty_cols_list[col_idx]:
#             warp_jumps_vertical += 1
#         if empty_rows_list[row_idx]:
#             warp_jumps_vertical += 1
#         x_adjusted = col[0] + (warp_jumps_vertical * jump_size)
#         y_adjusted = col[1] + (warp_jumps_horizontal * jump_size)
#         new_row.append((x_adjusted, y_adjusted))
#     raw_map[row_idx] = new_row

print('=========')
for row in raw_map:
    print(row)
print('=========')

print('empty_rows_list', empty_rows_list)
print('empty_cols_list', empty_cols_list)

galaxies = []
pairings = []

for row_idx, row in enumerate(raw_map):
    for col_idx, col in enumerate(row):
        if col == '#':
            galaxies.append((row_idx, col_idx))

pairing_idx = 0
while pairing_idx < len(galaxies) - 1:
    pairing_continue_idx = pairing_idx + 1
    while pairing_continue_idx < len(galaxies):
        pairings.append((pairing_idx, pairing_continue_idx))
        pairing_continue_idx += 1
    pairing_idx += 1

# print('galaxies', len(galaxies), galaxies)
# print('pairings', len(pairings), pairings)


class AStarNode():
    def __init__(self, _parent=None, _position=None):
        self.parent = _parent
        self.position = _position

        self.g = 0
        self.h = 0
        self.f = 0

    def __repr__(self) -> str:
        return f'<AStarNode position={self.position} g={self.g} h={self.h} f={self.f}>'

    def __eq__(self, comparison):
        return self.position == comparison.position


def reconstruct_path(current: AStarNode):
    path = []
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]


def is_node_in_void(current: AStarNode):
    return empty_rows_list[current.position[0]] or empty_cols_list[current.position[1]]


def standard_heuristic(current: AStarNode, goal: AStarNode):
    goal_adjusted = [goal.position[0], goal.position[1]]

    # if is_node_in_void(current):
    #     if goal.position[0] > current.position[0]:
    #         goal_adjusted[0] += 100
    #     else:
    #         goal_adjusted[0] -= 100
    #     if goal.position[1] > current.position[1]:
    #         goal_adjusted[1] += 100
    #     else:
    #         goal_adjusted[1] -= 100

    # if current.position[1] in empty_cols_list and empty_cols_list[current.position[1]]:
    #     if goal.position[1] > current.position[1]:
    #         goal_adjusted[1] += 1
    #     else:
    #         goal_adjusted[1] -= 1

    x_diff = current.position[0] - goal_adjusted[0]
    y_diff = current.position[1] - goal_adjusted[1]
    return (x_diff ** 2) + (y_diff ** 2)


def pt2_heuristic(current: AStarNode, goal: AStarNode):
    goal_adjusted = [current.position[0], current.position[1]]

    # if is_node_in_void(current):
    #     if goal.position[0] > current.position[0]:
    #         goal_adjusted[0] += 10
    #     else:
    #         goal_adjusted[0] -= 10
    #     if goal.position[1] > current.position[1]:
    #         goal_adjusted[1] += 10
    #     else:
    #         goal_adjusted[1] -= 10

    x_diff = goal_adjusted[0] - goal.position[0]
    y_diff = goal_adjusted[1] - goal.position[1]
    return (x_diff ** 2) + (y_diff ** 2)


def a_star(start, goal, h=standard_heuristic):
    start_node = AStarNode(None, start)
    goal_node = AStarNode(None, goal)

    open_set = [start_node]
    closed_set = []

    while len(open_set) > 0:
        # print('--------------------------------')
        current = open_set[0]
        current_idx = 0

        for index, item in enumerate(open_set):
            if item.f < current.f:
                current = item
                current_idx = index

        open_set.pop(current_idx)
        closed_set.append(current)

        # print(current, goal_node, current == goal_node)
        if current == goal_node:
            return reconstruct_path(current)

        # Create a list of potential neighbors.
        neighbors_coords = [
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1),
        ]
        neighbours = []
        for coords in neighbors_coords:
            x_coord = current.position[0] + coords[0]
            y_coord = current.position[1] + coords[1]
            if x_coord >= 0 and x_coord < len(raw_map) and y_coord >= 0 and y_coord < len(raw_map[0]):
                neighbour = (x_coord, y_coord)
                neighbour_node = AStarNode(current, neighbour)
                neighbours.append(neighbour_node)

        # Test each neighbour
        for neighbour in neighbours:
            
            # Discount any node in the closed set.
            for closed_item in closed_set:
                # print('Closed set check for neighbour', neighbour)
                if closed_item == neighbour:
                    # print('> Found in closed set, CONTINUING...')
                    continue
            
            # print('Checking neighbour', neighbour)
            # is_void = is_node_in_void(neighbour)
            neighbour.g = current.g + 1 # (1_000_000 if is_void else 1)
            neighbour.h = h(neighbour, goal_node)
            neighbour.f = neighbour.g + neighbour.h
            # print('Secondary check', neighbour)

            for open_item in open_set:
                if neighbour == open_item:
                    # print('Neighbour matches open set item...', neighbour.g, open_item.g, neighbour.g > open_item.g)
                    if neighbour.g > open_item.g:
                        # print('...neighbour has larger g.')
                        continue
            
            # print('OPEN set: appending neighbour')
            open_set.append(neighbour)

# res = a_star((2, 0), (10, 14))
# # res = a_star((6, 1), (11, 5))
# print('a_star((2, 0), (10, 14))', res)
# # print('a_star((6, 1), (11, 5))', res)
# for coord in res[1:-1]:
#     raw_map[coord[0]][coord[1]] = '+'

for line in raw_map:
    print(line)

final_value = 0

print('empty_rows_list', empty_rows_list)
print('empty_cols_list', empty_cols_list)
print('pairings converted', [[galaxies[x[0]], galaxies[x[1]]] for x in pairings])
pair_idx = 0
test_idx = 528491
# print(galaxies[pairings[test_idx][0]], galaxies[pairings[test_idx][1]])
# print(a_star(galaxies[0], galaxies[1]))

jump_step = 1
if is_part_2:
    jump_step = 999_999

for pairing in pairings:
    galaxy1 = galaxies[pairing[0]]
    galaxy2 = galaxies[pairing[1]]
    additional_distance = 0

    distance = a_star(galaxy1, galaxy2, pt2_heuristic)
    for coord_idx, coords in enumerate(distance):
        if empty_rows_list[coords[0]]:
            # print('[1.] coords in empty ROW list')
            if distance[coord_idx - 1][0] != coords[0]:
                # print('[2.] Rows do not match')
                additional_distance += jump_step
                # if pair_idx == test_idx:
                #     print(pairing, '[3.]', additional_distance)
        if empty_cols_list[coords[1]]:
            # print('[4.] coords in empty COL list')
            if distance[coord_idx - 1][1] != coords[1]:
                # print('[5.] Cols do not match')
                additional_distance += jump_step
                # if pair_idx == test_idx:
                #     print(pairing, '[6.]', additional_distance)
    pair_idx += 1

    # print('Checking galaxies: ', galaxy1, galaxy2, '-> distance', len(distance) - 1)
    if pair_idx == test_idx:
        # print(distance, len(distance) - 1)
        print(distance, additional_distance, (len(distance) - 1) + additional_distance)
    # final_value += len(distance) - 1
    print(galaxies[pairing[0]], galaxies[pairing[1]], ': ', (len(distance) - 1) + additional_distance)
    final_value += (len(distance) - 1) + additional_distance

print('Total: ', final_value)
