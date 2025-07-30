# Day 24: Crossed Wires - Strategy Plan

## Problem Analysis
Simulate a boolean logic circuit with AND, OR, and XOR gates to produce a decimal number from z-wires.

## Key Requirements
- Two input sections: initial wire values and gate definitions
- Three gate types: AND, OR, XOR with standard boolean logic
- Gates wait for both inputs before producing output
- No loops in the circuit - acyclic directed graph
- Output: decimal number formed by z-wires (z00 = LSB, z01, z02, etc.)

## Data Structures
- **Wire values**: Dictionary mapping wire names to boolean values (0/1)
- **Gate definitions**: List of tuples (input1, operation, input2, output)
- **Dependency graph**: Track which gates depend on which wires
- **Output collection**: Sort z-wires numerically to form binary number

## Algorithm Steps
1. Parse initial wire values from first section
2. Parse gate definitions from second section
3. Simulate gates in dependency order (topological sort or queue-based)
4. Continue until all z-wires have values
5. Convert z-wire binary sequence to decimal

## Functions Needed
1. `parse_input(filename)` - Parse wire values and gate definitions
2. `simulate_gates(wires, gates)` - Run circuit simulation
3. `get_z_output(wires)` - Extract and convert z-wire values to decimal
4. `solve(filename)` - Main solution function

## Gate Logic
- AND: output = input1 & input2
- OR: output = input1 | input2  
- XOR: output = input1 ^ input2

## Implementation Plan
1. Parse input into initial wires and gate list
2. Use queue-based simulation: process gates when both inputs available
3. Extract z-wires in order and convert binary to decimal
4. Test with example data first

## Part 1 Results ✓
- Example: binary 0011111101000 = decimal 2024 ✓
- Actual puzzle input result: 52038112429798
- Queue-based simulation handles acyclic gate network efficiently

## Part 2 Analysis
**New Problem**: Fix a binary adder circuit by finding 4 pairs of swapped gate outputs.

**Key Insights**:
- The circuit is supposed to perform binary addition: x + y = z
- System has exactly 4 pairs of gates with swapped outputs (8 wires total)
- Need to identify which gates have incorrect output connections
- Goal: Make the circuit correctly add any x and y inputs

**Binary Adder Structure**:
- Should implement ripple-carry adder or similar
- Each bit position needs: sum bit (XOR) and carry bit (AND + OR logic)
- Pattern: `xi XOR yi XOR carry_in -> zi`, `(xi AND yi) OR (carry_in AND (xi XOR yi)) -> carry_out`

**Algorithm Approaches**:
1. **Pattern Analysis**: Analyze expected adder structure vs actual gates
2. **Test Cases**: Try multiple x,y inputs and detect incorrect z outputs
3. **Constraint Satisfaction**: Find swaps that make all test cases work
4. **Graph Analysis**: Look for structural anomalies in gate connections

**Implementation Strategy**:
1. Generate test cases with known correct x + y = z results
2. Try all possible 4-pair swaps (combinatorial search)
3. For each swap configuration, test if it produces correct results
4. Return the 8 wire names involved in swaps, sorted

**Part 2 Results ✓**:
- **Correct Answer**: `cph,jqn,kwb,qkf,tgr,z12,z16,z24`
- **Successful Strategy**: Systematic full adder analysis
- **Key Insight**: Treat as standard 45-bit ripple-carry adder

**The 4 Swapped Pairs**:
1. **`z12 ↔ kwb`**: `z12` gets `x12 AND y12` instead of sum; `kwb` gets correct sum `ggr XOR hnd`
2. **`z16 ↔ qkf`**: `z16` gets `gkw AND cmc` instead of sum; `qkf` gets correct sum `gkw XOR cmc`
3. **`z24 ↔ tgr`**: `z24` gets `vhm OR wwd` instead of sum; `tgr` gets correct sum `ttg XOR stj`
4. **`jqn ↔ cph`**: `jqn` is `x29 AND y29` but feeds z29; `cph` is `x29 XOR y29` but goes elsewhere

**Two-Approach Method**:
1. **Bit-by-bit testing**: Test x + y = z with various patterns to find failing bits
2. **Structure analysis**: Compare actual gates with expected full adder structure

**Algorithm Success**:
- Identified all z-wires with wrong operations (AND/OR instead of XOR)
- Traced xi XOR yi usage to find correct sum generators
- Found structural anomaly in bit 29 where AND/XOR results were swapped