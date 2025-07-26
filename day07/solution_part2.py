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
        elif op == '||':
            # Concatenation: convert to strings, concatenate, convert back
            result = int(str(result) + str(numbers[i + 1]))
    
    return result

def can_make_target(target: int, numbers: List[int]) -> bool:
    """Check if target can be made by placing operators between numbers."""
    if len(numbers) == 1:
        return target == numbers[0]
    
    # Number of operator positions is len(numbers) - 1
    num_operators = len(numbers) - 1
    
    # Try all combinations of +, *, and || operators
    for operators in product(['+', '*', '||'], repeat=num_operators):
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
        combinations_for_this = 3 ** (len(numbers) - 1)
        total_combinations += combinations_for_this
        
        if can_make_target(target, numbers):
            total += target
            achievable_count += 1
            if verbose:
                print(f"✓ {target}: {numbers}")
        else:
            if verbose:
                print(f"✗ {target}: {numbers}")
        
        # Progress update every 50 equations (more frequent due to slower execution)
        if (i + 1) % 50 == 0:
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
    """Test the Part 2 solution on example data."""
    print("Testing Part 2 solution with concatenation operator...")
    print("=" * 60)
    
    equations = parse_input('example.txt')
    
    # Test specific Part 2 examples
    print("Testing new Part 2 examples:")
    
    # 156: 15 6 -> 15 || 6 = 156
    print(f"156: 15 6 -> can_make: {can_make_target(156, [15, 6])}")
    
    # 7290: 6 8 6 15 -> 6 * 8 || 6 * 15 = 486 * 15 = 7290
    print(f"7290: 6 8 6 15 -> can_make: {can_make_target(7290, [6, 8, 6, 15])}")
    
    # 192: 17 8 14 -> 17 || 8 + 14 = 178 + 14 = 192
    print(f"192: 17 8 14 -> can_make: {can_make_target(192, [17, 8, 14])}")
    
    print("\n" + "=" * 60)
    print("Full Part 2 solution:")
    
    total = solve_calibration(equations)
    print(f"\nTotal calibration result: {total}")
    print(f"Expected: 11387")

def test_concatenation():
    """Test concatenation operator specifically."""
    print("Testing concatenation operator:")
    print("=" * 40)
    
    test_cases = [
        ([12, 345], ['||'], 12345),
        ([15, 6], ['||'], 156),
        ([6, 8, 6], ['*', '||'], 486),  # 6 * 8 = 48, 48 || 6 = 486
        ([17, 8, 14], ['||', '+'], 192),  # 17 || 8 = 178, 178 + 14 = 192
    ]
    
    for numbers, operators, expected in test_cases:
        result = evaluate_left_to_right(numbers, operators)
        status = "✓" if result == expected else "✗"
        op_str = " ".join(f"{numbers[i]} {operators[i]}" for i in range(len(operators))) + f" {numbers[-1]}"
        print(f"{op_str} = {result} {status} (expected {expected})")

def solve_full_input():
    """Solve the full input.txt problem for Part 2."""
    print("Solving full input.txt for Part 2...")
    print("=" * 60)
    
    start_parse = time.time()
    equations = parse_input('input.txt')
    parse_time = time.time() - start_parse
    
    print(f"Parsed {len(equations)} equations in {parse_time:.3f} seconds")
    print(f"Starting Part 2 solution with 3 operators (+, *, ||)...")
    print("Warning: This will be significantly slower than Part 1 due to 3^n complexity")
    print()
    
    total = solve_calibration(equations, verbose=False)
    print(f"\nFinal Part 2 Answer: {total}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "full":
            solve_full_input()
        elif sys.argv[1] == "concat":
            test_concatenation()
    else:
        test_concatenation()
        print()
        test_examples()