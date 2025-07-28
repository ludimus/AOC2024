#!/usr/bin/env python3

import sys

def parse_input(filename):
    """Parse the input file and return a 2D grid of characters."""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    return [list(line) for line in lines]

def is_valid_xmas(grid, row, col):
    """Check if 'A' at position forms a valid X-MAS pattern."""
    rows, cols = len(grid), len(grid[0])
    
    # Check if we can form a 3x3 pattern around this position
    if row < 1 or row >= rows - 1 or col < 1 or col >= cols - 1:
        return False
    
    # Check if center is 'A'
    if grid[row][col] != 'A':
        return False
    
    # Get the two diagonals
    # Diagonal 1: top-left to bottom-right
    diagonal1 = grid[row-1][col-1] + grid[row][col] + grid[row+1][col+1]
    
    # Diagonal 2: top-right to bottom-left
    diagonal2 = grid[row-1][col+1] + grid[row][col] + grid[row+1][col-1]
    
    # Check if both diagonals form "MAS" or "SAM"
    valid_patterns = ["MAS", "SAM"]
    
    return diagonal1 in valid_patterns and diagonal2 in valid_patterns

def count_xmas_patterns(grid):
    """Count all X-MAS pattern occurrences in the grid."""
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    # Check each position that could be the center of an X
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if is_valid_xmas(grid, row, col):
                count += 1
    
    return count

def main():
    # Check command line arguments
    test_mode = '--test' in sys.argv
    debug_mode = '--debug' in sys.argv
    
    filename = 'example.txt' if test_mode else 'input.txt'
    
    if debug_mode:
        print(f"Reading from: {filename}")
    
    grid = parse_input(filename)
    
    if debug_mode:
        print(f"Grid dimensions: {len(grid)}x{len(grid[0])}")
        print("Grid:")
        for row in grid:
            print(''.join(row))
        print()
    
    result = count_xmas_patterns(grid)
    
    if debug_mode:
        print(f"X-MAS patterns found: {result}")
        # Show pattern locations for debugging
        rows, cols = len(grid), len(grid[0])
        for row in range(1, rows - 1):
            for col in range(1, cols - 1):
                if is_valid_xmas(grid, row, col):
                    print(f"X-MAS found at center ({row}, {col})")
    
    if test_mode or debug_mode:
        print(f"X-MAS appears {result} times")
    else:
        print(result)

if __name__ == "__main__":
    main()