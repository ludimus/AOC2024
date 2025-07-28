#!/usr/bin/env python3
import sys

def parse_input(filename):
    """Parse the disk map from input file and return the dense format string."""
    with open(filename, 'r') as f:
        return f.read().strip()

def build_disk(disk_map):
    """Convert dense format to block representation and track free space spans."""
    disk = []
    free_spans = []
    file_id = 0
    
    for i, length in enumerate(disk_map):
        length = int(length)
        if i % 2 == 0:  # Even index = file
            disk.extend([file_id] * length)
            file_id += 1
        else:  # Odd index = free space
            if length > 0:  # Only add non-empty spans
                free_spans.append({
                    'start': len(disk),
                    'size': length
                })
            disk.extend(['.'] * length)
    
    return disk, free_spans

def find_files(disk):
    """Identify all files with their ID, start position, and size."""
    files = {}
    current_file_id = None
    current_start = None
    current_size = 0
    
    for i, block in enumerate(disk):
        if block != '.':
            if block != current_file_id:
                # Save previous file if exists
                if current_file_id is not None:
                    files[current_file_id] = {
                        'start': current_start,
                        'size': current_size
                    }
                # Start new file
                current_file_id = block
                current_start = i
                current_size = 1
            else:
                current_size += 1
        else:
            # End of file
            if current_file_id is not None:
                files[current_file_id] = {
                    'start': current_start,
                    'size': current_size
                }
                current_file_id = None
    
    # Handle last file if disk doesn't end with free space
    if current_file_id is not None:
        files[current_file_id] = {
            'start': current_start,
            'size': current_size
        }
    
    return files

def find_free_spans(disk):
    """Find all contiguous free space spans with start position and size."""
    spans = []
    current_start = None
    current_size = 0
    
    for i, block in enumerate(disk):
        if block == '.':
            if current_start is None:
                current_start = i
                current_size = 1
            else:
                current_size += 1
        else:
            # End of free space
            if current_start is not None:
                spans.append({
                    'start': current_start,
                    'size': current_size
                })
                current_start = None
                current_size = 0
    
    # Handle last span if disk ends with free space
    if current_start is not None:
        spans.append({
            'start': current_start,
            'size': current_size
        })
    
    return spans

def move_whole_file(disk, file_id, file_info, target_start):
    """Move entire file to target position."""
    # Clear original position
    for i in range(file_info['start'], file_info['start'] + file_info['size']):
        disk[i] = '.'
    
    # Place at new position
    for i in range(target_start, target_start + file_info['size']):
        disk[i] = file_id

def update_free_spans_after_move(free_spans, used_span_idx, file_size, target_start, original_start, original_size):
    """Update free spans list after a file is moved."""
    # Remove or shrink the used span
    used_span = free_spans[used_span_idx]
    if used_span['size'] == file_size:
        # Entire span used, remove it
        free_spans.pop(used_span_idx)
    else:
        # Partial span used, shrink it
        free_spans[used_span_idx] = {
            'start': target_start + file_size,
            'size': used_span['size'] - file_size
        }
    
    # Add new free space where the file originally was
    new_free_span = {
        'start': original_start,
        'size': original_size
    }
    
    # Insert in sorted order by start position
    inserted = False
    for i, span in enumerate(free_spans):
        if span['start'] > new_free_span['start']:
            free_spans.insert(i, new_free_span)
            inserted = True
            break
    if not inserted:
        free_spans.append(new_free_span)
    
    # Merge adjacent free spans
    merge_adjacent_spans(free_spans)

def merge_adjacent_spans(free_spans):
    """Merge adjacent free space spans."""
    if len(free_spans) <= 1:
        return
    
    # Sort by start position
    free_spans.sort(key=lambda x: x['start'])
    
    i = 0
    while i < len(free_spans) - 1:
        current = free_spans[i]
        next_span = free_spans[i + 1]
        
        # Check if spans are adjacent
        if current['start'] + current['size'] == next_span['start']:
            # Merge spans
            free_spans[i] = {
                'start': current['start'],
                'size': current['size'] + next_span['size']
            }
            free_spans.pop(i + 1)
        else:
            i += 1

def defragment_whole_files(disk, free_spans, debug=False):
    """Perform whole-file defragmentation by processing files in decreasing ID order."""
    disk = disk.copy()  # Don't modify original
    free_spans = [span.copy() for span in free_spans]  # Don't modify original
    
    if debug:
        print(f"Initial: {''.join(str(x) for x in disk)}")
        print(f"Initial free spans: {free_spans}")
    
    # Find all files
    files = find_files(disk)
    if debug:
        print(f"Found {len(files)} files: {dict(sorted(files.items()))}")
    
    # Process files in decreasing ID order
    for file_id in sorted(files.keys(), reverse=True):
        file_info = files[file_id]
        
        if debug:
            print(f"Processing file {file_id} (size {file_info['size']}, pos {file_info['start']})")
        
        # Find first suitable free span (already sorted by position during construction)
        target_span_idx = None
        for i, span in enumerate(free_spans):
            # Must be large enough and to the left of current position
            if span['size'] >= file_info['size'] and span['start'] < file_info['start']:
                target_span_idx = i
                break
        
        if target_span_idx is not None:
            target_span = free_spans[target_span_idx]
            if debug:
                print(f"  Moving to position {target_span['start']}")
            
            # Move the file
            move_whole_file(disk, file_id, file_info, target_span['start'])
            
            # Update free spans
            update_free_spans_after_move(
                free_spans, target_span_idx, file_info['size'], 
                target_span['start'], file_info['start'], file_info['size']
            )
            
            # Update file info for potential debug output
            files[file_id]['start'] = target_span['start']
            
            if debug:
                print(f"  Updated free spans: {free_spans}")
        else:
            if debug:
                print(f"  No suitable free space found")
        
        if debug:
            print(f"  Result: {''.join(str(x) for x in disk)}")
    
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
    
    disk, free_spans = build_disk(disk_map)
    if debug_mode:
        print(f"Initial disk size: {len(disk)} blocks")
        print(f"Initial free spans: {len(free_spans)} spans")
    
    # Defragment using whole-file method
    defragmented_disk = defragment_whole_files(disk, free_spans, debug_mode)
    
    # Calculate checksum
    checksum = calculate_checksum(defragmented_disk)
    
    print(f"Filesystem checksum: {checksum}")

if __name__ == "__main__":
    main()