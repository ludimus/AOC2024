#!/usr/bin/env python3

def parse_gates(filename):
    gates = []
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    separator_idx = None
    for i, line in enumerate(lines):
        if '->' in line:
            separator_idx = i
            break
    
    for i in range(separator_idx, len(lines)):
        line = lines[i]
        parts = line.split(' -> ')
        output_wire = parts[1]
        gate_parts = parts[0].split()
        input1 = gate_parts[0]
        operation = gate_parts[1]
        input2 = gate_parts[2]
        gates.append((input1, operation, input2, output_wire))
    
    return gates

def trace_full_adder_structure(gates):
    """Trace the full adder structure for bits 0 and 1 to understand the pattern."""
    
    gate_by_output = {}
    for input1, operation, input2, output in gates:
        gate_by_output[output] = (input1, operation, input2)
    
    print("=== FULL ADDER STRUCTURE ANALYSIS ===")
    print()
    
    print("📋 FULL ADDER THEORY:")
    print("For a ripple-carry adder, each bit i needs:")
    print("  1. Sum bit: zi = (xi XOR yi) XOR carry_in_i")
    print("  2. Carry out: carry_out_i = (xi AND yi) OR (carry_in_i AND (xi XOR yi))")
    print()
    
    # Analyze bit 0 (special case - no carry in)
    print("🔍 BIT 0 ANALYSIS (LSB - no carry in):")
    print("Expected: z0 = x0 XOR y0, carry_out_0 = x0 AND y0")
    print()
    
    # Find x00 XOR y00 and x00 AND y00
    x00_xor_y00 = None
    x00_and_y00 = None
    
    for input1, operation, input2, output in gates:
        if sorted([input1, input2]) == ['x00', 'y00']:
            if operation == 'XOR':
                x00_xor_y00 = output
            elif operation == 'AND':
                x00_and_y00 = output
    
    print(f"  x00 XOR y00 -> {x00_xor_y00}")
    print(f"  x00 AND y00 -> {x00_and_y00}")
    
    # Check z00
    if 'z00' in gate_by_output:
        in1, op, in2 = gate_by_output['z00']
        print(f"  z00 = {in1} {op} {in2}")
        if op == 'XOR' and sorted([in1, in2]) == ['x00', 'y00']:
            print("  ✅ z00 is correct: x00 XOR y00")
        else:
            print("  ❌ z00 is incorrect")
    
    print(f"  Carry out of bit 0: {x00_and_y00} (this becomes carry into bit 1)")
    print()
    
    # Analyze bit 1 (first bit with carry in)
    print("🔍 BIT 1 ANALYSIS (first bit with carry in):")
    print("Expected:")
    print("  z1 = (x1 XOR y1) XOR carry_in_1")
    print("  carry_out_1 = (x1 AND y1) OR (carry_in_1 AND (x1 XOR y1))")
    print()
    
    # Find x01 XOR y01 and x01 AND y01
    x01_xor_y01 = None
    x01_and_y01 = None
    
    for input1, operation, input2, output in gates:
        if sorted([input1, input2]) == ['x01', 'y01']:
            if operation == 'XOR':
                x01_xor_y01 = output
            elif operation == 'AND':
                x01_and_y01 = output
    
    print(f"  x01 XOR y01 -> {x01_xor_y01}")
    print(f"  x01 AND y01 -> {x01_and_y01}")
    print(f"  carry_in_1 = {x00_and_y00} (carry out from bit 0)")
    print()
    
    # Check z01
    if 'z01' in gate_by_output:
        in1, op, in2 = gate_by_output['z01']
        print(f"  z01 = {in1} {op} {in2}")
        
        # Should be (x01 XOR y01) XOR carry_in_1
        expected_inputs = sorted([x01_xor_y01, x00_and_y00])
        actual_inputs = sorted([in1, in2])
        
        if op == 'XOR' and actual_inputs == expected_inputs:
            print(f"  ✅ z01 is correct: {x01_xor_y01} XOR {x00_and_y00}")
        else:
            print(f"  ❌ z01 is incorrect. Expected: {x01_xor_y01} XOR {x00_and_y00}")
    
    print()
    
    # Find carry out of bit 1
    print("  Carry out of bit 1 calculation:")
    print(f"    Should be: ({x01_and_y01}) OR ({x00_and_y00} AND {x01_xor_y01})")
    
    # Look for these intermediate calculations
    carry_propagate_1 = None  # carry_in_1 AND (x01 XOR y01)
    carry_out_1 = None        # (x01 AND y01) OR carry_propagate_1
    
    for input1, operation, input2, output in gates:
        if operation == 'AND':
            if sorted([input1, input2]) == sorted([x00_and_y00, x01_xor_y01]):
                carry_propagate_1 = output
                print(f"    {x00_and_y00} AND {x01_xor_y01} -> {carry_propagate_1}")
    
    for input1, operation, input2, output in gates:
        if operation == 'OR':
            if carry_propagate_1 and sorted([input1, input2]) == sorted([x01_and_y01, carry_propagate_1]):
                carry_out_1 = output
                print(f"    {x01_and_y01} OR {carry_propagate_1} -> {carry_out_1}")
                break
    
    print(f"    Carry out of bit 1: {carry_out_1}")
    print()
    
    # Create visual diagram
    print("📊 VISUAL DIAGRAM OF BITS 0 AND 1:")
    print()
    print("BIT 0 (Half Adder):")
    print("    x00 ──┐")
    print("          ├─ XOR ──→ z00 (sum)")
    print("    y00 ──┘")
    print("    x00 ──┐")
    print("          ├─ AND ──→ gtb (carry out)")
    print("    y00 ──┘")
    print()
    print("BIT 1 (Full Adder):")
    print("    x01 ──┐")
    print("          ├─ XOR ──→ tdh ──┐")
    print("    y01 ──┘                │")
    print("                           ├─ XOR ──→ z01 (sum)")
    print("    gtb ───────────────────┘")
    print("    (carry in)")
    print()
    print("    x01 ──┐")
    print("          ├─ AND ──→ vpp ──┐")
    print("    y01 ──┘                │")
    print("                           ├─ OR ───→ prf (carry out)")
    print("    gtb ──┐                │")
    print("          ├─ AND ──→ svv ──┘")
    print("    tdh ──┘")
    print()
    
    # Verify the actual wiring matches this pattern
    print("🔍 VERIFICATION OF ACTUAL WIRING:")
    
    # Check the carry propagation chain
    if carry_out_1:
        print(f"✅ Carry chain bit 0→1: {x00_and_y00} → {carry_out_1}")
    
    # Check bit 2 to see if it uses carry_out_1
    if 'z02' in gate_by_output:
        in1, op, in2 = gate_by_output['z02']
        print(f"  z02 = {in1} {op} {in2}")
        if carry_out_1 in [in1, in2]:
            print(f"  ✅ Bit 2 correctly uses carry from bit 1: {carry_out_1}")
        else:
            print("  🔍 Need to trace bit 2 carry chain...")
            
            # Look for what feeds into z02
            for inp in [in1, in2]:
                if inp in gate_by_output:
                    inp_in1, inp_op, inp_in2 = gate_by_output[inp]
                    print(f"    {inp} = {inp_in1} {inp_op} {inp_in2}")
    
    print()
    print("🎯 KEY INSIGHTS:")
    print("1. Bit 0 is a half adder (no carry in)")
    print("2. Bits 1+ are full adders (carry in, sum out, carry out)")
    print("3. Each bit follows the pattern:")
    print("   - Intermediate: xi XOR yi")
    print("   - Sum: (xi XOR yi) XOR carry_in")
    print("   - Carry: (xi AND yi) OR (carry_in AND (xi XOR yi))")
    print("4. The swapped wires broke this chain at specific bit positions")

if __name__ == "__main__":
    gates = parse_gates('input.txt')
    trace_full_adder_structure(gates)