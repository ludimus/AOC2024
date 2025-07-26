# Advent of Code 2024 - Day 6: Guard Gallivant
# Simulate guard patrol and count distinct positions visited

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

def print_local_view(grid, guard_pos, guard_dir, size=5):
    """Print a local 5x5 view around the guard's position"""
    row, col = guard_pos
    half = size // 2
    
    print(f"\n5x5 view around guard at {guard_pos} facing {guard_dir}:")
    for r in range(row - half, row + half + 1):
        line = ""
        for c in range(col - half, col + half + 1):
            if r == row and c == col:
                line += guard_dir  # Show guard
            elif 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                line += grid[r][c]
            else:
                line += " "  # Out of bounds
        print(line)

def simulate_guard_patrol(grid, start_pos, start_dir, debug=False):
    """Simulate the guard's patrol and return visited positions"""
    visited = set()
    current_pos = start_pos
    current_dir = start_dir
    step_count = 0
    
    while True:
        # Mark current position as visited
        visited.add(current_pos)
        
        if debug and step_count < 20:  # Only show first 20 steps to avoid spam
            print(f"\nStep {step_count + 1}:")
            print(f"Current position: {current_pos}, facing: {current_dir}")
            print_local_view(grid, current_pos, current_dir)
        
        # Calculate next position
        dr, dc = get_direction_vector(current_dir)
        next_row = current_pos[0] + dr
        next_col = current_pos[1] + dc
        
        # Check if next position is outside the grid
        if not is_valid_position(next_row, next_col, grid):
            if debug and step_count < 20:
                print(f"Decision: Move to {(next_row, next_col)} - OUTSIDE GRID, stopping")
            break
        
        # Check if there's an obstacle at next position
        if grid[next_row][next_col] == '#':
            # Turn right instead of moving
            if debug and step_count < 20:
                print(f"Decision: Obstacle at {(next_row, next_col)}, turning right")
            current_dir = turn_right(current_dir)
        else:
            # Move forward
            if debug and step_count < 20:
                print(f"Decision: Move forward to {(next_row, next_col)}")
            current_pos = (next_row, next_col)
        
        step_count += 1
        if debug and step_count == 20:
            print("\n... (showing only first 20 steps)")
    
    return visited

def solve_part1(filename='input.txt', debug=False):
    """Main solution function"""
    grid, guard_pos, guard_dir = parse_input(filename)
    
    print(f"Grid size: {len(grid)}x{len(grid[0])}")
    print(f"Guard starts at {guard_pos} facing {guard_dir}")
    
    visited_positions = simulate_guard_patrol(grid, guard_pos, guard_dir, debug)
    
    print(f"Distinct positions visited: {len(visited_positions)}")
    return len(visited_positions)

if __name__ == "__main__":
    print("Testing with example (with debug output):")
    example_result = solve_part1('example.txt', debug=True)
    print(f"Example result: {example_result}")
    print("\n" + "="*50 + "\n")
    
    print("Running on actual input:")
    actual_result = solve_part1('input.txt', debug=False)
    print(f"Actual result: {actual_result}")