#!/usr/bin/env python3
"""
Simplified Backtracking Explanation
"""

from solution_part1 import run_program

def demonstrate_tree_structure():
    program = [0, 3, 5, 4, 3, 0]
    
    print("=== THE TREE STRUCTURE ===")
    print("Since A gets divided by 8 each iteration, we have:")
    print()
    
    # Show the relationship backwards from our known answer
    a = 117440
    level = 0
    
    while a > 0:
        registers = {'A': a, 'B': 0, 'C': 0}
        output = run_program(registers, program)
        
        indent = "  " * level
        print(f"{indent}A = {a:6d} -> output: {output}")
        
        a = a // 8
        level += 1
    
    print()
    print("=== THE BACKTRACKING IDEA ===")
    print("1. We know the final output should be [0, 3, 5, 4, 3, 0]")
    print("2. Work backwards: what A values can produce [0] as the last element?")
    print("3. Then: what A values can produce [3, 0] as the last two elements?")
    print("4. Continue until we build the full sequence")
    print()

def show_manual_backtracking():
    program = [0, 3, 5, 4, 3, 0]
    target = [0, 3, 5, 4, 3, 0]
    
    print("=== MANUAL BACKTRACKING EXAMPLE ===")
    print(f"Target: {target}")
    print()
    
    # Step 1: Find A values that produce just [0]
    print("STEP 1: Find A values that output [0]")
    candidates_1 = []
    for a in range(1, 64):  # Check first few values
        registers = {'A': a, 'B': 0, 'C': 0}
        output = run_program(registers, program)
        if output == [0]:
            candidates_1.append(a)
            if len(candidates_1) <= 5:  # Show first few
                print(f"  A={a} -> [0] ✓")
    
    print(f"  Found {len(candidates_1)} candidates for [0]")
    print()
    
    # Step 2: Find A values that produce [3, 0]
    print("STEP 2: Build from [0] candidates to find [3, 0]")
    candidates_2 = []
    for base_a in candidates_1[:3]:  # Check first few
        for digit in range(8):
            test_a = base_a * 8 + digit
            registers = {'A': test_a, 'B': 0, 'C': 0}
            output = run_program(registers, program)
            if output == [3, 0]:
                candidates_2.append(test_a)
                print(f"  A={test_a} (built from {base_a}) -> [3, 0] ✓")
    
    print(f"  Found {len(candidates_2)} candidates for [3, 0]")
    print()
    
    print("STEP 3-6: Continue this process...")
    print("  [3, 0] -> [4, 3, 0] -> [5, 4, 3, 0] -> [3, 5, 4, 3, 0] -> [0, 3, 5, 4, 3, 0]")
    print()
    print(f"Final answer: A = 117440")
    
    # Verify
    registers = {'A': 117440, 'B': 0, 'C': 0}
    output = run_program(registers, program)
    print(f"Verification: A=117440 -> {output}")

def show_why_this_works():
    print("=== WHY BACKTRACKING WORKS ===")
    print()
    print("✅ PROGRAM IS DETERMINISTIC:")
    print("   Same A always produces same output")
    print()
    print("✅ HIERARCHICAL STRUCTURE:")
    print("   A -> A//8 -> A//64 -> ... (each division by 8)")
    print("   This creates a search tree we can traverse backwards")
    print()
    print("✅ EARLY PRUNING:")
    print("   If A doesn't produce the right suffix, no point trying extensions")
    print()
    print("✅ FINITE SEARCH SPACE:")
    print("   Only 8 possible extensions at each level (0-7)")
    print()
    print("⚡ PERFORMANCE:")
    print("   Instead of 8^16 = 281 trillion attempts (brute force)")
    print("   We try ~8 * 16 = 128 candidates (backtracking)")
    print("   That's a 2.2 billion times speedup! 🚀")

if __name__ == "__main__":
    demonstrate_tree_structure()
    print()
    show_manual_backtracking()
    print()
    show_why_this_works()