#!/usr/bin/env python3
import sys
from collections import deque

def parse_input(filename):
    """Parse the topographic map from input file and return 2D grid."""
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                row = [int(char) for char in line]
                grid.append(row)
    return grid

def find_trailheads(grid):
    """Find all positions with height 0 (trailheads)."""
    trailheads = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                trailheads.append((row, col))
    return trailheads

def get_valid_moves(grid, row, col):
    """Get adjacent cells that have height = current_height + 1."""
    current_height = grid[row][col]
    target_height = current_height + 1
    valid_moves = []
    
    # Check all 4 directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        
        # Check bounds
        if (0 <= new_row < len(grid) and 
            0 <= new_col < len(grid[0]) and
            grid[new_row][new_col] == target_height):
            valid_moves.append((new_row, new_col))
    
    return valid_moves

def calculate_all_trailhead_scores(grid, trailheads, debug=False):
    """Use layer-by-layer propagation to find all reachable positions efficiently."""
    rows, cols = len(grid), len(grid[0])
    
    # For each trailhead, track which positions are reachable
    trailhead_reachable = {}
    for i, (tr_row, tr_col) in enumerate(trailheads):
        trailhead_reachable[i] = set()
        trailhead_reachable[i].add((tr_row, tr_col))
    
    if debug:
        print(f"Starting layer-by-layer propagation for {len(trailheads)} trailheads")
    
    # Propagate layer by layer from height 0 to 9
    for target_height in range(1, 10):
        if debug:
            print(f"  Processing height {target_height}")
        
        new_reachable = {}
        for trailhead_idx in trailhead_reachable:
            new_reachable[trailhead_idx] = set()
        
        # For each position at current height, check if reachable from previous height
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == target_height:
                    # Check all 4 neighbors for previous height
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    
                    for dr, dc in directions:
                        prev_row, prev_col = row + dr, col + dc
                        
                        # Check bounds and height
                        if (0 <= prev_row < rows and 
                            0 <= prev_col < cols and
                            grid[prev_row][prev_col] == target_height - 1):
                            
                            # Check which trailheads can reach the previous position
                            for trailhead_idx, reachable_set in trailhead_reachable.items():
                                if (prev_row, prev_col) in reachable_set:
                                    new_reachable[trailhead_idx].add((row, col))
                                    if debug and target_height == 9:
                                        tr_row, tr_col = trailheads[trailhead_idx]
                                        print(f"    Trailhead ({tr_row}, {tr_col}) can reach 9 at ({row}, {col})")
        
        # Update reachable sets with new positions
        for trailhead_idx in trailhead_reachable:
            trailhead_reachable[trailhead_idx].update(new_reachable[trailhead_idx])
    
    # Calculate scores (count of reachable 9s for each trailhead)
    scores = []
    for trailhead_idx, (tr_row, tr_col) in enumerate(trailheads):
        reachable_nines = {pos for pos in trailhead_reachable[trailhead_idx] 
                          if grid[pos[0]][pos[1]] == 9}
        score = len(reachable_nines)
        scores.append(score)
        
        if debug:
            print(f"  Trailhead ({tr_row}, {tr_col}) score: {score}")
            print(f"  Reachable 9s: {sorted(reachable_nines)}")
    
    return scores

def main():
    """Main function with command line argument support."""
    test_mode = '--test' in sys.argv or '-t' in sys.argv
    debug_mode = '--debug' in sys.argv or '-d' in sys.argv
    
    filename = 'example.txt' if test_mode else 'input.txt'
    
    if debug_mode:
        print(f"Running in {'test' if test_mode else 'normal'} mode with debug enabled")
        print(f"Reading from: {filename}")
    
    # Parse input and build grid
    grid = parse_input(filename)
    if debug_mode:
        print(f"Grid size: {len(grid)}x{len(grid[0])}")
        print("Grid:")
        for i, row in enumerate(grid):
            print(f"  {i:2}: {''.join(str(x) for x in row)}")
    
    # Find all trailheads
    trailheads = find_trailheads(grid)
    if debug_mode:
        print(f"Found {len(trailheads)} trailheads: {trailheads}")
    
    # Calculate scores for all trailheads using optimized layer propagation
    scores = calculate_all_trailhead_scores(grid, trailheads, debug_mode)
    total_score = sum(scores)
    
    if debug_mode:
        print(f"\nFinal scores: {scores}")
    
    print(f"Sum of all trailhead scores: {total_score}")

if __name__ == "__main__":
    main()