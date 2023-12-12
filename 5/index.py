import sys
import re
import os

# Needed to import from folder directory. Replace with your own project.
# Probably a better way to do this that doesn't involve revealing my own file structure but whatever, you're not my mum. 
sys.path.append(r'C:\dev\advent-of-code-2023')

from utils.read_input import read_input

text = read_input('./5/input.txt')

seeds = re.findall('[0-9]+', text[0][7:])
print(seeds)

class Range:
    def __init__(self, _from_start, _to_start, _length) -> None:
        self.from_start = int(_from_start)
        self.from_end = int(_from_start) + int(_length) - 1
        self.to_start = int(_to_start)
        self.to_end = int(_to_start) + int(_length) - 1
        self.length = int(_length)
    
    def is_value_in_start_range(self, value, show=True):
        if show:
            print('value start range check ', str(self), value, value >= self.from_start, value <= self.from_end, value >= self.from_start and value <= self.from_end)
        return value >= self.from_start and value <= self.from_end

    def is_value_in_end_range(self, value, show=True):
        if show:
            print('value end range check ', str(self), value, value >= self.to_start, value <= self.to_end, value >= self.to_start and value <= self.to_end)
        return value >= self.to_start and value <= self.to_end
    
    def convert_forward(self, value):
        return self.to_start + (value - self.from_start)

    def convert_backward(self, value):
        return self.from_start + (value - self.to_start)
    
    def to_json(self):
        return {
            'from_start': self.from_start,
            'from_end': self.from_end,
            'to_start': self.to_start,
            'length': self.length,
        }
    
    def __repr__(self) -> str:
        return f'<Range from_start={self.from_start} from_end={self.from_end} len={self.length} to_start={self.to_start} to_end={self.to_end}>'

class Converter:
    def __init__(self, _name: str = '', _next = None, _ranges = []) -> None:
        self.name = _name
        self.next = _next
        self.ranges = _ranges

    def add_range(self, range_list: str):
        print('Adding Range on ', self.name, range_list)
        split = re.findall('[0-9]+', range_list)
        to_start = split[0]
        from_start = split[1]
        length = split[2]
        created_range = Range(from_start, to_start, length)
        self.ranges = [*self.ranges, created_range]

    def add_next(self, lines: list):
        print(f'Adding a new Converter "{lines[0][:-1]}"')
        self.name = lines[0][:-1]
        idx = 1
        found_end = False
        while idx < len(lines) and not found_end:
            if lines[idx] == '':
                found_end = True
            else:
                self.add_range(lines[idx])
            idx += 1
        if idx < len(lines):
            created_converter = Converter()
            created_converter.add_next(lines[idx:])
            self.next = created_converter

    def process_number(self, number):
        print(self.name)
        print('Processing', number)
        found = False
        for range_child in self.ranges:
            if range_child.is_value_in_start_range(number):
                number = range_child.convert_forward(number)
                found = True
                print('number converted forward to', number)
        if not found:
            for range_child in self.ranges:
                if range_child.is_value_in_end_range(number):
                    number = range_child.convert_backward(number)
                    print('number converted backwards to', number)
        if self.next:
            return self.next.process_number(number)
        return number
    
    def to_json(self):
        return {
            'name': self.name,
            'next': self.next.to_json() if self.next else None,
            'ranges': self.ranges,
            'range_len': len(self.ranges),
        }

# Part 1
pt1_value = 0
root_converter = Converter()
root_converter.add_next(text[2:])
print(root_converter.to_json())

seed_locations = []

for seed in seeds:
    print('===================')
    seed_locations.append(int(root_converter.process_number(int(seed))))

pt1_value = min(*seed_locations)

print(seed_locations)

# Part 2
pt2_value = 0


print('Part 1 Total: ', pt1_value)
print('Part 2 Total: ', pt2_value)
