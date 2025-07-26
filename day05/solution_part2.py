# Advent of Code 2024 - Day 5: Print Queue - Part 2
# Fix incorrectly ordered updates and sum their middle page numbers

from functools import cmp_to_key

def parse_input(filename):
    """Parse ordering rules and updates from input file"""
    with open(filename, 'r') as f:
        content = f.read().strip()
    
    # Split into rules and updates sections
    sections = content.split('\n\n')
    rules_section = sections[0]
    updates_section = sections[1]
    
    # Parse rules into dictionary: {page: set_of_pages_that_must_come_after}
    rules = {}
    for rule_line in rules_section.split('\n'):
        before, after = map(int, rule_line.split('|'))
        if before not in rules:
            rules[before] = set()
        rules[before].add(after)
    
    # Parse updates into list of lists
    updates = []
    for update_line in updates_section.split('\n'):
        update = [int(x) for x in update_line.split(',')]
        updates.append(update)
    
    return rules, updates

def is_valid_update(update, rules):
    """Check if update sequence follows all applicable ordering rules"""
    # Create position mapping for this update
    positions = {page: i for i, page in enumerate(update)}
    
    # Check each rule that applies to pages in this update
    for before_page, after_pages in rules.items():
        if before_page in positions:
            for after_page in after_pages:
                if after_page in positions:
                    # Rule applies: before_page must come before after_page
                    if positions[before_page] > positions[after_page]:
                        return False
    
    return True

def fix_update_ordering(update, rules):
    """Sort pages in update according to ordering rules using custom comparator"""
    
    def compare_pages(page_a, page_b):
        """Compare two pages based on ordering rules
        Returns: -1 if page_a should come before page_b
                  1 if page_b should come before page_a  
                  0 if no rule applies
        """
        # Check if there's a rule page_a|page_b (page_a must come before page_b)
        if page_a in rules and page_b in rules[page_a]:
            return -1  # page_a comes before page_b
        
        # Check if there's a rule page_b|page_a (page_b must come before page_a)  
        if page_b in rules and page_a in rules[page_b]:
            return 1   # page_b comes before page_a
        
        # No applicable rule - maintain relative order
        return 0
    
    # Sort using the custom comparator
    sorted_update = sorted(update, key=cmp_to_key(compare_pages))
    return sorted_update

def get_middle_page(update):
    """Get the middle page number from an update"""
    return update[len(update) // 2]

def solve_part2(filename='input.txt', test_mode=False):
    """Main solution function for Part 2"""
    rules, updates = parse_input(filename)
    
    if test_mode:
        print("=== PART 2: FIXING INVALID UPDATES ===")
        print(f"Total updates: {len(updates)}")
        print()
    
    total = 0
    invalid_updates = []
    fixed_updates = []
    
    for i, update in enumerate(updates):
        if not is_valid_update(update, rules):
            # This update is invalid - fix it
            invalid_updates.append(update)
            fixed_update = fix_update_ordering(update, rules)
            fixed_updates.append(fixed_update)
            
            middle_page = get_middle_page(fixed_update)
            total += middle_page
            
            if test_mode:
                print(f"Update {i+1}: {update}")
                print(f"  Fixed:  {fixed_update}")
                print(f"  Middle: {middle_page}")
                print()
    
    print(f"Invalid updates found: {len(invalid_updates)}")
    print(f"All updates fixed successfully: {len(fixed_updates)}")
    print(f"Sum of middle page numbers from fixed updates: {total}")
    return total

def verify_solution(filename='example.txt'):
    """Verify solution with example input and expected results"""
    print("=== VERIFICATION WITH EXAMPLE ===")
    
    # Expected results from problem description
    expected_fixes = [
        ([75, 97, 47, 61, 53], [97, 75, 47, 61, 53], 47),
        ([61, 13, 29], [61, 29, 13], 29),
        ([97, 13, 75, 29, 47], [97, 75, 47, 29, 13], 47)
    ]
    expected_sum = 123
    
    rules, updates = parse_input(filename)
    
    print("Expected fixes:")
    for original, expected_fixed, expected_middle in expected_fixes:
        print(f"  {original} → {expected_fixed} (middle: {expected_middle})")
    print(f"Expected sum: {expected_sum}")
    print()
    
    # Test our fixes
    print("Our fixes:")
    total = 0
    for update in updates:
        if not is_valid_update(update, rules):
            fixed = fix_update_ordering(update, rules)
            middle = get_middle_page(fixed)
            total += middle
            print(f"  {update} → {fixed} (middle: {middle})")
    
    print(f"Our sum: {total}")
    print(f"Match expected: {total == expected_sum}")
    
    return total == expected_sum

if __name__ == "__main__":
    # First verify with example
    print("Verifying with example input:")
    verification_passed = verify_solution('example.txt')
    
    if verification_passed:
        print("\n" + "="*50 + "\n")
        print("Verification passed! Running on actual input:")
        actual_result = solve_part2('input.txt', test_mode=False)
    else:
        print("\nVerification failed! Check the implementation.")
        print("Running anyway for debugging:")
        solve_part2('example.txt', test_mode=True)