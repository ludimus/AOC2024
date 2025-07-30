# Day 17: Chronospatial Computer - Strategy Plan

## Problem Analysis
**Part 1**: Simulate a 3-bit computer with 8 instructions, 3 registers (A, B, C), and an instruction pointer.
**Part 2**: Find the initial value of register A that makes the program output a copy of itself (quine problem).

## Data Structures
1. **Registers**: Dictionary `{'A': int, 'B': int, 'C': int}`
2. **Program**: List of integers `[2, 4, 1, 2, 7, 5, 4, 1, 1, 3, 5, 5, 0, 3, 3, 0]`
3. **Instruction Pointer**: Integer (starts at 0, increments by 2)
4. **Output**: List of integers to be joined with commas

## Functions Needed
1. **parse_input(filename)**: Parse register values and program from input file
2. **get_combo_value(operand, registers)**: Convert combo operand to actual value
3. **execute_instruction(opcode, operand, registers, ip, output)**: Execute single instruction
4. **run_program(registers, program)**: Main simulation loop
5. **main()**: Entry point with test/debug modes

## Algorithm Steps
1. Parse input to get initial register values and program
2. Initialize instruction pointer to 0 and empty output list
3. While instruction pointer < program length:
   - Read opcode and operand
   - Execute instruction based on opcode
   - Update registers, output, or instruction pointer as needed
   - Move instruction pointer by 2 (unless jump occurred)
4. Return comma-separated output

## Instruction Implementation
- **adv (0)**: A = A // (2^combo_operand)
- **bxl (1)**: B = B XOR literal_operand
- **bst (2)**: B = combo_operand % 8
- **jnz (3)**: Jump to literal_operand if A ≠ 0
- **bxc (4)**: B = B XOR C
- **out (5)**: Append combo_operand % 8 to output
- **bdv (6)**: B = A // (2^combo_operand)
- **cdv (7)**: C = A // (2^combo_operand)

## Testing Strategy - Part 1
- Test with example: A=729, B=0, C=0, Program=[0,1,5,4,3,0]
- Expected output: "4,6,3,5,6,3,5,2,1,0"
- Verify each instruction type works correctly

---

# Part 2: Quine Problem Analysis

## Problem Scale & Complexity
- **Target**: Program must output itself: `[2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0]` (16 digits)
- **Search Space**: A values range from ~8^15 to 8^16 (≈ 35 quadrillion to 281 quadrillion)
- **Brute Force**: Completely infeasible (would take decades)

## Key Insights - Program Structure Analysis

### The Hierarchical Pattern
Every program iteration follows this pattern:
1. **Process current A value** → produces one output digit
2. **A = A // 8** (adv 3 instruction) → reduces A for next iteration
3. **Loop until A = 0** (jnz 0 instruction)

This creates a tree structure:
```
A=37221261688308 → [2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0] (16 digits)
  ↓ (÷8)
A=4652657711038  → [4,1,2,7,5,4,1,1,3,5,5,0,3,3,0]   (15 digits)
  ↓ (÷8)  
A=581582213879   → [1,2,7,5,4,1,1,3,5,5,0,3,3,0]     (14 digits)
  ... continues until A=0
```

### Why Backtracking Works
1. **Deterministic**: Same A always produces same output
2. **Hierarchical**: A → A//8 → A//64 creates searchable tree
3. **Finite Branches**: Only 8 possible 3-bit extensions (0-7) at each level
4. **Early Pruning**: Discard branches that don't produce correct suffix

## Solution Approaches & Performance

### 1. Brute Force Approach ❌
```python
def brute_force_solution(program, max_attempts=10000000):
    for a in range(1, max_attempts):
        if run_program({'A': a, 'B': 0, 'C': 0}, program) == program:
            return a
```
**Performance**: 
- Example (6 digits): 0.515s, 117,440 attempts
- Actual (16 digits): Failed after 200,000 attempts in 2.7s
- **Theoretical time for full search**: ~89 years

### 2. Backtracking Approach ✅
```python
def solve_with_backtracking(program):
    def dfs(a_candidate, target_index):
        if target_index < 0:
            return a_candidate
        
        for digit in range(8):  # Try all 3-bit extensions
            new_a = a_candidate + digit * (8 ** target_index)
            output = run_program({'A': new_a, 'B': 0, 'C': 0}, program)
            
            if output[target_index:] == program[target_index:]:
                result = dfs(new_a, target_index - 1)
                if result is not None:
                    return result
        return None
    
    return dfs(0, len(program) - 1)
```
**Performance**:
- Example (6 digits): Not tested, but would be ~0.001s
- Actual (16 digits): **0.005s** ⚡
- **Speedup**: ~500,000x faster than brute force could theoretically be

### 3. Mathematical Approach ❌
Attempted to analyze the specific instruction sequence mathematically, but the complex interactions between instructions make this approach difficult to implement correctly.

## Algorithm Walkthrough - Backtracking

### Step-by-Step Process
1. **Start with full target**: `[2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0]`
2. **Find A candidates for last digit** (0): Try A=0,1,2,3,4,5,6,7
3. **Extend to produce last 2 digits** (3,0): Try A=candidate×8+digit for digit=0-7
4. **Continue building**: Keep extending until we match the full sequence
5. **Return minimum valid A**

### Tree Search Visualization
```
Level 0: Find A producing [0]           → ~8 candidates
Level 1: Extend to produce [3,0]        → ~8 candidates  
Level 2: Extend to produce [3,3,0]      → ~8 candidates
...
Level 15: Full sequence match           → 1 solution
```

**Total candidates tested**: ~8 × 16 = 128 (vs 281 trillion for brute force)

## Performance Summary

| Method | Time Complexity | Actual Performance | Success Rate |
|--------|----------------|-------------------|--------------|
| Brute Force | O(8^n) | 2.7s for 200K attempts | ❌ Infeasible |
| Backtracking | O(8×n) | 0.005s | ✅ Fast & Reliable |
| Mathematical | O(1) theoretical | Failed implementation | ❌ Too Complex |

**Final Answer**: A = 37,221,261,688,308

## Implementation Files
- `solution_part1.py`: Basic computer simulator
- `solution_part2_final.py`: All three approaches with performance testing
- `backtracking_demo.py`: Educational explanation of the algorithm