#!/usr/bin/env python3
"""
Debug script to show all 1D lines extracted from the example grid
"""

from solution_regex import get_horizontal_lines, get_vertical_lines, get_diagonal_lines, count_xmas_in_line

def main():
    example_grid = [
        "MMMSXXMASM",
        "MSAMXMSMSA",
        "AMXSXMAAMM",
        "MSAMASMSMX",
        "XMASAMXAMM",
        "XXAMMXXAMA",
        "SMSMSASXSS",
        "SAXAMASAAA",
        "MAMMMXMMMM",
        "MXMXAXMASX"
    ]
    
    print("=== EXAMPLE GRID ===")
    for i, row in enumerate(example_grid):
        print(f"{i:2}: {row}")
    
    print("\n=== HORIZONTAL LINES (ROWS) ===")
    horizontal = get_horizontal_lines(example_grid)
    total_h = 0
    for i, line in enumerate(horizontal):
        count = count_xmas_in_line(line)
        total_h += count
        print(f"Row {i:2}: {line} -> {count} matches")
    print(f"Total horizontal matches: {total_h}")
    
    print("\n=== VERTICAL LINES (COLUMNS) ===")
    vertical = get_vertical_lines(example_grid)
    total_v = 0
    for i, line in enumerate(vertical):
        count = count_xmas_in_line(line)
        total_v += count
        print(f"Col {i:2}: {line} -> {count} matches")
    print(f"Total vertical matches: {total_v}")
    
    print("\n=== DIAGONAL LINES ===")
    diagonal = get_diagonal_lines(example_grid)
    total_d = 0
    for i, line in enumerate(diagonal):
        count = count_xmas_in_line(line)
        total_d += count
        if len(line) >= 4:  # Only show diagonals long enough for XMAS
            print(f"Diag {i:2}: {line} -> {count} matches")
    print(f"Total diagonal matches: {total_d}")
    
    print(f"\n=== SUMMARY ===")
    print(f"Horizontal: {total_h}")
    print(f"Vertical: {total_v}")
    print(f"Diagonal: {total_d}")
    print(f"Total: {total_h + total_v + total_d}")

if __name__ == "__main__":
    main()