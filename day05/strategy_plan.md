# Day 5 Strategy Plan: Print Queue

## Problem Analysis
- **Input Structure**: Two sections separated by blank line
  1. **Ordering Rules**: Lines like "47|53" meaning page 47 must come before page 53
  2. **Updates**: Lines like "75,47,61,53,29" representing sequences of pages to print
- **Goal**: Find which updates are already correctly ordered and sum their middle page numbers
- **Expected Result**: Example should yield 143 (middle pages: 61 + 53 + 29)

## Data Structures
- **Rules**: Dictionary/set to store ordering relationships
  - Could use `rules[(x,y)] = True` to indicate x must come before y
  - Or `before[x] = set()` containing all pages that must come before x
- **Updates**: List of lists, each containing page numbers
- **Middle Pages**: Extract middle element from correctly ordered updates

## Algorithmic Approach: Bubble Sort Solution

### Why Bubble Sort?
Bubble sort is perfect for this problem because:
1. **Beginner Friendly**: Easy to understand and implement
2. **Natural Fit**: The "swap if out of order" logic maps directly to our ordering rules
3. **Custom Comparison**: We can easily define what "out of order" means using our rules
4. **Validation Tool**: Sort each update and compare with original to check if already ordered

### Algorithm Steps (Simplified for Part 1)
1. **Parse Input**: 
   - Read rules into a set for O(1) lookup: `{(before, after), ...}`
   - Read updates as lists of integers

2. **Validation Function**:
   ```python
   def is_correctly_ordered(update, rules):
       for i in range(len(update)):
           for j in range(i + 1, len(update)):
               page_before = update[i]  # comes first in update
               page_after = update[j]   # comes later in update
               # If there's a rule saying page_after should come before page_before
               if (page_after, page_before) in rules:
                   return False  # Rule violation found
       return True
   ```

3. **Check All Updates**:
   - For each update, check if any pair violates the ordering rules
   - If no violations found, extract middle page number
   - Sum middle pages from all correctly ordered updates

### Why This Simpler Approach Works Better for Part 1
- **No sorting needed**: We only validate, don't rearrange
- **More efficient**: O(n²) validation vs O(n²) sorting per update
- **Clearer logic**: Direct rule checking is easier to understand
- **Extensible**: Bubble sort approach will be useful for Part 2

## Functions Needed
- `parse_input(filename)`: Read and parse rules and updates
- `should_swap(a, b, rules)`: Check if two pages need to be swapped
- `bubble_sort_with_rules(pages, rules)`: Sort pages using ordering rules
- `is_correctly_ordered(update, rules)`: Check if update is already correctly ordered
- `get_middle_page(update)`: Extract middle page from an update
- `solve_part1(rules, updates)`: Main solving function

## Implementation Notes
- Handle the blank line separator when parsing input
- Rules only apply to pages that are present in each update
- Middle page is always at index `len(pages) // 2` (integer division)
- Test with example.txt (expected: 143)

## Why This Approach Works
1. **Intuitive**: Bubble sort's comparison-based swapping mirrors the rule checking
2. **Robust**: Works regardless of rule complexity or update size
3. **Educational**: Demonstrates how sorting algorithms can solve ordering problems
4. **Extensible**: Easy to modify for Part 2 (involving actual sorting of incorrect updates)

## Part 2: Fix Incorrectly Ordered Updates

### Problem Analysis
- **Goal**: Take incorrectly ordered updates and sort them using the ordering rules
- **Process**: 
  1. Identify incorrectly ordered updates (from Part 1)
  2. Sort each one using bubble sort with custom comparison
  3. Extract middle page from each sorted update
  4. Sum the middle pages
- **Expected Result**: Example should yield 123 (middle pages: 47 + 29 + 47)

### Algorithm: Bubble Sort Implementation
Now the bubble sort approach from our original plan becomes essential!

