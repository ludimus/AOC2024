#!/usr/bin/env python3
"""
AOC 2024 Day 4 Part B - X-MAS Search
Find X-MAS patterns where two MAS words cross in an X formation
"""

import time

def read_grid(filename):
    """Read the grid from file"""
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def is_valid_xmas(grid, center_row, center_col):
    """
    Check if there's a valid X-MAS pattern centered at the given position
    
    Pattern looks like:
    M.S
    .A.
    M.S
    
    Both diagonals must contain MAS or SAM
    """
    rows, cols = len(grid), len(grid[0])
    
    # Check bounds - need 1 cell in each direction from center
    if (center_row < 1 or center_row >= rows - 1 or 
        center_col < 1 or center_col >= cols - 1):
        return False
    
    # Center must be 'A'
    if grid[center_row][center_col] != 'A':
        return False
    
    # Extract the 3x3 grid around the center
    # Positions:
    # TL . TR
    # .  A .
    # BL . BR
    top_left = grid[center_row - 1][center_col - 1]
    top_right = grid[center_row - 1][center_col + 1]
    bottom_left = grid[center_row + 1][center_col - 1]
    bottom_right = grid[center_row + 1][center_col + 1]
    
    # Main diagonal: top-left -> center -> bottom-right
    main_diagonal = top_left + 'A' + bottom_right
    
    # Anti-diagonal: top-right -> center -> bottom-left  
    anti_diagonal = top_right + 'A' + bottom_left
    
    # Both diagonals must be either "MAS" or "SAM"
    valid_words = {"MAS", "SAM"}
    
    return (main_diagonal in valid_words and 
            anti_diagonal in valid_words)

def solve_xmas(filename):
    """Find all X-MAS patterns in the grid"""
    grid = read_grid(filename)
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    # Check each possible center position
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if is_valid_xmas(grid, row, col):
                count += 1
    
    return count

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
    
    print("Testing X-MAS solution:")
    example_result = solve_xmas('example.txt')
    print(f"Example result: {example_result} (expected: 9)")
    
    # Solve actual puzzle
    print("\nSolving actual puzzle:")
    start_time = time.time()
    result = solve_xmas('input.txt')
    end_time = time.time()
    
    print(f"Result: {result}")
    print(f"Time taken: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    main()