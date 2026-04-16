import sys
import re

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()
lines = html.split('\n')

# Find _fbListen('playerMoves'
start = None
for i, line in enumerate(lines):
    if "_fbListen('playerMoves" in line:
        start = i
        break

if start is None:
    print("NOT FOUND")
    sys.exit(1)

print(f"playerMoves _fbListen starts at line {start+1}")

# Track bracket depth from that line to line 12250
depth = 0
for i in range(start, min(12250, len(lines))):
    line = lines[i]
    # Simple approach: count non-string parens
    in_str = False
    str_char = None
    opens = 0
    closes = 0
    for c in line:
        if in_str:
            if c == str_char:
                in_str = False
        elif c in ("'", '"'):
            in_str = True
            str_char = c
        elif c == '/' and i < len(lines) - 1:
            pass  # skip simple comment detection for now
        elif c in '({[':
            opens += 1
        elif c in ')}]':
            closes += 1
    prev = depth
    depth += opens - closes
    if depth < 0:
        print(f"NEGATIVE DEPTH at line {i+1}: depth went from {prev} to {depth}")
        print(f"  {line.rstrip()}")

print(f"Final bracket depth at line 12250: {depth}")