```python
def should_swap(page_a, page_b, rules):
    """Check if page_a and page_b need to be swapped based on rules.
    Returns True if page_a should come after page_b."""
    # If there's a rule saying page_b must come before page_a, then swap
    return (page_b, page_a) in rules

def bubble_sort_with_rules(pages, rules):
    """Sort pages using bubble sort with custom ordering rules."""
    n = len(pages)
    sorted_pages = pages.copy()
    
    # Bubble sort: repeatedly go through the list and swap adjacent elements if out of order
    for i in range(n):
        for j in range(0, n - i - 1):
            if should_swap(sorted_pages[j], sorted_pages[j + 1], rules):
                # Swap the elements
                sorted_pages[j], sorted_pages[j + 1] = sorted_pages[j + 1], sorted_pages[j]
    
    return sorted_pages
```

### Part 2 Steps
1. **Reuse Part 1**: Use `is_correctly_ordered()` to identify incorrect updates
2. **Sort Incorrect Updates**: Apply bubble sort to each incorrectly ordered update
3. **Extract Middle Pages**: Get middle page from each sorted update
4. **Sum Results**: Add up all middle pages from corrected updates

### Functions Needed for Part 2
- `parse_input(filename)`: Reuse from Part 1
- `is_correctly_ordered(update, rules)`: Reuse from Part 1  
- `should_swap(page_a, page_b, rules)`: New - comparison function for bubble sort
- `bubble_sort_with_rules(pages, rules)`: New - sort using ordering rules
- `get_middle_page(update)`: Reuse from Part 1
- `solve_part2(rules, updates)`: Main solving function for Part 2

### Why Bubble Sort is Perfect Here
- **Custom Comparison**: We need to compare based on ordering rules, not numeric values
- **Beginner Friendly**: Easy to understand swap-based sorting
- **Guaranteed Correctness**: Will produce correct ordering regardless of rule complexity
- **Educational Value**: Shows how sorting algorithms can solve domain-specific problems

## Input Analysis: Complete Ordering Validation

### Analysis Results from input.txt
- **Total rules**: 1,176 ordering relationships
- **Total updates**: 189 sequences to validate/sort
- **Pages in play**: 49 unique page numbers
- **Rule coverage**: ✅ **Perfect** - every page in updates has rules

### Key Findings
1. **Complete Rule Set**: Each of the 49 pages has exactly 48 rules (paired with every other page)
2. **Total Ordering**: 1,176 rules = 49 × 48 ÷ 2, meaning complete pairwise relationships
3. **No Missing Rules**: Every page that appears in updates is covered by ordering rules
4. **Mathematical Guarantee**: The rule set defines a complete total ordering

### Why This Matters for Bubble Sort
**Perfect conditions for bubble sort success:**
- ✅ **Every comparison has a rule**: No ambiguous orderings
- ✅ **Complete transitivity**: Elements can bubble through all positions
- ✅ **Guaranteed termination**: Total ordering ensures unique correct solution
- ✅ **No partial ordering issues**: Unlike minimal examples, full rule coverage exists

### Comparison with Minimal Example
**Our test case**: `rule(1,3)` with `[3,2,6,7,1]` failed because:
- ❌ Only 1 rule out of 10 possible pairs
- ❌ 1 couldn't bubble past 2,6,7 (no rules)
- ❌ Partial ordering insufficient for sorting

**AOC input**: Complete success because:
- ✅ 1,176 rules out of 1,176 possible pairs  
- ✅ Every element can bubble past every other element
- ✅ Total ordering ensures unique correct solution

### Educational Value
This demonstrates why **rule completeness** is crucial for custom sorting algorithms:
1. **Partial rules** → **sorting failure** (our simple example)
2. **Complete rules** → **sorting success** (AOC input)
3. **Bubble sort works perfectly** when comparison function is well-defined for all pairs

The beginner-friendly bubble sort approach is not just pedagogically sound—it's **mathematically guaranteed** to work for this specific problem! 🎯