# Day 23: LAN Party - Strategy Plan

## Problem Analysis
Find groups of 3 interconnected computers (triangles/cliques) where at least one computer name starts with 't'.

## Key Requirements
- Each line represents an undirected connection between two computers
- Find all sets of 3 computers where each is connected to the other two
- Count only those sets containing at least one computer starting with 't'

## Data Structures
- **Graph representation**: Dictionary mapping each computer to its connected neighbors
- **Connections**: Set of computer pairs (bidirectional edges)
- **Triangles**: Set of 3-computer cliques (sorted tuples to avoid duplicates)

## Algorithm Steps
1. Parse input to build adjacency graph
2. For each computer, check all pairs of its neighbors
3. If two neighbors are also connected to each other, we have a triangle
4. Filter triangles to only those containing at least one computer starting with 't'

## Functions Needed
1. `parse_input(filename)` - Build graph from connection pairs  
2. `find_triangles(graph)` - Find all 3-cliques in the graph
3. `has_t_computer(triangle)` - Check if any computer starts with 't'
4. `solve(filename)` - Main solution function

## Implementation Plan
1. Build undirected graph from input connections
2. Use nested loops to find all triangles efficiently
3. Filter results for 't' constraint
4. Test with example data first

## Part 1 Results ✓
- Example: 12 total triangles, 7 containing computers starting with 't'
- Actual puzzle input result: 1054
- Algorithm efficiently finds all 3-cliques in sparse graph

## Part 2 Analysis
**New Problem**: Find the largest clique (maximal complete subgraph) in the network.

**Key Changes**:
- Not just triangles (3-cliques), but the largest possible clique
- Every computer in the clique must be connected to every other computer
- Output format: alphabetically sorted computer names joined with commas

**Algorithm Options**:
1. **Bron-Kerbosch Algorithm**: Classic maximal clique enumeration
2. **Greedy Expansion**: Start with high-degree nodes and expand
3. **Brute Force**: Check all possible subsets (exponential - avoid)

**Data Structures for Part 2**:
- Same adjacency graph as Part 1
- Clique representation: Set of computer names
- Result: Largest clique found

**Implementation Plan**:
1. Use Bron-Kerbosch algorithm for finding all maximal cliques
2. Track the largest clique encountered
3. Format result as comma-separated sorted names

**Part 2 Results ✓**:
- Example: Largest clique {co, de, ka, ta} (size 4) → password "co,de,ka,ta"
- Actual puzzle input result: "ch,cz,di,gb,ht,ku,lu,tw,vf,vt,wo,xz,zk" (size 13)
- Bron-Kerbosch algorithm successfully finds maximum clique in sparse network
- Solution handles exponential problem efficiently with pivot optimization