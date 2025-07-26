# Advent of Code 2024 - Day 6: Guard Gallivant - Part 2
# Find positions where adding a single obstacle creates a loop

def parse_input(filename):
    """Parse the grid and find guard's starting position and direction"""
    with open(filename, 'r') as f:
        grid = [line.rstrip() for line in f]
    
    # Find guard's starting position and direction
    guard_pos = None
    guard_dir = None
    
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] in '^v<>':
                guard_pos = (row, col)
                guard_dir = grid[row][col]
                break
        if guard_pos:
            break
    
    return grid, guard_pos, guard_dir

def get_direction_vector(direction):
    """Convert direction character to row,col movement vector"""
    directions = {
        '^': (-1, 0),  # up
        'v': (1, 0),   # down
        '<': (0, -1),  # left
        '>': (0, 1)    # right
    }
    return directions[direction]

def turn_right(direction):
    """Turn the guard 90 degrees to the right"""
    turns = {
        '^': '>',
        '>': 'v', 
        'v': '<',
        '<': '^'
    }
    return turns[direction]

def is_valid_position(row, col, grid):
    """Check if position is within grid bounds"""
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def get_original_path(grid, start_pos, start_dir):
    """Get the guard's original patrol path (from Part 1)"""
    visited = set()
    current_pos = start_pos
    current_dir = start_dir
    
    while True:
        # Mark current position as visited
        visited.add(current_pos)
        
        # Calculate next position
        dr, dc = get_direction_vector(current_dir)
        next_row = current_pos[0] + dr
        next_col = current_pos[1] + dc
        
        # Check if next position is outside the grid
        if not is_valid_position(next_row, next_col, grid):
            break
        
        # Check if there's an obstacle at next position
        if grid[next_row][next_col] == '#':
            # Turn right instead of moving
            current_dir = turn_right(current_dir)
        else:
            # Move forward
            current_pos = (next_row, next_col)
    
    return visited

def detect_loop_with_obstacle(grid, start_pos, start_dir, obstacle_pos):
    """
    Simulate guard patrol with an additional obstacle and detect if it creates a loop.
    Returns True if loop detected, False if guard exits normally.
    """
    visited_states = set()  # Store (row, col, direction) tuples
    current_pos = start_pos
    current_dir = start_dir
    
    while True:
        # Create state tuple: (row, col, direction)
        state = (current_pos[0], current_pos[1], current_dir)
        
        # If we've seen this state before, we're in a loop
        if state in visited_states:
            return True
        
        visited_states.add(state)
        
        # Calculate next position
        dr, dc = get_direction_vector(current_dir)
        next_row = current_pos[0] + dr
        next_col = current_pos[1] + dc
        
        # Check if next position is outside the grid (guard exits)
        if not is_valid_position(next_row, next_col, grid):
            return False
        
        # Check if there's an obstacle at next position (including our new obstacle)
        next_pos = (next_row, next_col)
        if grid[next_row][next_col] == '#' or next_pos == obstacle_pos:
            # Turn right instead of moving
            current_dir = turn_right(current_dir)
        else:
            # Move forward
            current_pos = next_pos

def solve_part2(filename='input.txt', debug=False):
    """Main solution function for Part 2"""
    grid, guard_pos, guard_dir = parse_input(filename)
    
    print(f"Grid size: {len(grid)}x{len(grid[0])}")
    print(f"Guard starts at {guard_pos} facing {guard_dir}")
    
    # Get the original patrol path to optimize our search
    original_path = get_original_path(grid, guard_pos, guard_dir)
    print(f"Original path contains {len(original_path)} positions")
    
    # Test each position on the original path (except starting position)
    loop_positions = []
    test_positions = original_path - {guard_pos}  # Remove starting position
    
    print(f"Testing {len(test_positions)} potential obstacle positions...")
    
    for i, test_pos in enumerate(test_positions):
        if debug and i < 10:
            print(f"Testing obstacle at {test_pos}...")
        
        # Only test empty positions (not existing obstacles)
        row, col = test_pos
        if grid[row][col] == '.':
            # Test if placing obstacle here creates a loop
            if detect_loop_with_obstacle(grid, guard_pos, guard_dir, test_pos):
                loop_positions.append(test_pos)
                if debug and i < 10:
                    print(f"  → LOOP DETECTED!")
        
        # Progress indicator
        if (i + 1) % 500 == 0:
            print(f"  Processed {i + 1}/{len(test_positions)} positions...")
    
    print(f"Found {len(loop_positions)} positions that create loops")
    return len(loop_positions)

def verify_with_example():
    """Verify with the example - should find 6 loop positions"""
    print("=== VERIFICATION WITH EXAMPLE ===")
    print("Expected: 6 positions that create loops")
    
    result = solve_part2('example.txt', debug=True)
    print(f"Our result: {result}")
    print(f"Match expected: {result == 6}")
    
    return result == 6

if __name__ == "__main__":
    print("Verifying with example:")
    verification_passed = verify_with_example()
    
    if verification_passed:
        print("\n" + "="*50 + "\n")
        print("Verification passed! Running on actual input:")
        actual_result = solve_part2('input.txt', debug=False)
        print(f"Final answer: {actual_result}")
    else:
        print("\nVerification failed! Check the implementation.")
        print("Running anyway for debugging:")
        solve_part2('example.txt', debug=True)