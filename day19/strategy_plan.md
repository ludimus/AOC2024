# Day 19: Linen Layout - Strategy Plan

## Problem Analysis
- Classic "Word Break" problem - can target strings be segmented using dictionary patterns
- Given: Available towel patterns (unlimited quantity)
- Goal: Count how many designs can be formed using these patterns

## Data Structures
- **Patterns**: Set of available towel patterns for O(1) lookup
- **Designs**: List of target designs to check
- **Memoization**: Cache for recursive approach

## Algorithm 1: Dynamic Programming
1. For each design, create boolean array `dp[i]` = "can form first i characters"
2. `dp[0] = True` (empty string always possible)
3. For each position i, check all patterns that could end at position i
4. If pattern matches and `dp[i-pattern_length]` is True, set `dp[i] = True`
5. Return `dp[len(design)]`

**Time**: O(n² × p) where n=design length, p=pattern count
**Space**: O(n)

## Algorithm 2: Recursive + Memoization
1. Try each pattern at current position in design
2. If pattern matches, recursively check remainder of design
3. Use memoization to cache results for substrings
4. Base case: empty string returns True

**Time**: O(n² × p)
**Space**: O(n) for recursion + memoization

## Functions Needed
1. `parse_input(filename)`: Parse patterns and designs from input
2. `can_form_dp(design, patterns)`: DP approach
3. `can_form_recursive(design, patterns, memo, start)`: Recursive approach
4. `solve_both_methods(patterns, designs)`: Compare both solutions

## Testing Strategy
- Example: 6 out of 8 designs should be possible
- Compare results from both algorithms to ensure consistency

## Part 2 Analysis
- Count ALL possible ways to form each design (not just if possible)
- Same algorithms but return counts instead of booleans
- Example total: 16 arrangements (2+1+4+6+1+2+0+0)

## Part 2 Algorithms
**DP Counting**: `dp[i]` = number of ways to form first i characters
**Recursive Counting**: Sum all valid recursive paths instead of OR-ing boolean results