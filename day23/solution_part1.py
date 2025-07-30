#!/usr/bin/env python3
import sys
import argparse
from collections import defaultdict

def parse_input(filename):
    """Parse input file to build adjacency graph."""
    graph = defaultdict(set)
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse connection pair
            comp1, comp2 = line.split('-')
            
            # Add bidirectional edges
            graph[comp1].add(comp2)
            graph[comp2].add(comp1)
    
    return graph

def find_triangles(graph):
    """Find all triangles (3-cliques) in the graph."""
    triangles = set()
    
    for comp1 in graph:
        neighbors = list(graph[comp1])
        
        # Check all pairs of neighbors
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                comp2, comp3 = neighbors[i], neighbors[j]
                
                # If comp2 and comp3 are also connected, we have a triangle
                if comp3 in graph[comp2]:
                    # Sort to create canonical representation
                    triangle = tuple(sorted([comp1, comp2, comp3]))
                    triangles.add(triangle)
    
    return triangles

def has_t_computer(triangle):
    """Check if any computer in the triangle starts with 't'."""
    return any(comp.startswith('t') for comp in triangle)

def solve(filename, debug=False):
    """Main solution function."""
    graph = parse_input(filename)
    
    if debug:
        print(f"Graph has {len(graph)} computers")
        print(f"Total connections: {sum(len(neighbors) for neighbors in graph.values()) // 2}")
    
    # Find all triangles
    triangles = find_triangles(graph)
    
    if debug:
        print(f"Total triangles found: {len(triangles)}")
        print("All triangles:")
        for triangle in sorted(triangles):
            print(f"  {','.join(triangle)}")
    
    # Filter triangles containing at least one computer starting with 't'
    t_triangles = [triangle for triangle in triangles if has_t_computer(triangle)]
    
    if debug:
        print(f"\nTriangles with 't' computers: {len(t_triangles)}")
        for triangle in sorted(t_triangles):
            print(f"  {','.join(triangle)}")
    
    return len(t_triangles)

def main():
    parser = argparse.ArgumentParser(description='Day 23: LAN Party - Part 1')
    parser.add_argument('--test', action='store_true', help='Run with example.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    result = solve(filename, args.debug)
    
    print(f"Sets of three computers with at least one 't' computer: {result}")

if __name__ == "__main__":
    main()