import sys

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from utils.read_input import read_input, read_input_raw

# text = read_input('./10/example4.txt')
text = read_input('./10/input.txt')

# Each char creates a map from one direction to another.
# x, y represent the starting input
# Each position in the tuple returned represents a modification to the x, y value (i.e. +/- 0/1) per input direction and a new direction.
# E.g. encountering an 'F' from the South would return (-1, +1, 2) meaning go 'North' in Y axis, 'East' in X axis, and your new direction is East.
# Directions go NORTH, EAST, WEST, SOUTH
# None values are used when a direction is not available.
# E.g. accessing the versicle pipe at index 1 or 3 (East and West) is not allowed.
constructors = {
    '|': lambda x, y: ((-1, 0, 0), None, (1, 0, 2), None),
    '-': lambda x, y: (None, (0, 1, 1), None, (0, -1, 3)),
    'L': lambda x, y: (None, None, (0, 1, 1), (-1, 0, 0)),
    'J': lambda x, y: (None, (-1, 0, 0), (0, -1, 3), None),
    '7': lambda x, y: ((0, -1, 3), (1, 0, 2), None, None),
    'F': lambda x, y: ((0, 1, 1), None, None, (1, 0, 2)),
    '.': lambda x, y: (None, None, None, None),
    'S': lambda x, y: ((-1, 0, 0), (0, 1, 1), (1, 0, 2), (0, -1, 3)),
}

# Tracks all cells which are part of the main loop.
loop_cells = []

# Two-dimensional list representing the rows and columns of the map, converted into instructions.
directions = []

# Map of the raw characters in a two-dimensional arrays. Mirrors the 'directions' map.
raw_map = []

# The location of 'S'
starting_coords = (0, 0)

# Any possible directions 'S' may start on.
starting_directions = []

# List of cells contained within the loop.
detected_nests = []

line_idx = 0
for line in text:
    parsed_line = []
    char_idx = 0
    raw_map.append(list(line))
    for char in list(line):
        if char == 'S':
            starting_coords = (line_idx, char_idx)

        instruction = constructors[char](line_idx, char_idx)
        parsed_line.append(instruction)
        char_idx += 1
    directions.append(parsed_line)
    line_idx += 1

def valid_directions(starting_x: int, starting_y: int):
    direction_checks = [
        (starting_x - 1, starting_y, 0, 'Going North'),
        (starting_x, starting_y + 1, 1, 'Going East'),
        (starting_x + 1, starting_y, 2, 'Going South'),
        (starting_x, starting_y - 1, 3, 'Going West'),
    ]
    possible_directions = []
    for check in direction_checks:
        if check[0] >= 0 and check[1] >= 0:
            print('Checking', check)
            print(directions[check[0]][check[1]])
            if directions[check[0]][check[1]][check[2]]:
                print('! Direction valid: ', check)
                possible_directions.append(check[2])
    return possible_directions

starting_directions = valid_directions(starting_coords[0], starting_coords[1])

# Part 1
pt1_value = 1

def calculate_next_cell(last_cell):
    instruction = directions[last_cell[0]][last_cell[1]][last_cell[2]]
    next_cell = (last_cell[0] + instruction[0], last_cell[1] + instruction[1], instruction[2])
    return next_cell

current_cell = calculate_next_cell((starting_coords[0], starting_coords[1], starting_directions[0]))
loop_cells = [(starting_coords[0], starting_coords[1]), (current_cell[0], current_cell[1])]

print('(pre) Current cell, starting coords', current_cell, starting_coords)
while current_cell[0] != starting_coords[0] or current_cell[1] != starting_coords[1]:
    print('(1) Cell is not home, calculating next cell...')
    pt1_value += 1
    print('(2) Next pt1 index', pt1_value)
    current_cell = calculate_next_cell(current_cell)
    loop_cells.append((current_cell[0], current_cell[1]))
    print('(3) Next cell', current_cell)

pt1_value = int(pt1_value / 2)

# Part 2
print('================================ PT2')
pt2_value = 0

# =========== Unused Shoelace algorithm attempt ===========
def shoelace(coords: list):
    coord_idx = 0
    accumulated = 0
    while coord_idx < len(coords):
        left = coords[coord_idx]
        right = coords[(coord_idx + 1) % len(coords)]
        num1 = left[0] * right[1]
        num2 = left[1] * right[0]
        accumulated += num1 - num2
        coord_idx += 1
    return abs(accumulated) / 2

print('shoelace(loop_cells): ', shoelace(loop_cells))
# # print(shoelace([(1, 6), (3, 1), (7, 2), (4, 4), (8, 5)]))
# # print('Loop Cells', [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (2, 1)])
# # print(shoelace([(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (2, 1)]))
# print('Loop Cells', [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 5), (3, 5), (3, 4), (3, 3), (3, 2), (3, 1), (2, 1)])
# print(shoelace([(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 5), (3, 5), (3, 4), (3, 3), (3, 2), (3, 1), (2, 1)]))
# =========== / Unused Shoelace algorithm attempt ===========

