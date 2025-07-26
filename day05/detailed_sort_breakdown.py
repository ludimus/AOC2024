# Detailed breakdown of sorting the last example update: [97, 13, 75, 29, 47]

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

def show_applicable_rules(update, rules):
    """Show which rules apply to this specific update"""
    print(f"=== APPLICABLE RULES FOR {update} ===")
    update_set = set(update)
    applicable_rules = []
    
    for before_page, after_pages in rules.items():
        if before_page in update_set:
            for after_page in after_pages:
                if after_page in update_set:
                    applicable_rules.append((before_page, after_page))
    
    print("Rules that apply to pages in this update:")
    for before, after in sorted(applicable_rules):
        print(f"  {before}|{after} - Page {before} must come before page {after}")
    
    print(f"\nTotal applicable rules: {len(applicable_rules)}")
    return applicable_rules

def simulate_sorting_step_by_step():
    """Simulate Python's sorting algorithm step by step"""
    rules = parse_input('example.txt')
    update = [97, 13, 75, 29, 47]
    
    print(f"=== STEP-BY-STEP SORTING OF {update} ===")
    print("Target: [97, 75, 47, 29, 13]")
    print()
    
    # Show applicable rules first
    applicable_rules = show_applicable_rules(update, rules)
    print()
    
    # Create comparator with detailed logging
    comparison_count = 0
    
    def detailed_compare(page_a, page_b):
        nonlocal comparison_count
        comparison_count += 1
        
        print(f"Step {comparison_count}: Compare {page_a} vs {page_b}")
        
        # Check rule page_a|page_b
        if page_a in rules and page_b in rules[page_a]:
            print(f"  Found rule {page_a}|{page_b}")
            print(f"  → {page_a} should come BEFORE {page_b}")
            print(f"  → Return -1 (keep current order: {page_a} before {page_b})")
            print()
            return -1
        
        # Check rule page_b|page_a
        if page_b in rules and page_a in rules[page_b]:
            print(f"  Found rule {page_b}|{page_a}")
            print(f"  → {page_b} should come BEFORE {page_a}")
            print(f"  → Return 1 (SWAP: {page_b} should come before {page_a})")
            print()
            return 1
        
        # No rule
        print(f"  No rule between {page_a} and {page_b}")
        print(f"  → Return 0 (maintain current relative position)")
        print()
        return 0
    
    print("=== SORTING PROCESS ===")
    print("Python uses a stable sorting algorithm (Timsort)")
    print("It makes pairwise comparisons to determine the final order")
    print()
    
    # Perform the sort
    sorted_update = sorted(update, key=cmp_to_key(detailed_compare))
    
    print(f"=== FINAL RESULT ===")
    print(f"Original: {update}")
    print(f"Sorted:   {sorted_update}")
    print(f"Expected: [97, 75, 47, 29, 13]")
    print(f"Correct:  {sorted_update == [97, 75, 47, 29, 13]}")
    print(f"Total comparisons made: {comparison_count}")

def show_why_each_position():
    """Explain why each page ends up in its final position"""
    rules = parse_input('example.txt')
    update = [97, 13, 75, 29, 47]
    final = [97, 75, 47, 29, 13]
    
    print("\n=== WHY EACH PAGE ENDS UP WHERE IT DOES ===")
    
    explanations = {
        97: "Position 1 (first): 97 has rules to ALL other pages (97|13, 97|75, 97|29, 97|47)",
        75: "Position 2: 75 comes after 97 (rule 97|75) but before all others (75|13, 75|29, 75|47)",
        47: "Position 3: 47 comes after 97,75 but before 29,13 (rules 97|47, 75|47, 47|29, 47|13)",
        29: "Position 4: 29 comes after 97,75,47 but before 13 (rules 97|29, 75|29, 47|29, 29|13)",
        13: "Position 5 (last): 13 comes after ALL others (97|13, 75|13, 47|13, 29|13)"
    }
    
    for i, page in enumerate(final, 1):
        print(f"{page}: {explanations[page]}")

def show_violation_fixes():
    """Show what violations were fixed by the sorting"""
    print("\n=== VIOLATIONS FIXED BY SORTING ===")
    
    original = [97, 13, 75, 29, 47]
    final = [97, 75, 47, 29, 13]
    
    print("Original violations:")
    violations = [
        ("75 at position 3, but 97|75 says 97 should come first", "75 before 97"),
        ("29 at position 4, but 75|29 says 75 should come first", "29 before 75"), 
        ("47 at position 5, but 75|47 says 75 should come first", "47 before 75"),
        ("47 at position 5, but 29|47 violates 47|29", "47 after 29 (should be before)"),
        ("13 at position 2, but many rules violated", "13 in wrong position")
    ]
    
    for violation, simple in violations:
        print(f"  ❌ {simple}")
    
    print("\nAfter sorting - all violations fixed:")
    print(f"  ✅ {final} - respects all applicable rules")

if __name__ == "__main__":
    simulate_sorting_step_by_step()
    show_why_each_position()
    show_violation_fixes()