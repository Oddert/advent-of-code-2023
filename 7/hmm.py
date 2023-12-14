""" 2023 aoc07 """

import functools

with open("7/input.txt", "r", encoding="utf-8") as f:
    input_list = f.read().splitlines()

with open('7/comp.txt') as c:
    comp = c.read().splitlines()

bids = {}
hands = []
for line in input_list:
    cards, bid = line.split()
    bid = int(bid)
    bids[cards] = bid
    hands.append(cards)

def compare(hand1, hand2):
    # print(hand1, hand2)
    for x in range(6):
        # print(values.index(hand1[x]), values.index(hand2[x]))
        if values.index(hand1[x]) < values.index(hand2[x]):
            return -1
        if values.index(hand1[x]) > values.index(hand2[x]):
            return 1
    return 0


ranks = []
fives = []
fours = []
full_house = []
threes = []
twos = []
pairs = []
highs = []
values = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

for hand in hands:
    if len(set(list(hand))) == 1:
        fives.append(hand)
    if len(set(list(hand))) == 2:
        if hand.count(hand[0]) == 1 or hand.count(hand[0]) == 4:
            fours.append(hand)
        else:
            full_house.append(hand)
    if len(set(list(hand))) == 3:
        if hand.count(hand[0]) == 3 or hand.count(hand[1]) == 3 or hand.count(hand[2]) == 3:
            threes.append(hand)
        else:
            twos.append(hand)
    if len(set(list(hand))) == 4:
        pairs.append(hand)
    if len(set(list(hand))) == 5:
        highs.append(hand)

fives = sorted(fives, key=functools.cmp_to_key(compare))
fours = sorted(fours, key=functools.cmp_to_key(compare))
full_house = sorted(full_house, key=functools.cmp_to_key(compare))
threes = sorted(threes, key=functools.cmp_to_key(compare))
twos = sorted(twos, key=functools.cmp_to_key(compare))
pairs = sorted(pairs, key=functools.cmp_to_key(compare))
highs = sorted(highs, key=functools.cmp_to_key(compare))

for hand in fives:
    ranks.append(hand)
for hand in fours:
    ranks.append(hand)
for hand in full_house:
    ranks.append(hand)
for hand in threes:
    ranks.append(hand)
for hand in twos:
    ranks.append(hand)
for hand in pairs:
    ranks.append(hand)
for hand in highs:
    ranks.append(hand)

i = 1
answer1 = 0
for hand in reversed(ranks):
    # print(hand, comp[i-1], hand == comp[i-1])
    answer1 += i * bids[hand]
    i += 1
# print(i, len(comp))

print("Answer 1:", answer1)

ranks = []
fives = []
fours = []
full_house = []
threes = []
twos = []
pairs = []
highs = []
values = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

for hand in hands:
    # print()
    # print(hand)
    if len(set(list(hand))) == 1:
        # print("Fives")
        fives.append(hand)
    if len(set(list(hand))) == 2:
        if "J" in hand:
            # print("Fives")
            fives.append(hand)
        elif hand.count(hand[0]) == 1 or hand.count(hand[0]) == 4:
            # print("Fours")
            fours.append(hand)
        else:
            # print("Full House")
            full_house.append(hand)
    if len(set(list(hand))) == 3:
        if hand.count(hand[0]) == 3 or hand.count(hand[1]) == 3 or hand.count(hand[2]) == 3:
            if "J" in hand:
                # print("Fours")
                fours.append(hand)
            else:
                # print("Threes")
                threes.append(hand)
        else:
            if "J" in hand:
                if hand.count("J") == 2:
                    # print("Fours")
                    fours.append(hand)
                else:
                    # print("Full House")
                    full_house.append(hand)
            else:
                # print("Twos")
                twos.append(hand)
    if len(set(list(hand))) == 4:
        if "J" in hand:
            # print("Threes")
            threes.append(hand)
        else:
            # print("Pairs")
            pairs.append(hand)
    if len(set(list(hand))) == 5:
        if "J" in hand:
            # print("Pairs")
            pairs.append(hand)
        else:
            # print("Highs")
            highs.append(hand)

fives = sorted(fives, key=functools.cmp_to_key(compare))
fours = sorted(fours, key=functools.cmp_to_key(compare))
full_house = sorted(full_house, key=functools.cmp_to_key(compare))
threes = sorted(threes, key=functools.cmp_to_key(compare))
twos = sorted(twos, key=functools.cmp_to_key(compare))
pairs = sorted(pairs, key=functools.cmp_to_key(compare))
highs = sorted(highs, key=functools.cmp_to_key(compare))

for hand in fives:
    ranks.append(hand)
for hand in fours:
    ranks.append(hand)
for hand in full_house:
    ranks.append(hand)
for hand in threes:
    ranks.append(hand)
for hand in twos:
    ranks.append(hand)
for hand in pairs:
    ranks.append(hand)
for hand in highs:
    ranks.append(hand)

i = 1
answer2 = 0
for hand in reversed(ranks):
    print(hand, comp[i-1], hand == comp[i-1])
    answer2 += i * bids[hand]
    i += 1
print(i, len(comp))

print("Answer 2:", answer2)
