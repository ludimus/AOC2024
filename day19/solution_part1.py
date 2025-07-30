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

def can_form_dp(design, patterns):
    """Check if design can be formed using DP approach."""
    n = len(design)
    dp = [False] * (n + 1)
    dp[0] = True  # Base case: empty string
    
    pattern_set = set(patterns)  # O(1) lookup
    
    for i in range(1, n + 1):
        for pattern in patterns:
            pattern_len = len(pattern)
            if (pattern_len <= i and 
                dp[i - pattern_len] and 
                design[i - pattern_len:i] == pattern):
                dp[i] = True
                break
    
    return dp[n]

def can_form_recursive(design, patterns):
    """Check if design can be formed using recursive + memoization approach."""
    pattern_set = set(patterns)
    
    @lru_cache(maxsize=None)
    def helper(start_idx):
        if start_idx == len(design):
            return True
        
        for pattern in patterns:
            pattern_len = len(pattern)
            if (start_idx + pattern_len <= len(design) and
                design[start_idx:start_idx + pattern_len] == pattern):
                if helper(start_idx + pattern_len):
                    return True
        
        return False
    
    return helper(0)

def solve_both_methods(patterns, designs, debug=False):
    """Solve using both methods and compare results."""
    results_dp = []
    results_recursive = []
    
    for design in designs:
        # Method 1: Dynamic Programming
        result_dp = can_form_dp(design, patterns)
        results_dp.append(result_dp)
        
        # Method 2: Recursive + Memoization
        result_recursive = can_form_recursive(design, patterns)
        results_recursive.append(result_recursive)
        
        if debug:
            print(f"{design}: DP={result_dp}, Recursive={result_recursive}")
    
    # Verify both methods give same results
    if results_dp != results_recursive:
        print("WARNING: Methods gave different results!")
    
    return sum(results_dp), sum(results_recursive)

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
    count_dp, count_recursive = solve_both_methods(patterns, designs, debug_mode)
    
    if debug_mode:
        print(f"\nResults:")
        print(f"DP method: {count_dp} possible designs")
        print(f"Recursive method: {count_recursive} possible designs")
    else:
        print(f"Possible designs: {count_dp}")

if __name__ == "__main__":
    main()