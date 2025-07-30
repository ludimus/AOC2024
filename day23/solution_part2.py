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

def bron_kerbosch(graph, r, p, x, cliques):
    """
    Bron-Kerbosch algorithm to find all maximal cliques.
    
    Args:
        graph: adjacency graph
        r: current clique being built
        p: candidate set (nodes that could extend the clique)
        x: excluded set (nodes already processed)
        cliques: list to store found cliques
    """
    if not p and not x:
        # Found a maximal clique
        cliques.append(r.copy())
        return
    
    # Choose a pivot to minimize branching
    pivot = next(iter(p | x)) if p | x else None
    
    # For each vertex in P that's not connected to pivot
    for v in list(p):
        if pivot and v in graph[pivot]:
            continue
            
        # Recursive call
        bron_kerbosch(
            graph,
            r | {v},                    # Add v to current clique
            p & graph[v],               # New candidates: neighbors of v in P
            x & graph[v],               # New excluded: neighbors of v in X
            cliques
        )
        
        # Move v from P to X
        p.remove(v)
        x.add(v)

def find_largest_clique(graph):
    """Find the largest clique in the graph using Bron-Kerbosch algorithm."""
    cliques = []
    
    # Initialize: R=empty, P=all vertices, X=empty
    all_vertices = set(graph.keys())
    bron_kerbosch(graph, set(), all_vertices, set(), cliques)
    
    # Find the largest clique
    if not cliques:
        return set()
    
    return max(cliques, key=len)

def solve(filename, debug=False):
    """Main solution function for Part 2."""
    graph = parse_input(filename)
    
    if debug:
        print(f"Graph has {len(graph)} computers")
        print(f"Total connections: {sum(len(neighbors) for neighbors in graph.values()) // 2}")
    
    # Find the largest clique
    largest_clique = find_largest_clique(graph)
    
    if debug:
        print(f"Largest clique size: {len(largest_clique)}")
        print(f"Largest clique: {sorted(largest_clique)}")
    
    # Format as password (sorted, comma-separated)
    password = ','.join(sorted(largest_clique))
    
    return password

def main():
    parser = argparse.ArgumentParser(description='Day 23: LAN Party - Part 2')
    parser.add_argument('--test', action='store_true', help='Run with example.txt')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    filename = 'example.txt' if args.test else 'input.txt'
    result = solve(filename, args.debug)
    
    print(f"LAN party password: {result}")

if __name__ == "__main__":
    main()