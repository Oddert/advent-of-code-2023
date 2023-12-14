import sys
import re
import os

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from utils.read_input import read_input

text = read_input('./7/input.txt')

print(text)

# Reddit User submitted examples
# User | Part1 | Part2
# AdmirableUse2453 | 2237 | 2297 - https://www.reddit.com/r/adventofcode/comments/18cq5j3/comment/kcd2xnr/
# Sostratus | 1343 | ? - https://www.reddit.com/r/adventofcode/comments/18cq5j3/2023_day_7_part_1_two_hints_for_anyone_stuck/
# Cue_23 | 292 | ? - https://www.reddit.com/r/adventofcode/comments/18cq5j3/comment/kcd2xnr/

# Part 1
pt1_value = 0

card_hierarchy = {
    'A': 12,
    'K': 11,
    'Q': 10,
    'J': 9,
    'T': 8,
    '9': 7,
    '8': 6,
    '7': 5,
    '6': 4,
    '5': 3,
    '4': 2,
    '3': 1,
    '2': 0,
}

def quicksort(items, comparator):
    if len(items) <= 1:
        return items
    pivot = items[0]
    left_side = [item for item in items[1:] if comparator(item, pivot, True)]
    right_side = [item for item in items[1:] if comparator(pivot, item)]
    return [*quicksort(left_side, comparator), pivot, *quicksort(right_side, comparator)]

def rank_hand(hand: str):
    '''
    7 - Five of a kind: set of length 1
    6 - Four of a kind: set of length 2
    5 - Full house: set of length 2, no char count > 3
    4 - Three of a kind: set of length 3
    3 - Two pair: set of length 3, no char count > 2
    2 - One pair: set of length 4
    1 - High card: set of length 5
    '''
    hand_set = {}
    for char in list(hand):
        if not char in hand_set:
            hand_set[char] = 1
        else:
            hand_set[char] += 1

    match len(hand_set):
        case 5:
            return 1
        case 4:
            return 2
        case 3:
            for char in hand_set:
                if hand_set[char] == 3:
                    return 4
            return 3
        case 2:
            for char in hand_set:
                if hand_set[char] == 4:
                    return 6
            return 5
        case _:
            return 7

def linear_comparison(item1: str, item2: str, idx: int = 0):
    if idx >= len(item1):
        return 'same'
    if card_hierarchy[item1[idx]] == card_hierarchy[item2[idx]]:
        return linear_comparison(item1, item2, idx + 1)
    return card_hierarchy[item1[idx]] <= card_hierarchy[item2[idx]]

def linear_comparison2(item1: str, item2: str, idx: int = 0):
    # print('doing linear comparison round ', idx, item1, item2)
    if idx == len(item1) - 1:
        # print('...end of index')
        return 'same'
    if card_hierarchy[item1[idx]] == card_hierarchy[item2[idx]]:
        # print('hierarchies are the same..')
        return linear_comparison2(item1, item2, idx + 1)
    # print(card_hierarchy[item1[idx]], card_hierarchy[item2[idx]])
    # print(card_hierarchy[item1[idx]] < card_hierarchy[item2[idx]])
    return card_hierarchy[item1[idx]] < card_hierarchy[item2[idx]]

def comparator(item1, item2, left_side=False):
    # ranking into categories
    rank1 = rank_hand(item1)
    rank2 = rank_hand(item2)
    if rank1 == rank2:
        comp = linear_comparison(item1, item2)
        if comp == 'same':
            return left_side
        return comp
    return rank1 < rank2

class Node:
    def __init__(self, row) -> None:
        split = row.split(' ')
        split[0] = split[0][::-1]
        self.left = None
        self.right = None
        self.rank = rank_hand(split[0])
        self.hand = split[0]
        self.bid = split[1]

    def add_child(self, child_node):
        if child_node.rank < self.rank:
            self.add_child_left(child_node)
        elif child_node.rank > self.rank:
            self.add_child_right(child_node)
        else:
            child_larger = linear_comparison2(child_node.hand, self.hand)
            if child_larger:
                self.add_child_left(child_node)
            else:
                self.add_child_right(child_node)

    def add_child_left(self, child_node):
        if self.left:
            self.left.add_child(child_node)
        else:
            self.left = child_node

    def add_child_right(self, child_node):
        if self.right:
            self.right.add_child(child_node)
        else:
            self.right = child_node

    def to_array(self):
        arr = []
        if self.left:
            arr = [*arr, *self.left.to_array()]
        arr.append([self.hand, self.bid])
        if self.right:
            arr = [*arr, *self.right.to_array()]
        return arr

    def to_json(self) -> str:
        return {
            'left': self.left.to_json() if self.left else None,
            'right': self.right.to_json() if self.right else None,
            'rank': self.rank,
            'hand': self.hand,
            'bid': self.bid,
        }

bids = {}
hands = []

for line in text:
    split = line.split(' ')
    hands.append(split[0])
    bids[split[0]] = int(split[1])

