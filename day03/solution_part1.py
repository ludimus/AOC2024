#!/usr/bin/env python3

import re
import argparse

def parse_input(filename):
    with open(filename, 'r') as f:
        return f.read()

def find_valid_mul_instructions(memory):
    # Pattern: mul(1-3 digits, 1-3 digits)
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    matches = re.findall(pattern, memory)
    return matches

def calculate_total(instructions):
    total = 0
    for x_str, y_str in instructions:
        x = int(x_str)
        y = int(y_str)
        product = x * y
        total += product
    return total

def main():
    parser = argparse.ArgumentParser(description='Day 3 Part 1: Sum valid mul instructions from corrupted memory')
    parser.add_argument('--test', action='store_true', help='Run with example.txt instead of input.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    
    if args.debug or args.test:
        print(f"Reading from {filename}")
    
    memory = parse_input(filename)
    
    if args.debug or args.test:
        print(f"Memory length: {len(memory)} characters")
        print(f"Memory content: {memory}")
    
    instructions = find_valid_mul_instructions(memory)
    
    if args.debug or args.test:
        print(f"\nFound {len(instructions)} valid mul instructions:")
        total = 0
        for i, (x_str, y_str) in enumerate(instructions):
            x, y = int(x_str), int(y_str)
            product = x * y
            total += product
            print(f"  {i+1}: mul({x},{y}) = {product}")
        print(f"\nTotal sum: {total}")
    else:
        result = calculate_total(instructions)
        print(result)

if __name__ == "__main__":
    main()