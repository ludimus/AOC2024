#!/usr/bin/env python3

import argparse
from collections import defaultdict
from itertools import combinations

def parse_input(filename):
    """Parse input file and extract antenna positions by frequency"""
    antennas = defaultdict(list)
    grid = []
    
    with open(filename, 'r') as f:
        for row, line in enumerate(f):
            line = line.strip()
            grid.append(line)
            for col, char in enumerate(line):
                if char != '.':
                    antennas[char].append((row, col))
    
    return antennas, grid

def calculate_antinodes(pos1, pos2):
    """Calculate the two antinode positions for a pair of antennas"""
    r1, c1 = pos1
    r2, c2 = pos2
    
    # Calculate displacement vector
    dr = r2 - r1
    dc = c2 - c1
    
    # Calculate antinodes (one on each side)
    antinode1 = (r1 - dr, c1 - dc)  # Beyond first antenna
    antinode2 = (r2 + dr, c2 + dc)  # Beyond second antenna
    
    return antinode1, antinode2

def is_within_bounds(row, col, grid):
    """Check if position is within grid bounds"""
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def solve_part1(filename, debug=False):
    """Main function to solve part 1"""
    antennas, grid = parse_input(filename)
    
    if debug:
        print(f"Grid size: {len(grid)}x{len(grid[0])}")
        print(f"Found antennas for frequencies: {list(antennas.keys())}")
        for freq, positions in antennas.items():
            print(f"  {freq}: {len(positions)} antennas at {positions}")
    
    antinodes = set()
    
    # Process each frequency separately
    for frequency, positions in antennas.items():
        if len(positions) < 2:
            continue  # Need at least 2 antennas to create antinodes
        
        if debug:
            print(f"\nProcessing frequency '{frequency}' with {len(positions)} antennas:")
        
        # Check all pairs of antennas for this frequency
        for pos1, pos2 in combinations(positions, 2):
            antinode1, antinode2 = calculate_antinodes(pos1, pos2)
            
            if debug:
                print(f"  Antennas at {pos1} and {pos2}")
                print(f"    Antinode candidates: {antinode1}, {antinode2}")
            
            # Add valid antinodes (within bounds)
            if is_within_bounds(antinode1[0], antinode1[1], grid):
                antinodes.add(antinode1)
                if debug:
                    print(f"    Added antinode: {antinode1}")
            
            if is_within_bounds(antinode2[0], antinode2[1], grid):
                antinodes.add(antinode2)
                if debug:
                    print(f"    Added antinode: {antinode2}")
    
    if debug:
        print(f"\nTotal unique antinodes: {len(antinodes)}")
        if len(antinodes) <= 20:  # Only show if not too many
            print(f"Antinode positions: {sorted(antinodes)}")
    
    return len(antinodes)

def main():
    parser = argparse.ArgumentParser(description='Day 8: Resonant Collinearity - Part 1')
    parser.add_argument('--test', action='store_true', help='Run on example.txt instead of input.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    debug = args.debug or args.test  # Enable debug by default when testing
    
    result = solve_part1(filename, debug)
    print(f"Unique antinode locations: {result}")

if __name__ == "__main__":
    main()