def ray_cast_detect(point: tuple):
    x_toggle = False
    y_toggle = False
    x_check = None
    y_check = None
    x_crawl = 0
    y_crawl = 0

    def adapt_s(x: int, y: int):
        top = raw_map[x - 1][y] in ['F', '7', '|']
        bottom = raw_map[x + 1][y] in ['L', 'J', '|']
        left = raw_map[x][y - 1] in ['L', 'F', '-']
        right = raw_map[x][y + 1] in ['J', '7', '-']
        if top and bottom:
            return '|'
        if left and right:
            return '-'
        if top and right:
            return 'L'
        if top and left:
            return 'J'
        if bottom and right:
            return 'F'
        if bottom and left:
            return '7'

    if point in loop_cells:
        return False

    while x_crawl < point[0]:
        char = raw_map[x_crawl][point[1]]
        if char == 'S':
            char = adapt_s(x_crawl, point[1])
        if (x_crawl, point[1]) in loop_cells:
            if char == '-':
                x_toggle = not x_toggle
            elif char in ['F', '7']:
                x_check = char
            elif x_check:
                if x_check == 'F' and char == 'J':
                    x_toggle = not x_toggle
                    x_check = None
                if x_check == 'F' and char == 'L':
                    x_check = None
                if x_check == '7' and char == 'L':
                    x_toggle = not x_toggle
                    x_check = None
                if x_check == '7' and char == 'J':
                    x_check = None

        x_crawl += 1

    while y_crawl < point[1]:
        char = raw_map[point[0]][y_crawl]
        if char == 'S':
            char = adapt_s(point[0], y_crawl)
        print('### Checking char line 18 at ', y_crawl, char)
        if (point[0], y_crawl) in loop_cells:
            if char == '|':
                y_toggle = not y_toggle
                print('Char is vertical pipe. y_toggle now', y_toggle)
            elif char in ['L', 'F']:
                print('Junction OPEN. y_check is ', char)
                y_check = char
            elif y_check:
                if y_check == 'L' and char == '7':
                    y_toggle = not y_toggle
                    y_check = None
                    print('L7 Junction CLOSED. y_toggle is now ', y_toggle)
                if y_check == 'L' and char == 'J':
                    y_check = None
                    print('L7 Junction CLOSED with NO change.')
                if y_check == 'F' and char == 'J':
                    y_toggle = not y_toggle
                    y_check = None
                    print('FJ Junction CLOSED. y_toggle is now ', y_toggle)
                if y_check == 'F' and char == '7':
                    y_check = None
                    print('FJ Junction CLOSED with NO change.')

        y_crawl += 1

    return x_toggle or y_toggle

# Inefficient code but whatever
row_idx = 0
for row in raw_map:
    col_idx = 0
    for col in row:
        if ray_cast_detect((row_idx, col_idx)):
            detected_nests.append((row_idx, col_idx))
            pt2_value += 1
        col_idx += 1
    row_idx += 1
# Also boss if you're watching, I mean not that & that I will surely refactor this later...

def to_string(board):
    table = []
    row_idx = 0
    head_row = '<div class="head-row">'
    for head_idx in range(len(board) + 1):
        head_row += '<div>' + str(head_idx) + '</div>'
    head_row += '</div>'
    table.append(head_row)
    for row in board:
        table_row = ['<div class="head-col">' + str(row_idx) + '</div>']
        char_idx = 0
        for char in row:
            open_tag = '<div>'
            if (row_idx, char_idx) in loop_cells:
                open_tag = '<div style="background: orange;">'
            if (row_idx, char_idx) in detected_nests:
                open_tag = '<div style="background: blue;">'

            table_row.append(open_tag + char + '</div>')
            char_idx += 1
        table.append('<div>' + ''.join(table_row) + '</div>')
        row_idx += 1

    html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                body > div {
                    display: flex;
                    width: min-content;
                    font-family: monospace;
                }
                body > div div {
                    width: 20px;
                    height: 20px;
                    background: #ecf0f1;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border: 1px solid #222;
                }
                .head-row {
                    position: sticky;
                    top: 0;
                    font-size: 10px;
                }
                .head-col {
                    position: sticky;
                    left: 0;
                    font-size: 10px;
                }
            </style>
        </head>
        <body>
        ''' + ''.join(table) + '''
        </body>
        </html>
    '''
    with open('./10/vis.html', 'w') as f:
        f.write(html)
        f.close()

to_string(raw_map)

print('Part 1 Total: ', pt1_value)
print('Part 2 Total: ', pt2_value)