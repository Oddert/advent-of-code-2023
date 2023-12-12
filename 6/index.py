import sys
import re
import os

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from utils.read_input import read_input

text = read_input('./6/input.txt')

times = re.findall('[0-9]+', text[0])
distances = re.findall('[0-9]+', text[1])
print(times, distances)

# Part 1
pt1_value = 0

def part1(times_list, distance_list):
    possibilities = []

    idx = 0
    for time in times_list:
        possible_moves = 0
        charge_time = 0
        while charge_time < int(time):
            distance = (int(time) - charge_time) * charge_time
            if distance > int(distance_list[idx]):
                possible_moves += 1
            charge_time += 1
        idx += 1
        if possible_moves > 0:
            possibilities.append(possible_moves)

    return possibilities

part1_possibilities = part1(times, distances)

print(part1_possibilities)
if len(part1_possibilities) > 0:
    pt1_value = 1
    for value in part1_possibilities:
        pt1_value *= value

# Part 2
pt2_time = ''
pt2_distance = ''
for pt2_index in range(len(times)):
    pt2_time += times[pt2_index]
    pt2_distance += distances[pt2_index]

print(pt2_time, pt2_distance)

[pt2_value] = part1([pt2_time], [pt2_distance])

print('Part 1 Total: ', pt1_value)
print('Part 2 Total: ', pt2_value)
