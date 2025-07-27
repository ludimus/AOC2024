from collections import defaultdict
from itertools import combinations

def solve_antinodes_part2(filename):
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
        
        # Add antenna positions themselves as antinodes
        for pos in positions:
            antinodes.add(pos)
            
        # For each pair of antennas with same frequency
        for (r1, c1), (r2, c2) in combinations(positions, 2):
            # Calculate displacement vector
            dr, dc = r2 - r1, c2 - c1
            
            # Extend line in both directions with original vector
            # Forward direction from antenna 2
            r, c = r2 + dr, c2 + dc
            while 0 <= r < rows and 0 <= c < cols:
                antinodes.add((r, c))
                r += dr
                c += dc
            
            # Backward direction from antenna 1
            r, c = r1 - dr, c1 - dc
            while 0 <= r < rows and 0 <= c < cols:
                antinodes.add((r, c))
                r -= dr
                c -= dc
    
    return len(antinodes)

if __name__ == "__main__":
    # Test with example
    result_example = solve_antinodes_part2("example.txt")
    print(f"Part 2 Example result: {result_example}")
    
    # Solve actual input
    result = solve_antinodes_part2("input.txt")
    print(f"Part 2 answer: {result}")