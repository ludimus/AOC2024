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

def count_safe_reports(reports):
    safe_count = 0
    for report in reports:
        if is_safe_report(report):
            safe_count += 1
    return safe_count

def main():
    parser = argparse.ArgumentParser(description='Day 2 Part 1: Count safe reactor reports')
    parser.add_argument('--test', action='store_true', help='Run with example.txt instead of input.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    
    if args.debug or args.test:
        print(f"Reading from {filename}")
    
    reports = parse_input(filename)
    
    if args.debug or args.test:
        print(f"Total reports: {len(reports)}")
        print("\nAnalyzing each report:")
        for i, report in enumerate(reports):
            safe = is_safe_report(report)
            print(f"Report {i+1}: {report} -> {'Safe' if safe else 'Unsafe'}")
            
            if args.debug:
                # Show differences for debugging
                if len(report) > 1:
                    diffs = [report[j] - report[j-1] for j in range(1, len(report))]
                    print(f"  Differences: {diffs}")
    
    result = count_safe_reports(reports)
    
    if args.debug or args.test:
        print(f"\nSafe reports: {result}")
    else:
        print(result)

if __name__ == "__main__":
    main()