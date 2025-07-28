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

def simulate_guard_path(grid, start_pos, detect_loops=False):
    """Simulate guard movement. Returns visited positions or detects loops."""
    # Direction vectors: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction_idx = 0  # Start facing up
    
    row, col = start_pos
    visited_positions = set()
    visited_states = set()  # For loop detection: (row, col, direction)
    
    if not is_valid_position(row, col, grid):
        return visited_positions if not detect_loops else False
    
    while True:
        # Current state for loop detection
        current_state = (row, col, direction_idx)
        
        if detect_loops:
            # Check if we've been in this state before (loop detected)
            if current_state in visited_states:
                return True  # Loop found
            visited_states.add(current_state)
        else:
            # Just track positions for Part 1
            visited_positions.add((row, col))
        
        # Calculate next position
        dr, dc = directions[direction_idx]
        next_row, next_col = row + dr, col + dc
        
        # Check if guard would leave the map
        if not is_valid_position(next_row, next_col, grid):
            if detect_loops:
                return False  # No loop, guard exits
            else:
                break  # Guard exits, simulation complete
        
        # Check if there's an obstacle ahead
        if has_obstacle(next_row, next_col, grid):
            # Turn right 90 degrees
            direction_idx = (direction_idx + 1) % 4
        else:
            # Move forward
            row, col = next_row, next_col
    
    return visited_positions if not detect_loops else False

def get_original_path(grid, start_pos):
    """Get the original patrol path (optimization for Part 2)."""
    return simulate_guard_path(grid, start_pos, detect_loops=False)

def test_obstacle_position(grid, start_pos, obstacle_pos):
    """Test if placing obstacle at given position creates a loop."""
    if obstacle_pos == start_pos:
        return False  # Can't place obstacle at starting position
    
    # Temporarily place obstacle
    original_cell = grid[obstacle_pos[0]][obstacle_pos[1]]
    grid[obstacle_pos[0]][obstacle_pos[1]] = '#'
    
    # Test for loop
    creates_loop = simulate_guard_path(grid, start_pos, detect_loops=True)
    
    # Restore original cell
    grid[obstacle_pos[0]][obstacle_pos[1]] = original_cell
    
    return creates_loop

def solve_part2(grid, start_pos):
    """Find all positions where adding obstacle creates infinite loop."""
    # Get original path to optimize search space
    original_path = get_original_path(grid, start_pos)
    
    loop_positions = set()
    
    # Test each position on the original path (except starting position)
    for pos in original_path:
        if pos == start_pos:
            continue  # Skip starting position
        
        if test_obstacle_position(grid, start_pos, pos):
            loop_positions.add(pos)
    
    return loop_positions

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
        print()
    
    # Get original path for reference
    original_path = get_original_path(grid, guard_pos)
    
    if debug_mode:
        print(f"Original path has {len(original_path)} positions")
        print("Testing obstacle positions...")
    
    # Find loop-creating obstacle positions
    loop_positions = solve_part2(grid, guard_pos)
    result = len(loop_positions)
    
    if debug_mode:
        print(f"Found {result} positions that create loops")
        if len(loop_positions) <= 20:  # Only show for small examples
            print("Loop-creating positions:")
            for pos in sorted(loop_positions):
                print(f"  {pos}")
    elif test_mode:
        print(f"Found {result} positions that create loops")
    else:
        print(result)

if __name__ == "__main__":
    main()