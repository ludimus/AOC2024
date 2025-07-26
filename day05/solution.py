# Advent of Code 2024 - Day 5: Print Queue
# Find correctly ordered updates and sum their middle page numbers

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

def is_valid_update(update, rules, log_failures=False):
    """Check if update sequence follows all applicable ordering rules"""
    # Create position mapping for this update
    positions = {page: i for i, page in enumerate(update)}
    failed_constraints = []
    
    # Check each rule that applies to pages in this update
    for before_page, after_pages in rules.items():
        if before_page in positions:
            for after_page in after_pages:
                if after_page in positions:
                    # Rule applies: before_page must come before after_page
                    if positions[before_page] > positions[after_page]:
                        constraint = f"{before_page}|{after_page} (positions: {before_page} at {positions[before_page]}, {after_page} at {positions[after_page]})"
                        failed_constraints.append(constraint)
    
    if failed_constraints and log_failures:
        print(f"Update {update} failed constraints: {failed_constraints}")
    
    return len(failed_constraints) == 0

def get_middle_page(update):
    """Get the middle page number from an update"""
    return update[len(update) // 2]

def solve(filename='input.txt', test_mode=False):
    """Main solution function"""
    rules, updates = parse_input(filename)
    
    if test_mode:
        print("=== TESTING WITH EXAMPLE INPUT ===")
        print(f"Rules: {dict(list(rules.items())[:5])}...")  # Show first 5 rules
        print(f"Updates: {updates}")
        print()
    
    total = 0
    valid_updates = []
    invalid_updates = []
    
    for i, update in enumerate(updates):
        if is_valid_update(update, rules, log_failures=test_mode):
            valid_updates.append(update)
            middle_page = get_middle_page(update)
            total += middle_page
            if test_mode:
                print(f"✓ Update {i+1}: {update} - VALID (middle: {middle_page})")
        else:
            invalid_updates.append(update)
            if test_mode:
                print(f"✗ Update {i+1}: {update} - INVALID")
    
    if test_mode:
        print()
    print(f"Valid updates: {len(valid_updates)}")
    print(f"Invalid updates: {len(invalid_updates)}")
    print(f"Sum of middle page numbers: {total}")
    return total

if __name__ == "__main__":
    # Test with example first
    print("Testing with example.txt:")
    example_result = solve('example.txt', test_mode=True)
    print(f"Expected: 143, Got: {example_result}")
    print("\n" + "="*50 + "\n")
    
    # Run with actual input
    print("Running with actual input.txt:")
    actual_result = solve('input.txt', test_mode=False)