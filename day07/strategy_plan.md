# Day 7: Bridge Repair - Strategy Plan

## Problem Understanding
- Each line has a test value before the colon and numbers after
- Need to determine if operators (+, *) can be placed between numbers to produce the test value
- Operators are evaluated left-to-right (no precedence rules)
- Numbers cannot be rearranged
- Sum all test values from equations that can be made true

## Data Structures
1. **Equation class/tuple**: Store test value and list of numbers
2. **List of equations**: Parse all input lines into this structure

## Algorithm Approach (Recursive)
1. **Parse input**: Split each line by ':' to get test value and numbers
2. **Recursive evaluation**: Build result left-to-right, trying both operators at each step
   - Base case: If only one number left, check if it equals target
   - Recursive case: Try both '+' and '*' with first two numbers, recurse with remaining
3. **Early termination**: Stop recursion if current result exceeds target (optimization)
4. **Sum results**: Add test values of all valid equations

## Functions Needed
1. `parse_input(filename)`: Parse input file into list of (test_value, numbers) tuples
2. `can_be_solved_recursive(target, current_result, remaining_numbers)`: Recursive solver
3. `can_be_solved(test_value, numbers)`: Wrapper function
4. `solve_part1(filename)`: Main function to solve the problem

## Recursive Logic
- `can_be_solved_recursive(target, current, [next, ...rest])`
  - Try addition: `can_be_solved_recursive(target, current + next, rest)`
  - Try multiplication: `can_be_solved_recursive(target, current * next, rest)`
  - Return True if either path succeeds

## Time Complexity
- Still O(2^n) worst case, but with early pruning and cleaner logic
- Much more readable and follows the left-to-right evaluation naturally

---

# Part 2 Changes

## New Operator: Concatenation (||)
- Concatenation operator combines digits from left and right inputs
- Example: 12 || 345 = 12345
- All operators still evaluated left-to-right

## Updated Algorithm for Part 2
The recursive approach remains the same, but now we have three operators to try:
- Addition (+)
- Multiplication (*)
- Concatenation (||)

## Implementation Changes
1. **Concatenation function**: `concatenate(a, b)` returns `int(str(a) + str(b))`
2. **Updated recursion**: Try all three operators at each step
3. **Time complexity**: Now O(3^n) instead of O(2^n)

## Functions to Update
- `can_be_solved_recursive()`: Add third branch for concatenation
- Early termination still applies (concatenation only makes numbers larger)

## Expected Results
- Part 1 example result: 3749 (3 valid equations)
- Part 2 example result: 11387 (6 valid equations total)
- New valid equations in part 2:
  - 156: 15 || 6 = 156
  - 7290: 6 * 8 || 6 * 15 = 7290
  - 192: 17 || 8 + 14 = 192

---

# Implementation Status

## ✅ Completed Files
- `strategy_plan.md`: Complete strategy and algorithm documentation
- `example.txt`: Test data extracted from problem description
- `solution_part1.py`: Recursive solution with +, * operators
- `solution_part2.py`: Extended solution with +, *, || operators

## ✅ Key Features Implemented
- Recursive left-to-right evaluation approach (no brute force iteration)
- Early termination optimization when result exceeds target
- Command-line options for testing and debug modes
- Proper input parsing and error handling
- Clean, readable code following established patterns

## 🧪 Testing Commands
```bash
python3 solution_part1.py --test  # Expected: 3749
python3 solution_part2.py --test  # Expected: 11387
python3 solution_part1.py         # Run on actual input
python3 solution_part2.py         # Run on actual input
```