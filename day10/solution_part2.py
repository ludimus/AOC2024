#!/usr/bin/env python3
import sys

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

def calculate_all_trailhead_ratings(grid, trailheads, debug=False):
    """Use layer-by-layer propagation to count distinct trails from each trailhead."""
    rows, cols = len(grid), len(grid[0])
    
    # For each trailhead, track number of distinct paths to each position
    trailhead_paths = {}
    for i, (tr_row, tr_col) in enumerate(trailheads):
        trailhead_paths[i] = {}
        # Initialize: 1 path to the trailhead itself
        trailhead_paths[i][(tr_row, tr_col)] = 1
    
    if debug:
        print(f"Starting path counting for {len(trailheads)} trailheads")
        for i, (tr_row, tr_col) in enumerate(trailheads):
            print(f"  Trailhead {i}: ({tr_row}, {tr_col})")
    
    # Propagate paths layer by layer from height 0 to 9
    for target_height in range(1, 10):
        if debug:
            print(f"  Processing height {target_height}")
        
        new_paths = {}
        for trailhead_idx in trailhead_paths:
            new_paths[trailhead_idx] = {}
        
        # For each position at current height, count paths from previous height
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
                            
                            # For each trailhead, add paths from previous position
                            for trailhead_idx, path_counts in trailhead_paths.items():
                                if (prev_row, prev_col) in path_counts:
                                    # Add the number of paths from previous position
                                    if (row, col) not in new_paths[trailhead_idx]:
                                        new_paths[trailhead_idx][(row, col)] = 0
                                    new_paths[trailhead_idx][(row, col)] += path_counts[(prev_row, prev_col)]
                                    
                                    if debug and target_height == 9:
                                        tr_row, tr_col = trailheads[trailhead_idx]
                                        print(f"    Trailhead ({tr_row}, {tr_col}) has {new_paths[trailhead_idx][(row, col)]} paths to 9 at ({row}, {col})")
        
        # Update path counts with new positions
        for trailhead_idx in trailhead_paths:
            trailhead_paths[trailhead_idx].update(new_paths[trailhead_idx])
    
    # Calculate ratings (sum of distinct trails to all 9s for each trailhead)
    ratings = []
    for trailhead_idx, (tr_row, tr_col) in enumerate(trailheads):
        rating = 0
        trail_count_details = []
        
        for (row, col), path_count in trailhead_paths[trailhead_idx].items():
            if grid[row][col] == 9:
                rating += path_count
                trail_count_details.append(f"{path_count} to ({row},{col})")
        
        ratings.append(rating)
        
        if debug:
            print(f"  Trailhead ({tr_row}, {tr_col}) rating: {rating}")
            if trail_count_details:
                print(f"    Trail details: {', '.join(trail_count_details)}")
    
    return ratings

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
    
    # Calculate ratings for all trailheads using layer propagation
    ratings = calculate_all_trailhead_ratings(grid, trailheads, debug_mode)
    total_rating = sum(ratings)
    
    if debug_mode:
        print(f"\nFinal ratings: {ratings}")
    
    print(f"Sum of all trailhead ratings: {total_rating}")

if __name__ == "__main__":
    main()