#!/usr/bin/env python3

import sys
from collections import deque

def parse_input(filename):
    """Parse input file and return list of (x, y) coordinates."""
    coordinates = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                coordinates.append((x, y))
    return coordinates

def bfs_shortest_path(corrupted, start, end, grid_size):
    """Find shortest path using BFS, avoiding corrupted positions."""
    if start in corrupted or end in corrupted:
        return -1
    
    queue = deque([(start, 0)])  # (position, steps)
    visited = {start}
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # up, down, right, left
    
    while queue:
        (x, y), steps = queue.popleft()
        
        if (x, y) == end:
            return steps
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check bounds
            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                # Check if not corrupted and not visited
                if (nx, ny) not in corrupted and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), steps + 1))
    
    return -1  # No path found

def main():
    # Parse command line arguments
    test_mode = '--test' in sys.argv
    debug_mode = '--debug' in sys.argv
    
    if test_mode:
        filename = 'example.txt'
        grid_size = 7
        num_bytes = 12
        start = (0, 0)
        end = (6, 6)
    else:
        filename = 'input.txt'
        grid_size = 71
        num_bytes = 1024
        start = (0, 0)
        end = (70, 70)
    
    # Parse coordinates
    coordinates = parse_input(filename)
    
    if debug_mode:
        print(f"Total coordinates: {len(coordinates)}")
        print(f"Using first {num_bytes} bytes")
        print(f"Grid size: {grid_size}x{grid_size}")
        print(f"Start: {start}, End: {end}")
    
    # Get first num_bytes corrupted positions
    corrupted = set(coordinates[:num_bytes])
    
    if debug_mode:
        print(f"Corrupted positions: {len(corrupted)}")
    
    # Find shortest path
    result = bfs_shortest_path(corrupted, start, end, grid_size)
    
    if result == -1:
        print("No path found!")
    else:
        print(f"Minimum steps needed: {result}")

if __name__ == "__main__":
    main()