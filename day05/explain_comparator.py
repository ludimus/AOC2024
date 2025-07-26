# Explain the custom comparator with detailed tracing

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

def compare_pages_verbose(page_a, page_b, rules):
    """Compare two pages with detailed explanation"""
    print(f"    Comparing {page_a} vs {page_b}:")
    
    # Check if there's a rule page_a|page_b (page_a must come before page_b)
    if page_a in rules and page_b in rules[page_a]:
        print(f"      Found rule {page_a}|{page_b} → {page_a} comes BEFORE {page_b} → return -1")
        return -1
    
    # Check if there's a rule page_b|page_a (page_b must come before page_a)  
    if page_b in rules and page_a in rules[page_b]:
        print(f"      Found rule {page_b}|{page_a} → {page_b} comes BEFORE {page_a} → return 1")
        return 1
    
    # No applicable rule
    print(f"      No rule between {page_a} and {page_b} → return 0 (maintain order)")
    return 0

def trace_sorting_process(update, rules):
    """Trace through the sorting process step by step"""
    print(f"\n=== TRACING SORT OF {update} ===")
    
    # Create a comparator that logs each comparison
    comparison_count = 0
    def logged_compare(page_a, page_b):
        nonlocal comparison_count
        comparison_count += 1
        print(f"  Comparison #{comparison_count}:")
        result = compare_pages_verbose(page_a, page_b, rules)
        return result
    
    # Sort with logging
    sorted_update = sorted(update, key=cmp_to_key(logged_compare))
    
    print(f"\n  Original: {update}")
    print(f"  Sorted:   {sorted_update}")
    print(f"  Total comparisons: {comparison_count}")
    
    return sorted_update

def explain_comparator_concept():
    """Explain how custom comparators work in Python"""
    print("=== HOW CUSTOM COMPARATORS WORK ===")
    print()
    print("Python's sorted() function needs to know how to compare elements.")
    print("For numbers: 3 < 5 is built-in")
    print("For our pages: We need custom rules!")
    print()
    print("Comparator function returns:")
    print("  -1: first element comes BEFORE second")
    print("   0: elements are equal (maintain current order)")
    print("   1: first element comes AFTER second")
    print()
    print("Example with numbers:")
    print("  compare(3, 5) → -1 because 3 < 5")
    print("  compare(5, 3) → 1 because 5 > 3")
    print("  compare(4, 4) → 0 because 4 == 4")
    print()
    print("Our page comparator:")
    print("  compare(97, 75) → -1 because rule 97|75 exists")
    print("  compare(75, 97) → 1 because rule 97|75 exists")
    print("  compare(42, 99) → 0 because no rule exists")
    print()

def show_all_example_fixes():
    """Trace all three example fixes"""
    rules = parse_input('example.txt')
    
    examples = [
        [75, 97, 47, 61, 53],
        [61, 13, 29], 
        [97, 13, 75, 29, 47]
    ]
    
    for update in examples:
        trace_sorting_process(update, rules)

def demonstrate_key_comparisons():
    """Show the most important comparisons that drive the sorting"""
    rules = parse_input('example.txt')
    
    print("\n=== KEY COMPARISONS THAT DRIVE SORTING ===")
    print()
    
    key_pairs = [
        (97, 75), (97, 47), (97, 61), (97, 53), (97, 29), (97, 13),
        (75, 47), (75, 61), (75, 53), (75, 29), (75, 13),
        (47, 61), (47, 53), (47, 29), (47, 13),
        (61, 53), (61, 29), (61, 13),
        (53, 29), (53, 13),
        (29, 13)
    ]
    
    print("These are the rules that establish the sorting order:")
    for page_a, page_b in key_pairs:
        result = compare_pages_verbose(page_a, page_b, rules)
        if result != 0:
            print()

if __name__ == "__main__":
    explain_comparator_concept()
    demonstrate_key_comparisons()
    
    print("\n" + "="*60)
    show_all_example_fixes()