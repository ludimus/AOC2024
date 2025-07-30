# Day 25: Code Chronicle - Strategy Plan

## Problem Analysis
Find how many unique lock/key pairs fit together without overlapping in any column.

## Key Requirements
- Locks: start with `#####` (filled top row), pins extend downward
- Keys: start with `.....` (empty top row), teeth extend upward from filled bottom row
- Compatibility: lock_height[col] + key_height[col] ≤ 7 for all 5 columns
- Count all valid lock/key combinations

## Data Structures
- **Schematics**: List of 7×5 character grids
- **Locks**: List of height arrays [h0, h1, h2, h3, h4]
- **Keys**: List of height arrays [h0, h1, h2, h3, h4] 
- **Heights**: Count of '#' symbols in each column

## Algorithm Steps
1. Parse input by splitting on blank lines to get individual schematics
2. Classify each schematic as lock (starts with #####) or key (starts with .....)
3. For each schematic, calculate column heights by counting '#' symbols
4. Test all lock/key pairs for compatibility (sum ≤ 7 in each column)
5. Count and return total compatible pairs

## Functions Needed
1. `parse_input(filename)` - Split input into individual schematics
2. `classify_schematic(lines)` - Determine if lock or key
3. `calculate_heights(lines)` - Count '#' per column to get height array
4. `is_compatible(lock_heights, key_heights)` - Check if pair fits
5. `solve(filename)` - Main solution function

## Implementation Plan
1. Read and parse input into schematics
2. Separate locks and keys, convert to height arrays
3. Brute force check all lock/key combinations
4. Count compatible pairs
5. Test with example data first

## Results ✅
- **Example**: 3 compatible pairs (matches expected)
- **Actual input**: **3264** compatible pairs
- **Performance**: 62,500 pairs checked instantly
- **Algorithm**: O(locks × keys × columns) = O(62,500 × 5) - very efficient

## Final Day Notes
Day 25 traditionally has **Part 1 only** - it's the grand finale of Advent of Code!
Simple constraint satisfaction problem with no edge cases, perfect for wrapping up the journey. 🎄🌟