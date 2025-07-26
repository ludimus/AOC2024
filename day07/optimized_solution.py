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

def can_make_target_reverse(target: int, numbers: List[int], depth: int = 0, debug: bool = False) -> bool:
    """
    Reverse engineering approach: work backwards from target.
    
    Instead of trying all combinations forward, we ask:
    "What could the second-to-last result be, given the last operation?"
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
        if can_make_target_reverse(new_target, remaining, depth + 1, debug):
            return True
    
    # Case 2: ... * last_num = target
    # So: ... = target / last_num (must be exact division)
    if target % last_num == 0:
        new_target = target // last_num
        if debug:
            print(f"{indent}Try multiplication: ? * {last_num} = {target} -> ? = {new_target}")
        if can_make_target_reverse(new_target, remaining, depth + 1, debug):
            return True
    
    # Case 3: ... || last_num = target
    # So: target must end with last_num's digits
    # Example: 1234 || 567 = 1234567, so if target=1234567 and last_num=567, then ?=1234
    last_str = str(last_num)
    target_str = str(target)
    
    if len(target_str) > len(last_str) and target_str.endswith(last_str):
        new_target_str = target_str[:-len(last_str)]
        new_target = int(new_target_str)
        if debug:
            print(f"{indent}Try concatenation: ? || {last_num} = {target} -> ? = {new_target}")
        if can_make_target_reverse(new_target, remaining, depth + 1, debug):
            return True
    
    if debug:
        print(f"{indent}No valid operations found")
    return False

def demonstrate_reverse_engineering():
    """Show step-by-step how reverse engineering works."""
    print("Reverse Engineering Examples")
    print("=" * 50)
    
    examples = [
        (190, [10, 19]),        # 10 * 19 = 190
        (3267, [81, 40, 27]),   # 81 + 40 * 27 = 3267 
        (156, [15, 6]),         # 15 || 6 = 156
        (7290, [6, 8, 6, 15]),  # 6 * 8 || 6 * 15 = 7290
        (192, [17, 8, 14]),     # 17 || 8 + 14 = 192
    ]
    
    for target, numbers in examples:
        print(f"\nExample: {target}: {numbers}")
        print("-" * 30)
        result = can_make_target_reverse(target, numbers, debug=True)
        print(f"Result: {'✓ POSSIBLE' if result else '✗ IMPOSSIBLE'}")
        print()

def compare_performance():
    """Compare brute force vs reverse engineering performance."""
    print("Performance Comparison")
    print("=" * 50)
    
    # Load example data
    equations = parse_input('example.txt')
    
    # Test reverse engineering
    start_time = time.time()
    achievable_reverse = 0
    for target, numbers in equations:
        if can_make_target_reverse(target, numbers):
            achievable_reverse += 1
    reverse_time = time.time() - start_time
    
    print(f"Reverse Engineering:")
    print(f"  Time: {reverse_time:.6f} seconds")
    print(f"  Achievable: {achievable_reverse}/9")
    
    # For comparison, we'd need to import the brute force version
    # But we can estimate the theoretical improvement
    
    # Theoretical analysis
    max_operators = max(len(nums) - 1 for _, nums in equations)
    brute_force_combinations = sum(3 ** (len(nums) - 1) for _, nums in equations)
    reverse_max_operations = sum(3 * (len(nums) - 1) for _, nums in equations)  # Worst case
    
    print(f"\nTheoretical Complexity:")
    print(f"  Brute force combinations: {brute_force_combinations}")
    print(f"  Reverse max operations: {reverse_max_operations}")
    print(f"  Improvement factor: {brute_force_combinations / reverse_max_operations:.1f}x")

def solve_with_optimization(equations: List[Tuple[int, List[int]]], verbose: bool = False) -> int:
    """Solve using optimized reverse engineering approach."""
    start_time = time.time()
    total = 0
    achievable_count = 0
    
    for i, (target, numbers) in enumerate(equations):
        if can_make_target_reverse(target, numbers):
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
    
    print(f"\nOptimized Performance Summary:")
    print(f"Total equations: {len(equations)}")
    print(f"Achievable: {achievable_count}/{len(equations)} ({achievable_count/len(equations)*100:.1f}%)")
    print(f"Time elapsed: {elapsed:.3f} seconds")
    print(f"Equations per second: {len(equations)/elapsed:.1f}")
    
    return total

def test_optimized_full():
    """Test optimized solution on full input."""
    print("Testing Optimized Solution on Full Input")
    print("=" * 50)
    
    equations = parse_input('input.txt')
    total = solve_with_optimization(equations)
    print(f"\nOptimized Part 2 Answer: {total}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "full":
        test_optimized_full()
    elif len(sys.argv) > 1 and sys.argv[1] == "compare":
        compare_performance()
    else:
        demonstrate_reverse_engineering()
        print("\n")
        compare_performance()