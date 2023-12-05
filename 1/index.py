import sys
import re
import os

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from config import project_dir

from utils.read_input import read_input
from utils.string_utils import reverse_string

text = read_input('./1/input.txt')

def get_pairing(num_list):
	if len(num_list) == 0:
		return 0
	if len(num_list) == 1:
		return int(num_list[0])
	return int(str(num_list[0]) + str(num_list[-1]))

# Part 1
part1_coords = []

for line in text:
	print(line)
	nums = re.findall('[0-9]', line)
	print(nums)
	part1_coords.append(get_pairing(nums))

part1_total = 0

for coord in part1_coords:
	part1_total += coord

# Part 2
matches = {
	'one': 1,
	'two': 2,
	'three': 3,
	'four': 4,
	'five': 5,
	'six': 6,
	'seven': 7,
	'eight': 8,
	'nine': 9,
}

part2_coords = []
part2_total = 0

def parse_search(matcher, line, reverse_match=False):
	print('Matching ', matcher, line)
	matched_digits = re.findall(matcher, line)
	print('Matched Digits: ', matched_digits)
	parsed_digits = []
	for digit in matched_digits:
		if reverse_match:
			digit = reverse_string(digit)
		if digit in matches:
			parsed_digits.append(matches[digit])
		else:
			parsed_digits.append(digit)
	print('Parsed Digits: ', parsed_digits)
	return parsed_digits

for line in text:
	if line == '':
		continue
	print('# line', line)
	forward_matches = parse_search('one|two|three|four|five|six|seven|eight|nine|[0-9]', line)
	reversed_matches = parse_search(f"{reverse_string('one|two|three|four|five|six|seven|eight|nine')}|[0-9]", reverse_string(line), True)

	part2_coords.append(get_pairing([forward_matches[0], reversed_matches[0]]))

print(part2_coords)
for coord in part2_coords:
	part2_total += coord

print('Part 1 Total: ', part1_total)
print('Part 2 Total: ', part2_total)
