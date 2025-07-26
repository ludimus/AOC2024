# Detailed analysis of the last update line: [97, 13, 75, 29, 47]

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

def show_violations_in_update(update, rules):
    """Show all rule violations in the current update"""
    print(f"Checking violations in: {update}")
    positions = {page: i for i, page in enumerate(update)}
    violations = []
    
    for before_page, after_pages in rules.items():
        if before_page in positions:
            for after_page in after_pages:
                if after_page in positions:
                    if positions[before_page] > positions[after_page]:
                        violations.append((before_page, after_page, positions[before_page], positions[after_page]))
    
    if violations:
        print("❌ Violations found:")
        for before, after, before_pos, after_pos in violations:
            print(f"   Rule {before}|{after}: {before} at pos {before_pos}, {after} at pos {after_pos}")
    else:
        print("✅ No violations - update is correctly ordered!")
    
    return violations

def detailed_bubble_sort_last_update():
    """Detailed bubble sort of the last update with enhanced visualization"""
    rules = parse_input('example.txt')
    update = [97, 13, 75, 29, 47]
    
    print("=" * 70)
    print("DETAILED BUBBLE SORT: [97, 13, 75, 29, 47]")
    print("=" * 70)
    
    # Show initial state and violations
    current = update.copy()
    print(f"INITIAL STATE:")
    print(f"Array: {current}")
    print(f"Index:  0   1   2   3   4")
    print()
    
    show_violations_in_update(current, rules)
    print()
    
    step = 0
    pass_number = 0
    
    # Keep track of all states
    states = [current.copy()]
    
    made_swap = True
    while made_swap:
        made_swap = False
        pass_number += 1
        
        print(f"🔄 PASS {pass_number}")
        print("-" * 30)
        
        # Check each adjacent pair
        for i in range(len(current) - 1):
            page_a = current[i]
            page_b = current[i + 1]
            
            print(f"  Checking position {i} and {i+1}: {page_a} vs {page_b}")
            
            # Check if we need to swap
            need_swap = False
            rule_violated = None
            
            if page_b in rules and page_a in rules[page_b]:
                need_swap = True
                rule_violated = f"{page_b}|{page_a}"
            
            if need_swap:
                # Perform the swap
                current[i], current[i + 1] = current[i + 1], current[i]
                step += 1
                made_swap = True
                states.append(current.copy())
                
                print(f"    ⚠️  Rule {rule_violated} violated!")
                print(f"    🔄 SWAP: {page_a} ↔ {page_b}")
                print(f"    📋 New array: {current}")
                print(f"    📍 Index:      0   1   2   3   4")
                
                # Show what moved
                old_pos_a = i + 1  # where page_a was
                old_pos_b = i      # where page_b was
                new_pos_a = i      # where page_a is now
                new_pos_b = i + 1  # where page_b is now
                
                print(f"    📈 {page_a}: position {old_pos_a} → {new_pos_a}")
                print(f"    📈 {page_b}: position {old_pos_b} → {new_pos_b}")
                print()
            else:
                print(f"    ✅ No swap needed - order is correct")
        
        print(f"End of pass {pass_number}: {current}")
        show_violations_in_update(current, rules)
        print()
    
    print("=" * 50)
    print("📊 SUMMARY OF ALL STATES")
    print("=" * 50)
    
    for i, state in enumerate(states):
        if i == 0:
            print(f"Initial:  {state}")
        else:
            print(f"Step {i:2d}:  {state}")
    
    print()
    print(f"🎯 FINAL RESULT:")
    print(f"   Original: {update}")
    print(f"   Sorted:   {current}")
    print(f"   Total steps: {step}")
    print(f"   Total passes: {pass_number}")
    
    # Verify the result
    print()
    print("🔍 VERIFICATION:")
    violations = show_violations_in_update(current, rules)
    if not violations:
        print("🎉 SUCCESS! All ordering rules are now satisfied.")
    
    return current

def show_element_journey():
    """Show how each element moves during the sorting"""
    print("\n" + "=" * 50)
    print("🗺️  ELEMENT JOURNEY TRACKER")
    print("=" * 50)
    
    # Track positions through the process
    journey = {
        97: [0, 0, 0, 0, 0],  # stays at position 0
        13: [1, 2, 3, 4, 4],  # moves 1→2→3→4
        75: [2, 1, 1, 1, 1],  # moves 2→1
        29: [3, 3, 2, 3, 3],  # temp move then back
        47: [4, 4, 4, 2, 2]   # moves 4→2
    }
    
    states = [
        "[97, 13, 75, 29, 47]",
        "[97, 75, 13, 29, 47]", 
        "[97, 75, 29, 13, 47]",
        "[97, 75, 29, 47, 13]",
        "[97, 75, 47, 29, 13]"
    ]
    
    print("State progression:")
    for i, state in enumerate(states):
        print(f"Step {i}: {state}")
    
    print("\nElement movements:")
    for page, positions in journey.items():
        moves = " → ".join(str(p) for p in positions)
        if positions[0] != positions[-1]:
            print(f"Page {page}: {moves} ({'moves' if len(set(positions)) > 1 else 'stays'})")
        else:
            print(f"Page {page}: {moves} (stays in place)")

if __name__ == "__main__":
    detailed_bubble_sort_last_update()
    show_element_journey()