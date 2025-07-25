#!/usr/bin/env python3
import re

def solve_day3(input_text):
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    matches = re.findall(pattern, input_text)
    print(matches)
    total = 0
    for x, y in matches:
        total += int(x) * int(y)
    
    return total

def main():
    with open('input.txt', 'r') as f:
        input_text = f.read()
    
    result = solve_day3(input_text)
    print(f"Sum of all multiplications: {result}")
    
    test_input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    test_result = solve_day3(test_input)
    print(f"Test result: {test_result} (expected: 161)")

if __name__ == "__main__":
    main()