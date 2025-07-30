#!/usr/bin/env python3
import sys
import argparse

def parse_input(filename):
    """Parse input file to get initial wire values and gate definitions."""
    wires = {}
    gates = []
    
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    separator_idx = None
    for i, line in enumerate(lines):
        if '->' in line:
            separator_idx = i
            break
    
    for i in range(separator_idx):
        line = lines[i]
        wire_name, value = line.split(': ')
        wires[wire_name] = int(value)
    
    for i in range(separator_idx, len(lines)):
        line = lines[i]
        parts = line.split(' -> ')
        output_wire = parts[1]
        gate_parts = parts[0].split()
        input1 = gate_parts[0]
        operation = gate_parts[1]
        input2 = gate_parts[2]
        gates.append((input1, operation, input2, output_wire))
    
    return wires, gates

def analyze_full_adder_structure(gates, debug=False):
    """
    Analyze the 45-bit full adder structure to find swapped wires.
    
    Strategy: In a proper ripple-carry adder:
    - z0 = x0 XOR y0 (half adder)
    - zi = (xi XOR yi) XOR carry_in_i (full adder sum)
    - All z-wires should be XOR operations (except z45 which can be OR for final carry)
    """
    
    gate_by_output = {}
    gates_by_inputs = {}
    
    for input1, operation, input2, output in gates:
        gate_by_output[output] = (input1, operation, input2)
        # Create normalized key for finding specific gate patterns
        key = tuple(sorted([input1, input2]) + [operation])
        if key not in gates_by_inputs:
            gates_by_inputs[key] = []
        gates_by_inputs[key].append(output)
    
    if debug:
        print("Analyzing 45-bit full adder structure...")
    
    swapped_pairs = []
    
    # Step 1: Find z-wires with wrong operations
    z_wires = sorted([output for output in gate_by_output.keys() if output.startswith('z')])
    
    for z_wire in z_wires:
        if z_wire == 'z45':  # Final carry can be OR
            continue
            
        if z_wire in gate_by_output:
            in1, op, in2 = gate_by_output[z_wire]
            
            if op != 'XOR':
                if debug:
                    print(f"❌ {z_wire} = {in1} {op} {in2} (should be XOR)")
                
                # Find the correct XOR gate for this bit
                bit_num = int(z_wire[1:])
                x_wire = f'x{bit_num:02d}'
                y_wire = f'y{bit_num:02d}'
                
                # Find xi XOR yi
                xy_xor_key = tuple(sorted([x_wire, y_wire]) + ['XOR'])
                if xy_xor_key in gates_by_inputs:
                    xy_xor_wire = gates_by_inputs[xy_xor_key][0]
                    
                    # Find XOR gate that uses xy_xor_wire (this should be zi)
                    for input1, operation, input2, output in gates:
                        if (operation == 'XOR' and xy_xor_wire in [input1, input2] 
                            and not output.startswith('z')):
                            
                            if debug:
                                print(f"✅ Found correct {z_wire}: {output}")
                            
                            swapped_pairs.append((z_wire, output))
                            break
    
    # Step 2: Check for other structural anomalies
    # Look for cases where xi XOR yi goes to wrong place
    for bit in range(45):
        x_wire = f'x{bit:02d}'
        y_wire = f'y{bit:02d}'
        z_wire = f'z{bit:02d}'
        
        xy_xor_key = tuple(sorted([x_wire, y_wire]) + ['XOR'])
        xy_and_key = tuple(sorted([x_wire, y_wire]) + ['AND'])
        
        if xy_xor_key in gates_by_inputs and xy_and_key in gates_by_inputs:
            xy_xor_wire = gates_by_inputs[xy_xor_key][0]
            xy_and_wire = gates_by_inputs[xy_and_key][0]
            
            if bit == 0:
                # Bit 0: xi XOR yi should be zi directly
                if xy_xor_wire != z_wire:
                    if debug:
                        print(f"❌ Bit {bit}: {xy_xor_wire} should be {z_wire}")
                    swapped_pairs.append((xy_xor_wire, z_wire))
            else:
                # Check if xi XOR yi is used correctly
                # It should be used in an XOR to produce zi
                used_correctly = False
                for input1, operation, input2, output in gates:
                    if (operation == 'XOR' and xy_xor_wire in [input1, input2] 
                        and output == z_wire):
                        used_correctly = True
                        break
                
                if not used_correctly:
                    # Check what's actually feeding zi
                    if z_wire in gate_by_output:
                        zin1, zop, zin2 = gate_by_output[z_wire]
                        
                        # Special case: check if AND/XOR are swapped (like bit 29)
                        if zop == 'XOR':
                            # zi is XOR, but might use wrong inputs
                            for inp in [zin1, zin2]:
                                if inp in gate_by_output:
                                    inp_in1, inp_op, inp_in2 = gate_by_output[inp]
                                    # Check if this input should be xi XOR yi instead
                                    if (inp_op == 'AND' and 
                                        sorted([inp_in1, inp_in2]) == sorted([x_wire, y_wire])):
                                        # Found xi AND yi being used where xi XOR yi should be
                                        if debug:
                                            print(f"❌ Bit {bit}: {inp} ({inp_op}) swapped with {xy_xor_wire} (XOR)")
                                        swapped_pairs.append((inp, xy_xor_wire))
    
    if debug:
        print(f"Found {len(swapped_pairs)} swapped pairs:")
        for pair in swapped_pairs:
            print(f"  {pair[0]} ↔ {pair[1]}")
    
    return swapped_pairs

def solve(filename, debug=False):
    """Main solution function for Part 2."""
    wires, gates = parse_input(filename)
    
    if debug:
        print(f"Loaded {len(wires)} initial wires and {len(gates)} gates")
    
    # Analyze the full adder structure to find swapped wires
    swapped_pairs = analyze_full_adder_structure(gates, debug)
    
    # Extract all wire names and sort
    all_wires = []
    for pair in swapped_pairs:
        all_wires.extend(pair)
    
    return ','.join(sorted(all_wires))

def main():
    parser = argparse.ArgumentParser(description='Day 24: Crossed Wires - Part 2')
    parser.add_argument('--test', action='store_true', help='Run with example.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    result = solve(filename, args.debug)
    
    print(f"Swapped wires: {result}")

if __name__ == "__main__":
    main()