print(len(hands))
sorted_hands = quicksort(hands, comparator)
# print(sorted_hands)
print(len(sorted_hands))

pt1_idx = 1
for hand in sorted_hands:
    # print(hand)
    score = pt1_idx * bids[hand]
    pt1_value += score
    # print(hand, bids[hand], score, pt1_idx)
    # print(f'hand: {hand}. multiplying {pt1_idx} with {bids[hand]} to give {score}. adding to total to give {pt1_value}')
    pt1_idx += 1

test = {
    '3JKKQ': 5,
}

for test_item in test:
    result = rank_hand(test_item)
    print(test[test_item], result)

# print(linear_comparison('TTT98', 'T55J5'))
print(quicksort([
    '32T3K',
    'T65J5',
    'T55J5',
    'KK677',
    'KTJJT',
    'QQQJA',
], comparator))

sectioned_arrays = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
}

for hand in sorted_hands:
    rank = rank_hand(hand)
    sectioned_arrays[rank].append(hand)

for arr in sectioned_arrays:
    print('==================================', arr)
    print(sectioned_arrays[arr])


root_node = Node(text[0])
for hand in text[1:]:
    root_node.add_child(Node(hand))
    
alt_list = root_node.to_array()

alt_total = 0
j = 0
print(len(alt_list), len(sorted_hands))
for alt_hand in alt_list:
    alt_total += int(alt_hand[1]) * (j + 1)
    # print(alt_hand[0], sorted_hands[j], alt_hand[0] == sorted_hands[j])
    j += 1

# Part 2
pt2_value = 0

card_hierarchy_pt2 = {
    'A': 12,
    'K': 11,
    'Q': 10,
    'T': 9,
    '9': 8,
    '8': 7,
    '7': 6,
    '6': 5,
    '5': 4,
    '4': 3,
    '3': 2,
    '2': 1,
    'J': 0,
}


def convert_hand_pt2(hand: str):
    hand_no_jay = hand.replace('J', '')
    initial_set = {}
    if hand_no_jay == '':
        return hand

    for char in list(hand_no_jay):
        if not char in initial_set:
            initial_set[char] = 1
        else:
            initial_set[char] += 1

    largest = [hand_no_jay[0], 1]

    for char, count in initial_set.items():
        if count > largest[1]:
            largest = [char, count]
    return hand.replace('J', largest[0])


def linear_comparison_pt2(item1: str, item2: str, idx: int = 0):
    if item1 == '9A4JJ' or item2 == '9A4JJ':
        print(f'loop idx {idx}, {item1} {item2}')
    if idx >= len(item1):
        print('end of index...')
        return 'same'
    if item1 == '9A4JJ' or item2 == '9A4JJ':
        print(item1[idx], item2[idx], card_hierarchy_pt2[item1[idx]] == card_hierarchy_pt2[item2[idx]])
        print(card_hierarchy_pt2[item1[idx]], card_hierarchy_pt2[item2[idx]], card_hierarchy_pt2[item1[idx]] == card_hierarchy_pt2[item2[idx]])
    if card_hierarchy_pt2[item1[idx]] == card_hierarchy_pt2[item2[idx]]:
        if item1 == '9A4JJ' or item2 == '9A4JJ':
            print('items are the same, going to loop again...')
        return linear_comparison_pt2(item1, item2, idx + 1)
    if item1 == '9A4JJ' or item2 == '9A4JJ':
        print('final check', card_hierarchy_pt2[item1[idx]] <= card_hierarchy_pt2[item2[idx]])
    return card_hierarchy_pt2[item1[idx]] <= card_hierarchy_pt2[item2[idx]]

def comparator_pt2(item1, item2, left_side=False):
    # ranking into categories
    if item1 == '9A4JJ' or item2 == '9A4JJ':
        print(f'item 1 converted from {item1} to {convert_hand_pt2("" + item1)}')
        print(f'item 2 converted from {item2} to {convert_hand_pt2("" + item2)}')
    rank1 = rank_hand(convert_hand_pt2("" + item1))
    rank2 = rank_hand(convert_hand_pt2("" + item2))
    if rank1 == rank2:
        if item1 == '9A4JJ' or item2 == '9A4JJ':
            print('-----------------------------')
        comp = linear_comparison_pt2(item1, item2)
        if comp == 'same':
            return left_side
        return comp
    return rank1 < rank2

print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
sorted_hands_pt2 = quicksort(hands, comparator_pt2)
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

print(sorted_hands_pt2)
pt2_idx = 1
for hand in sorted_hands_pt2:
    # print(pt2_idx, hand, bids[hand], pt2_idx * bids[hand])
    print(hand)
    pt2_value += pt2_idx * bids[hand]
    pt2_idx += 1

print('Part 1 Total: ', pt1_value)
print('Part 2 Total: ', pt2_value)

print(convert_hand_pt2('9A4JJ'))