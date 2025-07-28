# Day 2 Strategy Plan

## Problem Summary

**Part 1**: Analyze reactor safety reports to determine which are "safe" based on two criteria:
1. Levels must be either all increasing or all decreasing
2. Adjacent levels must differ by at least 1 and at most 3

## Data Structures

- **Input**: List of reports, each report is a list of integers (levels)
- **Processing**: For each report, check if it meets safety criteria
- **Output**: Count of safe reports

## Algorithm Approach

### Safety Check Function
1. Check if levels are consistently increasing or decreasing
2. Check if all adjacent differences are between 1 and 3 (inclusive)
3. Return True if both conditions met, False otherwise

### Main Algorithm
1. Parse each line into a list of integers
2. Apply safety check to each report
3. Count and return number of safe reports

## Functions Needed

- `parse_input(filename)`: Read file and return list of reports (each report is list of integers)
- `is_safe_report(levels)`: Check if a single report meets safety criteria
- `count_safe_reports(reports)`: Count safe reports in the input
- `main()`: Handle command line args (test mode, debug mode)

## Example Data
```
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
```

Expected safe reports: 2
- `7 6 4 2 1`: Safe (decreasing by 1-2)
- `1 3 6 7 9`: Safe (increasing by 1-3)

## Safety Rules
- All increasing OR all decreasing (not mixed)
- Adjacent differences: 1 ≤ |diff| ≤ 3

## Part 2: Problem Dampener

**New Rule**: A report is safe if either:
1. It's already safe (meets original criteria), OR
2. It becomes safe after removing exactly one level

### Algorithm for Part 2
1. Check if report is already safe (use Part 1 logic)
2. If not safe, try removing each level one at a time:
   - Create new list without that level
   - Check if the new list is safe
   - If any removal makes it safe, report is safe
3. If no single removal works, report remains unsafe

### Expected Results for Example
- `7 6 4 2 1`: Safe (already safe) ✓
- `1 2 7 8 9`: Unsafe (no single removal helps) ✗
- `9 7 6 2 1`: Unsafe (no single removal helps) ✗  
- `1 3 2 4 5`: Safe (remove 3: `1 2 4 5`) ✓
- `8 6 4 4 1`: Safe (remove one 4: `8 6 4 1`) ✓
- `1 3 6 7 9`: Safe (already safe) ✓

Total safe with dampener: 4