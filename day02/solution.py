def is_safe_report(levels):
    """Check if a report is safe according to the rules."""
    if len(levels) < 2:
        return True
    
    # Determine if sequence should be increasing or decreasing
    first_diff = levels[1] - levels[0]
    if first_diff == 0:
        return False  # No change is not allowed
    
    is_increasing = first_diff > 0
    
    # Check all adjacent pairs
    for i in range(len(levels) - 1):
        diff = levels[i + 1] - levels[i]
        
        # Check if difference is within bounds (1 to 3)
        if abs(diff) < 1 or abs(diff) > 3:
            return False
        
        # Check if direction is consistent
        if is_increasing and diff <= 0:
            return False
        if not is_increasing and diff >= 0:
            return False
    
    return True

def solve():
    """Solve the Red-Nosed Reports problem."""
    safe_count = 0
    
    with open('input.txt', 'r') as file:
        for line in file:
            if line.strip():
                levels = list(map(int, line.strip().split()))
                if is_safe_report(levels):
                    safe_count += 1
    
    return safe_count

if __name__ == "__main__":
    result = solve()
    print(f"Number of safe reports: {result}")