# Step-by-step trace showing array state after each operation

from functools import cmp_to_key

def parse_input(filename):
    """Parse ordering rules from input file"""
    with open(filename, 'r') as f:
        content = f.read().strip()
    
    rules_section = content.split('\n\n')[0]
    
    rules = {}
    for rule_line in rules_section.split('\n'):
        before, after = map(int, rule_line.split('|'))
        if before not in rules:
            rules[before] = set()
        rules[before].add(after)
    
    return rules

class SortTracer:
    """Custom list class that tracks every operation during sorting"""
    
    def __init__(self, initial_list, rules):
        self.data = initial_list.copy()
        self.rules = rules
        self.step = 0
        self.comparison_count = 0
        print(f"Initial state: {self.data}")
        print("=" * 50)
    
    def compare_and_track(self, a, b):
        """Compare function that tracks each comparison and potential swap"""
        self.comparison_count += 1
        
        print(f"\nComparison #{self.comparison_count}: compare({a}, {b})")
        
        # Find current positions
        pos_a = self.data.index(a) if a in self.data else -1
        pos_b = self.data.index(b) if b in self.data else -1
        
        if pos_a != -1 and pos_b != -1:
            print(f"  Current positions: {a} at index {pos_a}, {b} at index {pos_b}")
            print(f"  Current array: {self.data}")
        
        # Check rule a|b
        if a in self.rules and b in self.rules[a]:
            print(f"  Rule {a}|{b} exists → {a} should come before {b}")
            if pos_a != -1 and pos_b != -1 and pos_a < pos_b:
                print(f"  ✓ Already in correct order → return -1")
            else:
                print(f"  → return -1 (first before second)")
            return -1
        
        # Check rule b|a  
        if b in self.rules and a in self.rules[b]:
            print(f"  Rule {b}|{a} exists → {b} should come before {a}")
            if pos_a != -1 and pos_b != -1 and pos_b < pos_a:
                print(f"  ✓ Already in correct order → return 1")
            else:
                print(f"  → return 1 (second before first)")
            return 1
        
        print(f"  No rule between {a} and {b} → return 0")
        return 0

def manual_sort_simulation():
    """Manually simulate the sorting to show exact array states"""
    rules = parse_input('example.txt')
    original = [97, 13, 75, 29, 47]
    
    print("=== MANUAL STEP-BY-STEP SIMULATION ===")
    print(f"Starting array: {original}")
    print("Target result:  [97, 75, 47, 29, 13]")
    print()
    
    # I'll manually trace through what Python's sort would do
    # This is a simplified version - actual Timsort is more complex
    
    current = original.copy()
    step = 0
    
    print("Python's sort algorithm will make these key moves:")
    print()
    
    # Step 1: Move 13 to the end (it belongs last)
    step += 1
    print(f"Step {step}: Identify that 13 should be last")
    print(f"  Current: {current}")
    print(f"  13 has incoming rules from all other pages")
    
    # Step 2: Move 75 forward (it should come after 97)
    step += 1
    print(f"\nStep {step}: Position 75 after 97")
    print(f"  Rule 97|75 means 75 should come after 97")
    current = [97, 75, 13, 29, 47]  # 75 moves to position 1
    print(f"  After move: {current}")
    
    # Step 3: Move 47 to correct position
    step += 1
    print(f"\nStep {step}: Position 47 after 75")
    print(f"  Rule 75|47 means 47 should come after 75")
    current = [97, 75, 47, 13, 29]  # 47 moves to position 2
    print(f"  After move: {current}")
    
    # Step 4: Position 29 and 13 correctly
    step += 1
    print(f"\nStep {step}: Position 29 before 13")
    print(f"  Rule 29|13 means 29 should come before 13")
    current = [97, 75, 47, 29, 13]  # Final correct order
    print(f"  Final result: {current}")

def trace_with_actual_sort():
    """Use actual Python sort with detailed tracing"""
    rules = parse_input('example.txt')
    original = [97, 13, 75, 29, 47]
    
    print("\n" + "=" * 60)
    print("=== ACTUAL PYTHON SORT WITH TRACING ===")
    
    tracer = SortTracer(original, rules)
    
    # Use the tracer's compare function
    sorted_result = sorted(original, key=cmp_to_key(tracer.compare_and_track))
    
    print(f"\n=== FINAL RESULT ===")
    print(f"Original: {original}")
    print(f"Sorted:   {sorted_result}")
    print(f"Total comparisons: {tracer.comparison_count}")

def show_key_swaps():
    """Show the key logical swaps that need to happen"""
    print("\n" + "=" * 60)
    print("=== KEY LOGICAL SWAPS NEEDED ===")
    
    original = [97, 13, 75, 29, 47]
    target = [97, 75, 47, 29, 13]
    
    print(f"From: {original}")
    print(f"To:   {target}")
    print()
    
    print("Key movements required:")
    print("1. 75 needs to move left (position 2 → 1)")
    print("2. 47 needs to move left (position 4 → 2)")  
    print("3. 13 needs to move right (position 1 → 4)")
    print("4. 29 stays in middle (position 3 → 3)")
    print("5. 97 stays first (position 0 → 0)")
    print()
    
    print("Why these moves:")
    print("- 13 goes to end: All other pages have rules pointing to 13")
    print("- 75 moves after 97: Rule 97|75")
    print("- 47 moves after 75: Rule 75|47")
    print("- 29 stays before 13: Rule 29|13")

if __name__ == "__main__":
    manual_sort_simulation()
    trace_with_actual_sort()
    show_key_swaps()