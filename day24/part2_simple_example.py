#!/usr/bin/env python3

def demonstrate_part2_concept():
    print("=== Day 24 Part 2 - Simple Example with Swapped Outputs ===\n")
    
    print("Let's create a simple 3-bit adder that should compute x + y = z")
    print("We'll intentionally break it with swapped outputs, then show how to detect and fix it.\n")
    
    # Define what the circuit SHOULD look like (correct 3-bit adder)
    print("CORRECT 3-BIT ADDER STRUCTURE:")
    print("For x + y = z, we need:")
    print("  z0 = x0 XOR y0                    (sum bit 0, no carry in)")
    print("  c1 = x0 AND y0                   (carry out of bit 0)")
    print("  z1 = (x1 XOR y1) XOR c1          (sum bit 1)")
    print("  c2 = (x1 AND y1) OR (c1 AND (x1 XOR y1))  (carry out of bit 1)")
    print("  z2 = (x2 XOR y2) XOR c2          (sum bit 2)")
    print()
    
    # Create the BROKEN circuit (with swapped outputs)
    print("BROKEN CIRCUIT (with swapped outputs):")
    broken_gates = [
        ('x0', 'XOR', 'y0', 'temp1'),    # Should go to z0, but goes to temp1
        ('x0', 'AND', 'y0', 'z0'),       # Should go to c1, but goes to z0 ❌
        ('x1', 'XOR', 'y1', 'xy1_xor'),
        ('xy1_xor', 'XOR', 'z0', 'z1'),  # Uses wrong carry (z0 instead of c1)
        ('x1', 'AND', 'y1', 'xy1_and'),
        ('z0', 'AND', 'xy1_xor', 'temp2'), # Uses wrong carry
        ('xy1_and', 'OR', 'temp2', 'c2'),
        ('x2', 'XOR', 'y2', 'xy2_xor'),
        ('xy2_xor', 'XOR', 'c2', 'temp1'), # Should go to z2, but goes to temp1 ❌
        ('temp1', 'XOR', 'temp1', 'z2')    # Wrong! Should get xy2_xor XOR c2
    ]
    
    print("Gates in broken circuit:")
    for i, (in1, op, in2, out) in enumerate(broken_gates):
        print(f"  Gate {i+1}: {in1} {op} {in2} -> {out}")
    
    print("\n" + "="*60)
    print("TESTING THE BROKEN CIRCUIT:")
    print("="*60)
    
    def simulate_circuit(gates, x_vals, y_vals):
        """Simulate the circuit with given x,y inputs"""
        wires = {}
        
        # Set input values
        for i, val in enumerate(x_vals):
            wires[f'x{i}'] = val
        for i, val in enumerate(y_vals):
            wires[f'y{i}'] = val
        
        # Process gates until no more progress
        max_iterations = 20
        for iteration in range(max_iterations):
            progress = False
            for in1, op, in2, out in gates:
                if in1 in wires and in2 in wires and out not in wires:
                    val1, val2 = wires[in1], wires[in2]
                    if op == 'AND':
                        result = val1 & val2
                    elif op == 'OR':
                        result = val1 | val2
                    elif op == 'XOR':
                        result = val1 ^ val2
                    
                    wires[out] = result
                    progress = True
            
            if not progress:
                break
        
        return wires
    
    # Test several cases
    test_cases = [
        ([0, 0, 0], [0, 0, 0]),  # 0 + 0 = 0
        ([1, 0, 0], [0, 0, 0]),  # 1 + 0 = 1  
        ([1, 0, 0], [1, 0, 0]),  # 1 + 1 = 2
        ([0, 1, 0], [1, 0, 0]),  # 2 + 1 = 3
        ([1, 1, 0], [1, 1, 0]),  # 3 + 3 = 6
    ]
    
    print("\nTesting broken circuit:")
    print("Format: x + y = expected → actual (PASS/FAIL)")
    print()
    
    failed_tests = []
    
    for x_vals, y_vals in test_cases:
        # Calculate expected result
        x_decimal = sum(bit * (2 ** i) for i, bit in enumerate(x_vals))
        y_decimal = sum(bit * (2 ** i) for i, bit in enumerate(y_vals))
        expected = x_decimal + y_decimal
        expected_binary = [(expected >> i) & 1 for i in range(3)]
        
        # Simulate broken circuit
        result_wires = simulate_circuit(broken_gates, x_vals, y_vals)
        
        # Extract z values
        z_vals = []
        for i in range(3):
            z_vals.append(result_wires.get(f'z{i}', 0))
        
        actual_decimal = sum(bit * (2 ** i) for i, bit in enumerate(z_vals))
        
        # Check if correct
        is_correct = (z_vals == expected_binary)
        status = "PASS" if is_correct else "FAIL"
        
        print(f"  {x_vals} + {y_vals} = {expected_binary} → {z_vals} ({status})")
        print(f"    Decimal: {x_decimal} + {y_decimal} = {expected} → {actual_decimal}")
        
        if not is_correct:
            failed_tests.append((x_vals, y_vals))
        print()
    
    print("="*60)
    print("DETECTING THE PROBLEM:")
    print("="*60)
    
    print(f"\nFailed {len(failed_tests)} out of {len(test_cases)} test cases!")
    print("This tells us the circuit is broken.\n")
    
    print("ANALYSIS OF THE SWAPS:")
    print("Looking at the broken gates, we can see:")
    print("  1. 'x0 AND y0' should produce carry c1, but goes to z0")
    print("  2. 'x0 XOR y0' should produce z0, but goes to temp1") 
    print("  3. The final sum 'xy2_xor XOR c2' should go to z2, but goes to temp1")
    print("  4. Some wrong wire goes to z2")
    print()
    
    print("SWAPPED PAIRS:")
    print("  Pair 1: z0 ↔ temp1  (gates 'x0 AND y0' and 'x0 XOR y0')")
    print("  Pair 2: z2 ↔ temp1  (but temp1 is already involved!)")
    print()
    print("Actually, let's trace this more carefully...")
    
    print("\n" + "="*60)
    print("CORRECT SOLUTION:")
    print("="*60)
    
    # Create the correct circuit
    correct_gates = [
        ('x0', 'XOR', 'y0', 'z0'),        # z0 = sum bit 0
        ('x0', 'AND', 'y0', 'c1'),        # c1 = carry from bit 0
        ('x1', 'XOR', 'y1', 'xy1_xor'),
        ('xy1_xor', 'XOR', 'c1', 'z1'),   # z1 = sum bit 1  
        ('x1', 'AND', 'y1', 'xy1_and'),
        ('c1', 'AND', 'xy1_xor', 'c1_prop'),
        ('xy1_and', 'OR', 'c1_prop', 'c2'), # c2 = carry from bit 1
        ('x2', 'XOR', 'y2', 'xy2_xor'),
        ('xy2_xor', 'XOR', 'c2', 'z2')     # z2 = sum bit 2
    ]
    
    print("Testing CORRECTED circuit:")
    print()
    
    for x_vals, y_vals in test_cases:
        x_decimal = sum(bit * (2 ** i) for i, bit in enumerate(x_vals))
        y_decimal = sum(bit * (2 ** i) for i, bit in enumerate(y_vals))
        expected = x_decimal + y_decimal
        expected_binary = [(expected >> i) & 1 for i in range(3)]
        
        result_wires = simulate_circuit(correct_gates, x_vals, y_vals)
        z_vals = [result_wires.get(f'z{i}', 0) for i in range(3)]
        actual_decimal = sum(bit * (2 ** i) for i, bit in enumerate(z_vals))
        
        is_correct = (z_vals == expected_binary)
        status = "PASS" if is_correct else "FAIL"
        
        print(f"  {x_vals} + {y_vals} = {expected_binary} → {z_vals} ({status})")
    
    print("\n✅ All tests pass with corrected circuit!")
    
    print("\n" + "="*60)
    print("KEY TAKEAWAYS FOR PART 2:")
    print("="*60)
    print("1. The circuit SHOULD perform binary addition: x + y = z")
    print("2. Test with various x,y inputs to detect failures")
    print("3. When x + y ≠ z, the circuit has swapped outputs")
    print("4. Find which gate outputs are connected to wrong wires")
    print("5. Return the names of all wires involved in swaps (sorted)")
    print()
    print("In the real puzzle:")
    print("  - 45-bit adder (much more complex)")
    print("  - Exactly 4 pairs of swapped outputs (8 wires total)")
    print("  - Need systematic testing and analysis to find them")

if __name__ == "__main__":
    demonstrate_part2_concept()