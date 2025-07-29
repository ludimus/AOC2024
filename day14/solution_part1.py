#!/usr/bin/env python3
import argparse
import time
from typing import List, Tuple

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

def simulate_direct(robots: List[Robot], width: int, height: int, time_steps: int) -> List[Robot]:
    """Direct calculation using modular arithmetic"""
    result_robots = []
    
    for robot in robots:
        # Calculate final position directly
        final_x = (robot.x + robot.vx * time_steps) % width
        final_y = (robot.y + robot.vy * time_steps) % height
        
        result_robots.append(Robot(final_x, final_y, robot.vx, robot.vy))
    
    return result_robots

def simulate_stepwise(robots: List[Robot], width: int, height: int, time_steps: int) -> List[Robot]:
    """Step-by-step simulation"""
    # Create copies to avoid modifying original robots
    current_robots = [Robot(r.x, r.y, r.vx, r.vy) for r in robots]
    
    for step in range(time_steps):
        for robot in current_robots:
            # Update position
            robot.x += robot.vx
            robot.y += robot.vy
            
            # Handle wrapping
            robot.x = robot.x % width
            robot.y = robot.y % height
    
    return current_robots

def count_quadrants(robots: List[Robot], width: int, height: int) -> Tuple[int, int, int, int]:
    """Count robots in each quadrant (excluding middle lines)"""
    mid_x = width // 2
    mid_y = height // 2
    
    q1 = q2 = q3 = q4 = 0
    
    for robot in robots:
        if robot.x == mid_x or robot.y == mid_y:
            continue  # Skip robots on middle lines
        
        if robot.x < mid_x and robot.y < mid_y:
            q1 += 1
        elif robot.x > mid_x and robot.y < mid_y:
            q2 += 1
        elif robot.x < mid_x and robot.y > mid_y:
            q3 += 1
        elif robot.x > mid_x and robot.y > mid_y:
            q4 += 1
    
    return q1, q2, q3, q4

def calculate_safety_factor(robots: List[Robot], width: int, height: int) -> int:
    """Calculate safety factor from quadrant counts"""
    q1, q2, q3, q4 = count_quadrants(robots, width, height)
    return q1 * q2 * q3 * q4

def visualize_robots(robots: List[Robot], width: int, height: int, debug: bool = False):
    """Visualize robot positions on grid"""
    if not debug:
        return
    
    grid = [[0 for _ in range(width)] for _ in range(height)]
    
    for robot in robots:
        grid[robot.y][robot.x] += 1
    
    print("Robot positions:")
    for row in grid:
        line = ""
        for count in row:
            if count == 0:
                line += "."
            else:
                line += str(count)
        print(line)
    print()

def run_simulation(robots: List[Robot], width: int, height: int, time_steps: int, method: str, debug: bool = False) -> Tuple[int, float]:
    """Run simulation and return safety factor and execution time"""
    start_time = time.perf_counter()
    
    if method == "direct":
        final_robots = simulate_direct(robots, width, height, time_steps)
    elif method == "stepwise":
        final_robots = simulate_stepwise(robots, width, height, time_steps)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    if debug:
        print(f"Method: {method}")
        visualize_robots(final_robots, width, height, debug)
        q1, q2, q3, q4 = count_quadrants(final_robots, width, height)
        print(f"Quadrant counts: Q1={q1}, Q2={q2}, Q3={q3}, Q4={q4}")
    
    safety_factor = calculate_safety_factor(final_robots, width, height)
    
    return safety_factor, execution_time

def main():
    parser = argparse.ArgumentParser(description='Day 14: Restroom Redoubt Part 1')
    parser.add_argument('--test', action='store_true', help='Run on example.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--method', choices=['direct', 'stepwise', 'both'], default='both', 
                       help='Simulation method to use')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    width = 11 if args.test else 101
    height = 7 if args.test else 103
    time_steps = 100
    
    robots = parse_input(filename)
    
    if args.debug or args.test:
        print(f"Loaded {len(robots)} robots from {filename}")
        print(f"Grid size: {width}×{height}")
        print(f"Simulating {time_steps} seconds\n")
    
    if args.method == 'both':
        # Run both methods and compare
        print("=== DIRECT METHOD (Modular Arithmetic) ===")
        safety_direct, time_direct = run_simulation(robots, width, height, time_steps, "direct", args.debug or args.test)
        print(f"Safety Factor: {safety_direct}")
        print(f"Execution Time: {time_direct:.6f} seconds\n")
        
        print("=== STEPWISE METHOD (Simulation) ===")
        safety_stepwise, time_stepwise = run_simulation(robots, width, height, time_steps, "stepwise", args.debug or args.test)
        print(f"Safety Factor: {safety_stepwise}")
        print(f"Execution Time: {time_stepwise:.6f} seconds\n")
        
        print("=== COMPARISON ===")
        print(f"Results match: {safety_direct == safety_stepwise}")
        print(f"Speed improvement: {time_stepwise / time_direct:.1f}x faster (direct method)")
        
    else:
        safety_factor, execution_time = run_simulation(robots, width, height, time_steps, args.method, args.debug or args.test)
        print(f"Safety Factor: {safety_factor}")
        print(f"Execution Time: {execution_time:.6f} seconds")

if __name__ == "__main__":
    main()