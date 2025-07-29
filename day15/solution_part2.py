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

def scale_grid(grid):
    scaled = []
    for row in grid:
        new_row = []
        for cell in row:
            if cell == '#':
                new_row.extend(['#', '#'])
            elif cell == 'O':
                new_row.extend(['[', ']'])
            elif cell == '.':
                new_row.extend(['.', '.'])
            elif cell == '@':
                new_row.extend(['@', '.'])
        scaled.append(new_row)
    return scaled

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

def get_boxes_to_move(grid, start_pos, direction, debug=False):
    boxes_to_move = set()
    queue = [start_pos]
    
    while queue:
        r, c = queue.pop(0)
        dr, dc = direction
        new_r, new_c = r + dr, c + dc
        
        if new_r < 0 or new_r >= len(grid) or new_c < 0 or new_c >= len(grid[0]):
            return None
        
        if grid[new_r][new_c] == '#':
            return None
        
        if grid[new_r][new_c] == '.':
            continue
        
        if grid[new_r][new_c] == '[':
            box_left = (new_r, new_c)
            box_right = (new_r, new_c + 1)
            if box_left not in boxes_to_move:
                boxes_to_move.add(box_left)
                boxes_to_move.add(box_right)
                queue.append(box_left)
                queue.append(box_right)
        elif grid[new_r][new_c] == ']':
            box_left = (new_r, new_c - 1)
            box_right = (new_r, new_c)
            if box_left not in boxes_to_move:
                boxes_to_move.add(box_left)
                boxes_to_move.add(box_right)
                queue.append(box_left)
                queue.append(box_right)
    
    return boxes_to_move

def can_move_wide(grid, robot_pos, direction, debug=False):
    boxes_to_move = get_boxes_to_move(grid, robot_pos, direction, debug)
    return boxes_to_move is not None

def execute_wide_move(grid, robot_pos, direction, debug=False):
    r, c = robot_pos
    dr, dc = direction
    
    boxes_to_move = get_boxes_to_move(grid, robot_pos, direction, debug)
    if boxes_to_move is None:
        if debug:
            print(f"  Cannot move from ({r},{c}) in direction ({dr},{dc})")
        return robot_pos
    
    if debug and boxes_to_move:
        print(f"  Moving {len(boxes_to_move)//2} boxes")
    
    box_chars = {}
    for box_r, box_c in boxes_to_move:
        box_chars[(box_r, box_c)] = grid[box_r][box_c]
        grid[box_r][box_c] = '.'
    
    for (box_r, box_c), char in box_chars.items():
        new_box_r, new_box_c = box_r + dr, box_c + dc
        grid[new_box_r][new_box_c] = char
    
    grid[r][c] = '.'
    new_r, new_c = r + dr, c + dc
    grid[new_r][new_c] = '@'
    
    if debug:
        print(f"  Robot moved from ({r},{c}) to ({new_r},{new_c})")
    
    return (new_r, new_c)

def calculate_wide_gps_sum(grid):
    total = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '[':
                gps = 100 * r + c
                total += gps
    return total

def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print()

def simulate_wide_warehouse(grid, moves, robot_pos, debug=False):
    if debug:
        print("Initial state:")
        print_grid(grid)
    
    for i, move in enumerate(moves):
        if debug:
            print(f"Move {i+1}: {move}")
        
        direction = get_direction(move)
        robot_pos = execute_wide_move(grid, robot_pos, direction, debug)
        
        if debug:
            print_grid(grid)
    
    return robot_pos

def main():
    parser = argparse.ArgumentParser(description='Day 15: Warehouse Woes - Part 2')
    parser.add_argument('--test', action='store_true', help='Run with example.txt')
    parser.add_argument('--test2', action='store_true', help='Run with example2.txt')
    parser.add_argument('--large', action='store_true', help='Run with example_large.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    
    if args.large:
        filename = 'example_large.txt'
    elif args.test2:
        filename = 'example2.txt'
    elif args.test:
        filename = 'example.txt'
    else:
        filename = 'input.txt'
    
    debug = args.debug or args.test or args.test2 or args.large
    
    original_grid, moves = parse_input(filename)
    grid = scale_grid(original_grid)
    robot_pos = find_robot(grid)
    
    if debug:
        print(f"Using input file: {filename}")
        print(f"Original grid size: {len(original_grid)}x{len(original_grid[0])}")
        print(f"Scaled grid size: {len(grid)}x{len(grid[0])}")
        print(f"Robot starting position: {robot_pos}")
        print(f"Number of moves: {len(moves)}")
        print()
    
    final_robot_pos = simulate_wide_warehouse(grid, moves, robot_pos, debug)
    gps_sum = calculate_wide_gps_sum(grid)
    
    if debug:
        print(f"Final robot position: {final_robot_pos}")
        print("Final state:")
        print_grid(grid)
    
    print(f"Sum of GPS coordinates: {gps_sum}")

if __name__ == '__main__':
    main()