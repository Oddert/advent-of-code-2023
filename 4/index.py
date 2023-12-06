import sys
import re
import os

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from utils.read_input import read_input

text = read_input('./4/input.txt')

print(text)

def prep_cards(card):
    title = re.match('Card(\ )+[0-9]+:(\ )+', card)
    # print(title)
    stripped_line = card[title.end():]
    # print(stripped_line)
    split_line = stripped_line.split(' | ')
    winning_numbers = re.findall('([0-9]+)', split_line[0])
    card_numbers = re.findall('([0-9]+)', split_line[1])
    # print('win', winning_numbers, 'card', card_numbers)
    return [winning_numbers, card_numbers, card[title.start() : title.end()]]

# Part 1
pt1_total = 0
for card in text:
    print('==============================')
    match_count = 0
    print(card)
    [winning_numbers, card_numbers, *args] = prep_cards(card)
    for winning_number in winning_numbers:
        if winning_number in card_numbers:
            if match_count == 0:
                match_count = 1
            else:
                match_count *= 2
    pt1_total += match_count

# Part 2
pt2_total = 0

print('~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~')
initial_index = 0
for line in text:
    def recurse_cards(card, idx, trace = []):
        # print(trace, '--------------------------')
        print('recurse depth', idx, card)
        [winning_numbers, card_numbers, title] = prep_cards(card)
        num_matches = 1
        local_idx = idx + 1
        for winning_number in winning_numbers:
            if winning_number in card_numbers and local_idx <= len(text) - 1:
                # print('match found for index', local_idx, text[local_idx], 'won by', card)
                num_matches += recurse_cards(text[local_idx], local_idx, [*trace, title])
                local_idx += 1
        # print('Returning value ', card, 'num matches: ', num_matches, 'trace: ', trace)
        return num_matches
    pt2_total += recurse_cards(line, initial_index)
    initial_index += 1

print('Part 1 Total: ', pt1_total)
print('Part 2 Total: ', pt2_total)
