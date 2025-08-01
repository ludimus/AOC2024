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

def is_within_bounds(row, col, grid):
    """Check if position is within grid bounds"""
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def solve_part2(filename, debug=False):
    """Main function to solve part 2"""
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
        
        # Add all antenna positions as antinodes (new in part 2)
        for pos in positions:
            antinodes.add(pos)
            if debug:
                print(f"  Added antenna position as antinode: {pos}")
        
        # Check all pairs of antennas for this frequency
        for pos1, pos2 in combinations(positions, 2):
            r1, c1 = pos1
            r2, c2 = pos2
            
            # Calculate displacement vector
            dr = r2 - r1
            dc = c2 - c1
            
            if debug:
                print(f"  Processing antenna pair {pos1} and {pos2}")
                print(f"    Displacement vector: ({dr}, {dc})")
            
            # Extend line forward from second antenna
            r, c = r2 + dr, c2 + dc
            forward_count = 0
            while is_within_bounds(r, c, grid):
                antinodes.add((r, c))
                forward_count += 1
                if debug:
                    print(f"    Added forward antinode: ({r}, {c})")
                r += dr
                c += dc
            
            # Extend line backward from first antenna
            r, c = r1 - dr, c1 - dc
            backward_count = 0
            while is_within_bounds(r, c, grid):
                antinodes.add((r, c))
                backward_count += 1
                if debug:
                    print(f"    Added backward antinode: ({r}, {c})")
                r -= dr
                c -= dc
            
            if debug:
                print(f"    Added {forward_count} forward + {backward_count} backward antinodes")
    
    if debug:
        print(f"\nTotal unique antinodes: {len(antinodes)}")
        if len(antinodes) <= 50:  # Only show if not too many
            print(f"Antinode positions: {sorted(antinodes)}")
        
        # Print the grid with antinodes marked
        print(f"\nGrid with antinodes marked as '#':")
        for row in range(len(grid)):
            line = ""
            for col in range(len(grid[0])):
                if (row, col) in antinodes:
                    if grid[row][col] != '.':
                        # Show original antenna if it's also an antinode
                        line += grid[row][col]
                    else:
                        line += '#'
                else:
                    line += grid[row][col]
            print(line)
    
    return len(antinodes)

def main():
    parser = argparse.ArgumentParser(description='Day 8: Resonant Collinearity - Part 2')
    parser.add_argument('--test', action='store_true', help='Run on example.txt instead of input.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    debug = args.debug or args.test  # Enable debug by default when testing
    
    result = solve_part2(filename, debug)
    print(f"Unique antinode locations: {result}")

if __name__ == "__main__":
    main()