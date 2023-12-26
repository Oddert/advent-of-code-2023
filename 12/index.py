import sys
import re

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from utils.read_input import read_input, read_input_raw

raw_text = read_input_raw('./12/example.txt')
text = read_input('./12/example.txt')
# raw_text = read_input_raw('./12/input.txt')
# text = read_input('./12/input.txt')

# Part 1
pt1_value = 0

def recurse_string_options(preceding_string='', remaining_string=''):
    if len(remaining_string[1:]):
        arr = []
        if remaining_string[0] == '?':
            for option in recurse_string_options(preceding_string + '#', remaining_string[1:]):
                arr.append(option)
            for option in recurse_string_options(preceding_string + '.', remaining_string[1:]):
                arr.append(option)
        else:
            for option in recurse_string_options(preceding_string + remaining_string[0], remaining_string[1:]):
                arr.append(option)
        return arr
    else:
        if remaining_string[0] == '?':
            return [preceding_string + '#', preceding_string + '.']
        return [preceding_string + remaining_string]

pt1_permutations = recurse_string_options('', '???')
print(pt1_permutations)

def generate_valid_permutations(code_string: str, validation: str):
    validation_segments = ['#{' + x + '}' for x in validation.split(',')]
    print('validation_segments', validation_segments)
    valid_test = '^\.*'
    idx = 0
    for segment in validation_segments:
        valid_test += segment
        if idx < len(validation_segments) - 1:
            valid_test += '\.+'
        idx += 1
    valid_test += '\.*$'
    permutations = recurse_string_options('', code_string)
    total = 0
    for permutation in permutations:
        # print('-->', permutation, re.match(valid_test, permutation))
        if re.match(valid_test, permutation):
            total += 1
    return total

# for line in text:
#     code_string, validation = line.split(' ')
#     pt1_value += generate_valid_permutations(code_string, validation)

# Part 2
print('================================ PT2')
pt2_value = 0

for line in text:
    code_string, validation = line.split(' ')
    code_string_modified = ''
    validation_modified = ''
    for idx in range(5):
        code_string_modified += code_string
        validation_modified += validation
        if idx < 4:
            code_string_modified += '?'
            validation_modified += ','
    pt2_value += generate_valid_permutations(code_string_modified, validation_modified)

print('Part 1 Total: ', pt1_value)
print('Part 2 Total: ', pt2_value)
