# Advent of Code 2024 - Day 1 Part 2: Historian Hysteria
# Task: Calculate similarity score between two lists

def solve_part2():
    """
    This function calculates the similarity score between two lists.
    A similarity score is calculated by:
    1. Taking each number from the left list
    2. Counting how many times it appears in the right list
    3. Multiplying the number by its count
    4. Adding all these products together
    """
    
    # Step 1: Create empty lists to store our numbers
    # Think of lists like containers that can hold multiple items
    left_list = []   # This will hold numbers from the first column
    right_list = []  # This will hold numbers from the second column
    
    # Step 2: Read the input file and fill our lists
    # The 'with open()' statement safely opens and closes the file
    with open('input.txt', 'r') as file:
        # Loop through each line in the file
        for line in file:
            # Skip empty lines (lines with no content)
            if line.strip():  # .strip() removes whitespace and newlines
                # Split the line into two parts (left number and right number)
                # .split() breaks the line wherever there's a space
                left, right = line.strip().split()
                
                # Convert the text numbers into actual integer numbers
                # int() changes "123" (text) into 123 (number)
                left_list.append(int(left))    # Add to left list
                right_list.append(int(right))  # Add to right list
    
    # Step 3: Count how many times each number appears in the right list
    # We'll use a dictionary (like a phone book) to store counts
    # Key = the number, Value = how many times it appears
    right_count = {}
    
    # Go through each number in the right list
    for number in right_list:
        # If we've seen this number before, add 1 to its count
        if number in right_count:
            right_count[number] += 1
        # If this is the first time seeing this number, set count to 1
        else:
            right_count[number] = 1
    
    # Alternative way to do the counting above (more advanced):
    # from collections import Counter
    # right_count = Counter(right_list)
    
    # DEBUG: Show the right count dictionary
    print("=== Right Count Dictionary ===")
    print(f"Total unique numbers in right list: {len(right_count)}")
    
    # Convert dictionary to a list of (number, count) pairs
    # Example: {69184: 20, 53868: 19} becomes [(69184, 20), (53868, 19)]
    number_count_pairs = right_count.items()
    
    # Create a helper function to get the count from each pair
    def get_count_from_pair(pair):
        number, count = pair  # Unpack the pair
        return count          # Return just the count for sorting
    
    # Sort the pairs by count, highest first
    sorted_by_count = sorted(number_count_pairs, key=get_count_from_pair, reverse=True)
    
    print("Most frequent numbers in right list:")
    for number, count in sorted_by_count[:20]:  # Show top 20
        print(f"  {number}: {count} times")
    print("=" * 30)
    
    # Step 4: Calculate the similarity score
    similarity_score = 0  # Start with 0 and add to it
    
    # Look at each number in the left list
    for left_number in left_list:
        # Find how many times this number appears in the right list
        # .get() safely looks up a value, returns 0 if not found
        count_in_right = right_count.get(left_number, 0)
        
        # Calculate this number's contribution to the similarity score
        # (number from left) × (how many times it appears in right)
        contribution = left_number * count_in_right
        
        # Add this contribution to our total score
        similarity_score += contribution
        
        # No individual processing debug output to keep it clean
    
    # Step 5: Return the final similarity score
    return similarity_score

# This part runs when you execute the script directly
if __name__ == "__main__":
    # Call our function and store the result
    result = solve_part2()
    
    # Print the answer in a nice format
    print(f"\nFINAL ANSWER:")
    print(f"Similarity score: {result}")