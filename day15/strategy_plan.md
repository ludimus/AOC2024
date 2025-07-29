# Day 15: Warehouse Woes - Strategy Plan

## Problem Analysis

**Core Problem**: Simulate a robot moving boxes in a warehouse and calculate GPS coordinates.

### Key Components:
1. **Warehouse Grid**: 2D map with walls (#), boxes (O), robot (@), and empty spaces (.)
2. **Robot Movement**: Follows sequence of moves (^v<>) 
3. **Box Pushing Logic**: Robot pushes boxes when moving into them
4. **GPS Calculation**: 100 * row + column for each box position

### Data Structures:
- **Grid**: 2D list representing warehouse layout
- **Robot Position**: (row, col) tuple tracking robot location
- **Move Sequence**: String of movement commands
- **Direction Mapping**: Dict mapping move chars to (dr, dc) deltas

### Functions Needed:
1. `parse_input(filename)` - Parse warehouse grid and move sequence
2. `find_robot(grid)` - Locate initial robot position
3. `can_move(grid, pos, direction)` - Check if move is valid (handles box pushing)
4. `execute_move(grid, robot_pos, direction)` - Perform the move and update grid
5. `calculate_gps_sum(grid)` - Sum GPS coordinates of all boxes
6. `simulate_warehouse(grid, moves, robot_pos)` - Main simulation loop

### Algorithm Approach:
1. Parse input to get warehouse grid and move sequence
2. Find robot's starting position
3. For each move in sequence:
   - Check if move is valid (considering box pushing chain)
   - If valid, update grid and robot position
4. Calculate sum of GPS coordinates for all remaining boxes

### Edge Cases:
- Robot hitting walls directly
- Chain of boxes that can't be pushed (blocked by wall)
- Empty moves (robot can't push infinite boxes)
- Single box pushes vs multiple box chains

## Part 2: Scaled Warehouse

**New Problem**: Everything except the robot is twice as wide!

### Key Changes:
1. **Grid Transformation**: Original grid is doubled in width
   - `#` becomes `##`
   - `O` becomes `[]` (wide boxes)
   - `.` becomes `..`
   - `@` becomes `@.`

2. **Wide Box Logic**: Boxes are now 2 cells wide `[]`
   - Left part `[` and right part `]` must move together
   - Pushing one side affects the entire box
   - Complex collision detection for wide boxes

3. **GPS Calculation**: Distance measured from closest edge of box
   - For `[]` boxes, use position of `[` (left edge)

### Part 2 Data Structures:
- **Wide Grid**: Doubled width grid with 2-cell boxes
- **Box Tracking**: Need to handle `[` and `]` as single units
- **Collision Detection**: More complex for wide boxes pushing multiple boxes

### Part 2 Functions Needed:
1. `scale_grid(grid)` - Transform original grid to doubled width
2. `find_wide_boxes(grid)` - Identify all `[]` box pairs
3. `can_push_wide_box(grid, box_pos, direction)` - Check if wide box can move
4. `execute_wide_move(grid, robot_pos, direction)` - Handle wide box movement
5. `calculate_wide_gps_sum(grid)` - Sum GPS for `[` positions only

### Part 2 Edge Cases:
- Wide boxes pushing multiple other wide boxes simultaneously
- Vertical movement where one wide box pushes two boxes above/below
- Partial box collisions (one side blocked, other free)
- Complex cascading pushes with multiple wide boxes

## Results

### Part 1: ✅ Completed
- **Example**: 2028 GPS sum (matches expected)
- **Actual input**: 1437174 GPS sum

### Part 2: ✅ Completed  
- **Small example (example2.txt)**: 618 GPS sum
- **Large example (example_large.txt)**: 9021 GPS sum (matches expected)
- **Original example (example.txt)**: 1751 GPS sum
- **Actual input**: 1437468 GPS sum

Both parts implemented successfully with proper wide box collision detection using BFS traversal for Part 2.