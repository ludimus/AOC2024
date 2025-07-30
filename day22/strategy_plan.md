# Day 22: Monkey Market - Strategy Plan

## Problem Analysis
We need to simulate a pseudorandom number generator for each buyer to predict their 2000th secret number.

## Algorithm Steps
Each secret number evolves through these operations:
1. Multiply by 64, mix (XOR), prune (mod 16777216)
2. Divide by 32 (floor), mix (XOR), prune (mod 16777216)  
3. Multiply by 2048, mix (XOR), prune (mod 16777216)

## Data Structures
- **Input**: List of initial secret numbers (integers)
- **Processing**: Single integer for current secret number
- **Output**: Sum of all 2000th secret numbers

## Functions Needed
1. `parse_input(filename)` - Read initial secret numbers
2. `mix(value, secret)` - XOR operation
3. `prune(secret)` - Modulo 16777216 operation
4. `next_secret(secret)` - Apply the 3-step transformation
5. `generate_nth_secret(initial, n)` - Generate nth secret number
6. `solve(filename)` - Main solution function

## Implementation Plan
1. Parse input file to get initial secret numbers
2. For each initial secret, generate 2000 iterations
3. Sum all 2000th secret numbers
4. Test with example data first

## Part 1 Results ✓
- Example input (1, 10, 100, 2024) produces sum: 37327623
- Individual 2000th secrets: 8685429, 4700978, 15273692, 8667524
- Actual puzzle input result: 16619522798

## Part 2 Analysis
**New Problem**: Find optimal sequence of 4 consecutive price changes to maximize banana sales.

**Key Changes**:
- Prices = last digit of secret numbers (not the full secret)
- Need to track price changes (differences between consecutive prices)
- Find sequence of 4 changes that maximizes total bananas across all buyers
- Each buyer sells at FIRST occurrence of the sequence

**Data Structures for Part 2**:
- Price sequences: List of prices (last digits) for each buyer
- Change sequences: List of 4-tuples representing consecutive changes
- Pattern tracking: Map from change pattern to total bananas earned

**Algorithm**:
1. Generate all prices (last digits) for each buyer's 2000 secrets
2. Calculate price changes for each buyer
3. For each possible 4-change sequence, calculate total bananas
4. Return maximum total bananas possible

**Part 2 Results ✓**:
- Example 2 input: [1, 2, 3, 2024] → 23 bananas with sequence (-2, 1, -1, 3)
- Actual puzzle input result: 1854 bananas
- Algorithm successfully finds optimal 4-change pattern from ~7000 unique patterns
- Solution correctly handles first-occurrence-only constraint per buyer