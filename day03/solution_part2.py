#!/usr/bin/env python3
import re

def solve_day3_part2(input_text):
    pattern = r"(do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\))"
    matches = re.finditer(pattern, input_text)
    
    enabled = True
    total = 0
    
    for match in matches:
        instruction = match.group(1)
        
        if instruction == "do()":
            enabled = True
        elif instruction == "don't()":
            enabled = False
        elif instruction.startswith("mul(") and enabled:
            x, y = match.group(2), match.group(3)
            total += int(x) * int(y)
    
    return total

def main():
    with open('input.txt', 'r') as f:
        input_text = f.read()
    
    result = solve_day3_part2(input_text)
    print(f"Sum of enabled multiplications: {result}")
    
    test_input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    test_result = solve_day3_part2(test_input)
    print(f"Test result: {test_result} (expected: 48)")

if __name__ == "__main__":
    main()