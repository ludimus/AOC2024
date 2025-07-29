#!/usr/bin/env python3
import argparse

class Machine:
    def __init__(self, ax, ay, bx, by, px, py):
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.px = px
        self.py = py

def parse_input(filename):
    machines = []
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    i = 0
    while i < len(lines):
        # Parse Button A
        a_line = lines[i]
        ax = int(a_line.split('X+')[1].split(',')[0])
        ay = int(a_line.split('Y+')[1])
        
        # Parse Button B
        b_line = lines[i + 1]
        bx = int(b_line.split('X+')[1].split(',')[0])
        by = int(b_line.split('Y+')[1])
        
        # Parse Prize
        p_line = lines[i + 2]
        px = int(p_line.split('X=')[1].split(',')[0])
        py = int(p_line.split('Y=')[1])
        
        machines.append(Machine(ax, ay, bx, by, px, py))
        i += 3
    
    return machines

def solve_machine(machine, debug=False):
    # Solve linear system using Cramer's rule:
    # a * ax + b * bx = px
    # a * ay + b * by = py
    
    det = machine.ax * machine.by - machine.ay * machine.bx
    
    if det == 0:
        if debug:
            print(f"No unique solution (determinant = 0)")
        return None
    
    # Calculate a and b using Cramer's rule
    a_num = machine.px * machine.by - machine.py * machine.bx
    b_num = machine.ax * machine.py - machine.ay * machine.px
    
    # Check if solutions are integers
    if a_num % det != 0 or b_num % det != 0:
        if debug:
            print(f"No integer solution: a={a_num}/{det}, b={b_num}/{det}")
        return None
    
    a = a_num // det
    b = b_num // det
    
    # Check constraints: non-negative and ≤ 100
    if a < 0 or b < 0 or a > 100 or b > 100:
        if debug:
            print(f"Solution out of bounds: a={a}, b={b}")
        return None
    
    # Verify solution
    if a * machine.ax + b * machine.bx != machine.px or a * machine.ay + b * machine.by != machine.py:
        if debug:
            print(f"Verification failed: a={a}, b={b}")
        return None
    
    if debug:
        print(f"Solution found: a={a}, b={b}")
    
    return (a, b)

def calculate_cost(a_presses, b_presses):
    return 3 * a_presses + 1 * b_presses

def solve_all_machines(machines, debug=False):
    prizes_won = 0
    total_cost = 0
    
    for i, machine in enumerate(machines):
        if debug:
            print(f"\nMachine {i + 1}:")
            print(f"  Button A: X+{machine.ax}, Y+{machine.ay}")
            print(f"  Button B: X+{machine.bx}, Y+{machine.by}")
            print(f"  Prize: X={machine.px}, Y={machine.py}")
        
        solution = solve_machine(machine, debug)
        if solution:
            a, b = solution
            cost = calculate_cost(a, b)
            prizes_won += 1
            total_cost += cost
            if debug:
                print(f"  Cost: {cost} tokens")
        elif debug:
            print("  No solution")
    
    return prizes_won, total_cost

def main():
    parser = argparse.ArgumentParser(description='Day 13: Claw Contraption Part 1')
    parser.add_argument('--test', action='store_true', help='Run on example.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    machines = parse_input(filename)
    
    if args.debug or args.test:
        print(f"Loaded {len(machines)} machines from {filename}")
    
    prizes_won, total_cost = solve_all_machines(machines, args.debug or args.test)
    
    print(f"Prizes won: {prizes_won}")
    print(f"Total cost: {total_cost} tokens")

if __name__ == "__main__":
    main()