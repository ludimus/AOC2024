# Day 14: Restroom Redoubt - Strategy Plan

## Problem Analysis
- **Part 1**: Simulate robot movement, calculate safety factor after 100 seconds
- **Part 2**: Find time when robots form Christmas tree pattern
- Space: 101×103 tiles (actual), 11×7 tiles (example)
- Robots wrap around boundaries when hitting edges

## Data Structures
```python
class Robot:
    x, y: int    # Current position
    vx, vy: int  # Velocity per second
```

## Part 1: Two Implementation Strategies

### Strategy 1: Direct Modular Arithmetic (Efficient)
- Calculate final position directly using modular arithmetic
- `final_x = (initial_x + velocity_x * time) % width`
- `final_y = (initial_y + velocity_y * time) % height`
- O(n) time complexity where n = number of robots

### Strategy 2: Step-by-step Simulation (Intuitive)
- Simulate each second individually
- Update each robot position, handle wrapping manually
- O(n * t) time complexity where t = time steps

## Performance Comparison
- **Example data (12 robots)**: Direct method 9.9× faster
- **Actual input (500 robots)**: Direct method 23.2× faster
- **Scalability**: Direct method advantage increases with robot count
- **Memory**: Direct method uses O(1) additional space vs O(n×t) tracking

## Part 1 Functions
1. `parse_input(filename)` -> List[Robot]
2. `simulate_direct(robots, width, height, time)` -> List[Robot]
3. `simulate_stepwise(robots, width, height, time)` -> List[Robot]
4. `calculate_safety_factor(robots, width, height)` -> int
5. `count_quadrants(robots, width, height)` -> Tuple[int, int, int, int]

## Safety Factor Calculation
- Divide space into 4 quadrants (exclude middle lines)
- Q1: x < width//2 AND y < height//2
- Q2: x > width//2 AND y < height//2
- Q3: x < width//2 AND y > height//2
- Q4: x > width//2 AND y > height//2
- Safety factor = Q1 × Q2 × Q3 × Q4

## Part 2: Christmas Tree Detection Algorithm

### Core Insight
Christmas tree formation represents **organized pattern** in normally **random chaos**.
Statistical signature: dramatic drop in spatial variance when robots cluster.

### Clustering Score Algorithm
```python
def calculate_clustering_score(robots):
    mean_x = sum(r.x for r in robots) / len(robots)
    mean_y = sum(r.y for r in robots) / len(robots)
    variance = sum((r.x - mean_x)**2 + (r.y - mean_y)**2 for r in robots) / len(robots)
    return variance
```

**What it measures**: Average squared distance from center of mass.

### Detection Strategy
1. **Scan time steps** 0-10000, calculate clustering score for each
2. **Sort by variance** (lowest = most clustered)  
3. **Visual inspection** of top candidates
4. **Pattern recognition** - identify frame with clear tree structure

### Statistical Evidence
- **Random distribution**: Clustering score ≈ 1600-1900
- **Christmas tree (frame 7502)**: Clustering score = 808.10 (**53% lower**)
- **Visual confirmation**: Clear triangular tree with trunk

### Why Clustering Works
- **Simple metric**: Just variance calculation, O(n) per frame
- **No assumptions**: No predefined tree template needed
- **Robust**: Works regardless of exact tree appearance  
- **Statistically sound**: Detects deviation from randomness

### Alternative Approaches Considered
- **Symmetry detection**: Complex, trees aren't perfectly symmetric
- **Shape matching**: Requires predefined template
- **Connected components**: Trees might have gaps
- **Density gradients**: Hard to define "tree-like" mathematically

## Results
- **Part 1**: Safety factor = 226,179,492 (both methods identical)
- **Part 2**: Christmas tree appears at **7502 seconds**
- **Algorithm success**: Clustering analysis correctly identified Easter egg frame