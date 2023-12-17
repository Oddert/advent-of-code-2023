import sys
import re

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from utils.read_input import read_input, read_input_raw
from utils.maths import lowest_common_multiple

# raw_text = read_input_raw('./8/example2.txt')
# text = read_input('./8/example2.txt')
# raw_text = read_input_raw('./8/example1.txt')
# text = read_input('./8/example1.txt')
raw_text = read_input_raw('./8/input.txt')
text = read_input('./8/input.txt')

# Part 1
pt1_value = 0
instruction_index_map = {
    'L': 0,
    'R': 1,
}
instructions = [instruction_index_map[x] for x in list(text[0])]
instructions_len = len(instructions) - 1
directions = text[2:]

quagmire = {}
print(text[0])
print(instructions)

your_preferred_maps_service = {}
for direction in directions:
    components = re.findall('[0-9a-z]+', direction, re.I)
    print(components)
    your_preferred_maps_service[components[0]] = components[1:]
    if components[0] == components[1] == components[2]:
        quagmire[components[0]] = True

print(your_preferred_maps_service)

pt1_value = 0
pt1_instruction = 0
pt1_current = 'AAA'
found = False
while not found and pt1_value < 1000000000:
    print('================', pt1_value, pt1_current)
    if pt1_instruction > instructions_len:
        pt1_instruction = 0
    this_direction = instructions[pt1_instruction]
    pt1_next = your_preferred_maps_service[pt1_current][this_direction]
    pt1_value += 1
    pt1_instruction += 1
    if pt1_next == 'ZZZ':
        found = True
        break
    if pt1_next in quagmire:
        print(f'Value of {pt1_next} encountered. Infinite loop aborted.')
        break
    pt1_current = pt1_next

# Part 2
print('================================ PT2')
pt2_value = ''

pt2_ghost_maps = {}
# Yes it is pronounced "zed", if you are American, complaints may be made by contacting https://adventofcode.com/2023/support
pt2_zed_maps = {}
zeds = []

ghosts = re.findall('[A-Z]+A', raw_text)
print(ghosts)
print(1)
for ghost in ghosts:
    print('checking ghost', ghost)
    pt2_idx = 0
    pt2_instruction = 0
    pt2_current = ghost
    found = False
    ghost_path = []
    while not found:
        if pt2_instruction > instructions_len:
            pt2_instruction = 0
        this_direction = instructions[pt2_instruction]
        pt2_next = your_preferred_maps_service[pt2_current][this_direction]
        print('pt2_next, idx', pt2_next, pt2_idx)
        pt2_current = pt2_next
        ghost_path.append(pt2_current)
        match = re.match('[A-Z]+Z', pt2_current)
        if pt2_current == ghost or match:
            zeds.append(match.string)
            found = True
            break
        pt2_instruction += 1
        pt2_idx += 1
    pt2_ghost_maps[ghost] = [ghost, pt2_current, len(ghost_path)]

for zed in zeds:
    pt2_idx = 0
    pt2_instruction = 0
    pt2_current = zed
    found = False
    zed_path = []
    while not found:
        if pt2_instruction > instructions_len:
            pt2_instruction = 0
        this_direction = instructions[pt2_instruction]
        pt2_next = your_preferred_maps_service[pt2_current][this_direction]
        print('pt2_next, idx', pt2_next, pt2_idx)
        pt2_current = pt2_next
        zed_path.append(pt2_current)
        if pt2_current == ghost or re.match('[A-Z]+Z', pt2_current):
            found = True
            break
        pt2_instruction += 1
        pt2_idx += 1
    pt2_zed_maps[zed] = [zed, pt2_current, len(zed_path)]


print(ghosts)
print(pt2_zed_maps)
print([pt2_zed_maps[x][2] for x in pt2_zed_maps])
pt2_value = lowest_common_multiple(*[pt2_zed_maps[x][2] for x in pt2_zed_maps])

print('Part 1 Total: ', pt1_value)
print('Part 2 Total: ', pt2_value)
