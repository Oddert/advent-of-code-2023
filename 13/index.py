import sys
import re

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from utils.read_input import read_input, read_input_raw

# example4 - u/sinsworth https://www.reddit.com/r/adventofcode/comments/18hitog/2023_day_13_easy_additional_examples/ pt1 709, pt2 1400
# example5 - u/5nnn https://www.reddit.com/r/adventofcode/comments/18hitog/comment/kd9nil6/ pt1 n/a, pt2 5 + 10

# raw_text = read_input_raw('./13/example.txt')
# text = read_input('./13/example.txt')
# raw_text = read_input_raw('./13/example2.txt')
# text = read_input('./13/example2.txt')
# raw_text = read_input_raw('./13/example3.txt')
# text = read_input('./13/example3.txt')
# raw_text = read_input_raw('./13/example4.txt')
# text = read_input('./13/example4.txt')
# raw_text = read_input_raw('./13/example5.txt')
# text = read_input('./13/example5.txt')
raw_text = read_input_raw('./13/input.txt')
text = read_input('./13/input.txt')

def to_bin(string: str):
    replaced = string.replace('.', '0')
    replaced = replaced.replace('#', '1')
    return replaced

row_sets = []
open_set = []
for line in text:
    if line == '':
        row_sets.append(open_set)
        open_set = []
    else:
        open_set.append(line)
row_sets.append(open_set)

col_sets = []
for row_set in row_sets:
    idx = 0
    col_set = []
    while idx < len(row_set[0]):
        col = ''
        for line in row_set:
            col += line[idx]
        col_set.append(to_bin(col))
        idx += 1
    col_sets.append(col_set)

for row_idx, row_set in enumerate(row_sets):
    new_row = []
    for value in row_set:
        new_row.append(to_bin(value))
    row_sets[row_idx] = new_row

print('row_sets', row_sets)
print('col_sets', col_sets)

# Part 1
pt1_value = 0

def search_rows_pt1(rows, debug = 0):
    # print('===================================== search_rows_pt1')
    pairs = []
    for idx, row in enumerate(rows):
        if idx > 0:
            if row == rows[idx - 1]:
                pairs.append(idx)
    # print(debug, pairs)
    for pair in pairs:
        backward_idx = pair - 1
        forward_idx = pair
        valid = True
        # print('Initialising backward_idx, forward_idx', backward_idx, forward_idx)
        while backward_idx >= 0 and forward_idx < len(rows):
            # print('checking', backward_idx, forward_idx)
            if rows[backward_idx] != rows[forward_idx]:
                # print('match failed :(')
                valid = False
            backward_idx -= 1
            forward_idx += 1
        if valid:
            # print('-> pair valid', pair)
            return pair
    return 'no match'

# print('===>', search_rows_pt1([101100110, 1011010, 110000001, 110000001, 1011010, 1100110, 101011010]))
# print('===>', search_rows_pt1([1011001, 11000, 1100111, 1000010, 100101, 100101, 1000010, 1100111, 11000]))

row_match_list_pt1 = {}
col_match_list_pt1 = {}

for idx, row in enumerate(row_sets):
    res = search_rows_pt1(row, 'pt1 - row ' + str(idx))
    row_match_list_pt1[idx] = None
    if res != 'no match':
        row_match_list_pt1[idx] = res
        pt1_value += res * 100

for idx, col in enumerate(col_sets):
    res = search_rows_pt1(col, 'pt1 - col ' + str(idx))
    col_match_list_pt1[idx] = None
    if res != 'no match':
        col_match_list_pt1[idx] = res
        pt1_value += res

# Part 2
print('================================ PT2')
pt2_value = 0


def difference(string1: str, string2: str):
    differences = 0
    for idx, char in enumerate(list(string1)):
        if idx >= len(string2) or char != string2[idx]:
            differences += 1
    return differences


def search_rows_pt2(rows, pt1_idx = None, debug = 0):
    print('===================================== search_rows')
    print('pt1_list (to exclude)', pt1_idx)
    pairs = []
    pairs_with_smudge_removed = {}
    for idx, row in enumerate(rows):
        cleaned_smudge = False
        if idx > 0:
            diff = difference(row, rows[idx - 1])
            if row == rows[idx - 1]:
                pairs.append(idx)
            elif diff == 1 and not cleaned_smudge:
                pairs.append(idx)
                cleaned_smudge = True

    print('Pairs generated', debug, pairs)
    for pair in pairs:
        backward_idx = pair - 1
        forward_idx = pair
        valid = True
        cleaned_smudge = True if pair in pairs_with_smudge_removed else False
        print('Initialising backward_idx, forward_idx', backward_idx, forward_idx)
        while backward_idx >= 0 and forward_idx < len(rows):
            print('checking', backward_idx, forward_idx, 'values ', rows[backward_idx], rows[forward_idx])
            if rows[backward_idx] != rows[forward_idx]:
                diff = difference(str(rows[backward_idx]), str(rows[forward_idx]))
                print('Match failed for ', rows[backward_idx], rows[forward_idx],  'diff is', diff)
                if diff == 1 and not cleaned_smudge:
                    print('! Match is considered a smudge, fixing...')
                    cleaned_smudge = True
                else:
                    valid = False
            backward_idx -= 1
            forward_idx += 1
        if valid and pair != pt1_idx:
            print('-> pair valid', pair)
            return pair
    return 0


for idx, row in enumerate(row_sets):
    res = search_rows_pt2(row, row_match_list_pt1[idx], 'pt2 - row ' + str(idx))
    print('*** row idx ', idx, 'has returned ', res)
    if res:
        pt2_value += res * 100

for idx, col in enumerate(col_sets):
    res = search_rows_pt2(col, col_match_list_pt1[idx], 'pt2 - col ' + str(idx))
    print('*** col idx ', idx, 'has returned ', res)
    if res:
        pt2_value += res

print('Part 1 Total: ', pt1_value)
print('Part 2 Total: ', pt2_value)
