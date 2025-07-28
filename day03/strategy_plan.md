# Day 3 Strategy Plan

## Problem Summary

**Part 1**: Parse corrupted memory to find valid `mul(X,Y)` instructions and sum their results.

## Challenge Details

- **Input**: Corrupted computer memory with jumbled instructions
- **Valid Instructions**: `mul(X,Y)` where X and Y are 1-3 digit numbers
- **Invalid**: Any malformed sequences like `mul(4*`, `mul(6,9!`, `?(12,34)`, `mul ( 2 , 4 )`
- **Goal**: Find all valid mul instructions, calculate their products, sum the results

## Data Structures

- **Input**: String of corrupted memory
- **Processing**: Use regex to find valid `mul(X,Y)` patterns
- **Output**: Sum of all multiplication results

## Algorithm Approach

### Pattern Matching Strategy
1. Use regular expression to find all valid `mul(digit,digit)` patterns
2. Extract the two numbers from each match
3. Multiply the numbers and add to running sum
4. Return total sum

### Regex Pattern
- Pattern: `mul\((\d{1,3}),(\d{1,3})\)`
- Matches: `mul(` + 1-3 digits + `,` + 1-3 digits + `)`
- Captures: The two number groups for multiplication

## Functions Needed

- `parse_input(filename)`: Read file and return memory string
- `find_valid_mul_instructions(memory)`: Use regex to find all valid mul patterns
- `calculate_total(instructions)`: Sum all multiplication results
- `main()`: Handle command line args (test mode, debug mode)

## Example Data
```
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
```

Valid instructions:
- `mul(2,4)` → 2×4 = 8
- `mul(5,5)` → 5×5 = 25  
- `mul(11,8)` → 11×8 = 88
- `mul(8,5)` → 8×5 = 40

Expected total: 8 + 25 + 88 + 40 = **161**

## Part 2: Conditional Instructions

**New Instructions**:
- `do()`: Enables future mul instructions
- `don't()`: Disables future mul instructions
- **Initial state**: mul instructions are enabled
- **Rule**: Only the most recent do()/don't() applies

### Algorithm for Part 2
1. Find all instructions in order: `mul(X,Y)`, `do()`, `don't()`
2. Track enabled/disabled state as we process instructions
3. Only process mul instructions when enabled
4. Sum results of enabled mul instructions only

### Updated Regex Strategy
- Combined pattern: `(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))`
- Process matches sequentially to maintain state
- Track enabled flag and apply mul instructions conditionally

### Example for Part 2
```
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
```

Processing:
1. `mul(2,4)` → enabled → 2×4 = 8 ✓
2. `don't()` → disable mul instructions
3. `mul(5,5)` → disabled → skip ✗
4. `mul(32,64]` → invalid format → skip ✗
5. `mul(11,8)` → disabled → skip ✗
6. `do()` → enable mul instructions  
7. `mul(8,5)` → enabled → 8×5 = 40 ✓

Expected total: 8 + 40 = **48**