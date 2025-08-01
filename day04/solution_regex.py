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
    filename = 'input.txt'
    grid = parse_input(filename)
    lines = extract_all_lines(grid)
    result = count_xmas_regex(lines)
    print(result)

if __name__ == "__main__":
    main()