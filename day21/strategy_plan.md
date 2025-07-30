# Day 21: Keypad Conundrum - Strategy Plan

## Problem Summary
Multi-layer keypad control system where you control a chain of 3 robots to enter codes on a numeric keypad. Calculate the complexity of each code (sequence_length × numeric_value).

## Results
- **Part 1:** 174,124 total complexity (3 layers)
- **Part 2:** 216,668,579,770,346 total complexity (26 layers)

## Keypad Hierarchy (4 levels)
1. **You** → Directional keypad
2. **Robot 1** → Directional keypad (controlled by you)  
3. **Robot 2** → Directional keypad (controlled by Robot 1)
4. **Robot 3** → Numeric keypad (controlled by Robot 2)

## Keypad Layouts

### Numeric Keypad
```
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
```

### Directional Keypad  
```
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
```

## Data Structures
- `numeric_keypad`: Dict mapping buttons to (row, col) coordinates
- `directional_keypad`: Dict mapping buttons to (row, col) coordinates  
- `paths_cache`: Memoization for shortest paths between button pairs
- `sequence_cache`: Memoization for multi-layer sequence generation

## Algorithm Approach

### 1. Keypad Mapping
- Map each button to coordinates for both keypad types
- Identify gap positions to avoid during pathfinding

### 2. Shortest Path Generation
- For each keypad type, precompute shortest paths between all button pairs
- Use BFS to find paths, avoiding gaps
- Multiple valid shortest paths may exist - need to consider all

### 3. Multi-Layer Sequence Generation
- Start with target code (e.g., "029A")
- Work backwards through each control layer:
  1. Numeric keypad → directional sequences
  2. Each directional layer → next directional sequences  
- Use memoization to avoid recalculating common subsequences

### 4. Complexity Calculation
- For each code: `complexity = min_sequence_length × numeric_part`
- Sum all complexities for the final answer

## Implementation Details
- All robots start at 'A' button
- Cannot move through gaps (causes panic)
- Need to press 'A' to activate current button
- Multiple shortest paths exist - must consider all to find true minimum

## Critical Insights & Optimizations

### Initial Approach Issues
- **Exponential explosion**: Generating all possible full sequences leads to exponential growth
- **Deep recursion overhead**: Complex recursive calls with sequence generation
- **Memory/time complexity**: Combinatorial explosion made the approach slow and complex

### Final Optimized Strategy (solution_fast.py)
- **Button-to-button cost calculation**: Instead of full sequences, calculate the cost of each individual button transition
- **Layer-by-layer processing**: Use `get_move_cost(from_btn, to_btn, depth)` to handle each layer independently
- **Efficient memoization**: Cache button transition costs rather than full sequence results
- **Direct keypad handling**: Choose keypad type based on layer depth without complex switching

### Key Technical Breakthroughs
- **Transition-based DP**: Each button press becomes a cost calculation, not sequence generation
- **Minimal path exploration**: Only consider horizontal-first and vertical-first orderings
- **Clean recursion**: Simple depth-based recursion without complex state management
- **Gap avoidance**: Validate paths during generation, not after

### Performance Impact
- **Before**: Complex recursive approach, slow execution (minutes)
- **After**: Clean transition-based DP, extremely fast (0.024s for Part 1, 0.054s for Part 2)
- **Scalability**: Handles 26 layers efficiently due to optimal memoization strategy
- **Accuracy**: Still finds true optimal solutions by considering all valid shortest paths

## Functions (Final Optimized Version)
- `get_shortest_paths(start_pos, end_pos, gap_pos)`: Generate valid shortest paths between positions
- `get_move_cost(from_btn, to_btn, depth, is_numeric)`: Calculate minimum cost for button transition at given depth
- `calculate_sequence_cost(code, layers)`: Calculate total cost for entering a complete code
- `calculate_complexity(code, layers)`: Get final sequence length and multiply by numeric value
- `main()`: Process all codes with configurable layer depth for Part 1/2