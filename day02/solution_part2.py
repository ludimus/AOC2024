#!/usr/bin/env python3

import sys
import argparse

def parse_input(filename):
    reports = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                levels = list(map(int, line.split()))
                reports.append(levels)
    
    return reports

def is_safe_report(levels):
    if len(levels) < 2:
        return True
    
    # Check if all increasing or all decreasing
    differences = []
    for i in range(1, len(levels)):
        diff = levels[i] - levels[i-1]
        differences.append(diff)
    
    # All differences must be positive (increasing) or all negative (decreasing)
    all_increasing = all(diff > 0 for diff in differences)
    all_decreasing = all(diff < 0 for diff in differences)
    
    if not (all_increasing or all_decreasing):
        return False
    
    # Check if all differences are between 1 and 3 (absolute value)
    for diff in differences:
        abs_diff = abs(diff)
        if abs_diff < 1 or abs_diff > 3:
            return False
    
    return True

def is_safe_with_dampener(levels):
    # First check if already safe
    if is_safe_report(levels):
        return True
    
    # Try removing each level one at a time
    for i in range(len(levels)):
        # Create new list without the level at index i
        dampened_levels = levels[:i] + levels[i+1:]
        if is_safe_report(dampened_levels):
            return True
    
    return False

def count_safe_reports_with_dampener(reports):
    safe_count = 0
    for report in reports:
        if is_safe_with_dampener(report):
            safe_count += 1
    return safe_count

def main():
    parser = argparse.ArgumentParser(description='Day 2 Part 2: Count safe reactor reports with Problem Dampener')
    parser.add_argument('--test', action='store_true', help='Run with example.txt instead of input.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    
    if args.debug or args.test:
        print(f"Reading from {filename}")
    
    reports = parse_input(filename)
    
    if args.debug or args.test:
        print(f"Total reports: {len(reports)}")
        print("\nAnalyzing each report with Problem Dampener:")
        for i, report in enumerate(reports):
            safe_original = is_safe_report(report)
            safe_dampened = is_safe_with_dampener(report)
            
            status = "Safe"
            if safe_original:
                reason = "(already safe)"
            elif safe_dampened:
                # Find which removal works
                reason = "(safe after dampening)"
                if args.debug:
                    for j in range(len(report)):
                        test_levels = report[:j] + report[j+1:]
                        if is_safe_report(test_levels):
                            reason = f"(safe by removing index {j}: {report[j]})"
                            break
            else:
                status = "Unsafe"
                reason = "(unsafe even with dampener)"
            
            print(f"Report {i+1}: {report} -> {status} {reason}")
    
    result = count_safe_reports_with_dampener(reports)
    
    if args.debug or args.test:
        print(f"\nSafe reports with dampener: {result}")
    else:
        print(result)

if __name__ == "__main__":
    main()