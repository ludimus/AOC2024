#!/usr/bin/env python3
import sys
import argparse
from collections import defaultdict

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

def generate_prices(initial, n):
    """Generate n prices (last digits) from initial secret."""
    secret = initial
    prices = [secret % 10]  # Initial price
    
    for _ in range(n):
        secret = next_secret(secret)
        prices.append(secret % 10)
    
    return prices

def get_price_changes(prices):
    """Calculate price changes from consecutive prices."""
    changes = []
    for i in range(1, len(prices)):
        changes.append(prices[i] - prices[i-1])
    return changes

def find_pattern_sales(prices, changes):
    """Find all 4-change patterns and their first sale prices."""
    pattern_sales = {}
    
    for i in range(len(changes) - 3):
        pattern = tuple(changes[i:i+4])
        if pattern not in pattern_sales:
            # First occurrence of this pattern - record sale price
            sale_price = prices[i + 4]  # Price after the 4 changes
            pattern_sales[pattern] = sale_price
    
    return pattern_sales

def solve(filename, debug=False):
    """Main solution function for Part 2."""
    initial_secrets = parse_input(filename)
    
    if debug:
        print(f"Initial secrets: {initial_secrets}")
    
    # Track total bananas for each possible pattern
    pattern_totals = defaultdict(int)
    
    for i, initial in enumerate(initial_secrets):
        # Generate 2000 prices (plus initial)
        prices = generate_prices(initial, 2000)
        changes = get_price_changes(prices)
        
        # Find all patterns and their first sale prices for this buyer
        buyer_patterns = find_pattern_sales(prices, changes)
        
        if debug:
            print(f"Buyer {i+1} (initial: {initial}): {len(buyer_patterns)} unique patterns")
            if i == 0 and len(initial_secrets) <= 4:  # Show details for small examples
                print(f"  First few prices: {prices[:10]}")
                print(f"  First few changes: {changes[:9]}")
        
        # Add this buyer's contribution to each pattern's total
        for pattern, sale_price in buyer_patterns.items():
            pattern_totals[pattern] += sale_price
    
    # Find the pattern that gives maximum bananas
    best_pattern = max(pattern_totals.items(), key=lambda x: x[1])
    
    if debug:
        print(f"Best pattern: {best_pattern[0]} -> {best_pattern[1]} bananas")
        print(f"Total unique patterns found: {len(pattern_totals)}")
    
    return best_pattern[1]

def main():
    parser = argparse.ArgumentParser(description='Day 22: Monkey Market - Part 2')
    parser.add_argument('--test', action='store_true', help='Run with example.txt')
    parser.add_argument('--test2', action='store_true', help='Run with example2.txt (Part 2 example)')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    if args.test2:
        filename = 'example2.txt'
    elif args.test:
        filename = 'example.txt'
    else:
        filename = 'input.txt'
    
    result = solve(filename, args.debug)
    
    print(f"Maximum bananas possible: {result}")

if __name__ == "__main__":
    main()