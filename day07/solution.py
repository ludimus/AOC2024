from typing import List, Tuple
from itertools import product
import time

def parse_input(filename: str) -> List[Tuple[int, List[int]]]:
    """Parse input file and return list of (target, numbers) tuples."""
    equations = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Split on colon
            target_str, numbers_str = line.split(':', 1)
            target = int(target_str.strip())
            
            # Split numbers on whitespace
            numbers = [int(x) for x in numbers_str.strip().split()]
            
            equations.append((target, numbers))
    
    return equations

def evaluate_left_to_right(numbers: List[int], operators: List[str]) -> int:
    """Evaluate numbers with operators from left to right."""
    result = numbers[0]
    
    for i, op in enumerate(operators):
        if op == '+':
            result += numbers[i + 1]
        elif op == '*':
            result *= numbers[i + 1]
    
    return result

def can_make_target(target: int, numbers: List[int]) -> bool:
    """Check if target can be made by placing operators between numbers."""
    if len(numbers) == 1:
        return target == numbers[0]
    
    # Number of operator positions is len(numbers) - 1
    num_operators = len(numbers) - 1
    
    # Try all combinations of + and * operators
    for operators in product(['+', '*'], repeat=num_operators):
        result = evaluate_left_to_right(numbers, list(operators))
        if result == target:
            return True
    
    return False

def solve_calibration(equations: List[Tuple[int, List[int]]], verbose: bool = True) -> int:
    """Solve the calibration problem and return sum of achievable targets."""
    start_time = time.time()
    total = 0
    achievable_count = 0
    total_combinations = 0
    
    for i, (target, numbers) in enumerate(equations):
        equation_start = time.time()
        combinations_for_this = 2 ** (len(numbers) - 1)
        total_combinations += combinations_for_this
        
        if can_make_target(target, numbers):
            total += target
            achievable_count += 1
            if verbose:
                print(f"✓ {target}: {numbers}")
        else:
            if verbose:
                print(f"✗ {target}: {numbers}")
        
        # Progress update every 100 equations
        if (i + 1) % 100 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i+1}/{len(equations)} equations ({elapsed:.2f}s)")
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"\nPerformance Summary:")
    print(f"Total equations: {len(equations)}")
    print(f"Achievable: {achievable_count}/{len(equations)} ({achievable_count/len(equations)*100:.1f}%)")
    print(f"Total combinations tested: {total_combinations:,}")
    print(f"Time elapsed: {elapsed:.3f} seconds")
    print(f"Equations per second: {len(equations)/elapsed:.1f}")
    print(f"Combinations per second: {total_combinations/elapsed:,.0f}")
    
    return total

def test_examples():
    """Test the solution on example data."""
    print("Testing brute force strategy on example data...")
    print("=" * 50)
    
    equations = parse_input('example.txt')
    
    # Test individual equations from the problem description
    print("Testing specific examples:")
    
    # 190: 10 19 -> 10 * 19 = 190
    print(f"190: 10 19 -> can_make: {can_make_target(190, [10, 19])}")
    
    # 3267: 81 40 27 -> 81 + 40 * 27 = 121 * 27 = 3267 OR 81 * 40 + 27 = 3240 + 27 = 3267
    print(f"3267: 81 40 27 -> can_make: {can_make_target(3267, [81, 40, 27])}")
    
    # 292: 11 6 16 20 -> 11 + 6 * 16 + 20 = 17 * 16 + 20 = 272 + 20 = 292
    print(f"292: 11 6 16 20 -> can_make: {can_make_target(292, [11, 6, 16, 20])}")
    
    print("\n" + "=" * 50)
    print("Full solution:")
    
    total = solve_calibration(equations)
    print(f"\nTotal calibration result: {total}")
    print(f"Expected: 3749")

def solve_full_input():
    """Solve the full input.txt problem."""
    print("Solving full input.txt...")
    print("=" * 60)
    
    start_parse = time.time()
    equations = parse_input('input.txt')
    parse_time = time.time() - start_parse
    
    print(f"Parsed {len(equations)} equations in {parse_time:.3f} seconds")
    print(f"Starting brute force solution...")
    print()
    
    total = solve_calibration(equations, verbose=False)
    print(f"\nFinal Answer: {total}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "full":
        solve_full_input()
    else:
        test_examples()