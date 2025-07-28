#!/usr/bin/env python3
import sys
from collections import defaultdict

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

def simulate_blinks_optimized(initial_stones, num_blinks, debug=False):
    """Simulate stone transformations using count-based optimization."""
    # Convert initial stones to count dictionary
    stone_counts = defaultdict(int)
    for stone in initial_stones:
        stone_counts[stone] += 1
    
    if debug:
        print(f"Initial stone counts: {dict(stone_counts)}")
        print(f"Initial total: {sum(stone_counts.values())} stones")
    
    for blink in range(1, num_blinks + 1):
        next_counts = defaultdict(int)
        
        # Process each unique stone value and its count
        for stone_value, count in stone_counts.items():
            # Transform this stone value
            transformed_stones = transform_stone(stone_value)
            
            # Add the count to each resulting stone value
            for new_stone in transformed_stones:
                next_counts[new_stone] += count
        
        stone_counts = next_counts
        total_stones = sum(stone_counts.values())
        
        if debug:
            if blink <= 6 or blink % 5 == 0 or blink == num_blinks:
                unique_values = len(stone_counts)
                print(f"After {blink} blink{'s' if blink != 1 else ''}: {total_stones} stones ({unique_values} unique values)")
                if blink <= 6:
                    # Show actual stone counts for early blinks
                    stone_list = []
                    for value, count in sorted(stone_counts.items()):
                        stone_list.extend([value] * count)
                    if len(stone_list) <= 50:
                        print(f"  Stones: {' '.join(map(str, stone_list))}")
                    else:
                        print(f"  Top values: {dict(sorted(stone_counts.items(), key=lambda x: x[1], reverse=True)[:10])}")
    
    return sum(stone_counts.values())

def main():
    """Main function with command line argument support."""
    test_mode = '--test' in sys.argv or '-t' in sys.argv
    debug_mode = '--debug' in sys.argv or '-d' in sys.argv
    
    # Allow custom number of blinks for testing
    num_blinks = 75
    if '--blinks' in sys.argv:
        blink_idx = sys.argv.index('--blinks')
        if blink_idx + 1 < len(sys.argv):
            num_blinks = int(sys.argv[blink_idx + 1])
    
    filename = 'example.txt' if test_mode else 'input.txt'
    
    if debug_mode:
        print(f"Running in {'test' if test_mode else 'normal'} mode with debug enabled")
        print(f"Reading from: {filename}")
        print(f"Number of blinks: {num_blinks}")
    
    # Parse input
    initial_stones = parse_input(filename)
    if debug_mode:
        print(f"Initial stones: {initial_stones}")
    
    # Simulate blinks using optimized approach
    total_stones = simulate_blinks_optimized(initial_stones, num_blinks, debug_mode)
    
    print(f"After {num_blinks} blinks: {total_stones} stones")

if __name__ == "__main__":
    main()