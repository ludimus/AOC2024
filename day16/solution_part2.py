#!/usr/bin/env python3
import heapq
import sys
import argparse
from collections import defaultdict, deque

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

def dijkstra_all_paths(grid, start_pos, end_pos, debug=False):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_names = ['East', 'South', 'West', 'North']
    
    # Use distance dict and parent tracking
    dist = defaultdict(lambda: float('inf'))
    parents = defaultdict(list)
    
    start_state = (start_pos[0], start_pos[1], 0)  # Start facing East
    dist[start_state] = 0
    
    pq = [(0, start_pos[0], start_pos[1], 0)]
    
    while pq:
        cost, row, col, direction = heapq.heappop(pq)
        state = (row, col, direction)
        
        # Skip if we've found a better path
        if cost > dist[state]:
            continue
            
        if debug:
            print(f"Processing: cost={cost}, pos=({row},{col}), dir={dir_names[direction]}")
        
        # Try moving forward
        dr, dc = directions[direction]
        new_row, new_col = row + dr, col + dc
        if (0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and 
            grid[new_row][new_col] != '#'):
            new_state = (new_row, new_col, direction)
            new_cost = cost + 1
            
            if new_cost < dist[new_state]:
                dist[new_state] = new_cost
                parents[new_state] = [state]
                heapq.heappush(pq, (new_cost, new_row, new_col, direction))
            elif new_cost == dist[new_state]:
                parents[new_state].append(state)
        
        # Try rotating clockwise and counterclockwise
        for new_dir in [(direction + 1) % 4, (direction - 1) % 4]:
            new_state = (row, col, new_dir)
            new_cost = cost + 1000
            
            if new_cost < dist[new_state]:
                dist[new_state] = new_cost
                parents[new_state] = [state]
                heapq.heappush(pq, (new_cost, row, col, new_dir))
            elif new_cost == dist[new_state]:
                parents[new_state].append(state)
    
    # Find minimum cost to reach end
    min_end_cost = float('inf')
    end_states = []
    for direction in range(4):
        end_state = (end_pos[0], end_pos[1], direction)
        if dist[end_state] < min_end_cost:
            min_end_cost = dist[end_state]
            end_states = [end_state]
        elif dist[end_state] == min_end_cost:
            end_states.append(end_state)
    
    return min_end_cost, end_states, parents

def find_optimal_tiles(end_states, parents, debug=False):
    visited = set()
    optimal_tiles = set()
    queue = deque(end_states)
    
    while queue:
        state = queue.popleft()
        if state in visited:
            continue
            
        visited.add(state)
        row, col, direction = state
        optimal_tiles.add((row, col))
        
        if debug:
            print(f"Backtracking: pos=({row},{col}), dir={direction}")
        
        for parent in parents[state]:
            if parent not in visited:
                queue.append(parent)
    
    return optimal_tiles

def main():
    parser = argparse.ArgumentParser(description='Day 16 Part 2: Reindeer Maze - All Optimal Paths')
    parser.add_argument('--test', action='store_true', help='Use example.txt for testing')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('file', nargs='?', help='Specific file to use (example2, etc.)')
    args = parser.parse_args()
    
    if args.test:
        filename = 'example.txt'
    elif args.file == 'example2':
        filename = 'example2.txt'
    else:
        filename = 'input.txt'
    grid, start_pos, end_pos = parse_input(filename)
    
    if args.debug or args.test:
        print(f"Grid size: {len(grid)}x{len(grid[0])}")
        print(f"Start: {start_pos}")
        print(f"End: {end_pos}")
        print()
    
    min_cost, end_states, parents = dijkstra_all_paths(grid, start_pos, end_pos, debug=args.debug)
    
    if args.debug or args.test:
        print(f"Minimum cost: {min_cost}")
        print(f"End states with min cost: {len(end_states)}")
        print()
    
    optimal_tiles = find_optimal_tiles(end_states, parents, debug=args.debug)
    
    print(f"Tiles on optimal paths: {len(optimal_tiles)}")

if __name__ == "__main__":
    main()