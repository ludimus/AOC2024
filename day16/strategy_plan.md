# Day 16: Reindeer Maze - Strategy Plan

## Problem Summary
- Find the lowest score path from Start (S) to End (E) in a maze
- Reindeer starts facing East
- Scoring: Move forward = 1 point, Rotate 90° = 1000 points
- Cannot move into walls (#)

## Data Structures
- **Grid**: 2D list representing the maze
- **Position**: (row, col) coordinates
- **Direction**: 0=East, 1=South, 2=West, 3=North (for easy rotation math)
- **State**: (row, col, direction) - position + facing direction
- **Priority Queue**: For Dijkstra's algorithm with (cost, state)

## Algorithm Approach
Use **Dijkstra's algorithm** with state = (position, direction):

1. **State Space**: Each cell can be visited from 4 different directions
2. **Transitions**:
   - Move forward: cost +1, same direction
   - Rotate clockwise: cost +1000, direction = (dir + 1) % 4
   - Rotate counterclockwise: cost +1000, direction = (dir - 1) % 4

3. **Implementation**:
   - Parse maze to find S and E positions
   - Initialize with start state (S_pos, direction=0) with cost 0
   - Use priority queue to explore lowest cost states first
   - Track visited states to avoid cycles
   - Stop when reaching E with any direction

## Functions Needed
1. `parse_input(filename)` - Parse maze, return grid, start_pos, end_pos
2. `get_neighbors(state, grid)` - Get valid next states with costs
3. `dijkstra(grid, start_pos, end_pos)` - Main pathfinding algorithm
4. Part 1: Find minimum cost to reach end
5. Part 2: (likely) Count all tiles on optimal paths

## Simple Dijkstra Example
```python
import heapq

def dijkstra(grid, start_pos, end_pos):
    # Directions: 0=East, 1=South, 2=West, 3=North
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    # Priority queue: (cost, row, col, direction)
    pq = [(0, start_pos[0], start_pos[1], 0)]  # Start facing East
    visited = set()
    
    while pq:
        cost, row, col, direction = heapq.heappop(pq)
        
        # If we reached the end, return cost
        if (row, col) == end_pos:
            return cost
            
        # Skip if already visited this state
        state = (row, col, direction)
        if state in visited:
            continue
        visited.add(state)
        
        # Try moving forward
        dr, dc = directions[direction]
        new_row, new_col = row + dr, col + dc
        if grid[new_row][new_col] != '#':
            heapq.heappush(pq, (cost + 1, new_row, new_col, direction))
        
        # Try rotating clockwise and counterclockwise
        heapq.heappush(pq, (cost + 1000, row, col, (direction + 1) % 4))
        heapq.heappush(pq, (cost + 1000, row, col, (direction - 1) % 4))
    
    return -1  # No path found
```

## Expected Results
- Example 1: 7036 points (36 steps + 7 turns)
- Example 2: 11048 points

## Part 2: All Optimal Path Tiles

### Problem Analysis
- Need to find ALL tiles that are part of ANY optimal path
- Multiple paths can have the same minimum cost
- Must count unique tile positions, not path states

### Strategy Options
1. **Bidirectional Search**: Run Dijkstra from start AND from end, find intersections
2. **Backtracking**: Find min cost, then trace all paths with that cost
3. **Modified Dijkstra**: Track all predecessors for each state

### Chosen Approach: Modified Dijkstra with Predecessor Tracking
1. Run Dijkstra but track ALL predecessors that lead to optimal cost for each state
2. Once we find the minimum cost to reach end, backtrack from all end states
3. Collect all tiles visited during backtracking

### Implementation Details
```python
# For each state, track:
# - best_cost[state] = minimum cost to reach this state
# - predecessors[state] = list of all states that can reach this with optimal cost

# After finding min_cost to end:
# - Start from all end states with cost = min_cost
# - BFS/DFS backward through predecessors
# - Collect all unique (row, col) positions
```

### Expected Part 2 Results
- Example 1: 45 tiles on optimal paths
- Example 2: 64 tiles on optimal paths

## Final Results
- **Part 1**: 85432 (minimum cost path)
- **Part 2**: 465 (tiles on all optimal paths)

## Implementation Notes
- Part 1: Standard Dijkstra with state = (row, col, direction)
- Part 2: Modified Dijkstra tracking all predecessors, then backtrack from optimal end states
- Key insight: State space must include direction since rotation costs differ from movement
- Both solutions handle multiple optimal paths correctly

## Why heapq Instead of Standard Data Structures?

**Dijkstra's algorithm requires a priority queue** to always process the lowest-cost unvisited state first. This greedy approach guarantees optimal paths.

**Python's standard alternatives and why they fail:**

1. **Regular list with sorting**:
   - Inserting in sorted order: O(n) per insertion
   - With thousands of states, this becomes extremely slow
   - heapq provides O(log n) insertion instead

2. **deque (collections.deque)**:
   - Only supports FIFO/LIFO ordering, no priority
   - Would give breadth-first search, not Dijkstra
   - BFS doesn't guarantee optimal paths when edge weights differ (1 vs 1000 cost)

3. **set**:
   - No ordering capability at all
   - Cannot efficiently retrieve minimum-cost element

**What heapq provides:**
- `heappush()`: O(log n) to insert with priority
- `heappop()`: O(log n) to extract minimum element  
- Maintains heap property automatically (parent ≤ children)

**Critical for this maze problem:**
- Moving costs 1 point, rotating costs 1000 points
- Must explore cheaper paths first to guarantee optimality
- ~20,000 possible states (141×141 grid × 4 directions) require efficient operations
- Without proper priority ordering: wrong answers or terrible performance