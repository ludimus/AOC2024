#!/usr/bin/env python3

def create_visual_diagram():
    print("=== Day 24 Part 1 Example - Visual Circuit Diagram ===\n")
    
    # Initial values
    print("INITIAL WIRE VALUES:")
    initial_values = {
        'x00': 1, 'x01': 0, 'x02': 1, 'x03': 1, 'x04': 0,
        'y00': 1, 'y01': 1, 'y02': 1, 'y03': 1, 'y04': 1
    }
    
    for wire, value in sorted(initial_values.items()):
        print(f"  {wire}: {value}")
    
    print("\nGATE CONNECTIONS AND OPERATIONS:")
    print("(Showing how gates connect inputs to outputs)\n")
    
    # Group gates by their function for better visualization
    gates = [
        ('ntg', 'XOR', 'fgs', 'mjb'),
        ('y02', 'OR', 'x01', 'tnw'), 
        ('kwq', 'OR', 'kpj', 'z05'),
        ('x00', 'OR', 'x03', 'fst'),
        ('tgd', 'XOR', 'rvg', 'z01'),
        ('vdt', 'OR', 'tnw', 'bfw'),
        ('bfw', 'AND', 'frj', 'z10'),
        ('ffh', 'OR', 'nrd', 'bqk'),
        ('y00', 'AND', 'y03', 'djm'),
        ('y03', 'OR', 'y00', 'psh'),
        ('bqk', 'OR', 'frj', 'z08'),
        ('tnw', 'OR', 'fst', 'frj'),
        ('gnj', 'AND', 'tgd', 'z11'),
        ('bfw', 'XOR', 'mjb', 'z00'),
        ('x03', 'OR', 'x00', 'vdt'),
        ('gnj', 'AND', 'wpb', 'z02'),
        ('x04', 'AND', 'y00', 'kjc'),
        ('djm', 'OR', 'pbm', 'qhw'),
        ('nrd', 'AND', 'vdt', 'hwm'),
        ('kjc', 'AND', 'fst', 'rvg'),
        ('y04', 'OR', 'y02', 'fgs'),
        ('y01', 'AND', 'x02', 'pbm'),
        ('ntg', 'OR', 'kjc', 'kwq'),
        ('psh', 'XOR', 'fgs', 'tgd'),
        ('qhw', 'XOR', 'tgd', 'z09'),
        ('pbm', 'OR', 'djm', 'kpj'),
        ('x03', 'XOR', 'y03', 'ffh'),
        ('x00', 'XOR', 'y04', 'ntg'),
        ('bfw', 'OR', 'bqk', 'z06'),
        ('nrd', 'XOR', 'fgs', 'wpb'),
        ('frj', 'XOR', 'qhw', 'z04'),
        ('bqk', 'OR', 'frj', 'z07'),
        ('y03', 'OR', 'x01', 'nrd'),
        ('hwm', 'AND', 'bqk', 'z03'),
        ('tgd', 'XOR', 'rvg', 'z12'),
        ('tnw', 'OR', 'pbm', 'gnj')
    ]
    
    # Show a few key gate calculations step by step
    print("STEP-BY-STEP CALCULATION (first few gates):")
    print()
    
    # Calculate some intermediate values to show the flow
    step_by_step = [
        # Direct from inputs
        ("x00 XOR y04", "1 XOR 1", "0", "ntg"),
        ("y04 OR y02", "1 OR 1", "1", "fgs"), 
        ("y02 OR x01", "1 OR 0", "1", "tnw"),
        ("x00 OR x03", "1 OR 1", "1", "fst"),
        ("x03 OR x00", "1 OR 1", "1", "vdt"),
        ("y00 AND y03", "1 AND 1", "1", "djm"),
        ("y03 OR y00", "1 OR 1", "1", "psh"),
        ("y01 AND x02", "1 AND 1", "1", "pbm"),
        ("x04 AND y00", "0 AND 1", "0", "kjc"),
        ("x03 XOR y03", "1 XOR 1", "0", "ffh"),
        ("y03 OR x01", "1 OR 0", "1", "nrd"),
        
        # Second level
        ("ntg XOR fgs", "0 XOR 1", "1", "mjb"),
        ("vdt OR tnw", "1 OR 1", "1", "bfw"),
        ("tnw OR fst", "1 OR 1", "1", "frj"),
        ("psh XOR fgs", "1 XOR 1", "0", "tgd"),
        ("ntg OR kjc", "0 OR 0", "0", "kwq"),
        ("djm OR pbm", "1 OR 1", "1", "qhw"),
        ("pbm OR djm", "1 OR 1", "1", "kpj"),
        ("ffh OR nrd", "0 OR 1", "1", "bqk"),
        ("nrd AND vdt", "1 AND 1", "1", "hwm"),
        ("kjc AND fst", "0 AND 1", "0", "rvg"),
        ("nrd XOR fgs", "1 XOR 1", "0", "wpb"),
        ("tnw OR pbm", "1 OR 1", "1", "gnj"),
        
        # Output calculations  
        ("bfw XOR mjb", "1 XOR 1", "0", "z00"),
        ("tgd XOR rvg", "0 XOR 0", "0", "z01"),
        ("gnj AND wpb", "1 AND 0", "0", "z02"),
        ("hwm AND bqk", "1 AND 1", "1", "z03"),
        ("frj XOR qhw", "1 XOR 1", "0", "z04"),
        ("kwq OR kpj", "0 OR 1", "1", "z05"),
    ]
    
    for calculation, values, result, output in step_by_step:
        print(f"  {calculation:15} = {values:9} = {result} → {output}")
    
    print("\n" + "="*60)
    print("FINAL RESULT VISUALIZATION:")
    print("="*60)
    
    # Show final z-wire values
    final_z_values = [
        ('z00', 0), ('z01', 0), ('z02', 0), ('z03', 1), ('z04', 0),
        ('z05', 1), ('z06', 1), ('z07', 1), ('z08', 1), ('z09', 1),
        ('z10', 1), ('z11', 0), ('z12', 0)
    ]
    
    print("\nFINAL Z-WIRE VALUES (LSB to MSB):")
    binary_result = ""
    for wire, value in final_z_values:
        print(f"  {wire}: {value}")
        binary_result = str(value) + binary_result  # Build MSB first
    
    print(f"\nBINARY NUMBER: {binary_result}")
    print(f"DECIMAL VALUE: {int(binary_result, 2)}")
    
    print("\nCONCEPTUAL FLOW DIAGRAM:")
    print("""
    INPUT LAYER:      INTERMEDIATE LAYER:       OUTPUT LAYER:
    
    x00: 1 ──┐
             ├─ OR ──→ fst ──┐
    x03: 1 ──┘              │
                             ├─ OR ──→ frj ──┐
    y02: 1 ──┐              │              │
             ├─ OR ──→ tnw ──┘              │
    x01: 0 ──┘                             │
                                           ├─ XOR ──→ z04: 0
    y00: 1 ──┐                             │
             ├─ AND ──→ djm ──┐             │
    y03: 1 ──┘               │             │
                             ├─ OR ──→ qhw ──┘
    y01: 1 ──┐               │
             ├─ AND ──→ pbm ──┘
    x02: 1 ──┘
    
    [... and so on for all gates ...]
    
    FINAL OUTPUT: z12 z11 z10 z09 z08 z07 z06 z05 z04 z03 z02 z01 z00
                   0   0   1   1   1   1   1   1   0   1   0   0   0
                                  = 0011111101000₂ = 2024₁₀
    """)

if __name__ == "__main__":
    create_visual_diagram()