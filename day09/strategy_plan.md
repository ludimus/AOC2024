# Day 9: Disk Fragmenter - Strategy Plan

## Problem Analysis
**Part 1:** Move individual file blocks from the end to fill gaps at the beginning.
**Part 2:** Move whole files (not individual blocks) to leftmost free space that can fit the entire file.

## Input Format
- Single line of digits representing alternating file lengths and free space lengths
- Example: `2333133121414131402`
- Even positions (0,2,4...): file block lengths
- Odd positions (1,3,5...): free space lengths

## Data Structures

### 1. Disk Representation
Use a list to represent the disk with individual blocks:
- File blocks: represented by file ID (0, 1, 2, ...)
- Free space: represented by '.' or None

### 2. File Metadata
Track file information:
- File ID (starting from 0)
- Size (number of blocks)
- Current position on disk

## Algorithm Steps

### Phase 1: Parse Input and Build Disk
1. Read the dense format string
2. Parse alternating file/free space lengths
3. Build initial disk representation with file IDs and free spaces
4. Assign file IDs based on order (0, 1, 2, ...)

### Phase 2: Defragmentation
1. Identify rightmost file block
2. Find leftmost free space
3. Move file block to free space
4. Repeat until no gaps exist between file blocks

### Phase 3: Calculate Checksum
- Multiply each block's position by its file ID
- Sum all results
- Skip free space blocks

## Functions Needed

1. `parse_input(filename)` - Parse disk map and return disk representation
2. `build_disk(disk_map)` - Convert dense format to block representation  
3. `defragment_disk(disk)` - Perform the moving operation
4. `calculate_checksum(disk)` - Calculate final filesystem checksum
5. `main()` - Orchestrate the solution with test/debug modes

## Expected Output
For example input `2333133121414131402`:

**Part 1 (individual blocks):**
- Initial: `00...111...2...333.44.5555.6666.777.888899`
- Final: `0099811188827773336446555566..............`
- Checksum: 1928

**Part 2 (whole files):**
- Initial: `00...111...2...333.44.5555.6666.777.888899`
- Final: `00992111777.44.333....5555.6666.....8888..`
- Checksum: 2858

## Part 2 Specific Algorithm

### Key Differences from Part 1:
1. **Move whole files** instead of individual blocks
2. **Process files in decreasing ID order** (highest ID first)
3. **Each file attempts to move exactly once**
4. **Must find contiguous free space** large enough for entire file
5. **Files only move to the left** of their current position

### Part 2 Data Structures:
- **File tracking**: Store file ID, size, and current start position
- **Free space tracking**: Track contiguous free space spans with start position and size

### Part 2 Algorithm Steps:
1. Parse input and build initial disk representation
2. **Identify all files** with their positions and sizes
3. **Process files in reverse ID order** (9, 8, 7, ..., 1, 0)
4. For each file:
   - Find leftmost free space span that can fit the file
   - If found and to the left of current position, move entire file
   - Update free space tracking
5. Calculate checksum

### Part 2 Functions Needed:
1. `find_files(disk)` - Identify all files with positions and sizes
2. `find_free_spans(disk)` - Find all contiguous free space spans
3. `move_whole_file(disk, file_info, target_pos)` - Move entire file
4. `defragment_whole_files(disk)` - Main Part 2 algorithm

## Implementation Notes
- Support command line switches for test mode and debug mode
- Test mode uses example.txt, normal mode uses input.txt
- Debug mode prints intermediate states
- Part 2 requires different defragmentation strategy than Part 1

## Performance Optimizations

### Part 1 Optimization: Pointer Tracking
**Problem**: Original algorithm rescanned entire disk for each block movement (O(n²))
**Solution**: Track left_free_ptr and right_file_ptr, move incrementally (O(n))
**Results**: 38.25s → 0.053s (**722x speedup**)

### Part 2 Optimization: Pre-computed Free Spans
**Problem**: Called find_free_spans() for each file, scanning entire disk repeatedly
**Solution**: 
1. Build free spans list during disk construction
2. Maintain spans incrementally with updates after file moves
3. Merge adjacent spans to keep list compact
**Results**: 53.22s → 6.28s (**8.5x speedup**)

## Final Results
- **Part 1**: Checksum 6359213660505 (0.053s)
- **Part 2**: Checksum 6381624803796 (6.28s)
- **Example Part 1**: 1928 ✓
- **Example Part 2**: 2858 ✓

## Key Algorithmic Insights
1. **Avoid repeated scanning**: Pre-compute data structures when possible
2. **Incremental updates**: Maintain state rather than rebuilding
3. **Pointer tracking**: Move through data structures systematically
4. **Data structure choice**: Lists of spans vs. full disk representation for searches