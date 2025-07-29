# Day 13: Claw Contraption - Strategy Plan

## Problem Analysis
- Linear system of equations for each claw machine
- Part 1: Find integer solutions within constraints (≤100 button presses)
- Part 2: Remove press limit, add 10^13 offset to prize coordinates
- Minimize token cost while maximizing prizes won

## Data Structures
```python
class Machine:
    ax, ay: int  # Button A movement
    bx, by: int  # Button B movement
    px, py: int  # Prize position
```

## Functions Needed
1. `parse_input(filename, offset=0)` -> List[Machine]
2. `solve_machine(machine)` -> Optional[Tuple[int, int]]  # (a_presses, b_presses)
3. `calculate_cost(a_presses, b_presses)` -> int
4. `solve_all_machines(machines)` -> Tuple[int, int]  # (prizes_won, total_cost)

## Algorithm
1. Parse input into Machine objects (with optional offset for Part 2)
2. For each machine:
   - Solve linear system: a*ax + b*bx = px, a*ay + b*by = py
   - Use Cramer's rule or matrix determinant
   - Check if solution is non-negative integers (≤100 for Part 1 only)
   - Calculate cost if valid
3. Sum up all winnable prizes and costs

## Linear System Solution
Using Cramer's rule:
- det = ax*by - ay*bx
- a = (px*by - py*bx) / det
- b = (ax*py - ay*px) / det

## Results
- Part 1: 155 prizes, 31,552 tokens
- Part 2: 165 prizes, 95,273,925,552,482 tokens