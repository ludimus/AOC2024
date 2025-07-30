#!/usr/bin/env python3

import sys
from collections import deque

def parse_input(filename):
    """Parse the racetrack input file and return grid, start and end positions."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    grid = []
    start_pos = None
    end_pos = None
    
    for row, line in enumerate(lines):
        grid_row = []
        for col, char in enumerate(line):
            if char == 'S':
                start_pos = (row, col)
                grid_row.append('.')  # Start is walkable
            elif char == 'E':
                end_pos = (row, col)
                grid_row.append('.')  # End is walkable
            else:
                grid_row.append(char)
        grid.append(grid_row)
    
    return grid, start_pos, end_pos

def find_normal_path(grid, start_pos, end_pos):
    """Find the normal path without cheating using BFS. Return distance map."""
    rows, cols = len(grid), len(grid[0])
    distances = {}
    queue = deque([(start_pos, 0)])
    distances[start_pos] = 0
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
    
    while queue:
        (row, col), dist = queue.popleft()
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check bounds and walkable
            if (0 <= new_row < rows and 0 <= new_col < cols and 
                grid[new_row][new_col] == '.' and 
                (new_row, new_col) not in distances):
                
                new_dist = dist + 1
                distances[(new_row, new_col)] = new_dist
                queue.append(((new_row, new_col), new_dist))
    
    return distances

def find_cheats_part2(grid, normal_path, max_cheat_time=20, threshold=100):
    """Find all cheats that save at least threshold picoseconds with up to max_cheat_time moves."""
    rows, cols = len(grid), len(grid[0])
    cheats = []
    
    # Convert normal_path positions to a list for easier iteration
    path_positions = list(normal_path.keys())
    
    # Try cheating from each position on the normal path
    for start_pos in path_positions:
        start_row, start_col = start_pos
        start_time = normal_path[start_pos]
        
        # Check all positions within Manhattan distance of max_cheat_time
        for end_pos in path_positions:
            end_row, end_col = end_pos
            
            # Calculate Manhattan distance
            manhattan_dist = abs(end_row - start_row) + abs(end_col - start_col)
            
            # Skip if cheat would take too long or is the same position
            if manhattan_dist > max_cheat_time or manhattan_dist == 0:
                continue
            
            # Calculate time savings
            normal_time_to_end = normal_path[end_pos]
            cheat_time = start_time + manhattan_dist
            
            # Only count if we actually save time
            if normal_time_to_end > cheat_time:
                time_saved = normal_time_to_end - cheat_time
                
                if time_saved >= threshold:
                    cheats.append((start_pos, end_pos, time_saved))
    
    return cheats

def main():
    # Command line argument handling
    test_mode = '--test' in sys.argv
    debug_mode = '--debug' in sys.argv
    
    filename = 'example.txt' if test_mode else 'input.txt'
    threshold = 50 if test_mode else 100  # Lower threshold for example
    
    if debug_mode:
        print(f"Running in {'test' if test_mode else 'normal'} mode with threshold {threshold}")
    
    # Parse input
    grid, start_pos, end_pos = parse_input(filename)
    
    if debug_mode:
        print(f"Grid size: {len(grid)}x{len(grid[0])}")
        print(f"Start: {start_pos}, End: {end_pos}")
    
    # Find normal path
    normal_path = find_normal_path(grid, start_pos, end_pos)
    normal_time = normal_path[end_pos]
    
    if debug_mode:
        print(f"Normal race time: {normal_time} picoseconds")
        print(f"Positions on normal path: {len(normal_path)}")
    
    # Find cheats with up to 20 picosecond duration
    cheats = find_cheats_part2(grid, normal_path, max_cheat_time=20, threshold=threshold)
    
    if debug_mode or test_mode:
        # Group cheats by time saved for analysis
        savings_count = {}
        for _, _, time_saved in cheats:
            savings_count[time_saved] = savings_count.get(time_saved, 0) + 1
        
        for time_saved in sorted(savings_count.keys()):
            count = savings_count[time_saved]
            if time_saved >= threshold:  # Only show relevant savings
                print(f"There are {count} cheats that save {time_saved} picoseconds.")
    
    print(f"Total cheats saving at least {threshold} picoseconds: {len(cheats)}")

if __name__ == "__main__":
    main()