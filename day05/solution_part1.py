#!/usr/bin/env python3

import sys

def parse_input(filename):
    """Parse the input file and return rules and updates separately."""
    with open(filename, 'r') as f:
        content = f.read().strip()
    
    # Split by double newline to separate rules from updates
    sections = content.split('\n\n')
    
    # Parse rules: "47|53" means 47 must come before 53
    rules = set()
    for line in sections[0].split('\n'):
        if '|' in line:
            before, after = line.split('|')
            rules.add((int(before), int(after)))
    
    # Parse updates: "75,47,61,53,29" becomes [75, 47, 61, 53, 29]
    updates = []
    for line in sections[1].split('\n'):
        if ',' in line:
            pages = [int(x) for x in line.split(',')]
            updates.append(pages)
    
    return rules, updates

def is_correctly_ordered(update, rules):
    """Check if an update follows all applicable ordering rules."""
    # Check each pair of pages in the update
    for i in range(len(update)):
        for j in range(i + 1, len(update)):
            page_before = update[i]  # comes first in the update
            page_after = update[j]   # comes later in the update
            
            # Check if there's a rule saying page_after should come before page_before
            # If so, this update violates the rules
            if (page_after, page_before) in rules:
                return False
    
    return True

def get_middle_page(update):
    """Get the middle page number from an update."""
    return update[len(update) // 2]

def solve_part1(rules, updates):
    """Find correctly ordered updates and sum their middle page numbers."""
    middle_page_sum = 0
    
    for update in updates:
        if is_correctly_ordered(update, rules):
            middle_page = get_middle_page(update)
            middle_page_sum += middle_page
    
    return middle_page_sum

def main():
    # Check command line arguments
    test_mode = '--test' in sys.argv
    debug_mode = '--debug' in sys.argv
    
    filename = 'example.txt' if test_mode else 'input.txt'
    
    if debug_mode:
        print(f"Reading from: {filename}")
    
    rules, updates = parse_input(filename)
    
    if debug_mode:
        print(f"Parsed {len(rules)} rules and {len(updates)} updates")
        print("Sample rules:", list(rules)[:5])
        print("Sample updates:", updates[:3])
        print()
    
    result = solve_part1(rules, updates)
    
    if debug_mode:
        print("Checking each update:")
        for update in updates:
            is_correct = is_correctly_ordered(update, rules)
            status = "✓ CORRECT" if is_correct else "✗ INCORRECT"
            if is_correct:
                middle = get_middle_page(update)
                print(f"  {update} -> {status} (middle: {middle})")
            else:
                print(f"  {update} -> {status}")
        print(f"\nSum of middle pages: {result}")
    elif test_mode:
        print(f"Sum of middle pages from correctly ordered updates: {result}")
    else:
        print(result)

if __name__ == "__main__":
    main()