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

def should_swap(page_a, page_b, rules):
    """Check if page_a and page_b need to be swapped based on rules.
    Returns True if page_a should come after page_b."""
    # If there's a rule saying page_b must come before page_a, then swap
    return (page_b, page_a) in rules

def bubble_sort_with_rules(pages, rules):
    """Sort pages using bubble sort with custom ordering rules."""
    n = len(pages)
    sorted_pages = pages.copy()
    
    # Bubble sort: repeatedly go through the list and swap adjacent elements if out of order
    for i in range(n):
        for j in range(0, n - i - 1):
            if should_swap(sorted_pages[j], sorted_pages[j + 1], rules):
                # Swap the elements
                sorted_pages[j], sorted_pages[j + 1] = sorted_pages[j + 1], sorted_pages[j]
    
    return sorted_pages

def get_middle_page(update):
    """Get the middle page number from an update."""
    return update[len(update) // 2]

def solve_part2(rules, updates):
    """Fix incorrectly ordered updates and sum their middle page numbers."""
    middle_page_sum = 0
    incorrect_updates = []
    corrected_updates = []
    
    for update in updates:
        if not is_correctly_ordered(update, rules):
            # This update is incorrectly ordered, so fix it
            corrected_update = bubble_sort_with_rules(update, rules)
            middle_page = get_middle_page(corrected_update)
            middle_page_sum += middle_page
            
            incorrect_updates.append(update)
            corrected_updates.append(corrected_update)
    
    return middle_page_sum, incorrect_updates, corrected_updates

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
    
    result, incorrect, corrected = solve_part2(rules, updates)
    
    if debug_mode:
        print("Incorrectly ordered updates and their corrections:")
        for i, (original, fixed) in enumerate(zip(incorrect, corrected)):
            middle = get_middle_page(fixed)
            print(f"  {original} -> {fixed} (middle: {middle})")
        print(f"\nSum of middle pages from corrected updates: {result}")
    elif test_mode:
        print(f"Sum of middle pages from corrected updates: {result}")
    else:
        print(result)

if __name__ == "__main__":
    main()