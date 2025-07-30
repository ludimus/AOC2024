#!/usr/bin/env python3
import sys
import argparse

def parse_input(filename):
    """Parse input file to get initial secret numbers."""
    with open(filename, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]

def mix(value, secret):
    """Mix a value into the secret number using XOR."""
    return value ^ secret

def prune(secret):
    """Prune the secret number using modulo 16777216."""
    return secret % 16777216

def next_secret(secret):
    """Generate the next secret number using the 3-step process."""
    # Step 1: multiply by 64, mix, prune
    result = secret * 64
    secret = mix(result, secret)
    secret = prune(secret)
    
    # Step 2: divide by 32 (floor), mix, prune
    result = secret // 32
    secret = mix(result, secret)
    secret = prune(secret)
    
    # Step 3: multiply by 2048, mix, prune
    result = secret * 2048
    secret = mix(result, secret)
    secret = prune(secret)
    
    return secret

def generate_nth_secret(initial, n):
    """Generate the nth secret number from initial secret."""
    secret = initial
    for _ in range(n):
        secret = next_secret(secret)
    return secret

def solve(filename, debug=False):
    """Main solution function."""
    initial_secrets = parse_input(filename)
    
    if debug:
        print(f"Initial secrets: {initial_secrets}")
    
    total = 0
    for i, initial in enumerate(initial_secrets):
        secret_2000 = generate_nth_secret(initial, 2000)
        total += secret_2000
        
        if debug:
            print(f"Buyer {i+1} (initial: {initial}): 2000th secret = {secret_2000}")
    
    return total

def main():
    parser = argparse.ArgumentParser(description='Day 22: Monkey Market - Part 1')
    parser.add_argument('--test', action='store_true', help='Run with example.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    result = solve(filename, args.debug)
    
    print(f"Sum of 2000th secret numbers: {result}")

if __name__ == "__main__":
    main()