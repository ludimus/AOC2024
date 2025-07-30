# Day 24: Crossed Wires

## Problem Summary

**Part 1**: Simulate a boolean logic circuit with AND, OR, XOR gates to produce a decimal number from z-wires.

**Part 2**: Fix a 45-bit binary adder by finding 4 pairs of swapped gate outputs (8 wires total).

## Key Files

- `solution_part1.py` - Circuit simulation (queue-based gate processing)
- `solution_part2.py` - Full adder analysis to find swapped wires  
- `analyze_full_adder_structure.py` - Educational analysis of bits 0-1
- `visualize_example.py` - Visual breakdown of Part 1 example
- `part2_simple_example.py` - Simple 3-bit adder example for learning
- `strategy_plan.md` - Complete analysis and results

## Results

- **Part 1**: 52038112429798
- **Part 2**: cph,jqn,kwb,qkf,tgr,z12,z16,z24

## Key Insights

1. **Part 2 Strategy**: Treat the circuit as a standard 45-bit ripple-carry adder
2. **Two-Approach Method**: 
   - Bit-by-bit testing (find failing arithmetic)
   - Structure analysis (find gates with wrong operations)
3. **Pattern Recognition**: All z-wires should be XOR operations (except z45)
4. **Swapped Pairs Found**:
   - `z12 ↔ kwb`: Sum vs intermediate wire
   - `z16 ↔ qkf`: Sum vs intermediate wire  
   - `z24 ↔ tgr`: Sum vs intermediate wire
   - `jqn ↔ cph`: AND vs XOR for bit 29

## Running

```bash
# Part 1
python3 solution_part1.py [--test] [--debug]

# Part 2  
python3 solution_part2.py [--test] [--debug]

# Educational analysis
python3 analyze_full_adder_structure.py
python3 visualize_example.py
```