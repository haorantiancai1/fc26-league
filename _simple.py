import re
with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()
lines = html.split('\n')
depth = 0
neg = 0
for i, line in enumerate(lines):
    in_str = False
    sc = None
    for c in line:
        if in_str:
            if c == sc:
                in_str = False
        elif c == '/' and i < len(lines):
            pass
        elif c in "'\"":
            in_str = True
            sc = c
        elif c in '({[':
            depth += 1
        elif c in ')}]':
            depth -= 1
    if depth < 0:
        neg += 1
        if neg <= 5:
            print("Neg depth line %d: %d" % (i+1, depth))
print("Final depth: %d, neg dips: %d" % (depth, neg))
