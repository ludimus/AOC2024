# Day 10: Hoof It - Strategy Plan

## Problem Analysis
Find hiking trails on a topographic map where trails start at height 0, end at height 9, and increase by exactly 1 at each step. Calculate the sum of all trailhead scores.

## Input Format
- Grid of digits 0-9 representing heights
- Each position has a single digit height
- Example: 8x8 grid with various height patterns

## Data Structures

### 1. Grid Representation
Use 2D list/array to represent the topographic map:
- `grid[row][col]` = height at position (row, col)
- Convert input strings to integers for easy comparison

### 2. Position Tracking
- `(row, col)` tuples for coordinates
- Directions: up, down, left, right (no diagonals)
- Boundary checking for valid moves

### 3. Path Finding
- BFS or DFS to explore valid hiking trails
- Track visited positions to avoid cycles
- Set to store reachable 9-height positions per trailhead

## Algorithm Steps

### Phase 1: Parse Input and Build Grid
1. Read input file line by line
2. Convert each character to integer height
3. Build 2D grid representation

### Phase 2: Find All Trailheads
1. Scan grid for positions with height 0
2. Store trailhead positions as starting points

### Phase 3: Calculate Trailhead Scores
For each trailhead (height 0 position):
1. Use BFS/DFS to explore all valid paths
2. Valid move: adjacent cell with height = current_height + 1
3. Track all reachable height 9 positions
4. Score = count of unique reachable 9s

### Phase 4: Sum All Scores
Add up scores from all trailheads

## Functions Needed

1. `parse_input(filename)` - Parse grid from input file
2. `find_trailheads(grid)` - Find all positions with height 0
3. `get_valid_moves(grid, row, col)` - Get adjacent cells with height+1
4. `calculate_trailhead_score(grid, start_row, start_col)` - BFS/DFS to find reachable 9s
5. `main()` - Orchestrate solution with test/debug modes

## Expected Output

### Part 1 (Trailhead Scores - Unique 9s Reachable)
For the large example (8x8 grid):
- 9 trailheads with scores: 5, 6, 5, 3, 1, 3, 5, 3, 5
- Sum of all scores: 36

### Part 2 (Trailhead Ratings - Distinct Trail Counts)
For the same example:
- 9 trailheads with ratings: 20, 24, 10, 4, 1, 4, 5, 8, 5
- Sum of all ratings: 81

## Part 1 vs Part 2 Key Differences

| **Aspect** | **Part 1 (Score)** | **Part 2 (Rating)** |
|------------|-------------------|---------------------|
| **Metric** | Count unique 9-height destinations | Count distinct hiking trails |
| **Multiple paths to same 9** | Only count destination once | Count each path separately |
| **Algorithm fit** | BFS (sparse, goal-oriented) | Layer propagation (path counting) |
| **Data structure** | Set of reachable positions | Path count accumulation |

## Algorithm Analysis & Optimization Journey

### Initial Implementation: BFS Approach
**Concept**: Breadth-first search from each trailhead to find reachable 9s
**Part 1 Performance**: 0.035s ⚡ (Winner for Part 1)
**Part 2 Applicability**: ❌ Cannot count distinct paths (BFS avoids revisiting)

### Optimization Attempt: Layer-by-Layer Propagation
**Concept**: Process all positions at each height level systematically
**Part 1 Performance**: 0.126s (3.6x slower than BFS)
**Part 2 Performance**: 0.161s ⚡ (Perfect fit for path counting)

### Performance Insights

**Why BFS Won Part 1:**
- Early termination when reaching height 9
- Sparse exploration (only follows valid trails)
- No overhead from processing entire grid

**Why Layer Propagation Won Part 2:**
- Natural path accumulation through dynamic programming
- Handles path multiplication (multiple routes to same destination)
- Systematic processing prevents missing any trails

## Final Results
- **Part 1**: Score sum 760 (0.035s with BFS)
- **Part 2**: Rating sum 1764 (0.161s with layer propagation)

## Implementation Notes
- Support command line switches for test mode and debug mode
- Test mode uses example.txt, normal mode uses input.txt
- Debug mode shows trailhead positions and detailed path counts
- Part 1: Uses BFS for optimal performance
- Part 2: Uses layer propagation for path counting via dynamic programming

## Key Algorithmic Insights
1. **Problem type determines optimal approach**: Destination counting vs. path counting require different strategies
2. **Early vs. comprehensive processing**: BFS wins for sparse search, layer propagation wins for exhaustive analysis
3. **Algorithm prediction**: The "slower" optimization became the perfect solution for Part 2
4. **Dynamic programming power**: Path counts naturally accumulate through systematic layer processing