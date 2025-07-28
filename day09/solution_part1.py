#!/usr/bin/env python3
import sys

def parse_input(filename):
    """Parse the disk map from input file and return the dense format string."""
    with open(filename, 'r') as f:
        return f.read().strip()

def build_disk(disk_map):
    """Convert dense format to block representation with file IDs and free spaces."""
    disk = []
    file_id = 0
    
    for i, length in enumerate(disk_map):
        length = int(length)
        if i % 2 == 0:  # Even index = file
            disk.extend([file_id] * length)
            file_id += 1
        else:  # Odd index = free space
            disk.extend(['.'] * length)
    
    return disk

def defragment_disk(disk, debug=False):
    """Perform defragmentation by moving file blocks from end to leftmost free space."""
    disk = disk.copy()  # Don't modify original
    
    if debug:
        print(f"Initial: {''.join(str(x) for x in disk)}")
    
    # Initialize pointers - find initial positions
    left_free_ptr = 0
    right_file_ptr = len(disk) - 1
    
    # Find first free space from left
    while left_free_ptr < len(disk) and disk[left_free_ptr] != '.':
        left_free_ptr += 1
    
    # Find first file block from right
    while right_file_ptr >= 0 and disk[right_file_ptr] == '.':
        right_file_ptr -= 1
    
    # Main defragmentation loop
    while left_free_ptr < right_file_ptr:
        # Move the block
        disk[left_free_ptr] = disk[right_file_ptr]
        disk[right_file_ptr] = '.'
        
        if debug:
            print(f"Step:    {''.join(str(x) for x in disk)}")
        
        # Update left pointer - find next free space
        while left_free_ptr < len(disk) and disk[left_free_ptr] != '.':
            left_free_ptr += 1
        
        # Update right pointer - find next file block
        while right_file_ptr >= 0 and disk[right_file_ptr] == '.':
            right_file_ptr -= 1
        
        # Check if we're done
        if left_free_ptr >= right_file_ptr:
            break
    
    if debug:
        print(f"Final:   {''.join(str(x) for x in disk)}")
    
    return disk

def calculate_checksum(disk):
    """Calculate filesystem checksum by multiplying position by file ID."""
    checksum = 0
    for position, block in enumerate(disk):
        if block != '.':
            checksum += position * block
    return checksum

def main():
    """Main function with command line argument support."""
    test_mode = '--test' in sys.argv or '-t' in sys.argv
    debug_mode = '--debug' in sys.argv or '-d' in sys.argv
    
    filename = 'example.txt' if test_mode else 'input.txt'
    
    if debug_mode:
        print(f"Running in {'test' if test_mode else 'normal'} mode with debug enabled")
        print(f"Reading from: {filename}")
    
    # Parse input and build disk
    disk_map = parse_input(filename)
    if debug_mode:
        print(f"Disk map: {disk_map}")
    
    disk = build_disk(disk_map)
    if debug_mode:
        print(f"Initial disk size: {len(disk)} blocks")
    
    # Defragment
    defragmented_disk = defragment_disk(disk, debug_mode)
    
    # Calculate checksum
    checksum = calculate_checksum(defragmented_disk)
    
    print(f"Filesystem checksum: {checksum}")

if __name__ == "__main__":
    main()