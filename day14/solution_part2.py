#!/usr/bin/env python3
import argparse
from typing import List

class Robot:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    
    def __repr__(self):
        return f"Robot(x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy})"

def parse_input(filename: str) -> List[Robot]:
    robots = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse p=x,y v=vx,vy
            parts = line.split(' ')
            pos_part = parts[0][2:]  # Remove 'p='
            vel_part = parts[1][2:]  # Remove 'v='
            
            x, y = map(int, pos_part.split(','))
            vx, vy = map(int, vel_part.split(','))
            
            robots.append(Robot(x, y, vx, vy))
    
    return robots

def simulate_to_time(robots: List[Robot], width: int, height: int, time_step: int) -> List[Robot]:
    """Calculate robot positions at specific time step"""
    result_robots = []
    
    for robot in robots:
        final_x = (robot.x + robot.vx * time_step) % width
        final_y = (robot.y + robot.vy * time_step) % height
        result_robots.append(Robot(final_x, final_y, robot.vx, robot.vy))
    
    return result_robots

def visualize_frame(robots: List[Robot], width: int, height: int, time_step: int):
    """Display robots at given time step"""
    grid = [['.' for _ in range(width)] for _ in range(height)]
    
    for robot in robots:
        if grid[robot.y][robot.x] == '.':
            grid[robot.y][robot.x] = '1'
        else:
            # Multiple robots on same tile
            current = grid[robot.y][robot.x]
            if current.isdigit() and int(current) < 9:
                grid[robot.y][robot.x] = str(int(current) + 1)
            else:
                grid[robot.y][robot.x] = '*'
    
    print(f"=== Time Step {time_step} ===")
    for row in grid:
        print(''.join(row))
    print()

def calculate_clustering_score(robots: List[Robot]) -> float:
    """Calculate a simple clustering metric"""
    if len(robots) < 2:
        return 0.0
    
    # Calculate variance in positions
    mean_x = sum(r.x for r in robots) / len(robots)
    mean_y = sum(r.y for r in robots) / len(robots)
    
    variance = sum((r.x - mean_x)**2 + (r.y - mean_y)**2 for r in robots) / len(robots)
    return variance

def main():
    parser = argparse.ArgumentParser(description='Day 14: Restroom Redoubt Part 2')
    parser.add_argument('--test', action='store_true', help='Run on example.txt')
    parser.add_argument('--start', type=int, default=0, help='Start time step')
    parser.add_argument('--end', type=int, default=100, help='End time step')
    parser.add_argument('--step', type=int, default=1, help='Time step increment')
    parser.add_argument('--show-scores', action='store_true', help='Show clustering scores only')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    width = 11 if args.test else 101
    height = 7 if args.test else 103
    
    robots = parse_input(filename)
    
    print(f"Loaded {len(robots)} robots from {filename}")
    print(f"Grid size: {width}×{height}")
    print(f"Showing frames from {args.start} to {args.end}\n")
    
    if args.show_scores:
        # Just show clustering scores to identify interesting frames
        scores = []
        for t in range(args.start, args.end + 1, args.step):
            current_robots = simulate_to_time(robots, width, height, t)
            score = calculate_clustering_score(current_robots)
            scores.append((t, score))
            print(f"Time {t:4d}: Clustering score = {score:.2f}")
        
        # Find frames with lowest clustering scores (most clustered)
        scores.sort(key=lambda x: x[1])
        print(f"\nMost clustered frames (lowest scores):")
        for i, (t, score) in enumerate(scores[:10]):
            print(f"{i+1:2d}. Time {t:4d}: {score:.2f}")
    
    else:
        # Show visual frames
        for t in range(args.start, args.end + 1, args.step):
            current_robots = simulate_to_time(robots, width, height, t)
            visualize_frame(current_robots, width, height, t)
            
            # Pause for large ranges to avoid overwhelming output
            if args.end - args.start > 50:
                if t > args.start and (t - args.start) % 20 == 0:
                    input("Press Enter to continue...")

if __name__ == "__main__":
    main()