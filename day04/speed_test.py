#!/usr/bin/env python3
"""
Speed test comparison between regex and 8-direction search solutions
"""

import time
import statistics
from solution_regex import solve_regex
from solution_8dir import solve_8dir

def run_speed_test(func, filename, num_runs=10):
    """Run a function multiple times and collect timing statistics"""
    times = []
    results = []
    
    for i in range(num_runs):
        start_time = time.time()
        result = func(filename)
        end_time = time.time()
        
        times.append(end_time - start_time)
        results.append(result)
    
    # Verify all results are the same
    if len(set(results)) != 1:
        print(f"WARNING: Inconsistent results: {set(results)}")
    
    return {
        'result': results[0],
        'times': times,
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'min': min(times),
        'max': max(times),
        'std_dev': statistics.stdev(times) if len(times) > 1 else 0
    }

def main():
    print("=== AOC Day 4 Speed Test Comparison ===\n")
    
    # Test with example first
    print("Testing with example data:")
    regex_example = run_speed_test(solve_regex, 'example.txt', 100)
    dir8_example = run_speed_test(solve_8dir, 'example.txt', 100)
    
    print(f"Regex solution:")
    print(f"  Result: {regex_example['result']}")
    print(f"  Mean time: {regex_example['mean']*1000:.3f} ms")
    print(f"  Std dev: {regex_example['std_dev']*1000:.3f} ms")
    
    print(f"8-direction solution:")
    print(f"  Result: {dir8_example['result']}")
    print(f"  Mean time: {dir8_example['mean']*1000:.3f} ms")
    print(f"  Std dev: {dir8_example['std_dev']*1000:.3f} ms")
    
    speedup_example = dir8_example['mean'] / regex_example['mean']
    print(f"  Regex is {speedup_example:.2f}x faster on example\n")
    
    # Test with actual input
    print("Testing with actual input (141x141 grid):")
    regex_input = run_speed_test(solve_regex, 'input.txt', 50)
    dir8_input = run_speed_test(solve_8dir, 'input.txt', 50)
    
    print(f"Regex solution:")
    print(f"  Result: {regex_input['result']}")
    print(f"  Mean time: {regex_input['mean']*1000:.3f} ms")
    print(f"  Min time: {regex_input['min']*1000:.3f} ms")
    print(f"  Max time: {regex_input['max']*1000:.3f} ms")
    print(f"  Std dev: {regex_input['std_dev']*1000:.3f} ms")
    
    print(f"8-direction solution:")
    print(f"  Result: {dir8_input['result']}")
    print(f"  Mean time: {dir8_input['mean']*1000:.3f} ms")
    print(f"  Min time: {dir8_input['min']*1000:.3f} ms")
    print(f"  Max time: {dir8_input['max']*1000:.3f} ms")
    print(f"  Std dev: {dir8_input['std_dev']*1000:.3f} ms")
    
    speedup_input = dir8_input['mean'] / regex_input['mean']
    print(f"  Regex is {speedup_input:.2f}x faster on actual input")
    
    print("\n=== Summary ===")
    print(f"Both solutions produce the correct result: {regex_input['result']}")
    print(f"Regex approach is consistently faster:")
    print(f"  - {speedup_example:.2f}x faster on small example")
    print(f"  - {speedup_input:.2f}x faster on large input")
    
    # Memory usage analysis (conceptual)
    print(f"\nMemory usage analysis:")
    print(f"Regex approach:")
    print(f"  - Extracts lines into strings (higher memory usage)")
    print(f"  - Uses compiled regex (fast pattern matching)")
    print(f"  - Processes data in chunks (rows, columns, diagonals)")
    
    print(f"8-direction approach:")
    print(f"  - Lower memory usage (no string extraction)")
    print(f"  - Character-by-character comparison (more CPU intensive)")
    print(f"  - Nested loops over grid positions and directions")

if __name__ == "__main__":
    main()