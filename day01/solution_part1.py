#!/usr/bin/env python3

import sys
import argparse

def parse_input(filename):
    left_list = []
    right_list = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                left, right = map(int, line.split())
                left_list.append(left)
                right_list.append(right)
    
    return left_list, right_list

def calculate_total_distance(left_list, right_list):
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)
    
    total_distance = 0
    for left_val, right_val in zip(left_sorted, right_sorted):
        distance = abs(left_val - right_val)
        total_distance += distance
        
    return total_distance

def main():
    parser = argparse.ArgumentParser(description='Day 1 Part 1: Calculate total distance between lists')
    parser.add_argument('--test', action='store_true', help='Run with example.txt instead of input.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    
    if args.debug or args.test:
        print(f"Reading from {filename}")
    
    left_list, right_list = parse_input(filename)
    
    if args.debug or args.test:
        print(f"Left list: {left_list}")
        print(f"Right list: {right_list}")
        print(f"Sorted left: {sorted(left_list)}")
        print(f"Sorted right: {sorted(right_list)}")
    
    result = calculate_total_distance(left_list, right_list)
    
    if args.debug or args.test:
        print(f"Total distance: {result}")
    else:
        print(result)

if __name__ == "__main__":
    main()