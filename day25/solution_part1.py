#!/usr/bin/env python3
import sys
import argparse

def parse_input(filename):
    """Parse input file to get individual schematics."""
    with open(filename, 'r') as f:
        content = f.read().strip()
    
    # Split by blank lines to get individual schematics
    schematics = content.split('\n\n')
    
    parsed_schematics = []
    for schematic in schematics:
        lines = schematic.strip().split('\n')
        parsed_schematics.append(lines)
    
    return parsed_schematics

def classify_schematic(lines):
    """Determine if schematic is a lock or key."""
    # Locks start with ##### (filled top row)
    # Keys start with ..... (empty top row)
    if lines[0] == '#####':
        return 'lock'
    elif lines[0] == '.....':
        return 'key'
    else:
        raise ValueError(f"Unknown schematic type: {lines[0]}")

def calculate_heights(lines):
    """Calculate height of each column by counting '#' symbols."""
    heights = []
    
    # Process each of the 5 columns
    for col in range(5):
        height = 0
        for row in lines:
            if row[col] == '#':
                height += 1
        heights.append(height)
    
    return heights

def is_compatible(lock_heights, key_heights):
    """Check if lock and key are compatible (no overlap)."""
    # For each column, lock_height + key_height must be ≤ 7
    for i in range(5):
        if lock_heights[i] + key_heights[i] > 7:
            return False
    return True

def solve(filename, debug=False):
    """Main solution function."""
    schematics = parse_input(filename)
    
    if debug:
        print(f"Parsed {len(schematics)} schematics")
    
    locks = []
    keys = []
    
    # Classify and convert schematics to height arrays
    for schematic in schematics:
        schematic_type = classify_schematic(schematic)
        heights = calculate_heights(schematic)
        
        if schematic_type == 'lock':
            locks.append(heights)
        else:  # key
            keys.append(heights)
    
    if debug:
        print(f"Found {len(locks)} locks and {len(keys)} keys")
        print(f"Example lock heights: {locks[0] if locks else 'None'}")
        print(f"Example key heights: {keys[0] if keys else 'None'}")
    
    # Check all lock/key combinations
    compatible_pairs = 0
    
    for i, lock_heights in enumerate(locks):
        for j, key_heights in enumerate(keys):
            if is_compatible(lock_heights, key_heights):
                compatible_pairs += 1
                if debug:
                    print(f"Lock {i} {lock_heights} + Key {j} {key_heights} = COMPATIBLE")
    
    if debug:
        print(f"Total pairs checked: {len(locks) * len(keys)}")
        print(f"Compatible pairs: {compatible_pairs}")
    
    return compatible_pairs

def main():
    parser = argparse.ArgumentParser(description='Day 25: Code Chronicle - Part 1')
    parser.add_argument('--test', action='store_true', help='Run with example.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    result = solve(filename, args.debug)
    
    print(f"Compatible lock/key pairs: {result}")

if __name__ == "__main__":
    main()