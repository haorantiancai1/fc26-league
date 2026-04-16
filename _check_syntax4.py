import sys

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()
lines = html.split('\n')

# Find initFirebaseSync function
start = None
for i, line in enumerate(lines):
    if 'function initFirebaseSync()' in line:
        start = i
        break

print(f"initFirebaseSync starts at line {start+1}")

depth = 0
neg_lines = []
for i in range(start, min(start + 200, len(lines))):
    line = lines[i]
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
        elif c in '({[':
            opens += 1
        elif c in ')}]':
            closes += 1
    prev = depth
    depth += opens - closes
    if depth < 0:
        neg_lines.append((i+1, prev, depth, line.rstrip()))
        if len(neg_lines) <= 5:
            print(f"  {i+1:5d}  depth {prev:3d} -> {depth:3d}  {line.rstrip()[:120]}")

# Check if function ends properly - look for depth returning to 0
print(f"\nFinal depth: {depth}")
print(f"Total negative depth occurrences: {len(neg_lines)}")
if depth == 0 and not neg_lines:
    print("BRACKET BALANCE: OK!")
elif depth == 0:
    print(f"BRACKET BALANCE: depth returns to 0 but had {len(neg_lines)} negative dips (likely OK)")
else:
    print(f"BRACKET BALANCE: BROKEN (depth={depth})")
