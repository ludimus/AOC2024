#!/usr/bin/env python3
import heapq
import sys
import argparse

def parse_input(filename):
    with open(filename, 'r') as f:
        grid = [list(line.strip()) for line in f]
    
    start_pos = None
    end_pos = None
    
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                start_pos = (row, col)
            elif grid[row][col] == 'E':
                end_pos = (row, col)
    
    return grid, start_pos, end_pos

def dijkstra(grid, start_pos, end_pos, debug=False):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_names = ['East', 'South', 'West', 'North']
    
    pq = [(0, start_pos[0], start_pos[1], 0)]
    visited = set()
    
    while pq:
        cost, row, col, direction = heapq.heappop(pq)
        
        if debug:
            print(f"Exploring: cost={cost}, pos=({row},{col}), dir={dir_names[direction]}")
        
        if (row, col) == end_pos:
            return cost
            
        state = (row, col, direction)
        if state in visited:
            continue
        visited.add(state)
        
        dr, dc = directions[direction]
        new_row, new_col = row + dr, col + dc
        if (0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and 
            grid[new_row][new_col] != '#'):
            heapq.heappush(pq, (cost + 1, new_row, new_col, direction))
        
        heapq.heappush(pq, (cost + 1000, row, col, (direction + 1) % 4))
        heapq.heappush(pq, (cost + 1000, row, col, (direction - 1) % 4))
    
    return -1

def main():
    parser = argparse.ArgumentParser(description='Day 16 Part 1: Reindeer Maze')
    parser.add_argument('--test', action='store_true', help='Use example.txt for testing')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    grid, start_pos, end_pos = parse_input(filename)
    
    if args.debug or args.test:
        print(f"Grid size: {len(grid)}x{len(grid[0])}")
        print(f"Start: {start_pos}")
        print(f"End: {end_pos}")
        print()
    
    result = dijkstra(grid, start_pos, end_pos, debug=args.debug)
    print(f"Lowest score: {result}")

if __name__ == "__main__":
    main()