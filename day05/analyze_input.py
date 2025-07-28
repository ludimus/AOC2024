#!/usr/bin/env python3

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

def analyze_coverage(rules, updates):
    """Analyze if all pages in updates are covered by rules."""
    # Get all pages that appear in rules
    pages_in_rules = set()
    for before, after in rules:
        pages_in_rules.add(before)
        pages_in_rules.add(after)
    
    # Get all pages that appear in updates
    pages_in_updates = set()
    for update in updates:
        pages_in_updates.update(update)
    
    # Find pages that appear in updates but not in rules
    uncovered_pages = pages_in_updates - pages_in_rules
    
    # Find pages that appear in rules but not in updates
    unused_rules_pages = pages_in_rules - pages_in_updates
    
    print(f"=== Input Analysis ===")
    print(f"Total rules: {len(rules)}")
    print(f"Total updates: {len(updates)}")
    print(f"Pages mentioned in rules: {len(pages_in_rules)}")
    print(f"Pages mentioned in updates: {len(pages_in_updates)}")
    print()
    
    print(f"Pages in updates: {sorted(pages_in_updates)}")
    print()
    
    if uncovered_pages:
        print(f"❌ PROBLEM: {len(uncovered_pages)} pages in updates have NO rules:")
        print(f"   {sorted(uncovered_pages)}")
    else:
        print(f"✅ SUCCESS: All pages in updates are covered by rules!")
    
    print()
    
    if unused_rules_pages:
        print(f"ℹ️  INFO: {len(unused_rules_pages)} pages mentioned in rules but not in updates:")
        print(f"   {sorted(unused_rules_pages)}")
    else:
        print(f"ℹ️  INFO: All rule pages are used in updates")
    
    return uncovered_pages, unused_rules_pages

def analyze_rule_density(rules, updates):
    """Analyze how many rules exist for each page in updates."""
    # Get all pages in updates
    pages_in_updates = set()
    for update in updates:
        pages_in_updates.update(update)
    
    # Count rules for each page
    rule_count = {}
    for page in pages_in_updates:
        count = 0
        for before, after in rules:
            if page == before or page == after:
                count += 1
        rule_count[page] = count
    
    print(f"\n=== Rule Density Analysis ===")
    print(f"Rules per page (sorted by rule count):")
    
    for page, count in sorted(rule_count.items(), key=lambda x: x[1]):
        print(f"  Page {page:2d}: {count:2d} rules")
    
    min_rules = min(rule_count.values())
    max_rules = max(rule_count.values())
    avg_rules = sum(rule_count.values()) / len(rule_count)
    
    print(f"\nRule statistics:")
    print(f"  Minimum rules per page: {min_rules}")
    print(f"  Maximum rules per page: {max_rules}")
    print(f"  Average rules per page: {avg_rules:.1f}")
    
    # Find pages with minimal rules
    minimal_pages = [page for page, count in rule_count.items() if count == min_rules]
    print(f"  Pages with minimal rules ({min_rules}): {sorted(minimal_pages)}")

def main():
    rules, updates = parse_input('input.txt')
    
    uncovered, unused = analyze_coverage(rules, updates)
    analyze_rule_density(rules, updates)
    
    print(f"\n=== Conclusion ===")
    if not uncovered:
        print("✅ All pages in updates are covered by at least one rule")
        print("✅ Bubble sort should work correctly for all updates")
    else:
        print("❌ Some pages lack rules - bubble sort may not work properly")

if __name__ == "__main__":
    main()