#!/usr/bin/env python3
"""
AOC 2024 Day 4 - Regex-based solution
Find all occurrences of 'XMAS' in a word search grid using regex
"""

import re
import time

def read_grid(filename):
    """Read the grid from file"""
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def get_horizontal_lines(grid):
    """Get all horizontal lines (rows)"""
    return grid

def get_vertical_lines(grid):
    """Get all vertical lines (columns)"""
    if not grid:
        return []
    
    rows, cols = len(grid), len(grid[0])
    vertical_lines = []
    
    for col in range(cols):
        line = ''.join(grid[row][col] for row in range(rows))
        vertical_lines.append(line)
    
    return vertical_lines

def get_diagonal_lines(grid):
    """Get all diagonal lines (both directions)"""
    if not grid:
        return []
    
    rows, cols = len(grid), len(grid[0])
    diagonals = []
    
    # Top-left to bottom-right diagonals
    # Starting from top row
    for start_col in range(cols):
        line = ''
        row, col = 0, start_col
        while row < rows and col < cols:
            line += grid[row][col]
            row += 1
            col += 1
        if len(line) >= 4:  # Only consider diagonals long enough for XMAS
            diagonals.append(line)
    
    # Starting from left column (excluding top-left corner to avoid duplicate)
    for start_row in range(1, rows):
        line = ''
        row, col = start_row, 0
        while row < rows and col < cols:
            line += grid[row][col]
            row += 1
            col += 1
        if len(line) >= 4:
            diagonals.append(line)
    
    # Top-right to bottom-left diagonals
    # Starting from top row
    for start_col in range(cols):
        line = ''
        row, col = 0, start_col
        while row < rows and col >= 0:
            line += grid[row][col]
            row += 1
            col -= 1
        if len(line) >= 4:
            diagonals.append(line)
    
    # Starting from right column (excluding top-right corner to avoid duplicate)
    for start_row in range(1, rows):
        line = ''
        row, col = start_row, cols - 1
        while row < rows and col >= 0:
            line += grid[row][col]
            row += 1
            col -= 1
        if len(line) >= 4:
            diagonals.append(line)
    
    return diagonals

def count_xmas_in_line(line):
    """Count XMAS occurrences in a single line (both directions)"""
    # Use lookahead to handle overlapping matches
    forward_matches = len(re.findall(r'(?=XMAS)', line))
    backward_matches = len(re.findall(r'(?=SAMX)', line))
    return forward_matches + backward_matches

def solve_regex(filename):
    """Solve using regex approach"""
    grid = read_grid(filename)
    total_count = 0
    
    # Get all lines in different directions
    horizontal_lines = get_horizontal_lines(grid)
    vertical_lines = get_vertical_lines(grid)
    diagonal_lines = get_diagonal_lines(grid)
    
    # Count XMAS in all lines
    for line in horizontal_lines:
        total_count += count_xmas_in_line(line)
    
    for line in vertical_lines:
        total_count += count_xmas_in_line(line)
    
    for line in diagonal_lines:
        total_count += count_xmas_in_line(line)
    
    return total_count

def main():
    # Test with example
    example_grid = [
        "MMMSXXMASM",
        "MSAMXMSMSA",
        "AMXSXMAAMM",
        "MSAMASMSMX",
        "XMASAMXAMM",
        "XXAMMXXAMA",
        "SMSMSASXSS",
        "SAXAMASAAA",
        "MAMMMXMMMM",
        "MXMXAXMASX"
    ]
    
    # Write example to temporary file for testing
    with open('example.txt', 'w') as f:
        for line in example_grid:
            f.write(line + '\n')
    
    print("Testing regex solution:")
    example_result = solve_regex('example.txt')
    print(f"Example result: {example_result} (expected: 18)")
    
    # Solve actual puzzle
    print("\nSolving actual puzzle:")
    start_time = time.time()
    result = solve_regex('input.txt')
    end_time = time.time()
    
    print(f"Result: {result}")
    print(f"Time taken: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    main()