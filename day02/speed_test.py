import time
import solution_original
import solution_differences

def time_function(func, iterations=1000):
    """Time a function over multiple iterations."""
    start_time = time.perf_counter()
    for _ in range(iterations):
        result = func()
    end_time = time.perf_counter()
    return end_time - start_time, result

def main():
    print("Speed Test: Original vs Difference List Algorithms")
    print("=" * 60)
    
    # Test Part 1
    print("\nPART 1 COMPARISON:")
    print("-" * 30)
    
    # Original algorithm
    orig_time, orig_result = time_function(solution_original.solve_part1, 1000)
    print(f"Original Algorithm:")
    print(f"  Result: {orig_result}")
    print(f"  Time (1000 runs): {orig_time:.4f} seconds")
    print(f"  Avg per run: {orig_time/1000:.6f} seconds")
    
    # Difference algorithm
    diff_time, diff_result = time_function(solution_differences.solve_part1, 1000)
    print(f"\nDifference Algorithm:")
    print(f"  Result: {diff_result}")
    print(f"  Time (1000 runs): {diff_time:.4f} seconds")
    print(f"  Avg per run: {diff_time/1000:.6f} seconds")
    
    # Compare results
    if orig_result == diff_result:
        print(f"\n✓ Results match: {orig_result}")
    else:
        print(f"\n✗ Results differ! Original: {orig_result}, Difference: {diff_result}")
    
    # Speed comparison
    if diff_time < orig_time:
        speedup = orig_time / diff_time
        print(f"🚀 Difference algorithm is {speedup:.2f}x faster")
    else:
        slowdown = diff_time / orig_time
        print(f"🐌 Difference algorithm is {slowdown:.2f}x slower")
    
    # Test Part 2
    print("\n" + "=" * 60)
    print("\nPART 2 COMPARISON:")
    print("-" * 30)
    
    # Original algorithm
    orig_time, orig_result = time_function(solution_original.solve_part2, 100)
    print(f"Original Algorithm:")
    print(f"  Result: {orig_result}")
    print(f"  Time (100 runs): {orig_time:.4f} seconds")
    print(f"  Avg per run: {orig_time/100:.6f} seconds")
    
    # Difference algorithm
    diff_time, diff_result = time_function(solution_differences.solve_part2, 100)
    print(f"\nDifference Algorithm:")
    print(f"  Result: {diff_result}")
    print(f"  Time (100 runs): {diff_time:.4f} seconds")
    print(f"  Avg per run: {diff_time/100:.6f} seconds")
    
    # Compare results
    if orig_result == diff_result:
        print(f"\n✓ Results match: {orig_result}")
    else:
        print(f"\n✗ Results differ! Original: {orig_result}, Difference: {diff_result}")
    
    # Speed comparison
    if diff_time < orig_time:
        speedup = orig_time / diff_time
        print(f"🚀 Difference algorithm is {speedup:.2f}x faster")
    else:
        slowdown = diff_time / orig_time
        print(f"🐌 Difference algorithm is {slowdown:.2f}x slower")

if __name__ == "__main__":
    main()