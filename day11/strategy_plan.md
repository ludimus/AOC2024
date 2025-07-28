# Day 11: Plutonian Pebbles - Strategy Plan

## Problem Analysis
Simulate stone transformations over multiple "blinks" where stones change according to specific rules. Count total stones after 25 blinks.

## Transformation Rules (Applied in Order)
1. **If stone = 0**: Replace with stone marked 1
2. **If stone has even number of digits**: Split into two stones (left half and right half of digits, no leading zeros)
3. **Otherwise**: Replace with stone marked (original number × 2024)

## Input Format
- Single line of space-separated integers representing initial stone arrangements
- Example: `125 17`

## Data Structures

### 1. Stone Representation
Use list of integers to represent stones in order:
- `stones = [125, 17]` for initial arrangement
- Maintain order as stones transform

### 2. Transformation Processing
- Process all stones simultaneously (current state → next state)
- Cannot modify list while iterating, so create new list each blink

## Algorithm Steps

### Phase 1: Parse Input
1. Read line and split by spaces
2. Convert strings to integers
3. Store in list/array

### Phase 2: Simulate Blinks
For each blink (1 to 25):
1. Create new empty list for next state
2. For each stone in current state:
   - Apply transformation rules in order
   - Add result(s) to next state list
3. Replace current state with next state

### Phase 3: Count Final Stones
Return length of final stone list

## Functions Needed

1. `parse_input(filename)` - Parse initial stone arrangement
2. `count_digits(number)` - Count digits in a number
3. `split_number(number)` - Split number into left and right halves
4. `transform_stone(stone)` - Apply transformation rules to single stone
5. `simulate_blinks(stones, num_blinks)` - Main simulation loop
6. `main()` - Orchestrate solution with test/debug modes

## Transformation Examples

### Rule Applications:
- `0 → 1` (Rule 1)
- `10 → [1, 0]` (Rule 2: even digits, split "10" → "1", "0")
- `99 → [9, 9]` (Rule 2: even digits, split "99" → "9", "9")
- `999 → 2021976` (Rule 3: 999 × 2024 = 2021976)
- `1000 → [10, 0]` (Rule 2: split "1000" → "10", "0", no leading zeros)

### Step-by-step Example:
```
Initial: [125, 17]
After 1: [253000, 1, 7]     # 125→253000 (×2024), 17→[1,7] (split)
After 2: [253, 0, 2024, 14168]  # 253000→[253,0], 1→2024, 7→14168
...
After 6: 22 stones total
After 25: 55312 stones total
```

## Expected Output

### Part 1 (25 Blinks)
For example input `125 17`:
- After 6 blinks: 22 stones
- After 25 blinks: 55312 stones

For actual input:
- After 25 blinks: 197157 stones

### Part 2 (75 Blinks) 
For example input `125 17`:
- After 75 blinks: Would be trillions of stones

For actual input:
- After 75 blinks: 234430066982597 stones

## Part 1 vs Part 2: The Algorithmic Challenge

| **Aspect** | **Part 1 (25 blinks)** | **Part 2 (75 blinks)** |
|------------|------------------------|------------------------|
| **Approach** | Direct simulation with list | Count-based optimization |
| **Data structure** | `[stone1, stone2, ...]` | `{stone_value: count}` |
| **Memory usage** | ~200K stones | ~54 unique values |
| **Performance** | 0.213s | 0.139s |
| **Scalability** | Exponential growth | Linear in unique values |

## The "Fishy" Part 2 Trap 🐟

**The Deception**: Part 2 looks trivial (just change 25→75)
**The Reality**: Naive approach would require:
- **Memory**: Gigabytes for trillions of stones
- **Time**: Hours of computation
- **Result**: System crash/timeout

**The Insight**: We don't need individual stones, just counts!

## Algorithm Evolution

### Part 1: Direct Simulation
```python
stones = [125, 17, 125, 17]  # Track every stone
# After transformations: [1, 7, 253000, 1, 7, 253000]
```

### Part 2: Count-Based Optimization  
```python
stone_counts = {125: 2, 17: 2}  # Track counts per value
# After transformations: {1: 2, 7: 2, 253000: 2}
```

### Why The Optimization Works:
1. **Identical transformation**: Stones with same value always transform the same way
2. **Order irrelevant**: Final count doesn't depend on stone positions  
3. **Unique values**: Only ~54 unique stone values vs trillions of total stones
4. **Linear scaling**: Processing time depends on unique values, not total count

## Performance Analysis

### Exponential Growth Pattern:
- **25 blinks**: 197,157 stones
- **75 blinks**: 234,430,066,982,597 stones (1.2 million × growth!)

### Optimization Impact:
- **Part 1 approach**: O(total_stones) per blink → exponential explosion
- **Part 2 approach**: O(unique_values) per blink → manageable linear growth

## Final Results
- **Part 1**: 197,157 stones (0.213s with direct simulation)
- **Part 2**: 234,430,066,982,597 stones (0.139s with count optimization)

## Implementation Notes
- Support command line switches for test mode and debug mode
- Test mode uses example.txt, normal mode uses input.txt
- Debug mode shows stone arrangements/counts after each blink
- Part 1: Uses direct simulation for educational value
- Part 2: Uses count-based optimization for scalability
- Custom `--blinks N` parameter for testing different iteration counts

## Key Algorithmic Insights
1. **Recognize the trap**: Simple parameter changes can hide exponential complexity
2. **Find the invariant**: What really matters for the final answer?
3. **Exploit symmetry**: Identical inputs produce identical outputs
4. **Data structure choice**: Sometimes a dictionary beats a list by orders of magnitude
5. **Memory vs computation trade-off**: Smart data structures enable impossible computations