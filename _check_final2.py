import re

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()
lines = html.split('\n')

# Smarter bracket counter that skips strings and single-line comments
def count_brackets(line):
    opens = 0
    closes = 0
    in_str = False
    sc = None
    i = 0
    while i < len(line):
        c = line[i]
        if in_str:
            if c == '\\':
                i += 1  # skip escaped char
            elif c == sc:
                in_str = False
        elif c == '/' and i + 1 < len(line) and line[i+1] == '/':
            break  # rest is comment
        elif c in "'\"":
            in_str = True
            sc = c
        elif c in '({[':
            opens += 1
        elif c in ')}]':
            closes += 1
        i += 1
    return opens, closes

# Find initFirebaseSync and check to its closing
start = None
for i, line in enumerate(lines):
    if 'function initFirebaseSync()' in line:
        start = i
        break

depth = 0
func_depth_start = 0
for i in range(start, len(lines)):
    line = lines[i]
    o, c = count_brackets(line)
    prev = depth
    depth += o - c
    if depth < 0 and depth == -1 and prev == 0 and '}'
 not in line[:line.find('function')+1 if 'function' in line else 0]:
        pass
    # Check if function closes (depth returns to what it was before function def)
    if i == start:
        func_depth_start = depth  # after the function line
    if depth == func_depth_start - 2 and i > start + 5:
        print(f"Function likely closes at line {i+1}")
        print(f"  {line.rstrip()[:120]}")
        break

print(f"\nStarting from initFirebaseSync (line {start+1}):")
for i in range(start, start + 200):
    line = lines[i]
    o, c = count_brackets(line)
    prev = depth
    depth += o - c
    if o != c or depth <= 0:
        print(f"  {i+1:5d}  d{prev:3d}->{depth:3d} ({o:+d}o/{c:+d}c)  {line.rstrip()[:110]}")
    if depth == func_depth_start - 2 and i > start + 5:
        break

# Full file check
depth = 0
neg_count = 0
for i in range(len(lines)):
    o, c = count_brackets(lines[i])
    prev = depth
    depth += o - c
    if depth < 0:
        neg_count += 1
        if neg_count <= 3:
            print(f"\nNegative depth at line {i+1}: {prev}->{depth}")
            print(f"  {lines[i].rstrip()[:120]}")

print(f"\nFinal file depth: {depth}, total negative dips: {neg_count}")
