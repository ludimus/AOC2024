#!/usr/bin/env python3
import sys

def parse_input(filename):
    """Parse the initial stone arrangement from input file."""
    with open(filename, 'r') as f:
        line = f.read().strip()
        return [int(x) for x in line.split()]

def count_digits(number):
    """Count the number of digits in a number."""
    return len(str(number))

def split_number(number):
    """Split a number into left and right halves (no leading zeros)."""
    s = str(number)
    mid = len(s) // 2
    left = int(s[:mid])
    right = int(s[mid:])  # int() automatically removes leading zeros
    return [left, right]

def transform_stone(stone):
    """Apply transformation rules to a single stone and return list of resulting stones."""
    # Rule 1: If stone is 0, replace with 1
    if stone == 0:
        return [1]
    
    # Rule 2: If stone has even number of digits, split into two stones
    digit_count = count_digits(stone)
    if digit_count % 2 == 0:
        return split_number(stone)
    
    # Rule 3: Otherwise, multiply by 2024
    return [stone * 2024]

def simulate_blinks(stones, num_blinks, debug=False):
    """Simulate the stone transformations for the specified number of blinks."""
    current_stones = stones.copy()
    
    if debug:
        print(f"Initial arrangement: {' '.join(map(str, current_stones))}")
    
    for blink in range(1, num_blinks + 1):
        next_stones = []
        
        # Transform each stone according to the rules
        for stone in current_stones:
            transformed = transform_stone(stone)
            next_stones.extend(transformed)
        
        current_stones = next_stones
        
        if debug:
            if blink <= 6 or blink % 5 == 0 or blink == num_blinks:
                stones_str = ' '.join(map(str, current_stones))
                # Truncate very long arrangements for readability
                if len(stones_str) > 200:
                    stones_str = stones_str[:200] + f"... ({len(current_stones)} stones total)"
                print(f"After {blink} blink{'s' if blink != 1 else ''}: {stones_str}")
    
    return current_stones

def main():
    """Main function with command line argument support."""
    test_mode = '--test' in sys.argv or '-t' in sys.argv
    debug_mode = '--debug' in sys.argv or '-d' in sys.argv
    
    filename = 'example.txt' if test_mode else 'input.txt'
    
    if debug_mode:
        print(f"Running in {'test' if test_mode else 'normal'} mode with debug enabled")
        print(f"Reading from: {filename}")
    
    # Parse input
    initial_stones = parse_input(filename)
    if debug_mode:
        print(f"Initial stones: {initial_stones}")
    
    # Simulate 25 blinks
    num_blinks = 25
    final_stones = simulate_blinks(initial_stones, num_blinks, debug_mode)
    
    # Count final stones
    stone_count = len(final_stones)
    
    print(f"After {num_blinks} blinks: {stone_count} stones")

if __name__ == "__main__":
    main()