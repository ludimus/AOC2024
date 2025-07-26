# Bubble sort style solution showing individual swaps for visual explanation

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

def should_swap(page_a, page_b, rules):
    """Check if two adjacent pages should be swapped"""
    # If there's a rule page_b|page_a (page_b should come before page_a)
    # then we need to swap them
    if page_b in rules and page_a in rules[page_b]:
        return True
    return False

def fix_update_with_swaps(update, rules, show_steps=True):
    """Fix update ordering using bubble sort with visible swaps"""
    
    if show_steps:
        print(f"=== FIXING {update} WITH INDIVIDUAL SWAPS ===")
        print(f"Target: Satisfy all ordering rules")
        print()
    
    # Make a copy to avoid modifying original
    current = update.copy()
    step = 0
    total_swaps = 0
    
    if show_steps:
        print(f"Initial: {current}")
        print()
    
    # Keep making passes until no more swaps are needed
    made_swap = True
    pass_number = 0
    
    while made_swap:
        made_swap = False
        pass_number += 1
        
        if show_steps:
            print(f"--- Pass {pass_number} ---")
        
        # Go through adjacent pairs
        for i in range(len(current) - 1):
            page_a = current[i]
            page_b = current[i + 1]
            
            if should_swap(page_a, page_b, rules):
                # Swap them
                current[i], current[i + 1] = current[i + 1], current[i]
                step += 1
                total_swaps += 1
                made_swap = True
                
                if show_steps:
                    # Find which rule caused the swap
                    rule = f"{page_b}|{page_a}"
                    print(f"  Step {step}: Swap {page_a} ↔ {page_b} (rule {rule})")
                    print(f"    Before: {update if step == 1 else 'previous state'}")
                    print(f"    After:  {current}")
                    print()
        
        if not made_swap and show_steps:
            print(f"  No swaps needed in pass {pass_number}")
    
    if show_steps:
        print(f"=== FINAL RESULT ===")
        print(f"Original: {update}")
        print(f"Fixed:    {current}")
        print(f"Total swaps: {total_swaps}")
        print(f"Total passes: {pass_number}")
    
    return current

def demonstrate_example_swaps():
    """Show all three example fixes with detailed swap visualization"""
    rules = parse_input('example.txt')
    
    examples = [
        [75, 97, 47, 61, 53],
        [61, 13, 29],
        [97, 13, 75, 29, 47]
    ]
    
    for i, update in enumerate(examples, 1):
        print(f"{'='*60}")
        print(f"EXAMPLE {i}")
        fix_update_with_swaps(update, rules, show_steps=True)
        print()

def compare_methods():
    """Compare bubble sort method vs Python's built-in sort"""
    from functools import cmp_to_key
    
    rules = parse_input('example.txt')
    test_update = [97, 13, 75, 29, 47]
    
    print("=== COMPARING METHODS ===")
    print(f"Test update: {test_update}")
    print()
    
    # Method 1: Bubble sort with swaps
    print("Method 1: Bubble sort with individual swaps")
    bubble_result = fix_update_with_swaps(test_update, rules, show_steps=False)
    
    # Method 2: Python's built-in sort
    def compare_pages(page_a, page_b):
        if page_a in rules and page_b in rules[page_a]:
            return -1
        if page_b in rules and page_a in rules[page_b]:
            return 1
        return 0
    
    builtin_result = sorted(test_update, key=cmp_to_key(compare_pages))
    
    print(f"Bubble sort result:  {bubble_result}")
    print(f"Built-in sort result: {builtin_result}")
    print(f"Results match: {bubble_result == builtin_result}")

def visualize_swap_pattern():
    """Show the pattern of swaps for the complex example"""
    rules = parse_input('example.txt')
    update = [97, 13, 75, 29, 47]
    
    print("=== VISUAL SWAP PATTERN ===")
    print("Showing how elements 'bubble' to their correct positions")
    print()
    
    current = update.copy()
    step = 0
    
    print(f"Start:  {current}")
    print("        ↓")
    
    # Manually trace the key swaps for visual effect
    swaps_to_show = [
        (0, 1, "No swap needed: 97 already before 13"),
        (1, 2, "Swap 13 ↔ 75: rule 75|13"),
        (2, 3, "Swap 13 ↔ 29: rule 29|13"), 
        (3, 4, "Swap 13 ↔ 47: rule 47|13"),
    ]
    
    # Actually perform the swaps to show progression
    made_swap = True
    pass_num = 0
    
    while made_swap:
        made_swap = False
        pass_num += 1
        print(f"\nPass {pass_num}:")
        
        for i in range(len(current) - 1):
            if should_swap(current[i], current[i + 1], rules):
                page_a, page_b = current[i], current[i + 1]
                current[i], current[i + 1] = current[i + 1], current[i]
                step += 1
                made_swap = True
                
                print(f"  Swap {page_a} ↔ {page_b}: {current}")
                
                # Show which element is moving
                pos = current.index(page_a)
                arrow = " " * (pos * 4) + "↑"
                print(f"      {arrow}")
    
    print(f"\nFinal: {current}")
    print("All rules satisfied! ✓")

if __name__ == "__main__":
    demonstrate_example_swaps()
    print("\n" + "="*60)
    compare_methods()
    print("\n" + "="*60)
    visualize_swap_pattern()