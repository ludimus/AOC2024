#!/usr/bin/env python3

import sys

def parse_input(filename):
    """Parse the input file and return grid and guard starting position."""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    
    grid = [list(line) for line in lines]
    guard_pos = None
    
    # Find guard starting position (marked with ^)
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '^':
                guard_pos = (row, col)
                grid[row][col] = '.'  # Replace with empty space
                break
        if guard_pos:
            break
    
    return grid, guard_pos

def is_valid_position(row, col, grid):
    """Check if position is within grid boundaries."""
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def has_obstacle(row, col, grid):
    """Check if position contains an obstacle."""
    if not is_valid_position(row, col, grid):
        return False
    return grid[row][col] == '#'

def simulate_guard_path(grid, start_pos):
    """Simulate guard movement and return set of visited positions."""
    # Direction vectors: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction_idx = 0  # Start facing up
    
    row, col = start_pos
    visited = set()
    
    if not is_valid_position(row, col, grid):
        return visited
    
    while True:
        # Add current position to visited set
        visited.add((row, col))
        
        # Calculate next position
        dr, dc = directions[direction_idx]
        next_row, next_col = row + dr, col + dc
        
        # Check if guard would leave the map
        if not is_valid_position(next_row, next_col, grid):
            break
        
        # Check if there's an obstacle ahead
        if has_obstacle(next_row, next_col, grid):
            # Turn right 90 degrees
            direction_idx = (direction_idx + 1) % 4
        else:
            # Move forward
            row, col = next_row, next_col
    
    return visited

def main():
    # Check command line arguments
    test_mode = '--test' in sys.argv
    debug_mode = '--debug' in sys.argv
    
    filename = 'example.txt' if test_mode else 'input.txt'
    
    if debug_mode:
        print(f"Reading from: {filename}")
    
    grid, guard_pos = parse_input(filename)
    
    if debug_mode:
        print(f"Grid dimensions: {len(grid)}x{len(grid[0])}")
        print(f"Guard starting position: {guard_pos}")
        print("Grid:")
        for row in grid:
            print(''.join(row))
        print()
    
    visited_positions = simulate_guard_path(grid, guard_pos)
    result = len(visited_positions)
    
    if debug_mode:
        print(f"Guard visited {result} distinct positions")
        if len(visited_positions) <= 50:  # Only show for small examples
            print("Visited positions:")
            for pos in sorted(visited_positions):
                print(f"  {pos}")
    elif test_mode:
        print(f"Guard visited {result} distinct positions")
    else:
        print(result)

if __name__ == "__main__":
    main()