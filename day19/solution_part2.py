#!/usr/bin/env python3

import sys
from functools import lru_cache

def parse_input(filename):
    """Parse input file and return patterns and designs."""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    
    # First line contains patterns
    patterns = [p.strip() for p in lines[0].split(',')]
    
    # Remaining lines (after blank line) contain designs
    designs = []
    for line in lines[2:]:  # Skip first line and blank line
        if line.strip():
            designs.append(line.strip())
    
    return patterns, designs

def count_ways_dp(design, patterns):
    """Count ways design can be formed using DP approach."""
    n = len(design)
    dp = [0] * (n + 1)
    dp[0] = 1  # Base case: one way to form empty string
    
    for i in range(1, n + 1):
        for pattern in patterns:
            pattern_len = len(pattern)
            if (pattern_len <= i and 
                design[i - pattern_len:i] == pattern):
                dp[i] += dp[i - pattern_len]
    
    return dp[n]

def count_ways_recursive(design, patterns):
    """Count ways design can be formed using recursive + memoization approach."""
    
    @lru_cache(maxsize=None)
    def helper(start_idx):
        if start_idx == len(design):
            return 1  # Found one complete way
        
        total_ways = 0
        for pattern in patterns:
            pattern_len = len(pattern)
            if (start_idx + pattern_len <= len(design) and
                design[start_idx:start_idx + pattern_len] == pattern):
                total_ways += helper(start_idx + pattern_len)
        
        return total_ways
    
    return helper(0)

def solve_both_methods(patterns, designs, debug=False):
    """Solve using both methods and compare results."""
    results_dp = []
    results_recursive = []
    
    for design in designs:
        # Method 1: Dynamic Programming
        count_dp = count_ways_dp(design, patterns)
        results_dp.append(count_dp)
        
        # Method 2: Recursive + Memoization
        count_recursive = count_ways_recursive(design, patterns)
        results_recursive.append(count_recursive)
        
        if debug:
            print(f"{design}: DP={count_dp}, Recursive={count_recursive}")
    
    # Verify both methods give same results
    if results_dp != results_recursive:
        print("WARNING: Methods gave different results!")
        for i, (dp, rec) in enumerate(zip(results_dp, results_recursive)):
            if dp != rec:
                print(f"  {designs[i]}: DP={dp}, Recursive={rec}")
    
    return sum(results_dp), sum(results_recursive), results_dp

def main():
    # Parse command line arguments
    test_mode = '--test' in sys.argv
    debug_mode = '--debug' in sys.argv
    
    filename = 'example.txt' if test_mode else 'input.txt'
    
    # Parse input
    patterns, designs = parse_input(filename)
    
    if debug_mode:
        print(f"Patterns: {patterns}")
        print(f"Number of designs: {len(designs)}")
        print(f"Designs: {designs}")
        print()
    
    # Solve using both methods
    total_dp, total_recursive, individual_counts = solve_both_methods(patterns, designs, debug_mode)
    
    if debug_mode:
        print(f"\nResults:")
        print(f"DP method total: {total_dp}")
        print(f"Recursive method total: {total_recursive}")
        print(f"Individual counts: {individual_counts}")
        if test_mode:
            expected = [2, 1, 4, 6, 0, 1, 2, 0]
            print(f"Expected counts: {expected}")
            print(f"Expected total: {sum(expected)}")
    else:
        print(f"Total arrangements: {total_dp}")

if __name__ == "__main__":
    main()