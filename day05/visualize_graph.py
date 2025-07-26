# Visualize the dependency graph from Day 5 example input

def parse_rules(filename):
    """Parse just the rules from input file"""
    with open(filename, 'r') as f:
        content = f.read().strip()
    
    rules_section = content.split('\n\n')[0]
    
    # Parse rules into list of tuples and dictionary
    rule_list = []
    rules_dict = {}
    
    for rule_line in rules_section.split('\n'):
        before, after = map(int, rule_line.split('|'))
        rule_list.append((before, after))
        
        if before not in rules_dict:
            rules_dict[before] = set()
        rules_dict[before].add(after)
    
    return rule_list, rules_dict

def get_all_pages(rule_list):
    """Get all unique pages mentioned in rules"""
    pages = set()
    for before, after in rule_list:
        pages.add(before)
        pages.add(after)
    return sorted(pages)

def visualize_graph(filename='example.txt'):
    """Create a text visualization of the dependency graph"""
    rule_list, rules_dict = parse_rules(filename)
    all_pages = get_all_pages(rule_list)
    
    print("=== DEPENDENCY GRAPH VISUALIZATION ===")
    print(f"Pages: {all_pages}")
    print(f"Total rules: {len(rule_list)}")
    print()
    
    print("Raw rules (before|after):")
    for before, after in rule_list:
        print(f"  {before}|{after}")
    print()
    
    print("Dependency structure (page → pages_that_must_come_after):")
    for page in sorted(rules_dict.keys()):
        after_pages = sorted(rules_dict[page])
        print(f"  {page} → {after_pages}")
    print()
    
    # Show which pages have no dependencies (could be first)
    pages_with_deps = set(rules_dict.keys())
    pages_as_deps = set()
    for after_set in rules_dict.values():
        pages_as_deps.update(after_set)
    
    no_incoming = pages_with_deps - pages_as_deps
    only_incoming = pages_as_deps - pages_with_deps
    
    print("Graph analysis:")
    print(f"  Pages with no incoming edges (could be first): {sorted(no_incoming)}")
    print(f"  Pages with no outgoing edges (could be last): {sorted(only_incoming)}")
    print()
    
    return rule_list, rules_dict

def show_example_fixes(filename='example.txt'):
    """Show how the graph helps fix the invalid updates"""
    print("=== HOW GRAPH HELPS FIX UPDATES ===")
    
    with open(filename, 'r') as f:
        content = f.read().strip()
    updates_section = content.split('\n\n')[1]
    
    updates = []
    for line in updates_section.split('\n'):
        updates.append([int(x) for x in line.split(',')])
    
    rule_list, rules_dict = parse_rules(filename)
    
    # Show the problematic updates
    invalid_examples = [
        ([75, 97, 47, 61, 53], "75 comes before 97, but rule 97|75 says 97 should come first"),
        ([61, 13, 29], "29 comes before 13, but rule 29|13 says 29 should come first"),
        ([97, 13, 75, 29, 47], "Multiple violations: 75 before 97 (rule 97|75), 29 before 13 (rule 29|13), etc.")
    ]
    
    for update, explanation in invalid_examples:
        print(f"Invalid update: {update}")
        print(f"  Problem: {explanation}")
        
        # Show applicable rules for this update
        applicable_rules = []
        update_set = set(update)
        
        for before_page, after_pages in rules_dict.items():
            if before_page in update_set:
                for after_page in after_pages:
                    if after_page in update_set:
                        applicable_rules.append((before_page, after_page))
        
        print(f"  Applicable rules: {applicable_rules}")
        print()

def create_ascii_graph():
    """Create a simplified ASCII visualization of key dependencies"""
    print("=== ASCII GRAPH OF KEY DEPENDENCIES ===")
    print("(Showing main dependency chains)")
    print()
    
    print("97 → 75 → 47 → 61 → 53")
    print("     ↓    ↓    ↓    ↓")
    print("     29   29   29   29")
    print("     ↓")
    print("     13")
    print()
    
    print("Interpretation:")
    print("- 97 must come before 75, 47, 61, 53, 29")
    print("- 75 must come before 47, 61, 53, 29, 13") 
    print("- 47 must come before 61, 53, 29, 13")
    print("- 61 must come before 53, 29, 13")
    print("- 53 must come before 29, 13")
    print("- 29 must come before 13")
    print()
    
    print("Valid topological orders include:")
    print("- 97, 75, 47, 61, 53, 29, 13")
    print("- 97, 75, 61, 47, 53, 29, 13")
    print("- And other combinations that respect all rules")

if __name__ == "__main__":
    visualize_graph('example.txt')
    show_example_fixes('example.txt') 
    create_ascii_graph()