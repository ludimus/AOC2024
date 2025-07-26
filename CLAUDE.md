# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Advent of Code 2024 solutions repository containing daily puzzle solutions organized by day folders (day01/, day02/, etc.).

## Architecture and Structure

- **Daily Organization**: Each day's solutions are contained in their own directory (`dayXX/`)
- **Python Solutions**: All solutions are implemented in Python 3
  - Python files: `solution.py`, `solution_part2.py`, etc.
- **Input Files**: Each day contains `input.txt` (actual puzzle input) and `example.txt`/`example.in` (test cases)
- **Task Descriptions**: Problem statements stored as `taska.txt`, `taskb.txt`, `task_part1.txt`, `task_part2.txt`

## Common Development Commands

### Running Python Solutions
```bash
# Navigate to specific day and run Python solution
cd dayXX/
python3 solution.py
python3 solution_part2.py
```

### Testing Solutions
- Use `example.txt` or `example.in` files for testing before running on actual input
- Many directories contain speed comparison scripts like `speed_test.py`

## Code Patterns

- **Input Parsing**: Solutions read from `input.txt` using file I/O in Python
- **Two-Part Structure**: Most AoC problems have Part A and Part B, often implemented as separate files
- **Debugging Files**: Some days include debug utilities (e.g., `debug_lines.py`, `regex_examples.py`)

## Working with Solutions

When adding new solutions or modifying existing ones:
1. Follow the established naming convention (`solution.py`, `solution_part2.py`)
2. Ensure solutions can read from the standard input files (`input.txt`, `example.txt`)
3. Include appropriate comments explaining the algorithm approach
4. Test with example input before running on actual puzzle input
5. Use Python 3 syntax and features
6. Before coding, make a plan, explain datastructures to use, functions needed. store strategy plan in the dayxx folder