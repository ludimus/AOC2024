from typing import List, Tuple

def parse_input(filename: str) -> List[Tuple[int, List[int]]]:
    """Parse input file and return list of (target, numbers) tuples."""
    equations = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Split on colon
            target_str, numbers_str = line.split(':', 1)
            target = int(target_str.strip())
            
            # Split numbers on whitespace
            numbers = [int(x) for x in numbers_str.strip().split()]
            
            equations.append((target, numbers))
    
    return equations

def test_parsing():
    """Test the parsing function on example data."""
    print("Testing parsing function on example data...")
    
    equations = parse_input('example.txt')
    
    print(f"Parsed {len(equations)} equations:")
    for target, numbers in equations:
        print(f"  {target}: {numbers}")
    
    # Verify specific examples from the problem
    expected = [
        (190, [10, 19]),
        (3267, [81, 40, 27]),
        (83, [17, 5]),
        (156, [15, 6]),
        (7290, [6, 8, 6, 15]),
        (161011, [16, 10, 13]),
        (192, [17, 8, 14]),
        (21037, [9, 7, 18, 13]),
        (292, [11, 6, 16, 20])
    ]
    
    print("\nVerifying parsed data:")
    for i, (exp_target, exp_numbers) in enumerate(expected):
        target, numbers = equations[i]
        if target == exp_target and numbers == exp_numbers:
            print(f"  ✓ Equation {i+1}: {target} = {numbers}")
        else:
            print(f"  ✗ Equation {i+1}: Expected {exp_target}={exp_numbers}, got {target}={numbers}")

if __name__ == "__main__":
    test_parsing()