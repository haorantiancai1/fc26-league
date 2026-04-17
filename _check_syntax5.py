import sys

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()
lines = html.split('\n')

# Check the entire file's bracket balance, focusing on the main script
# Find the big script block
start = None
for i, line in enumerate(lines):
    if 'function initFirebaseSync()' in line:
        start = i
        break

print(f"initFirebaseSync starts at line {start+1}")

depth = 0
for i in range(start, len(lines)):
    line = lines[i]
    in_str = False
    str_char = None
    in_line_comment = False
    opens = 0
    closes = 0
    j = 0
    while j < len(line):
        c = line[j]
        if in_str:
            if c == str_char:
                in_str = False
        elif in_line_comment:
            pass  # ignore rest of line
        elif c == '/' and j + 1 < len(line) and line[j+1] == '/':
            in_line_comment = True
        elif c in ("'", '"'):
            in_str = True
            str_char = c
        elif c in '({[':
            opens += 1
        elif c in ')}]':
            closes += 1
        j += 1
    prev = depth
    depth += opens - closes
    
    # Only print when depth changes significantly
    if abs(opens - closes) > 0:
        status = ""
        if depth == 0 and i > start + 5:
            print(f"  >>> DEPTH RETURNS TO 0 at line {i+1}")
        print(f"  {i+1:5d}  d{prev:3d}->{depth:3d}  {line.rstrip()[:110]}")
