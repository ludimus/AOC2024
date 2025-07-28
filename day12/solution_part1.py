#!/usr/bin/env python3
import sys
from collections import deque

def parse_input(filename):
    """Parse the garden grid from input file."""
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                grid.append(list(line))
    return grid

def get_neighbors(row, col, grid):
    """Get valid adjacent cells (4-directional)."""
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if (0 <= new_row < len(grid) and 
            0 <= new_col < len(grid[0])):
            neighbors.append((new_row, new_col))
    
    return neighbors

def flood_fill(start_row, start_col, grid, visited):
    """Use BFS to find all cells in the connected region."""
    plant_type = grid[start_row][start_col]
    region_cells = []
    queue = deque([(start_row, start_col)])
    visited[start_row][start_col] = True
    
    while queue:
        row, col = queue.popleft()
        region_cells.append((row, col))
        
        # Check all neighbors
        for nr, nc in get_neighbors(row, col, grid):
            if (not visited[nr][nc] and 
                grid[nr][nc] == plant_type):
                visited[nr][nc] = True
                queue.append((nr, nc))
    
    return region_cells

def calculate_perimeter(region_cells, grid):
    """Calculate perimeter by counting edges that don't touch same-type neighbors."""
    perimeter = 0
    plant_type = grid[region_cells[0][0]][region_cells[0][1]]
    
    # Convert region_cells to set for O(1) lookup
    region_set = set(region_cells)
    
    for row, col in region_cells:
        # Check all 4 directions for this cell
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            
            # Edge contributes to perimeter if:
            # 1. Neighbor is out of bounds, OR
            # 2. Neighbor is different plant type
            if (nr < 0 or nr >= len(grid) or 
                nc < 0 or nc >= len(grid[0]) or
                (nr, nc) not in region_set):
                perimeter += 1
    
    return perimeter

def find_all_regions(grid, debug=False):
    """Find all connected regions in the grid."""
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    regions = []
    
    for row in range(rows):
        for col in range(cols):
            if not visited[row][col]:
                # Found a new region
                region_cells = flood_fill(row, col, grid, visited)
                plant_type = grid[row][col]
                area = len(region_cells)
                perimeter = calculate_perimeter(region_cells, grid)
                cost = area * perimeter
                
                region_info = {
                    'plant_type': plant_type,
                    'cells': region_cells,
                    'area': area,
                    'perimeter': perimeter,
                    'cost': cost
                }
                regions.append(region_info)
                
                if debug:
                    print(f"Region {plant_type}: area={area}, perimeter={perimeter}, cost={cost}")
    
    return regions

def main():
    """Main function with command line argument support."""
    test_mode = '--test' in sys.argv or '-t' in sys.argv
    debug_mode = '--debug' in sys.argv or '-d' in sys.argv
    
    filename = 'example.txt' if test_mode else 'input.txt'
    
    if debug_mode:
        print(f"Running in {'test' if test_mode else 'normal'} mode with debug enabled")
        print(f"Reading from: {filename}")
    
    # Parse input
    grid = parse_input(filename)
    if debug_mode:
        print(f"Grid size: {len(grid)}x{len(grid[0])}")
        if len(grid) <= 10:  # Show small grids
            print("Grid:")
            for i, row in enumerate(grid):
                print(f"  {i:2}: {''.join(row)}")
    
    # Find all regions
    regions = find_all_regions(grid, debug_mode)
    
    # Calculate total cost
    total_cost = sum(region['cost'] for region in regions)
    
    if debug_mode:
        print(f"\nFound {len(regions)} regions")
        # Group regions by plant type for summary
        plant_summary = {}
        for region in regions:
            plant = region['plant_type']
            if plant not in plant_summary:
                plant_summary[plant] = []
            plant_summary[plant].append(region)
        
        print("\nSummary by plant type:")
        for plant in sorted(plant_summary.keys()):
            regions_of_type = plant_summary[plant]
            total_area = sum(r['area'] for r in regions_of_type)
            total_cost_type = sum(r['cost'] for r in regions_of_type)
            print(f"  {plant}: {len(regions_of_type)} region(s), total area={total_area}, total cost={total_cost_type}")
    
    print(f"Total fencing cost: {total_cost}")

if __name__ == "__main__":
    main()