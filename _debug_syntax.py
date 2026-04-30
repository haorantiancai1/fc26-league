import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the main script
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
main_js = max(scripts, key=len)

# Find ALL regex literals in the JS - unbalanced parens in regex can cause this error
# Pattern: /.../ - but need to be careful about division operators
# Strategy: look for regex that contains ( without matching )
lines = main_js.split('\n')
print(f'Total lines: {len(lines)}')

# Check for suspicious patterns that could cause "missing ) after argument list"
# This error typically happens when JS parser encounters something like:
# func(arg   <-- missing closing paren
# OR a regex like /foo(bar/ which is interpreted as division + function call

import re as re_mod

for i, line in enumerate(lines):
    # Look for division followed by ( that might be misinterpreted
    # Look for patterns like: ) /something(  which could be confused
    stripped = line.strip()
    # Skip comments
    if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
        continue
    # Check for regex-like patterns
    # This is a heuristic - look for / that's not a division
    # Key pattern: if we see /[something]/g or similar but the regex contains unbalanced parens

    # Check for template literals with issues
    if '`' in stripped:
        # Count backticks
        bt_count = stripped.count('`')
        if bt_count % 2 != 0:
            print(f'Line {i+1}: UNBALANCED BACKTICKS: {stripped[:100]}')

    # Check for parentheses in strings that might confuse parser
    # Actually, let's look for something different:
    # "missing ) after argument list" often comes from a line like:
    # someFunc(arg1, arg2   <-- forgot closing paren
    # Let's count parens per line and track balance
