# Day 6: Guard Gallivant - Strategy Plan

## Problem Analysis
- **Part 1**: Simulate guard patrol following strict protocol, count distinct positions visited
- **Part 2**: Find positions where adding single obstacle creates infinite loops

## Data Structures

### Part 1 - Current Implementation
- **Grid**: 2D list of characters `[['#', '.', ...], ...]`
  - `'#'` = obstacle, `'.'` = empty space, `'^'` = guard start (converted to `.`)
- **Position**: Tuple `(row, col)` for current guard coordinates
- **Direction Index**: Integer `0-3` representing current facing direction
  - `0` = Up (-1,0), `1` = Right (0,1), `2` = Down (1,0), `3` = Left (0,-1)
- **Direction Vectors**: List `[(-1,0), (0,1), (1,0), (0,-1)]` for movement
- **Visited Set**: `set()` of `(row, col)` tuples tracking unique positions visited
- **Start Position**: Tuple `(row, col)` where guard begins (extracted during parsing)

### Part 2 - Implemented
- **State Set**: `set()` of `(row, col, direction_idx)` tuples for loop detection
- **Original Path**: Set of positions from Part 1 to optimize obstacle placement  
- **Loop Positions**: Set of positions where obstacles create loops
- **Temporary Obstacle**: Grid modification for testing each candidate position

### Key Data Structure Benefits
- **Direction Index + Vectors**: Clean rotation with `(direction_idx + 1) % 4`
- **Set for Visited**: O(1) add/lookup, automatic deduplication
- **Tuple Positions**: Immutable, hashable for set membership
- **Grid as List of Lists**: Direct indexing `grid[row][col]` for obstacle checking

## Functions Needed

### Part 1 - Implemented
1. `parse_input(filename)` - Load grid, find guard start position
2. `is_valid_position(row, col, grid)` - Check bounds
3. `has_obstacle(row, col, grid)` - Check if position contains obstacle
4. `simulate_guard_path(grid, start_pos, detect_loops=False)` - Main simulation loop
5. `main()` - Handle command line args and orchestrate solution

### Part 2 - Implemented
1. `get_original_path(grid, start_pos)` - Get baseline patrol path (reuses Part 1)
2. `test_obstacle_position(grid, start_pos, obstacle_pos)` - Test single obstacle placement
3. `solve_part2(grid, start_pos)` - Test each position on original path
4. `simulate_guard_path(grid, start_pos, detect_loops=True)` - Simulation with loop detection

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

### Part 2: Loop Detection with Obstacle Placement
1. **Optimization Strategy**: Only test obstacle positions on the guard's original path
   - Obstacles placed elsewhere cannot affect the patrol route
   - Reduces search space significantly (from all grid positions to ~5,000 path positions)
2. **Algorithm Steps**:
   - Get original patrol path from Part 1 simulation
   - For each position on original path (except starting position):
     - Temporarily place obstacle at that position
     - Simulate guard patrol with loop detection
     - Count positions that create infinite loops
3. **Loop Detection Implementation**:
   - Track complete states as `(row, col, direction_idx)` tuples
   - If guard revisits same position with same direction → infinite loop detected
   - This works because guard follows deterministic movement rules

### Loop Detection Method Details
- **State Tracking**: Set of `(row, col, direction_idx)` for visited states
- **Loop Condition**: Current state already exists in visited states set
- **Guaranteed Detection**: Deterministic rules ensure cycles are eventually detected
- **Early Termination**: Stop simulation immediately when loop found (efficiency)

## Performance Considerations
- Part 1: O(path_length) - linear in guard's path
- Part 2: O(path_length²) in worst case, but typically much better
- Loop detection prevents infinite simulation
- Path-only testing provides significant speedup

## Actual Results
- **Example**: Part 1 = 41 positions ✓, Part 2 = 6 loop positions ✓
- **Actual Input**: Part 1 = 4826 positions, Part 2 = 1721 loop positions

## Implementation Notes
- **Single Simulation Function**: `simulate_guard_path()` handles both parts with `detect_loops` parameter
- **Grid Modification**: Temporary obstacle placement/removal for clean testing
- **Efficient Optimization**: Only test ~41 positions instead of ~10,000 grid positions
- **Robust Loop Detection**: State-based tracking with early termination