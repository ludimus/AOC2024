#!/usr/bin/env python3

import sys
from functools import lru_cache

# Keypad layouts
NUMERIC_KEYPAD = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
                 '0': (3, 1), 'A': (3, 2)
}
NUMERIC_GAP = (3, 0)

DIRECTIONAL_KEYPAD = {
                 '^': (0, 1), 'A': (0, 2),
    '<': (1, 0), 'v': (1, 1), '>': (1, 2)
}
DIRECTIONAL_GAP = (0, 0)

def get_shortest_paths(start_pos, end_pos, gap_pos):
    """Get all shortest paths between two positions, avoiding gap."""
    if start_pos == end_pos:
        return ['']
    
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    
    row_diff = end_row - start_row
    col_diff = end_col - start_col
    
    # Generate moves
    moves = []
    if row_diff > 0:
        moves.extend(['v'] * row_diff)
    elif row_diff < 0:
        moves.extend(['^'] * abs(row_diff))
    
    if col_diff > 0:
        moves.extend(['>'] * col_diff)
    elif col_diff < 0:
        moves.extend(['<'] * abs(col_diff))
    
    if not moves:
        return ['']
    
    # Try both orderings: horizontal first, then vertical first
    paths = []
    
    # Horizontal first
    h_moves = [m for m in moves if m in '<>']
    v_moves = [m for m in moves if m in '^v']
    h_first = ''.join(h_moves + v_moves)
    
    # Check if horizontal-first avoids gap
    pos = start_pos
    valid = True
    for move in h_first:
        if move == '^': pos = (pos[0] - 1, pos[1])
        elif move == 'v': pos = (pos[0] + 1, pos[1])
        elif move == '<': pos = (pos[0], pos[1] - 1)
        elif move == '>': pos = (pos[0], pos[1] + 1)
        if pos == gap_pos:
            valid = False
            break
    
    if valid:
        paths.append(h_first)
    
    # Vertical first (if different)
    v_first = ''.join(v_moves + h_moves)
    if v_first != h_first:
        pos = start_pos
        valid = True
        for move in v_first:
            if move == '^': pos = (pos[0] - 1, pos[1])
            elif move == 'v': pos = (pos[0] + 1, pos[1])
            elif move == '<': pos = (pos[0], pos[1] - 1)
            elif move == '>': pos = (pos[0], pos[1] + 1)
            if pos == gap_pos:
                valid = False
                break
        
        if valid:
            paths.append(v_first)
    
    return paths if paths else ['']

@lru_cache(maxsize=None)
def get_move_cost(from_btn, to_btn, depth, is_numeric=False):
    """Get the cost of moving from one button to another at given depth."""
    if depth == 0:
        return 1  # Base case: just the button press itself
    
    # Choose keypad
    if is_numeric:
        keypad = NUMERIC_KEYPAD
        gap = NUMERIC_GAP
    else:
        keypad = DIRECTIONAL_KEYPAD
        gap = DIRECTIONAL_GAP
    
    # Get all possible movement sequences
    start_pos = keypad[from_btn]
    end_pos = keypad[to_btn]
    paths = get_shortest_paths(start_pos, end_pos, gap)
    
    min_cost = float('inf')
    
    for path in paths:
        # Each path needs to end with 'A' to activate
        full_sequence = path + 'A'
        
        # Calculate cost of this sequence at the next layer (directional)
        cost = 0
        current_btn = 'A'  # Always start at A
        
        for next_btn in full_sequence:
            cost += get_move_cost(current_btn, next_btn, depth - 1, is_numeric=False)
            current_btn = next_btn
        
        min_cost = min(min_cost, cost)
    
    return min_cost

def calculate_sequence_cost(code, layers):
    """Calculate the minimum cost to input a code through given layers."""
    total_cost = 0
    current_btn = 'A'  # Start at A
    
    for target_btn in code:
        # The final layer is numeric, all others are directional
        cost = get_move_cost(current_btn, target_btn, layers, is_numeric=True)
        total_cost += cost
        current_btn = target_btn
    
    return total_cost

def calculate_complexity(code, layers):
    """Calculate complexity for a single code."""
    numeric_part = int(code[:-1])  # Remove 'A' and convert to int
    min_length = calculate_sequence_cost(code, layers)
    complexity = min_length * numeric_part
    return complexity, min_length, numeric_part

def parse_input(filename):
    """Parse input file and return list of codes."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    # Command line argument handling
    test_mode = '--test' in sys.argv
    debug_mode = '--debug' in sys.argv
    part2_mode = '--part2' in sys.argv
    
    filename = 'example.txt' if test_mode else 'input.txt'
    layers = 26 if part2_mode else 3  # Part 1: 3 layers, Part 2: 26 layers
    
    if debug_mode:
        print(f"Running {'Part 2' if part2_mode else 'Part 1'} in {'test' if test_mode else 'normal'} mode")
        print(f"Using {layers} layers")
    
    # Parse input
    codes = parse_input(filename)
    
    if debug_mode:
        print(f"Codes to process: {codes}")
    
    total_complexity = 0
    
    for code in codes:
        complexity, min_length, numeric_part = calculate_complexity(code, layers)
        total_complexity += complexity
        
        if debug_mode or test_mode:
            print(f"{code}: {min_length} * {numeric_part} = {complexity}")
    
    print(f"Total complexity: {total_complexity}")

if __name__ == "__main__":
    main()