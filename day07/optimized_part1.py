from typing import List, Tuple
import time

def parse_input(filename: str) -> List[Tuple[int, List[int]]]:
    """Parse input file and return list of (target, numbers) tuples."""
    equations = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            target_str, numbers_str = line.split(':', 1)
            target = int(target_str.strip())
            numbers = [int(x) for x in numbers_str.strip().split()]
            equations.append((target, numbers))
    
    return equations

def can_make_target_part1(target: int, numbers: List[int], depth: int = 0, debug: bool = False) -> bool:
    """
    Reverse engineering approach for Part 1: only + and * operators.
    Work backwards from target to find if it's achievable.
    """
    indent = "  " * depth
    if debug:
        print(f"{indent}can_make({target}, {numbers})")
    
    # Base case: only one number left
    if len(numbers) == 1:
        result = target == numbers[0]
        if debug:
            print(f"{indent}Base case: {target} == {numbers[0]} -> {result}")
        return result
    
    # Get the last number and the remaining numbers
    last_num = numbers[-1]
    remaining = numbers[:-1]
    
    if debug:
        print(f"{indent}Last number: {last_num}, Remaining: {remaining}")
    
    # Try each possible last operation that could have produced 'target'
    
    # Case 1: ... + last_num = target
    # So: ... = target - last_num
    if target >= last_num:
        new_target = target - last_num
        if debug:
            print(f"{indent}Try addition: ? + {last_num} = {target} -> ? = {new_target}")
        if can_make_target_part1(new_target, remaining, depth + 1, debug):
            return True
    
    # Case 2: ... * last_num = target
    # So: ... = target / last_num (must be exact division)
    if target % last_num == 0:
        new_target = target // last_num
        if debug:
            print(f"{indent}Try multiplication: ? * {last_num} = {target} -> ? = {new_target}")
        if can_make_target_part1(new_target, remaining, depth + 1, debug):
            return True
    
    if debug:
        print(f"{indent}No valid operations found")
    return False

def demonstrate_part1_examples():
    """Show step-by-step how reverse engineering works for Part 1."""
    print("Part 1 Reverse Engineering Examples")
    print("=" * 50)
    
    examples = [
        (190, [10, 19]),        # 10 * 19 = 190
        (3267, [81, 40, 27]),   # 81 + 40 * 27 = 3267 OR 81 * 40 + 27 = 3267
        (83, [17, 5]),          # No solution
        (156, [15, 6]),         # No solution (would need concatenation)
        (292, [11, 6, 16, 20]), # 11 + 6 * 16 + 20 = 292
    ]
    
    for target, numbers in examples:
        print(f"\nExample: {target}: {numbers}")
        print("-" * 30)
        result = can_make_target_part1(target, numbers, debug=True)
        print(f"Result: {'✓ POSSIBLE' if result else '✗ IMPOSSIBLE'}")
        print()

def solve_part1_optimized(equations: List[Tuple[int, List[int]]], verbose: bool = False) -> int:
    """Solve Part 1 using optimized reverse engineering approach."""
    start_time = time.time()
    total = 0
    achievable_count = 0
    
    for i, (target, numbers) in enumerate(equations):
        if can_make_target_part1(target, numbers):
            total += target
            achievable_count += 1
            if verbose:
                print(f"✓ {target}: {numbers}")
        else:
            if verbose:
                print(f"✗ {target}: {numbers}")
        
        if (i + 1) % 100 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i+1}/{len(equations)} equations ({elapsed:.3f}s)")
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"\nOptimized Part 1 Performance Summary:")
    print(f"Total equations: {len(equations)}")
    print(f"Achievable: {achievable_count}/{len(equations)} ({achievable_count/len(equations)*100:.1f}%)")
    print(f"Time elapsed: {elapsed:.3f} seconds")
    print(f"Equations per second: {len(equations)/elapsed:.1f}")
    
    return total

def test_example_data():
    """Test optimized Part 1 solution on example data."""
    print("Testing Optimized Part 1 on Example Data")
    print("=" * 50)
    
    equations = parse_input('example.txt')
    
    print("Full solution:")
    total = solve_part1_optimized(equations, verbose=True)
    print(f"\nOptimized Part 1 Answer: {total}")
    print(f"Expected: 3749")

def test_full_input():
    """Test optimized Part 1 solution on full input."""
    print("Testing Optimized Part 1 on Full Input")
    print("=" * 50)
    
    equations = parse_input('input.txt')
    total = solve_part1_optimized(equations)
    print(f"\nOptimized Part 1 Answer: {total}")

def compare_with_brute_force():
    """Compare performance with original brute force approach."""
    print("Performance Comparison: Optimized vs Brute Force")
    print("=" * 60)
    
    equations = parse_input('example.txt')
    
    # Test optimized approach
    start_time = time.time()
    optimized_total = 0
    for target, numbers in equations:
        if can_make_target_part1(target, numbers):
            optimized_total += target
    optimized_time = time.time() - start_time
    
    print(f"Optimized Approach:")
    print(f"  Time: {optimized_time:.6f} seconds")
    print(f"  Answer: {optimized_total}")
    
    # Theoretical analysis
    brute_force_combinations = sum(2 ** (len(nums) - 1) for _, nums in equations)
    reverse_max_operations = sum(2 * (len(nums) - 1) for _, nums in equations)  # Worst case
    
    print(f"\nTheoretical Complexity:")
    print(f"  Brute force combinations: {brute_force_combinations}")
    print(f"  Reverse max operations: {reverse_max_operations}")
    print(f"  Improvement factor: {brute_force_combinations / reverse_max_operations:.1f}x")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "full":
            test_full_input()
        elif sys.argv[1] == "compare":
            compare_with_brute_force()
        elif sys.argv[1] == "example":
            test_example_data()
    else:
        demonstrate_part1_examples()
        print("\n")
        test_example_data()
        print("\n")
        compare_with_brute_force()