#!/usr/bin/env python3

import re
import argparse

def parse_input(filename):
    with open(filename, 'r') as f:
        return f.read()

def process_instructions_with_conditionals(memory):
    # Pattern to match mul(X,Y), do(), or don't()
    pattern = r'(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\))'
    matches = re.finditer(pattern, memory)
    
    enabled = True  # mul instructions start enabled
    total = 0
    
    for match in matches:
        instruction = match.group(1)
        
        if instruction == "do()":
            enabled = True
        elif instruction == "don't()":
            enabled = False
        elif instruction.startswith("mul(") and enabled:
            # Extract the numbers from groups 2 and 3
            x = int(match.group(2))
            y = int(match.group(3))
            product = x * y
            total += product
    
    return total

def process_instructions_with_conditionals_debug(memory):
    # Pattern to match mul(X,Y), do(), or don't()
    pattern = r'(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\))'
    matches = re.finditer(pattern, memory)
    
    enabled = True  # mul instructions start enabled
    total = 0
    instructions_processed = []
    
    for match in matches:
        instruction = match.group(1)
        
        if instruction == "do()":
            enabled = True
            instructions_processed.append(f"do() -> enable mul instructions")
        elif instruction == "don't()":
            enabled = False
            instructions_processed.append(f"don't() -> disable mul instructions")
        elif instruction.startswith("mul("):
            # Extract the numbers from groups 2 and 3
            x = int(match.group(2))
            y = int(match.group(3))
            product = x * y
            
            if enabled:
                total += product
                instructions_processed.append(f"mul({x},{y}) -> enabled -> {product} (total: {total})")
            else:
                instructions_processed.append(f"mul({x},{y}) -> disabled -> skip")
    
    return total, instructions_processed

def main():
    parser = argparse.ArgumentParser(description='Day 3 Part 2: Sum enabled mul instructions with do/don\'t conditionals')
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
        
        # Need to update example.txt for part 2
        if args.test:
            # Use the part 2 example instead
            memory = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
            print(f"Using Part 2 example: {memory}")
        
        total, instructions = process_instructions_with_conditionals_debug(memory)
        
        print(f"\nProcessing instructions:")
        for i, instruction in enumerate(instructions, 1):
            print(f"  {i}: {instruction}")
        
        print(f"\nTotal sum of enabled multiplications: {total}")
    else:
        result = process_instructions_with_conditionals(memory)
        print(result)

if __name__ == "__main__":
    main()