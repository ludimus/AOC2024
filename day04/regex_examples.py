#!/usr/bin/env python3
"""
Simple examples of regex capture groups in Python 3
"""

import re

def basic_capture_groups():
    """Basic capture group examples"""
    print("=== BASIC CAPTURE GROUPS ===")
    
    # Simple capture group - extract part of match
    text = "My phone is 123-456-7890"
    pattern = r"(\d{3})-(\d{3})-(\d{4})"
    match = re.search(pattern, text)
    
    if match:
        print(f"Full match: {match.group(0)}")  # Full match
        print(f"Area code: {match.group(1)}")   # First group
        print(f"Exchange: {match.group(2)}")    # Second group  
        print(f"Number: {match.group(3)}")      # Third group
        print(f"All groups: {match.groups()}")  # Tuple of all groups
    
    print()

def named_capture_groups():
    """Named capture groups for clarity"""
    print("=== NAMED CAPTURE GROUPS ===")
    
    text = "John Doe, age 25"
    pattern = r"(?P<first>\w+) (?P<last>\w+), age (?P<age>\d+)"
    match = re.search(pattern, text)
    
    if match:
        print(f"First name: {match.group('first')}")
        print(f"Last name: {match.group('last')}")
        print(f"Age: {match.group('age')}")
        print(f"Dict: {match.groupdict()}")
    
    print()

def email_extraction():
    """Extract parts of email addresses"""
    print("=== EMAIL EXTRACTION ===")
    
    emails = [
        "john.doe@example.com",
        "admin@test.org", 
        "user123@gmail.co.uk"
    ]
    
    pattern = r"([^@]+)@([^.]+)\.(.+)"
    
    for email in emails:
        match = re.search(pattern, email)
        if match:
            username, domain, tld = match.groups()
            print(f"{email} -> user: {username}, domain: {domain}, tld: {tld}")
    
    print()

def find_all_with_groups():
    """Using findall with capture groups"""
    print("=== FINDALL WITH GROUPS ===")
    
    text = "Items: apple $2.50, banana $1.00, orange $3.25"
    pattern = r"(\w+) \$(\d+\.\d{2})"
    
    matches = re.findall(pattern, text)
    print("Found items:")
    for item, price in matches:
        print(f"  {item}: ${price}")
    
    print()

def date_parsing():
    """Parse different date formats"""
    print("=== DATE PARSING ===")
    
    dates = [
        "2024-01-15",
        "01/15/2024", 
        "Jan 15, 2024"
    ]
    
    patterns = [
        r"(\d{4})-(\d{2})-(\d{2})",           # YYYY-MM-DD
        r"(\d{2})/(\d{2})/(\d{4})",           # MM/DD/YYYY
        r"(\w{3}) (\d{1,2}), (\d{4})"         # Mon DD, YYYY
    ]
    
    for date in dates:
        for pattern in patterns:
            match = re.search(pattern, date)
            if match:
                print(f"{date} -> {match.groups()}")
                break
    
    print()

def substitution_with_groups():
    """Using capture groups in substitutions"""
    print("=== SUBSTITUTION WITH GROUPS ===")
    
    # Swap first and last names
    names = ["John Doe", "Jane Smith", "Bob Wilson"]
    pattern = r"(\w+) (\w+)"
    
    for name in names:
        swapped = re.sub(pattern, r"\2, \1", name)
        print(f"{name} -> {swapped}")
    
    print()
    
    # Format phone numbers
    phones = ["1234567890", "5551234567"]
    pattern = r"(\d{3})(\d{3})(\d{4})"
    
    for phone in phones:
        formatted = re.sub(pattern, r"(\1) \2-\3", phone)
        print(f"{phone} -> {formatted}")
    
    print()

def optional_groups():
    """Optional capture groups"""
    print("=== OPTIONAL GROUPS ===")
    
    urls = [
        "https://example.com",
        "http://test.org:8080",
        "ftp://files.com"
    ]
    
    pattern = r"(https?|ftp)://([^:]+)(?::(\d+))?"
    
    for url in urls:
        match = re.search(pattern, url)
        if match:
            protocol, host, port = match.groups()
            port = port or "default"
            print(f"{url} -> protocol: {protocol}, host: {host}, port: {port}")
    
    print()

def non_capturing_groups():
    """Non-capturing groups (don't create capture groups)"""
    print("=== NON-CAPTURING GROUPS ===")
    
    text = "Colors: red, blue, green"
    
    # With capturing groups
    pattern1 = r"(red|blue|green)"
    matches1 = re.findall(pattern1, text)
    print(f"With capturing: {matches1}")
    
    # With non-capturing groups  
    pattern2 = r"(?:red|blue|green)"
    matches2 = re.findall(pattern2, text)
    print(f"Non-capturing: {matches2}")
    
    print()

def main():
    basic_capture_groups()
    named_capture_groups()
    email_extraction()
    find_all_with_groups()
    date_parsing()
    substitution_with_groups()
    optional_groups()
    non_capturing_groups()

if __name__ == "__main__":
    main()