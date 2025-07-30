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

def has_path(corrupted, start, end, grid_size):
    """Check if path exists using BFS, avoiding corrupted positions."""
    if start in corrupted or end in corrupted:
        return False
    
    queue = deque([start])
    visited = {start}
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # up, down, right, left
    
    while queue:
        x, y = queue.popleft()
        
        if (x, y) == end:
            return True
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check bounds
            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                # Check if not corrupted and not visited
                if (nx, ny) not in corrupted and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    
    return False

def find_blocking_byte(coordinates, start, end, grid_size, initial_bytes):
    """Find the first byte that blocks the path using binary search."""
    left = initial_bytes
    right = len(coordinates)
    
    while left < right:
        mid = (left + right) // 2
        corrupted = set(coordinates[:mid + 1])
        
        if has_path(corrupted, start, end, grid_size):
            left = mid + 1
        else:
            right = mid
    
    return coordinates[left]

def main():
    # Parse command line arguments
    test_mode = '--test' in sys.argv
    debug_mode = '--debug' in sys.argv
    
    if test_mode:
        filename = 'example.txt'
        grid_size = 7
        initial_bytes = 12
        start = (0, 0)
        end = (6, 6)
    else:
        filename = 'input.txt'
        grid_size = 71
        initial_bytes = 1024
        start = (0, 0)
        end = (70, 70)
    
    # Parse coordinates
    coordinates = parse_input(filename)
    
    if debug_mode:
        print(f"Total coordinates: {len(coordinates)}")
        print(f"Starting from byte {initial_bytes}")
        print(f"Grid size: {grid_size}x{grid_size}")
        print(f"Start: {start}, End: {end}")
    
    # Find the first blocking byte
    blocking_byte = find_blocking_byte(coordinates, start, end, grid_size, initial_bytes)
    
    if debug_mode:
        print(f"First blocking byte: {blocking_byte}")
    
    print(f"{blocking_byte[0]},{blocking_byte[1]}")

if __name__ == "__main__":
    main()