#!/usr/bin/env python3

import sys

def parse_input(filename):
    """Parse the input file and return a 2D grid of characters."""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    return [list(line) for line in lines]

def search_word(grid, row, col, direction, word):
    """Check if word exists starting at (row, col) in given direction."""
    rows, cols = len(grid), len(grid[0])
    dr, dc = direction
    
    for i in range(len(word)):
        new_row = row + i * dr
        new_col = col + i * dc
        
        if (new_row < 0 or new_row >= rows or 
            new_col < 0 or new_col >= cols or
            grid[new_row][new_col] != word[i]):
            return False
    
    return True

def count_xmas(grid):
    """Count all occurrences of XMAS in the grid."""
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    word = "XMAS"
    count = 0
    
    # 8 directions: right, left, down, up, down-right, down-left, up-right, up-left
    directions = [
        (0, 1),   # right
        (0, -1),  # left
        (1, 0),   # down
        (-1, 0),  # up
        (1, 1),   # down-right
        (1, -1),  # down-left
        (-1, 1),  # up-right
        (-1, -1)  # up-left
    ]
    
    for row in range(rows):
        for col in range(cols):
            for direction in directions:
                if search_word(grid, row, col, direction, word):
                    count += 1
    
    return count

def main():
    filename = 'input.txt'
    grid = parse_input(filename)
    result = count_xmas(grid)
    print(result)

if __name__ == "__main__":
    main()