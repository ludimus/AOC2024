#!/usr/bin/env python3

import sys
import argparse
from collections import Counter

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

def calculate_similarity_score(left_list, right_list):
    right_counts = Counter(right_list)
    
    similarity_score = 0
    for num in left_list:
        count_in_right = right_counts.get(num, 0)
        score_contribution = num * count_in_right
        similarity_score += score_contribution
        
    return similarity_score

def main():
    parser = argparse.ArgumentParser(description='Day 1 Part 2: Calculate similarity score between lists')
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
        right_counts = Counter(right_list)
        print(f"Right list counts: {dict(right_counts)}")
        
        print("\nSimilarity calculation:")
        total = 0
        for num in left_list:
            count = right_counts.get(num, 0)
            contribution = num * count
            total += contribution
            print(f"  {num} appears {count} times: {num} * {count} = {contribution}")
        print(f"Total similarity score: {total}")
    
    result = calculate_similarity_score(left_list, right_list)
    
    if not (args.debug or args.test):
        print(result)

if __name__ == "__main__":
    main()