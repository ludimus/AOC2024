# Day 4 Strategy Plan: XMAS Word Search

## Problem Analysis
- Find all occurrences of "XMAS" in a 2D grid
- Word can appear in 8 directions: horizontal (left/right), vertical (up/down), diagonal (4 directions)
- Words can overlap

## Data Structures
- **Grid**: 2D list of characters `grid[row][col]`
- **Directions**: List of 8 direction vectors for searching
- **Target word**: "XMAS" as string

## Algorithm Approach
1. **Parse Input**: Read grid into 2D list
2. **Direction Vectors**: Define 8 directions as (row_delta, col_delta) tuples
3. **Search Function**: For each position, try searching "XMAS" in all 8 directions
4. **Boundary Checking**: Ensure we don't go out of bounds
5. **Count Matches**: Sum all valid "XMAS" occurrences

## Functions Needed
- `parse_input(filename)`: Read file and return 2D grid
- `search_word(grid, row, col, direction, word)`: Check if word exists starting at position in given direction
- `count_xmas(grid)`: Main function to count all XMAS occurrences
- `main()`: Handle file selection and output

## Implementation Notes
- Use command line args for test/debug modes
- Test with example.txt (expected: 18 occurrences)
- Handle edge cases (boundaries, empty grid)

## Alternative Approach: Regex-Based Solution

### Concept
Instead of checking each position in 8 directions, extract all possible lines from the grid and use regex to find matches.

### Line Extraction
- **Horizontal**: All rows (10 lines for 10x10 grid)
- **Vertical**: All columns (10 lines for 10x10 grid)
- **Diagonals**: Extract all diagonal lines in both directions (~26 lines for 10x10 grid)
- **Total**: ~46 lines to search

### Regex Search
- Search for both "XMAS" (forward) and "SAMX" (backward) in each extracted line
- Use `re.findall()` for efficient pattern matching

### Performance Comparison Results
**Regex approach is ~2.6x faster than directional approach:**

- **Directional Method**: ~75ms average (70-88ms range)
  - Nested loops checking each position × 8 directions
  - Manual character-by-character validation
  - More Python overhead

- **Regex Method**: ~29ms average (28-37ms range)
  - Extract lines once, then regex search
  - Optimized regex engine
  - Fewer iterations overall

### Recommended Solution
Use the regex-based approach for both cleaner code and better performance. The line extraction step transforms the 2D search problem into multiple 1D regex searches, which is more efficient than the nested position checking.

## Part 2: X-MAS Pattern Search

### Problem Analysis
- Find X-MAS patterns: two "MAS" words forming an X shape
- Pattern structure:
  ```
  M.S
  .A.
  M.S
  ```
- Each "MAS" can be written forwards ("MAS") or backwards ("SAM")
- The center 'A' is shared between both diagonal "MAS" words
- Expected result: 9 occurrences in example

### Algorithm Approach
1. **Find Centers**: Look for 'A' characters that could be X centers
2. **Check Diagonals**: For each 'A', check both diagonal directions
3. **Validate Pattern**: Ensure both diagonals form "MAS" or "SAM"
4. **Boundary Check**: Ensure 'A' is not on edges (needs 3x3 space)

### Implementation Strategy
- Iterate through grid positions (excluding borders)
- For each 'A' at position (row, col):
  - Check diagonal 1: positions (row-1,col-1), (row,col), (row+1,col+1)
  - Check diagonal 2: positions (row-1,col+1), (row,col), (row+1,col-1)
  - Verify both diagonals spell "MAS" or "SAM"
- Count valid X-MAS patterns

### Functions Needed
- `parse_input(filename)`: Read grid (reuse from Part 1)
- `is_valid_xmas(grid, row, col)`: Check if 'A' at position forms valid X-MAS
- `count_xmas_patterns(grid)`: Count all X-MAS occurrences
- `main()`: Handle execution