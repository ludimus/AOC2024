# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Advent of Code 2024 solutions repository containing daily puzzle solutions organized by day folders (day01/, day02/, etc.).

## Architecture and Structure

- **Daily Organization**: Each day's solutions are contained in their own directory (`dayXX/`)
- **Python Solutions**: All solutions are implemented in Python 3
  - Python files: `solution.py`, `solution_part2.py`, etc.
- **Input Files**: Each day contains `input.txt` (actual puzzle input) and a generated `example.txt` (test cases)
- **Task Descriptions**: Problem statements stored as `part1.txt`, `part2.txt`

## Common Development Commands

### Running Python Solutions
```bash
# Navigate to specific day and run Python solution
cd dayXX/
python3 solution_part1.py
python3 solution_part2.py
```

### Testing Solutions
- extract the provided example data from  into `example.txt`
- Use `example.txt`  files for testing before running on actual input
- Testingmode should be selectable with a command line switch
- Testingmode should be done on example.txt
- Testingmode should should print debug statements by default.
- Debug mode should be selectable with a command line switch when running on the actual challenge data
- For speed testing use the bash command 'time'

## Code Patterns

- **Input Parsing**: Solutions read from `input.txt` or `example.txt` using file I/O in Python. This always should be a seperate function, parsing the input into datastructures. The datastructures should be returned to the main function
- **Two-Part Structure**: Most AoC problems have Part 1 and Part 2, implemented as separate files: solution_part1.py and solution_part2.py


## Working with Solutions

When adding new solutions or modifying existing ones:
1. Follow the established naming convention (`solution_part1.py`, `solution_part2.py`)
2. Ensure solutions can read from the standard input files (`input.txt`, `example.txt`)
3. Include appropriate comments explaining the algorithm approach
4. Test with example input before running on actual puzzle input
5. Use Python 3 syntax and features
6. Before coding, make a plan, explain datastructures to use, functions needed. store `strategy_plan.md` in the dayxx folder
7. when a challenge is accepted. Change woking directory to main folder, add everything to GIT, commit with a descriptive message and push to remote