# Advent of Code 2024 - Day 1: Historian Hysteria
# Task: Calculate total distance between two lists of location IDs

def solve_day1():
    # Step 1: Read and parse the input file
    left_list = []
    right_list = []
    
    with open('input.txt', 'r') as file:
        for line in file:
            # Each line contains two numbers separated by whitespace
            if line.strip():  # Skip empty lines
                left, right = line.strip().split()
                left_list.append(int(left))
                right_list.append(int(right))
    
    # Step 2: Sort both lists independently
    # We need to pair smallest with smallest, etc.
    left_list.sort()
    right_list.sort()
    
    # Step 3: Calculate absolute differences for each pair
    total_distance = 0
    for i in range(len(left_list)):
        # Find absolute difference between paired elements
        distance = abs(left_list[i] - right_list[i])
        total_distance += distance
    
    # Step 4: Return the total distance
    return total_distance

if __name__ == "__main__":
    # Calculate and print the result
    result = solve_day1()
    print(f"Total distance between lists: {result}")