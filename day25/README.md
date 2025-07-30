# Day 25: Code Chronicle 🎄

## Problem Summary

**Final Day!** Help The Historians unlock the Chief Historian's office by finding which lock/key pairs fit together without overlapping.

- **Locks**: Start with `#####` (pins extend downward)
- **Keys**: Start with `.....` (teeth extend upward from bottom `#####`)
- **Goal**: Count compatible lock/key pairs where column heights don't exceed 7

## Solution

**Part 1 Only**: Find compatible lock/key pairs
- **Algorithm**: Brute force check all combinations
- **Complexity**: O(locks × keys × columns) = O(250 × 250 × 5)
- **Result**: **3264** compatible pairs

## Key Implementation

1. **Parse**: Split input on blank lines into 500 schematics
2. **Classify**: Locks vs keys based on first row pattern
3. **Calculate Heights**: Count '#' symbols per column
4. **Check Compatibility**: Ensure `lock_height[i] + key_height[i] ≤ 7` for all columns
5. **Count**: Sum all valid combinations

## Files

- `solution_part1.py` - Main solution (no Part 2 for Day 25!)
- `example.txt` - Test data from problem description
- `analyze_challenge.py` - Educational analysis of the problem
- `strategy_plan.md` - Complete implementation strategy

## Running

```bash
# Part 1
python3 solution_part1.py [--test] [--debug]

# Analysis
python3 analyze_challenge.py
```

## Final Day Notes

Day 25 traditionally has only Part 1 - it's the grand finale! 🎉
A simpler, satisfying problem that wraps up the 25-day Advent of Code journey.

**🌟 Advent of Code 2024 Complete! 🌟**