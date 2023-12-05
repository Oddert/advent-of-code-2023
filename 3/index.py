import sys
import re
import os

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from utils.read_input import read_input

text = read_input('./3/example.txt')

print(text)

# Part 1
pt1_total = 0

def search_idx(lines, row_idx, char_idx):
    valid = False
    def search_single_line(single_line, start_idx):
        print('search single line ', single_line, start_idx)
        def search_idx(line, idx):
            if idx < 0 or idx > len(line) - 1:
                return False
            print('searching index ', idx, line[idx])
            if not re.match('[0-9]|\.', line[idx]):
                print('its a match!!')
                return True
            return False
        if (
            search_idx(single_line, start_idx - 1) or
            search_idx(single_line, start_idx) or
            search_idx(single_line, start_idx + 1)
        ):
            return True
        return False

    if row_idx >= 1:
        print('! searching above (', row_idx - 1, ')')
        if search_single_line(lines[row_idx - 1], char_idx):
            valid = True
    if search_single_line(lines[row_idx], char_idx):
        valid = True
    if row_idx < len(lines) - 1:
        print('! searching below (', row_idx + 1, ')')
        if search_single_line(lines[row_idx + 1], char_idx):
            valid = True
    return valid

part_numbers = []

pt1_idx = 0
for line in text:
    print('==============================')
    print(line)
    matches = re.finditer('[0-9]+', line)

    for match in matches:
        print('start', match.start(), 'end', match.end())
        beginning = search_idx(text, pt1_idx, match.start())
        end = search_idx(text, pt1_idx, match.end() - 1)
        print(beginning, end)
        if beginning or end:
            part_numbers.append(line[match.start() : match.end()])
    pt1_idx += 1
print(part_numbers)

for part_number in part_numbers:
    pt1_total += int(part_number)

print('~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~')
# Part 2
pt2_total = 0

register = {}

def search_idx(lines, row_idx, char_idx):
    valid = False
    def search_single_line(single_line, start_idx):
        # print('search single line ', single_line, start_idx)
        def search_char(line, idx):
            if idx < 0 or idx > len(line) - 1:
                return False
            # print('searching index ', idx, line[idx])
            if re.match('\*', line[idx]):
                print('its a match!!')
                return idx
            return False
        # Loop results and return char
        s1 = search_char(single_line, start_idx - 1)
        s2 = search_char(single_line, start_idx)
        s3 = search_char(single_line, start_idx + 1)
        for search_result in [s1, s2, s3]:
            if search_result:
                print('==========>>>>>>>>>>', search_result)
                register[(start_idx, search_result)] = []
                register[(start_idx, search_result)].push()
                continue
        if s1 or s2 or s3:
            return True
        return False

    if row_idx >= 1:
        print('! searching above (idx', row_idx - 1, ')')
        if search_single_line(lines[row_idx - 1], char_idx):
            valid = True
        print('! searching (idx', row_idx, ')')
    if search_single_line(lines[row_idx], char_idx):
        valid = True
    if row_idx < len(lines) - 1:
        print('! searching below (idx', row_idx + 1, ')')
        if search_single_line(lines[row_idx + 1], char_idx):
            valid = True
    return valid

part_numbers = []

pt2_idx = 0
for line in text:
    print('==============================')
    print(line)
    matches = re.finditer('[0-9]+', line)

    for match in matches:
        print('start', match.start(), 'end', match.end())
        beginning = search_idx(text, pt2_idx, match.start())
        end = search_idx(text, pt2_idx, match.end() - 1)
        print(beginning, end)
        if beginning or end:
            part_numbers.append(line[match.start() : match.end()])
    pt2_idx += 1
print(part_numbers)

for part_number in part_numbers:
    pt2_total += int(part_number)


print('Part 1 Total: ', pt1_total)
print('Part 2 Total: ', pt2_total)
