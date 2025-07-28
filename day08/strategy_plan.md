# Day 8: Resonant Collinearity - Strategy Plan

## Problem Understanding
- Grid map with antennas marked by lowercase letters, uppercase letters, or digits
- Antennas of same frequency create antinodes at specific positions
- Antinode occurs when one antenna is twice as far away as the other on the same line
- For each pair of same-frequency antennas, there are 2 antinodes (one on each side)  
- Count unique antinode locations within map bounds

## Key Rules
1. Antinodes only form between antennas of the same frequency
2. Antinodes are collinear with the antenna pair
3. One antenna must be exactly twice as far from the antinode as the other
4. Antinodes can overlap with antenna positions
5. Only count antinodes within the map boundaries

## Antinode Calculation
For two antennas at positions (r1, c1) and (r2, c2):
- Vector from antenna1 to antenna2: (dr, dc) = (r2-r1, c2-c1)
- Antinode1 (beyond antenna2): (r2 + dr, c2 + dc)
- Antinode2 (beyond antenna1): (r1 - dr, c1 - dc)

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

---

# Part 1 Results ✅
- **Test case**: 14 unique antinodes (expected)
- **Actual input**: 341 unique antinodes (accepted answer)
- **Implementation**: Discrete antinode calculation with 2x distance rule

# Part 2 Results ✅  
- **Test case**: 34 unique antinodes (expected, up from 14)
- **Actual input**: 1134 unique antinodes (accepted answer, up from 341)
- **Implementation**: Continuous line extension + antenna positions as antinodes

---

# Part 2: Resonant Harmonics

## Key Changes from Part 1
1. **New Rule**: Antinodes occur at ANY grid position exactly in line with 2+ same-frequency antennas
2. **No Distance Limit**: Not just 2x distance, but entire collinear lines
3. **Antenna Positions**: Antennas themselves become antinodes (if 2+ same frequency exist)
4. **Expected Results**: Example should go from 14 → 34

## Part 2 Algorithm
1. **For each frequency with 2+ antennas**:
   - Add all antenna positions as antinodes
   - For each pair of antennas, extend the line in both directions until out of bounds
2. **Line Extension**: 
   - Calculate displacement vector (dr, dc)
   - Walk forward: (r2+dr, c2+dc), (r2+2*dr, c2+2*dc), ...
   - Walk backward: (r1-dr, c1-dc), (r1-2*dr, c1-2*dc), ...
   - Continue until out of bounds

## Implementation Changes
```python
# Part 1: Only 2 specific antinodes per pair
antinode1 = (r1 - dr, c1 - dc)
antinode2 = (r2 + dr, c2 + dc)

# Part 2: All positions along the line
# Add antenna positions themselves
for pos in positions:
    antinodes.add(pos)

# Extend lines in both directions
r, c = r2 + dr, c2 + dc
while 0 <= r < rows and 0 <= c < cols:
    antinodes.add((r, c))
    r += dr
    c += dc
```