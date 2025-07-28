#!/usr/bin/env python3

import sys
import argparse

def parse_input(filename):
    """Parse input file into list of (test_value, numbers) tuples"""
    equations = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            test_value_str, numbers_str = line.split(': ')
            test_value = int(test_value_str)
            numbers = [int(x) for x in numbers_str.split()]
            equations.append((test_value, numbers))
    return equations

def can_be_solved_recursive(target, current, remaining_numbers):
    """Recursively check if target can be reached with remaining numbers"""
    # Base case: no more numbers to process
    if not remaining_numbers:
        return current == target
    
    # Early termination: if current result already exceeds target, stop
    # (since we only have + and * operations, result can only grow)
    if current > target:
        return False
    
    next_num = remaining_numbers[0]
    rest = remaining_numbers[1:]
    
    # Try addition
    if can_be_solved_recursive(target, current + next_num, rest):
        return True
    
    # Try multiplication
    if can_be_solved_recursive(target, current * next_num, rest):
        return True
    
    return False

def can_be_solved(test_value, numbers):
    """Check if equation can be made true with any combination of operators"""
    if len(numbers) == 1:
        return test_value == numbers[0]
    
    # Start recursion with first number as current result
    return can_be_solved_recursive(test_value, numbers[0], numbers[1:])

def solve_part1(filename, debug=False):
    """Main function to solve part 1"""
    equations = parse_input(filename)
    
    if debug:
        print(f"Parsed {len(equations)} equations")
    
    total_calibration_result = 0
    valid_count = 0
    
    for test_value, numbers in equations:
        if can_be_solved(test_value, numbers):
            total_calibration_result += test_value
            valid_count += 1
            if debug:
                print(f"Valid: {test_value}: {' '.join(map(str, numbers))}")
        elif debug:
            print(f"Invalid: {test_value}: {' '.join(map(str, numbers))}")
    
    if debug:
        print(f"Found {valid_count} valid equations out of {len(equations)}")
    
    return total_calibration_result

def main():
    parser = argparse.ArgumentParser(description='Day 7: Bridge Repair - Part 1')
    parser.add_argument('--test', action='store_true', help='Run on example.txt instead of input.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    debug = args.debug or args.test  # Enable debug by default when testing
    
    result = solve_part1(filename, debug)
    print(f"Total calibration result: {result}")

if __name__ == "__main__":
    main()