import sys
import re
import os

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from config import project_dir

from utils.read_input import read_input
from utils.string_utils import reverse_string

text = read_input('./2/input.txt')

print(text)

# Part 1
rules = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

pt1_total = 0

for game in text:
    game = game[:-1]
    title, draws_str = game.split(': ')
    game_num = int(title[5:])
    print(game_num)
    draws_list = draws_str.split('; ')
    valid = True
    for draw in draws_list:
        print('draw', draw)
        colours = draw.split(', ')
        for colour in colours:
            num, colour_name = colour.split(' ')
            num = int(num)
            if num > rules[colour_name]:
                valid = False
    if valid:
        pt1_total += game_num

# Part 2
pt2_total = 0

for game in text:
    game = game[:-1]
    max_draw_values = {
        'red': 0,
        'green': 0,
        'blue': 0,
    }

    title, draws_str = game.split(': ')
    game_num = int(title[5:])
    print(game_num)
    draws_list = draws_str.split('; ')
    valid = True
    for draw in draws_list:
        print('draw', draw)
        colours = draw.split(', ')
        for colour in colours:
            num, colour_name = colour.split(' ')
            num = int(num)
            if num > max_draw_values[colour_name]:
                max_draw_values[colour_name] = num
    print(max_draw_values)
    pwr = max_draw_values['red'] * max_draw_values['green'] * max_draw_values['blue']
    pt2_total += pwr
                
print('Part 1 Total: ', pt1_total)
print('Part 2 Total: ', pt2_total)
