# Day 1 Strategy Plan

## Problem Summary

**Part 1**: Compare two lists of location IDs by pairing smallest with smallest numbers and calculating total distance.

**Part 2**: Calculate similarity score by multiplying each number in left list by its frequency in right list.

## Data Structures

- **Input**: Two lists of integers (left_list, right_list)
- **Part 1**: Use sorted lists for efficient pairing
- **Part 2**: Use Counter/dictionary for frequency counting

## Algorithm Approach

### Part 1: Total Distance
1. Parse input into two separate lists
2. Sort both lists
3. Pair corresponding elements and calculate absolute differences
4. Sum all differences

### Part 2: Similarity Score  
1. Parse input into two separate lists
2. Count frequency of each number in right list
3. For each number in left list, multiply by its count in right list
4. Sum all products

## Functions Needed

- `parse_input(filename)`: Read file and return (left_list, right_list)
- `calculate_total_distance(left_list, right_list)`: Part 1 solution
- `calculate_similarity_score(left_list, right_list)`: Part 2 solution
- `main()`: Handle command line args (test mode, debug mode)

## Example Data
```
3   4
4   3
2   5
1   3
3   9
3   3
```
Expected: Part 1 = 11, Part 2 = 31