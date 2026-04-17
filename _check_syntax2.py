import sys

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()
lines = html.split('\n')

# Check depth line by line from 12156 to 12195
depth = 0
for i in range(12155, 12195):
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
    print(f"  {i+1:5d}  depth {prev:3d} -> {depth:3d}  (delta {opens-closes:+d})  {line.rstrip()[:100]}")
