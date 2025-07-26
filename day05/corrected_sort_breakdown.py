# CORRECTED: Detailed breakdown of sorting [97, 13, 75, 29, 47]

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

def corrected_analysis():
    """Corrected analysis of the sorting process"""
    rules = parse_input('example.txt')
    update = [97, 13, 75, 29, 47]
    
    print(f"=== CORRECTED ANALYSIS OF SORTING {update} ===")
    print("You're absolutely right! Let me fix the explanation.")
    print()
    
    print("Original array: [97, 13, 75, 29, 47]")
    print("Position indices: 0   1   2   3   4")
    print()
    
    print("Key insight: 97 is ALREADY before 13 (positions 0 and 1)")
    print("So when comparing them, NO SWAP is needed for this pair!")
    print()
    
    # Create corrected comparator with proper logging
    comparison_count = 0
    
    def corrected_compare(page_a, page_b):
        nonlocal comparison_count
        comparison_count += 1
        
        print(f"Comparison {comparison_count}: compare({page_a}, {page_b})")
        
        # Check rule page_a|page_b
        if page_a in rules and page_b in rules[page_a]:
            print(f"  Rule {page_a}|{page_b} exists → {page_a} should come before {page_b}")
            print(f"  Return -1 (first argument comes before second)")
            print()
            return -1
        
        # Check rule page_b|page_a
        if page_b in rules and page_a in rules[page_b]:
            print(f"  Rule {page_b}|{page_a} exists → {page_b} should come before {page_a}")
            print(f"  Return 1 (second argument comes before first)")
            print()
            return 1
        
        print(f"  No rule between {page_a} and {page_b}")
        print(f"  Return 0 (maintain relative order)")
        print()
        return 0
    
    # Perform the sort
    sorted_update = sorted(update, key=cmp_to_key(corrected_compare))
    
    print(f"=== RESULT ===")
    print(f"Original: {update}")
    print(f"Sorted:   {sorted_update}")

def show_what_actually_needs_fixing():
    """Show what elements actually need to move"""
    print("\n=== WHAT ACTUALLY NEEDS TO MOVE ===")
    
    original = [97, 13, 75, 29, 47]
    final = [97, 75, 47, 29, 13]
    
    print("Position analysis:")
    print("Original: [97, 13, 75, 29, 47]")
    print("Indices:   0   1   2   3   4")
    print()
    print("Final:    [97, 75, 47, 29, 13]") 
    print("Indices:   0   1   2   3   4")
    print()
    
    movements = {
        97: "Stays at position 0 ✓",
        13: "Moves from position 1 → position 4 (moves right)",
        75: "Moves from position 2 → position 1 (moves left)", 
        29: "Moves from position 3 → position 3 (stays same)",
        47: "Moves from position 4 → position 2 (moves left)"
    }
    
    print("Element movements:")
    for page, movement in movements.items():
        print(f"  {page}: {movement}")
    
    print()
    print("Key insight: 97 and 13 were already in correct RELATIVE order!")
    print("The issue was with OTHER elements being in wrong positions.")

def show_violated_rules_in_original():
    """Show which rules were actually violated in the original"""
    rules = parse_input('example.txt')
    original = [97, 13, 75, 29, 47]
    
    print("\n=== RULES VIOLATED IN ORIGINAL ORDER ===")
    
    # Create position mapping
    positions = {page: i for i, page in enumerate(original)}
    
    violations = []
    
    for before_page, after_pages in rules.items():
        if before_page in positions:
            for after_page in after_pages:
                if after_page in positions:
                    if positions[before_page] > positions[after_page]:
                        violations.append((before_page, after_page, positions[before_page], positions[after_page]))
    
    print("Actual rule violations:")
    for before, after, before_pos, after_pos in violations:
        print(f"  Rule {before}|{after} violated: {before} at pos {before_pos}, {after} at pos {after_pos}")
    
    print(f"\nNote: Rule 97|13 is NOT violated because 97 (pos 0) comes before 13 (pos 1)")

if __name__ == "__main__":
    corrected_analysis()
    show_what_actually_needs_fixing()
    show_violated_rules_in_original()