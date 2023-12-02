import sys
import re

sys.path.append(r'D:\Users\robyn\code\advent-of-code-2023')

from utils.read_input import read_input

text = read_input('./1/input.txt')

print(text)

def get_pairing(num_list):
	if len(num_list) == 0:
		return 0
	if len(num_list) == 1:
		return int(num_list[0])
	return int(str(num_list[0]) + str(num_list[-1]))

# Part 1
part1_coords = []

for line in text:
	line = line[:-1]
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

for line in text:
	if line == '':
		continue
	line = line[:-1]
	print('line', line)
	str_digits = re.findall('one|two|three|four|five|six|seven|eight|nine|[0-9]', line)
	print('str_digits', str_digits)
	parsed_digits = []
	for str_digit in str_digits:
		if str_digit in matches:
			parsed_digits.append(matches[str_digit])
		else:
			parsed_digits.append(str_digit)
	print('parsed_digits', parsed_digits)
	print('paring', get_pairing(parsed_digits))
	part2_coords.append(get_pairing(parsed_digits))

print(part2_coords)
for coord in part2_coords:
	part2_total += coord

print('Part 1 Total: ', part1_total)
print('Part 2 Total: ', part2_total)


print(re.findall('(?<=one|two|three|four|five|six|seven|eight|nine|[0-9])', 'one23twone'))