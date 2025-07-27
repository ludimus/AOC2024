from collections import defaultdict
from itertools import combinations

def solve_antinodes(filename):
    with open(filename, 'r') as f:
        grid = [line.strip() for line in f.readlines()]
    
    rows, cols = len(grid), len(grid[0])
    antennas = defaultdict(list)
    
    # Parse antennas by frequency
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '.':
                antennas[grid[r][c]].append((r, c))
    
    antinodes = set()
    
    # Generate antinodes for each frequency
    for frequency, positions in antennas.items():
        if len(positions) < 2:
            continue
            
        # For each pair of antennas with same frequency
        for (r1, c1), (r2, c2) in combinations(positions, 2):
            # Calculate displacement vector
            dr, dc = r2 - r1, c2 - c1
            
            # Two antinodes: one extending beyond each antenna
            antinode1 = (r1 - dr, c1 - dc)
            antinode2 = (r2 + dr, c2 + dc)
            
            # Add valid antinodes (within bounds)
            for ar, ac in [antinode1, antinode2]:
                if 0 <= ar < rows and 0 <= ac < cols:
                    antinodes.add((ar, ac))
    
    return len(antinodes)

if __name__ == "__main__":
    # Test with example
    result_example = solve_antinodes("example.txt")
    print(f"Example result: {result_example}")
    
    # Solve actual input
    result = solve_antinodes("input.txt")
    print(f"Part 1 answer: {result}")