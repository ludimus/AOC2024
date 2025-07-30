#!/usr/bin/env python3
import sys
import argparse
from collections import deque, defaultdict

def parse_input(filename):
    """Parse input file to get initial wire values and gate definitions."""
    wires = {}
    gates = []
    
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Find the separator between wire values and gates
    separator_idx = None
    for i, line in enumerate(lines):
        if '->' in line:
            separator_idx = i
            break
    
    # Parse initial wire values
    for i in range(separator_idx):
        line = lines[i]
        wire_name, value = line.split(': ')
        wires[wire_name] = int(value)
    
    # Parse gate definitions
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

def simulate_gates(wires, gates):
    """Simulate the gate network until all outputs are determined."""
    # Create a copy of wires to avoid modifying the original
    wire_values = wires.copy()
    
    # Create a queue of gates to process
    gate_queue = deque(gates)
    
    # Keep processing gates until no more progress can be made
    while gate_queue:
        processed_count = 0
        queue_size = len(gate_queue)
        
        # Try to process each gate in the current queue
        for _ in range(queue_size):
            input1, operation, input2, output = gate_queue.popleft()
            
            # Check if both inputs are available
            if input1 in wire_values and input2 in wire_values:
                # Calculate the output based on the operation
                val1 = wire_values[input1]
                val2 = wire_values[input2]
                
                if operation == 'AND':
                    result = val1 & val2
                elif operation == 'OR':
                    result = val1 | val2
                elif operation == 'XOR':
                    result = val1 ^ val2
                else:
                    raise ValueError(f"Unknown operation: {operation}")
                
                wire_values[output] = result
                processed_count += 1
            else:
                # Put the gate back in the queue to try later
                gate_queue.append((input1, operation, input2, output))
        
        # If no gates were processed in this iteration, we're done or stuck
        if processed_count == 0:
            break
    
    return wire_values

def get_z_output(wire_values):
    """Extract z-wire values and convert to decimal."""
    # Find all z-wires and sort them numerically
    z_wires = [(name, value) for name, value in wire_values.items() if name.startswith('z')]
    z_wires.sort(key=lambda x: int(x[0][1:]))  # Sort by number after 'z'
    
    # Build binary number (LSB first)
    binary_digits = [str(value) for name, value in z_wires]
    binary_string = ''.join(reversed(binary_digits))  # Reverse to get MSB first
    
    # Convert to decimal
    return int(binary_string, 2)

def solve(filename, debug=False):
    """Main solution function."""
    wires, gates = parse_input(filename)
    
    if debug:
        print(f"Initial wires: {len(wires)}")
        print(f"Gates: {len(gates)}")
        print("Initial wire values:")
        for name, value in sorted(wires.items()):
            print(f"  {name}: {value}")
    
    # Simulate the circuit
    final_wires = simulate_gates(wires, gates)
    
    if debug:
        print("\nFinal wire values:")
        for name, value in sorted(final_wires.items()):
            print(f"  {name}: {value}")
        
        # Show z-wires specifically
        z_wires = [(name, value) for name, value in final_wires.items() if name.startswith('z')]
        z_wires.sort(key=lambda x: int(x[0][1:]))
        print("\nZ-wire values (LSB to MSB):")
        for name, value in z_wires:
            print(f"  {name}: {value}")
        
        binary_digits = [str(value) for name, value in z_wires]
        binary_string = ''.join(reversed(binary_digits))
        print(f"\nBinary result: {binary_string}")
    
    # Get the decimal output
    result = get_z_output(final_wires)
    
    return result

def main():
    parser = argparse.ArgumentParser(description='Day 24: Crossed Wires - Part 1')
    parser.add_argument('--test', action='store_true', help='Run with example.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    result = solve(filename, args.debug)
    
    print(f"Decimal output: {result}")

if __name__ == "__main__":
    main()