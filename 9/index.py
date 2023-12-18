import sys
import re

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from utils.read_input import read_input, read_input_raw
from utils.maths import lowest_common_multiple

# raw_text = read_input_raw('./9/example.txt')
# text = read_input('./9/example.txt')
raw_text = read_input_raw('./9/input.txt')
text = read_input('./9/input.txt')

def is_all_zeros(row):
    for item in row:
        if item != 0:
            return False
    return True

def generate_next_line(row):
    idx = 0
    line = []
    while idx < len(row) - 1:
        first = row[idx]
        second = row[idx + 1]
        line.append(second - first)
        idx += 1
    return line

# Part 1
pt1_value = 0

for line in text:
    oasis = [[int(x) for x in line.split(' ')]]
    print(oasis[-1], is_all_zeros(oasis[-1]))
    while not is_all_zeros(oasis[-1]):
        last_line = oasis[-1]
        print('Processing raw line: ', last_line)
        next_line = generate_next_line(last_line)
        print(next_line)
        oasis.append(next_line)
    bubble_idx = len(oasis) - 1
    oasis[-1].append(0)
    while bubble_idx > 0:
        bottom_int = oasis[bubble_idx][-1]
        left_int = oasis[bubble_idx - 1][-1]
        oasis[bubble_idx - 1].append(bottom_int + left_int)
        bubble_idx -= 1
    pt1_value += oasis[0][-1]


# Part 2
print('================================ PT2')
pt2_value = 0

for line in text:
    oasis = [[int(x) for x in line.split(' ')]]
    print(oasis[-1], is_all_zeros(oasis[-1]))
    while not is_all_zeros(oasis[-1]):
        last_line = oasis[-1]   
        print('Processing raw line: ', last_line)
        next_line = generate_next_line(last_line)
        print(next_line)
        oasis.append(next_line)
    print('=====================')
    for t in oasis:
        print(t)
    print('---------------------')
    bubble_idx = len(oasis) - 1
    oasis[-1].insert(0, 0)
    while bubble_idx > 0:
        bottom_int = oasis[bubble_idx][0]
        right = oasis[bubble_idx - 1][0]
        oasis[bubble_idx - 1].insert(0, right - bottom_int)
        bubble_idx -= 1
    print('=====================')
    for t in oasis:
        print(t)
    print('---------------------')
    pt2_value += oasis[0][0]

print('Part 1 Total: ', pt1_value)
print('Part 2 Total: ', pt2_value)
