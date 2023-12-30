import sys
import json
# Go shout at Matt Parker for this he gave me the idea...
import math as maths

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from utils.read_input import read_input, read_input_raw

# raw_text = read_input_raw('./14/example.txt')
# text = read_input('./14/example.txt')
raw_text = read_input_raw('./14/input.txt')
text = read_input('./14/input.txt')

grid = []
for line in text:
    row = [char for char in list(line)]
    grid.append(row) 

print('----- initial grid')
for line in grid:
    print(line)
print('----- / initial grid')


def inc_north(x, y):
    return (x - 1, y)


def inc_east(x, y):
    return (x, y + 1)


def inc_south(x, y):
    return (x + 1, y)


def inc_west(x, y):
    return (x, y - 1)


def out_of_bounds(board_len: int, row_len: int, coords):
    return coords[0] < 0 or coords[0] >= board_len or\
            coords[1] < 0 or coords[1] >= row_len


def slide_em(board: list, increment=inc_north, direction='north'):
    new_board = [[x for x in row] for row in board]
    rocks = []
    match direction:
        case 'north':
            for row_idx, row in enumerate(board):
                for col_idx, col in enumerate(row):
                    if col == 'O':
                        rocks.append((row_idx, col_idx))
        case 'west':
            col_idx = 0
            while col_idx < len(board):
                for row_idx, row in enumerate(board):
                    col = board[row_idx][col_idx]
                    if col == 'O':
                        rocks.append((row_idx, col_idx))
                col_idx += 1
        case 'south':
            row_idx = len(board[0]) - 1
            while row_idx >= 0:
                row = board[row_idx]
                for col_idx, col in enumerate(row):
                    if col == 'O':
                        rocks.append((row_idx, col_idx))
                row_idx -= 1
        case 'east':
            col_idx = len(board[0]) - 1
            while col_idx >= 0:
                for row_idx, row in enumerate(board):
                    col = board[row_idx][col_idx]
                    if col == 'O':
                        rocks.append((row_idx, col_idx))
                col_idx -= 1

    for rock in rocks:
        forward_cell_coords = increment(*rock)
        oob = out_of_bounds(len(board), len(board[0]), forward_cell_coords)
        if not oob:
            forward_cell = new_board[forward_cell_coords[0]][forward_cell_coords[1]]
            if forward_cell == '.':

                finished = False
                while forward_cell == '.' and not finished:
                    next_forward_cell_coords = increment(*forward_cell_coords)
                    next_oob = out_of_bounds(len(board), len(board[0]), next_forward_cell_coords)

                    if next_oob:
                        finished = True
                        continue

                    next_forward_cell = new_board[next_forward_cell_coords[0]][next_forward_cell_coords[1]]
                    if next_forward_cell != '.':
                        finished = True
                    else:
                        forward_cell_coords = next_forward_cell_coords
                        forward_cell = next_forward_cell

                new_board[rock[0]][rock[1]] = '.'
                new_board[forward_cell_coords[0]][forward_cell_coords[1]] = 'O'
    return new_board


def calc_distances(board, direction = 'north'):
    distance = 0
    for row_idx, row in enumerate(board):
        for col_idx, col in enumerate(row):
            if col == 'O':
                match direction:
                    case 'north':
                        distance += len(board) - row_idx
                    case 'south':
                        distance += col_idx + 1
                    case 'east':
                        distance += len(row) - col_idx
                    case 'west':
                        distance += row_idx + 1
    return distance


# Part 1
pt1_value = 0

print('---------------')
pt1_board = slide_em(grid)
pt1_value = calc_distances(pt1_board)

for line in pt1_board:
    print(line)

# Part 2
print('================================ PT2')

# Repeating again to ensure no backward-mutations have occurred in pt1
print('----- initial grid')
for line in grid:
    print(line)
print('----- / initial grid')
pt2_value = 0

pt2_grid = [[x for x in row] for row in grid]

cache = {}

loop_start_idx = None
loop_end_idx = None

range_len = 1_000_000_000

for cycle in range(range_len - 1):
    print('cycle ', cycle)
    north = slide_em(pt2_grid, inc_north, 'north')
    west = slide_em(north, inc_west, 'west')
    south = slide_em(west, inc_south, 'south')
    east = slide_em(south, inc_east, 'east')
    pt2_grid = east

    json_obj = json.dumps(pt2_grid)
    if json_obj in cache:
        print('MATCH FOUND AT ', cache[json_obj], ' to ', cycle)
        loop_start_idx = cache[json_obj]
        loop_end_idx = cycle
        break
    cache[json_obj] = cycle

total_minus_start_idx = range_len - loop_start_idx - 1
print('total_minus_start_idx', total_minus_start_idx)
loop_len = loop_end_idx - loop_start_idx
print('loop_len', loop_len)
loop_count = maths.floor(total_minus_start_idx / loop_len)
print('loop_count', loop_count)
remainder = range_len - ((loop_count * loop_len) + loop_start_idx + 1)
print('remainder', remainder)

if remainder == 0:
    print('use the pt2_grid value')
else:
    print('incrementing...')
    for cycle in range(remainder):
        print('final cycle ', cycle)
        north = slide_em(pt2_grid, inc_north, 'north')
        west = slide_em(north, inc_west, 'west')
        south = slide_em(west, inc_south, 'south')
        east = slide_em(south, inc_east, 'east')
        pt2_grid = east
print('Done.')

pt2_value = calc_distances(pt2_grid)

print('Part 1 Total: ', pt1_value)
print('Part 2 Total: ', pt2_value)
