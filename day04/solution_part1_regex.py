#!/usr/bin/env python3

import sys
import re

def parse_input(filename):
    """Parse the input file and return a 2D grid of characters."""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    return [list(line) for line in lines]

def extract_all_lines(grid):
    """Extract all possible lines from the grid in all 8 directions."""
    if not grid or not grid[0]:
        return []
    
    rows, cols = len(grid), len(grid[0])
    lines = []
    
    # Horizontal lines (left-to-right)
    for row in range(rows):
        lines.append(''.join(grid[row]))
    
    # Vertical lines (top-to-bottom)
    for col in range(cols):
        lines.append(''.join(grid[row][col] for row in range(rows)))
    
    # Diagonal lines (top-left to bottom-right)
    # Starting from top row
    for start_col in range(cols):
        diagonal = []
        row, col = 0, start_col
        while row < rows and col < cols:
            diagonal.append(grid[row][col])
            row += 1
            col += 1
        if len(diagonal) >= 4:  # Only include if long enough for XMAS
            lines.append(''.join(diagonal))
    
    # Starting from left column (excluding top-left corner to avoid duplication)
    for start_row in range(1, rows):
        diagonal = []
        row, col = start_row, 0
        while row < rows and col < cols:
            diagonal.append(grid[row][col])
            row += 1
            col += 1
        if len(diagonal) >= 4:
            lines.append(''.join(diagonal))
    
    # Diagonal lines (top-right to bottom-left)
    # Starting from top row
    for start_col in range(cols):
        diagonal = []
        row, col = 0, start_col
        while row < rows and col >= 0:
            diagonal.append(grid[row][col])
            row += 1
            col -= 1
        if len(diagonal) >= 4:
            lines.append(''.join(diagonal))
    
    # Starting from right column (excluding top-right corner to avoid duplication)
    for start_row in range(1, rows):
        diagonal = []
        row, col = start_row, cols - 1
        while row < rows and col >= 0:
            diagonal.append(grid[row][col])
            row += 1
            col -= 1
        if len(diagonal) >= 4:
            lines.append(''.join(diagonal))
    
    return lines

def count_xmas_regex(lines):
    """Count XMAS occurrences in all lines using regex."""
    count = 0
    
    for line in lines:
        # Count XMAS (forward)
        count += len(re.findall(r'XMAS', line))
        # Count SAMX (backward)
        count += len(re.findall(r'SAMX', line))
    
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
    
    lines = extract_all_lines(grid)
    
    if debug_mode:
        print(f"Extracted {len(lines)} lines:")
        for i, line in enumerate(lines):
            print(f"{i:2d}: {line}")
        print()
    
    result = count_xmas_regex(lines)
    
    if test_mode or debug_mode:
        print(f"XMAS appears {result} times")
    else:
        print(result)

if __name__ == "__main__":
    main()