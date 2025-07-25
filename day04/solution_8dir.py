#!/usr/bin/env python3
"""
AOC 2024 Day 4 - 8-direction search solution
Find all occurrences of 'XMAS' in a word search grid using 8-direction search
"""

import time

def read_grid(filename):
    """Read the grid from file"""
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def search_from_position(grid, row, col, direction, target="XMAS"):
    """Search for target word from a specific position in a given direction"""
    rows, cols = len(grid), len(grid[0])
    dr, dc = direction
    
    # Check if we can fit the entire word in this direction
    end_row = row + dr * (len(target) - 1)
    end_col = col + dc * (len(target) - 1)
    
    if end_row < 0 or end_row >= rows or end_col < 0 or end_col >= cols:
        return False
    
    # Check each character
    for i in range(len(target)):
        curr_row = row + dr * i
        curr_col = col + dc * i
        if grid[curr_row][curr_col] != target[i]:
            return False
    
    return True

def solve_8dir(filename):
    """Solve using 8-direction search approach"""
    grid = read_grid(filename)
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    
    # 8 directions: N, NE, E, SE, S, SW, W, NW
    directions = [
        (-1, 0),   # North
        (-1, 1),   # Northeast
        (0, 1),    # East
        (1, 1),    # Southeast
        (1, 0),    # South
        (1, -1),   # Southwest
        (0, -1),   # West
        (-1, -1),  # Northwest
    ]
    
    total_count = 0
    
    # Check every position in the grid
    for row in range(rows):
        for col in range(cols):
            # For each position, check all 8 directions
            for direction in directions:
                if search_from_position(grid, row, col, direction, "XMAS"):
                    total_count += 1
    
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
    
    print("Testing 8-direction search solution:")
    example_result = solve_8dir('example.txt')
    print(f"Example result: {example_result} (expected: 18)")
    
    # Solve actual puzzle
    print("\nSolving actual puzzle:")
    start_time = time.time()
    result = solve_8dir('input.txt')
    end_time = time.time()
    
    print(f"Result: {result}")
    print(f"Time taken: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    main()