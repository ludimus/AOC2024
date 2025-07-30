#!/usr/bin/env python3
import sys
import argparse
import time
from solution_part1 import parse_input, run_program

def brute_force_solution(program, max_attempts=10000000):
    """Brute force approach - try values of A until we find a match"""
    print("Starting brute force approach...")
    start_time = time.time()
    
    target = program[:]
    a = 1
    
    while a <= max_attempts:
        if a % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"  Tried A={a:,}, elapsed: {elapsed:.1f}s")
        
        registers = {'A': a, 'B': 0, 'C': 0}
        output = run_program(registers, program)
        
        if output == target:
            elapsed = time.time() - start_time
            print(f"  FOUND! A={a} in {elapsed:.3f}s after {a:,} attempts")
            return a
        
        a += 1
    
    elapsed = time.time() - start_time
    print(f"  Brute force failed after {max_attempts:,} attempts in {elapsed:.1f}s")
    return None

def solve_with_backtracking(program):
    """Solve using backtracking - build A digit by digit"""
    print("Starting backtracking approach...")
    start_time = time.time()
    
    target = program[:]
    
    def dfs(a_candidate, target_index):
        """Depth-first search to build the A value"""
        if target_index < 0:
            # We've successfully built the entire A value
            return a_candidate
        
        # Try all possible 3-bit extensions (0-7)
        for digit in range(8):
            new_a = a_candidate + digit * (8 ** target_index)
            
            if new_a == 0:
                continue
            
            # Test this A value
            registers = {'A': new_a, 'B': 0, 'C': 0}
            output = run_program(registers, program)
            
            # Check if the output matches the target suffix
            if len(output) >= len(target) - target_index:
                if output[target_index:] == target[target_index:]:
                    # This partial A works, try to extend it
                    result = dfs(new_a, target_index - 1)
                    if result is not None:
                        return result
        
        return None
    
    # Start from the highest digit position
    result = dfs(0, len(target) - 1)
    
    elapsed = time.time() - start_time
    if result:
        print(f"  FOUND! A={result} in {elapsed:.3f}s")
        return result
    else:
        print(f"  No solution found in {elapsed:.3f}s")
        return None

def solve_mathematical_approach(program):
    """Mathematical approach - work backwards from the end"""
    print("Starting mathematical approach...")
    start_time = time.time()
    
    target = program[:]
    
    # The key insight: each output digit depends on the current A value
    # and A gets divided by 8 each iteration, so we can work backwards
    
    def find_a_for_output_sequence(output_seq, min_a=0):
        """Find the minimum A that produces the given output sequence"""
        if not output_seq:
            return min_a
        
        # Try all possible values for the lowest 3 bits
        for low_bits in range(8):
            candidate_a = min_a * 8 + low_bits
            
            if candidate_a == 0:
                continue
                
            # Test this candidate
            registers = {'A': candidate_a, 'B': 0, 'C': 0}
            actual_output = run_program(registers, program)
            
            # Check if this produces the right suffix
            if len(actual_output) >= len(output_seq):
                if actual_output[-len(output_seq):] == output_seq:
                    if len(actual_output) == len(output_seq):
                        # Perfect match
                        return candidate_a
                    else:
                        # Need to find A for the remaining prefix
                        remaining = actual_output[:-len(output_seq)]
                        result = find_a_for_output_sequence(remaining, candidate_a)
                        if result is not None:
                            return result
        
        return None
    
    # Start with the full target sequence
    result = find_a_for_output_sequence(target)
    
    elapsed = time.time() - start_time
    if result:
        print(f"  FOUND! A={result} in {elapsed:.3f}s")
        return result
    else:
        print(f"  No solution found in {elapsed:.3f}s")
        return None

def verify_solution(program, a_value):
    """Verify that a given A value produces the correct output"""
    registers = {'A': a_value, 'B': 0, 'C': 0}
    output = run_program(registers, program)
    return output == program

def main():
    parser = argparse.ArgumentParser(description='Day 17 Part 2: Find A that makes program output itself')
    parser.add_argument('--test', action='store_true', help='Run with example.txt')
    parser.add_argument('--method', choices=['brute', 'backtrack', 'math', 'all'], default='all',
                       help='Solution method to use')
    args = parser.parse_args()
    
    # Use different example for part 2
    if args.test:
        filename = 'example2.txt'
    else:
        filename = 'input.txt'
        
    registers, program = parse_input(filename)
    
    print(f"Target program: {program}")
    print(f"Program length: {len(program)} digits")
    print()
    
    solutions = {}
    
    if args.method in ['brute', 'all']:
        # Very limited brute force for demonstration
        max_attempts = 200000
        result = brute_force_solution(program, max_attempts)
        if result:
            solutions['brute_force'] = result
        print()
    
    if args.method in ['backtrack', 'all']:
        result = solve_with_backtracking(program)
        if result:
            solutions['backtracking'] = result
        print()
    
    if args.method in ['math', 'all']:
        result = solve_mathematical_approach(program)
        if result:
            solutions['mathematical'] = result
        print()
    
    # Verify solutions
    for method, a_val in solutions.items():
        print(f"Verifying {method} solution A={a_val}:")
        if verify_solution(program, a_val):
            print(f"  ✓ CORRECT! A={a_val} produces the target program")
        else:
            print(f"  ✗ FAILED! A={a_val} does not produce the target program")
        print()
    
    if solutions:
        min_a = min(solutions.values())
        print(f"Final answer: {min_a}")
    else:
        print("No solution found with any method")

if __name__ == "__main__":
    main()