# Day 8: Resonant Collinearity - Strategy Plan

## Problem Understanding
- **Goal**: Count unique antinode locations within map bounds
- **Input**: 51x51 grid with antennas (letters/digits) and empty spaces (.)
- **Antinode Rule**: For each pair of same-frequency antennas, antinodes occur where one antenna is twice as far as the other

## Data Structures
1. **Antenna Dictionary**: `frequency -> list of (row, col) positions`
   - Uses `defaultdict(list)` for automatic list creation
   - Example: `{'0': [(1, 8), (2, 5), (3, 7), (4, 4)], 'A': [(5, 6), (8, 8), (9, 9)]}`
   - Benefits: No need to check if key exists before appending positions
2. **Antinode Set**: Set of unique (row, col) antinode positions
3. **Grid Bounds**: 51x51 grid (indices 0-50)

## Key Implementation Detail: defaultdict(list)
```python
antennas = defaultdict(list)
antennas[frequency].append((r, c))  # Automatically creates empty list if key doesn't exist
```

**Why defaultdict(list)?**
- Without: `if frequency not in antennas: antennas[frequency] = []`
- With defaultdict: Automatic empty list creation on first access
- Cleaner code, no KeyError exceptions

## Algorithm Steps
1. **Parse Input**: 
   - Read grid line by line
   - For each non-'.' character, add position to antenna dictionary

2. **Generate Antinodes**:
   - For each frequency with 2+ antennas:
     - For each pair of antennas (r1,c1) and (r2,c2):
       - Calculate displacement vector: dr = r2-r1, dc = c2-c1
       - Antinode 1: (r1-dr, c1-dc) - extends beyond first antenna
       - Antinode 2: (r2+dr, c2+dc) - extends beyond second antenna
       - Add valid (in-bounds) antinodes to result set

3. **Bounds Checking**:
   - Only count antinodes where 0 <= row <= 50 and 0 <= col <= 50

4. **Return Count**: Length of unique antinode set

## Implementation Notes
- Use `collections.defaultdict(list)` for antenna grouping
- Use `set()` for automatic deduplication of antinode positions
- Consider using `itertools.combinations` for antenna pairs

---

# Part 2: Resonant Harmonics Analysis

## Key Changes from Part 1
1. **Unlimited Distance**: Antinodes occur at ALL positions in line with 2+ same-frequency antennas
2. **Antenna Positions**: Antennas themselves become antinodes (if 2+ exist)
3. **Continuous Lines**: Every grid position along the line between antenna pairs
4. **Expected Result**: Example gives 34 (vs 14 in Part 1)

## Part 2 Algorithm
```python
import math

def get_line_points(r1, c1, r2, c2, rows, cols):
    # Calculate and reduce direction vector using GCD
    dr, dc = r2 - r1, c2 - c1
    gcd = math.gcd(abs(dr), abs(dc))
    step_r, step_c = dr // gcd, dc // gcd
    
    points = set()
    
    # Walk entire line in both directions until out of bounds
    # Positive direction
    r, c = r1, c1
    while 0 <= r < rows and 0 <= c < cols:
        points.add((r, c))
        r += step_r
        c += step_c
    
    # Negative direction  
    r, c = r1 - step_r, c1 - step_c
    while 0 <= r < rows and 0 <= c < cols:
        points.add((r, c))
        r -= step_r
        c -= step_c
    
    return points
```

## Final Part 2 Implementation (No GCD Needed!)
After testing, the simple approach works correctly:

```python
# Add antenna positions themselves as antinodes
for pos in positions:
    antinodes.add(pos)

# Extend lines using original displacement vector
for (r1, c1), (r2, c2) in combinations(positions, 2):
    dr, dc = r2 - r1, c2 - c1
    
    # Forward from second antenna
    r, c = r2 + dr, c2 + dc
    while 0 <= r < rows and 0 <= c < cols:
        antinodes.add((r, c))
        r += dr
        c += dc
    
    # Backward from first antenna  
    r, c = r1 - dr, c1 - dc
    while 0 <= r < rows and 0 <= c < cols:
        antinodes.add((r, c))
        r -= dr
        c -= dc
```

## Results
- **Part 1**: 341 unique antinodes (2x distance rule)
- **Part 2**: 1134 unique antinodes (continuous lines + antenna positions)
- **Example verification**: 14 → 34 ✅

## Key Insights
- Part 2 doesn't need GCD reduction - original vector spacing works
- Antenna positions become antinodes when 2+ same-frequency antennas exist
- Simple line extension in both directions captures all required positions