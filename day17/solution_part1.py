#!/usr/bin/env python3
import sys
import argparse

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    
    registers = {}
    registers['A'] = int(lines[0].split(': ')[1])
    registers['B'] = int(lines[1].split(': ')[1])
    registers['C'] = int(lines[2].split(': ')[1])
    
    program = list(map(int, lines[4].split(': ')[1].split(',')))
    
    return registers, program

def get_combo_value(operand, registers):
    if operand <= 3:
        return operand
    elif operand == 4:
        return registers['A']
    elif operand == 5:
        return registers['B']
    elif operand == 6:
        return registers['C']
    else:
        raise ValueError(f"Invalid combo operand: {operand}")

def execute_instruction(opcode, operand, registers, ip, output, debug=False):
    new_ip = ip + 2
    
    if debug:
        print(f"IP={ip}: opcode={opcode}, operand={operand}, A={registers['A']}, B={registers['B']}, C={registers['C']}")
    
    if opcode == 0:  # adv
        combo_val = get_combo_value(operand, registers)
        registers['A'] = registers['A'] // (2 ** combo_val)
        if debug: print(f"  adv: A = A // 2^{combo_val} = {registers['A']}")
    
    elif opcode == 1:  # bxl
        registers['B'] = registers['B'] ^ operand
        if debug: print(f"  bxl: B = B XOR {operand} = {registers['B']}")
    
    elif opcode == 2:  # bst
        combo_val = get_combo_value(operand, registers)
        registers['B'] = combo_val % 8
        if debug: print(f"  bst: B = {combo_val} % 8 = {registers['B']}")
    
    elif opcode == 3:  # jnz
        if registers['A'] != 0:
            new_ip = operand
            if debug: print(f"  jnz: A != 0, jumping to {operand}")
        else:
            if debug: print(f"  jnz: A == 0, no jump")
    
    elif opcode == 4:  # bxc
        registers['B'] = registers['B'] ^ registers['C']
        if debug: print(f"  bxc: B = B XOR C = {registers['B']}")
    
    elif opcode == 5:  # out
        combo_val = get_combo_value(operand, registers)
        output_val = combo_val % 8
        output.append(output_val)
        if debug: print(f"  out: output {combo_val} % 8 = {output_val}")
    
    elif opcode == 6:  # bdv
        combo_val = get_combo_value(operand, registers)
        registers['B'] = registers['A'] // (2 ** combo_val)
        if debug: print(f"  bdv: B = A // 2^{combo_val} = {registers['B']}")
    
    elif opcode == 7:  # cdv
        combo_val = get_combo_value(operand, registers)
        registers['C'] = registers['A'] // (2 ** combo_val)
        if debug: print(f"  cdv: C = A // 2^{combo_val} = {registers['C']}")
    
    else:
        raise ValueError(f"Invalid opcode: {opcode}")
    
    return new_ip

def run_program(registers, program, debug=False):
    ip = 0
    output = []
    
    if debug:
        print(f"Starting: A={registers['A']}, B={registers['B']}, C={registers['C']}")
        print(f"Program: {program}")
        print()
    
    while ip < len(program):
        if ip + 1 >= len(program):
            break
        
        opcode = program[ip]
        operand = program[ip + 1]
        
        ip = execute_instruction(opcode, operand, registers, ip, output, debug)
        
        if debug:
            print(f"  -> A={registers['A']}, B={registers['B']}, C={registers['C']}, output={output}")
            print()
    
    return output

def main():
    parser = argparse.ArgumentParser(description='Day 17: Chronospatial Computer')
    parser.add_argument('--test', action='store_true', help='Run with example.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    
    registers, program = parse_input(filename)
    output = run_program(registers, program, args.debug or args.test)
    
    result = ','.join(map(str, output))
    print(result)

if __name__ == "__main__":
    main()