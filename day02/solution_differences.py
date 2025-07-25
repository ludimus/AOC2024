def get_differences(levels):
    """Get list of differences between adjacent levels."""
    return [levels[i+1] - levels[i] for i in range(len(levels) - 1)]

def is_safe_report_diff(levels):
    """Check if a report is safe using difference list approach."""
    if len(levels) < 2:
        return True
    
    diffs = get_differences(levels)
    
    # Check if all differences have same sign (all positive or all negative)
    if not (all(d > 0 for d in diffs) or all(d < 0 for d in diffs)):
        return False
    
    # Check if all differences are within bounds (1 to 3)
    return all(1 <= abs(d) <= 3 for d in diffs)

def is_safe_with_dampener_diff(levels):
    """Check if report is safe with Problem Dampener using difference approach."""
    # First check if already safe
    if is_safe_report_diff(levels):
        return True
    
    # Try removing each level one at a time
    for i in range(len(levels)):
        modified_levels = levels[:i] + levels[i+1:]
        if is_safe_report_diff(modified_levels):
            return True
    
    return False

def solve_part1():
    """Solve Part 1 using difference approach."""
    safe_count = 0
    with open('input.txt', 'r') as file:
        for line in file:
            if line.strip():
                levels = list(map(int, line.strip().split()))
                if is_safe_report_diff(levels):
                    safe_count += 1
    return safe_count

def solve_part2():
    """Solve Part 2 using difference approach."""
    safe_count = 0
    with open('input.txt', 'r') as file:
        for line in file:
            if line.strip():
                levels = list(map(int, line.strip().split()))
                if is_safe_with_dampener_diff(levels):
                    safe_count += 1
    return safe_count