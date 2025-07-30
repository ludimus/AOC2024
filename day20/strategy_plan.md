# Day 20: Race Condition - Strategy Plan

## Problem Summary
**Part 1:** Find cheats allowing exactly 2 moves through walls, count those saving ≥100 picoseconds
**Part 2:** Find cheats allowing up to 20 moves through walls, count those saving ≥100 picoseconds

## Results
- **Part 1:** 1,502 cheats saving ≥100 picoseconds
- **Part 2:** 1,028,136 cheats saving ≥100 picoseconds

## Data Structures
- `grid`: 2D list representing the racetrack
- `start_pos`, `end_pos`: (row, col) tuples for S and E positions  
- `normal_path`: dict mapping (row, col) -> distance_from_start
- `cheats`: list of valid cheats with time savings

## Algorithm Approach

### 1. Input Parsing
- Read grid into 2D list
- Find start (S) and end (E) positions
- Convert S/E to '.' in grid for pathfinding

### 2. Baseline Pathfinding
- Use BFS from start to map every reachable position to its distance from start
- Since there's only one path, this gives us the normal racing time to each position

### 3. Cheat Detection

**Part 1 (2-move cheats):**
- Try all possible 2-move sequences (up/down/left/right combinations)
- Check if end position after 2 moves is back on normal path
- Calculate time saved: `normal_time_to_end - current_time - 2`

**Part 2 (up to 20-move cheats):**
- For each start position, check all positions within Manhattan distance ≤20
- Use Manhattan distance as cheat time: `abs(r2-r1) + abs(c2-c1)`
- Calculate time saved: `normal_time_to_end - current_time - manhattan_distance`
- Much more efficient than exploring all possible paths

### 4. Implementation Details
- Directions: [(0,1), (0,-1), (1,0), (-1,0)] for right, left, down, up
- Cheat moves can go through walls (no bounds checking except grid limits)  
- Must end cheat back on normal track

## Functions
- `parse_input(filename)`: Return grid, start_pos, end_pos
- `find_normal_path(grid, start, end)`: Return distance map using BFS
- `find_cheats(grid, normal_path, threshold)`: Return count of valid cheats
- `main()`: Coordinate with command line args for test/debug modes