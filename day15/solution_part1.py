#!/usr/bin/env python3

import sys
import argparse

def parse_input(filename):
    with open(filename, 'r') as f:
        content = f.read().strip()
    
    parts = content.split('\n\n')
    grid_lines = parts[0].split('\n')
    moves = ''.join(parts[1].split('\n'))
    
    grid = [list(line) for line in grid_lines]
    return grid, moves

def find_robot(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '@':
                return (r, c)
    return None

def get_direction(move):
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }
    return directions[move]

def can_move_and_push(grid, pos, direction, debug=False):
    r, c = pos
    dr, dc = direction
    new_r, new_c = r + dr, c + dc
    
    if new_r < 0 or new_r >= len(grid) or new_c < 0 or new_c >= len(grid[0]):
        return False
    
    if grid[new_r][new_c] == '#':
        return False
    
    if grid[new_r][new_c] == '.':
        return True
    
    if grid[new_r][new_c] == 'O':
        return can_move_and_push(grid, (new_r, new_c), direction, debug)
    
    return False

def execute_move(grid, robot_pos, direction, debug=False):
    r, c = robot_pos
    dr, dc = direction
    
    if not can_move_and_push(grid, robot_pos, direction, debug):
        if debug:
            print(f"  Cannot move from ({r},{c}) in direction ({dr},{dc})")
        return robot_pos
    
    new_r, new_c = r + dr, c + dc
    
    if grid[new_r][new_c] == 'O':
        push_boxes(grid, (new_r, new_c), direction, debug)
    
    grid[r][c] = '.'
    grid[new_r][new_c] = '@'
    
    if debug:
        print(f"  Robot moved from ({r},{c}) to ({new_r},{new_c})")
    
    return (new_r, new_c)

def push_boxes(grid, box_pos, direction, debug=False):
    r, c = box_pos
    dr, dc = direction
    new_r, new_c = r + dr, c + dc
    
    if grid[new_r][new_c] == 'O':
        push_boxes(grid, (new_r, new_c), direction, debug)
    
    grid[new_r][new_c] = 'O'
    grid[r][c] = '.'
    
    if debug:
        print(f"    Box pushed from ({r},{c}) to ({new_r},{new_c})")

def calculate_gps_sum(grid):
    total = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'O':
                gps = 100 * r + c
                total += gps
    return total

def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print()

def simulate_warehouse(grid, moves, robot_pos, debug=False):
    if debug:
        print("Initial state:")
        print_grid(grid)
    
    for i, move in enumerate(moves):
        if debug:
            print(f"Move {i+1}: {move}")
        
        direction = get_direction(move)
        robot_pos = execute_move(grid, robot_pos, direction, debug)
        
        if debug:
            print_grid(grid)
    
    return robot_pos

def main():
    parser = argparse.ArgumentParser(description='Day 15: Warehouse Woes - Part 1')
    parser.add_argument('--test', action='store_true', help='Run with example.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    debug = args.debug or args.test
    
    grid, moves = parse_input(filename)
    robot_pos = find_robot(grid)
    
    if debug:
        print(f"Using input file: {filename}")
        print(f"Grid size: {len(grid)}x{len(grid[0])}")
        print(f"Robot starting position: {robot_pos}")
        print(f"Number of moves: {len(moves)}")
        print()
    
    final_robot_pos = simulate_warehouse(grid, moves, robot_pos, debug)
    gps_sum = calculate_gps_sum(grid)
    
    if debug:
        print(f"Final robot position: {final_robot_pos}")
        print("Final state:")
        print_grid(grid)
    
    print(f"Sum of GPS coordinates: {gps_sum}")

if __name__ == '__main__':
    main()