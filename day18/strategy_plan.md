# Day 18: RAM Run - Strategy Plan

## Problem Analysis
- We have a 2D grid representing memory space
- Bytes fall at specific coordinates, corrupting those positions
- Need to find shortest path from (0,0) to (70,70) after first 1024 bytes fall
- Example uses 7x7 grid (0-6) and first 12 bytes

## Data Structures
- **Grid**: 2D array/set to track corrupted positions
- **Coordinates**: List of (x,y) tuples from input
- **Path finding**: BFS to find shortest path

## Functions Needed
1. `parse_input(filename)`: Read coordinates from file, return list of (x,y) tuples
2. `create_grid(size, corrupted_coords, num_bytes)`: Create grid with first num_bytes corrupted
3. `bfs_shortest_path(grid, start, end, size)`: BFS to find shortest path
4. `main()`: Orchestrate the solution

## Algorithm Approach
1. Parse input coordinates
2. Create grid marking first 1024 bytes as corrupted
3. Use BFS from (0,0) to find shortest path to (70,70)
4. Return path length

## Testing Strategy
- Use example.txt with 7x7 grid and 12 bytes
- Expected result: 22 steps
- Then run on actual input.txt with 71x71 grid and 1024 bytes

## Part 2 Analysis
- Find the first byte that completely blocks the path to exit
- Need to simulate bytes falling one by one until no path exists
- Example: byte at (6,1) is the first to block the path
- Algorithm: Binary search or sequential search to find blocking byte

## Part 2 Approach
1. Use binary search for efficiency (since bytes fall in order)
2. For each candidate byte count, check if path still exists
3. Find the exact byte that first blocks the path
4. Return coordinates as "x,y" format