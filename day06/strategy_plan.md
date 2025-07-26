# Day 6: Guard Gallivant - Strategy Plan

## Problem Analysis
- **Part 1**: Simulate guard patrol following strict protocol, count distinct positions visited
- **Part 2**: Find positions where adding single obstacle creates infinite loops

## Data Structures

### Part 1
- **Grid**: 2D list/array of strings for the map
- **Position**: Tuple `(row, col)` for coordinates  
- **Direction**: Character `'^', 'v', '<', '>'` with direction vectors
- **Visited Set**: `set()` of position tuples to track unique locations
- **Direction Mapping**: Dict to convert direction chars to movement vectors

### Part 2
- **State Tracking**: Set of `(row, col, direction)` tuples for loop detection
- **Original Path**: Set of positions from Part 1 simulation (optimization)
- **Loop Counter**: Integer to count valid obstacle positions

## Functions Needed

### Part 1
1. `parse_input(filename)` - Load grid, find guard start position/direction
2. `get_direction_vector(direction)` - Convert direction char to (dr, dc) tuple
3. `turn_right(direction)` - Rotate direction 90° clockwise
4. `is_valid_position(row, col, grid)` - Check bounds
5. `simulate_guard_patrol(grid, start_pos, start_dir)` - Main simulation loop
6. `solve_part1(filename)` - Orchestrate solution

### Part 2  
1. `get_original_path(grid, start_pos, start_dir)` - Get baseline patrol path
2. `detect_loop_with_obstacle(grid, start_pos, start_dir, obstacle_pos)` - Loop detection
3. `solve_part2(filename)` - Test each position on original path

## Algorithm Strategy

### Part 1: Guard Simulation
1. Parse input to get grid and guard starting state
2. Track current position and direction
3. For each step:
   - Add current position to visited set
   - Calculate next position based on direction
   - If next position is out of bounds → stop (guard exits)
   - If next position has obstacle → turn right, don't move
   - Otherwise → move to next position
4. Return count of unique visited positions

### Part 2: Loop Detection Optimization
1. **Key Insight**: Only test obstacle positions on the guard's original path
   - Obstacles elsewhere have no effect on patrol
   - Reduces search space from ~15,000 to ~5,000 positions
2. For each position on original path (except start):
   - Temporarily add obstacle there
   - Simulate guard patrol with loop detection
   - Count positions that create loops

### Loop Detection Method
- Track states as `(row, col, direction)` tuples
- If guard visits same position with same direction twice → infinite loop
- This is guaranteed because guard follows deterministic rules

## Performance Considerations
- Part 1: O(path_length) - linear in guard's path
- Part 2: O(path_length²) in worst case, but typically much better
- Loop detection prevents infinite simulation
- Path-only testing provides significant speedup

## Expected Results
- **Example**: Part 1 = 41 positions, Part 2 = 6 loop positions
- **Actual Input**: Part 1 = ~5000 positions, Part 2 = ~1500-2000 loop positions