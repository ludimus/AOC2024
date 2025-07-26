# Day 7: Bridge Repair - Strategy Plan

## Problem Analysis
- **Goal**: Determine which calibration equations can be made true by inserting operators
- **Part 1 Operators**: `+` (addition) and `*` (multiplication)
- **Part 2 Operators**: `+`, `*`, and `||` (concatenation)
- **Evaluation**: Left-to-right, no precedence rules
- **Constraints**: Numbers cannot be rearranged
- **Output**: Sum of all achievable test values

## Data Structures

### Input Parsing (Optimized)
```python
# Simple tuple approach instead of class
def parse_input(filename: str) -> List[Tuple[int, List[int]]]:
    equations = []
    for line in file:
        target_str, numbers_str = line.split(':', 1)
        target = int(target_str.strip())
        numbers = [int(x) for x in numbers_str.strip().split()]
        equations.append((target, numbers))
    return equations
```

### Core Data Types
- `target`: int - The test value we want to achieve
- `numbers`: List[int] - The operands in order
- Return format: `List[Tuple[int, List[int]]]` for memory efficiency

## Algorithm Approaches

### ❌ Brute Force Approach (Initial Implementation)
**Strategy**: Generate all operator combinations and test each one
**Complexity**: 
- Part 1: O(2^n) per equation
- Part 2: O(3^n) per equation

**Performance Results**:
- Part 1: 0.244 seconds for 850 equations
- Part 2: 22.194 seconds for 850 equations

### ✅ Optimized Reverse Engineering (Final Implementation)
**Strategy**: Work backwards from the target to find valid operator sequences

**Key Insight**: Instead of asking "What operators make this work?", ask "What could the previous result have been?"

#### Reverse Engineering Algorithm
```python
def can_make_target_reverse(target: int, numbers: List[int]) -> bool:
    if len(numbers) == 1:
        return target == numbers[0]
    
    last_num = numbers[-1]
    remaining = numbers[:-1]
    
    # Try each possible last operation:
    
    # Case 1: ... + last_num = target
    if target >= last_num:
        if can_make_target_reverse(target - last_num, remaining):
            return True
    
    # Case 2: ... * last_num = target  
    if target % last_num == 0:
        if can_make_target_reverse(target // last_num, remaining):
            return True
    
    # Case 3 (Part 2): ... || last_num = target
    if target_str.endswith(last_str) and len(target_str) > len(last_str):
        new_target = int(target_str[:-len(last_str)])
        if can_make_target_reverse(new_target, remaining):
            return True
    
    return False
```

## Detailed Examples

### Example 1: `190: [10, 19]` (Part 1)

**Brute Force**: Try 2^1 = 2 combinations
- `10 + 19 = 29` ≠ 190
- `10 * 19 = 190` ✓

**Reverse Engineering**:
1. `? op 19 = 190`
2. Try `? + 19 = 190` → `? = 171` → Check if `[10]` can make 171 → No
3. Try `? * 19 = 190` → `? = 10` → Check if `[10]` can make 10 → Yes ✓

### Example 2: `7290: [6, 8, 6, 15]` (Part 2)

**Brute Force**: Try 3^3 = 27 combinations
**Reverse Engineering**:
1. `? op 15 = 7290`
2. Try `? + 15 = 7290` → `? = 7275` → Try with `[6,8,6]` → No solution
3. Try `? * 15 = 7290` → `? = 486` → Try with `[6,8,6]` → Continue...
4. `? op 6 = 486`
5. Try `? || 6 = 486` → `? = 48` → Try with `[6,8]` → Continue...
6. `? op 8 = 48`
7. Try `? * 8 = 48` → `? = 6` → Check if `[6]` can make 6 → Yes ✓

**Solution**: `6 * 8 || 6 * 15 = 48 || 6 * 15 = 486 * 15 = 7290`

### Example 3: `156: [15, 6]` (Part 2 only)

**Part 1 Analysis**:
1. `? op 6 = 156`
2. Try `? + 6 = 156` → `? = 150` → Check if `[15]` can make 150 → No
3. Try `? * 6 = 156` → `? = 26` → Check if `[15]` can make 26 → No
4. **Result**: Impossible in Part 1

**Part 2 Analysis**:
1. `? op 6 = 156`
2. Try `? + 6 = 156` → No
3. Try `? * 6 = 156` → No  
4. Try `? || 6 = 156` → `? = 15` → Check if `[15]` can make 15 → Yes ✓

**Solution**: `15 || 6 = 156`

## Performance Comparison

| Approach | Part 1 Time | Part 2 Time | Part 1 Speedup | Part 2 Speedup |
|----------|-------------|-------------|----------------|----------------|
| Brute Force | 0.244s | 22.194s | 1x | 1x |
| Reverse Engineering | 0.008s | 0.023s | **30.5x** | **965x** |

## Complexity Analysis

### Brute Force
- **Part 1**: O(2^n) combinations per equation
- **Part 2**: O(3^n) combinations per equation
- **Space**: O(1) for evaluation

### Reverse Engineering  
- **Part 1**: O(2n) operations per equation (worst case)
- **Part 2**: O(3n) operations per equation (worst case)
- **Space**: O(n) for recursion stack
- **Key Advantage**: Heavy pruning eliminates most branches early

## Implementation Strategy (Optimized)

1. **Parse Input**: Use tuples instead of classes for memory efficiency
2. **Reverse Engineering**: Work backwards from target
3. **Early Pruning**: Invalid operations rejected immediately
4. **Recursive Structure**: Clean, readable code with logarithmic depth
5. **Performance Monitoring**: Track equations per second

## Part 2 Specific Considerations

### Concatenation Operator (`||`)
- **Mathematical representation**: `a || b = int(str(a) + str(b))`
- **Reverse operation**: If `target` ends with `b`'s digits, then `a = target[:-len(str(b))]`
- **Example**: `1234 || 567 = 1234567`, so if target=1234567 and b=567, then a=1234

### Performance Impact
- Adds third branch to recursion
- Still maintains linear complexity due to aggressive pruning
- 965x speedup proves the optimization is extremely effective

## Final Results
- **Part 1 Answer**: 21,572,148,763,543
- **Part 2 Answer**: 581,941,094,529,163
- **Achievable Rate**: Part 1: 32.7%, Part 2: 66.1%