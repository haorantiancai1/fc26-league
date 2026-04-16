import sys
with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8-sig') as f:
    html = f.read()
lines = html.split('\n')
start = None
for i, line in enumerate(lines):
    if 'function initFirebaseSync()' in line:
        start = i
        break
print(f'initFirebaseSync starts at line {start+1}')
depth = 0
neg = 0
for i in range(start, len(lines)):
    line = lines[i]
    in_str = False
    sc = None
    for c in line:
        if in_str:
            if c == sc: in_str = False
        elif c in "'\"":
            in_str = True; sc = c
        elif c in '({[': depth += 1
        elif c in ')}]': depth -= 1
    if depth < 0: neg += 1
print(f'Final depth: {depth}, negative dips: {neg}')
if depth == 0 and neg == 0:
    print('BRACKET BALANCE: OK!')
else:
    print('BRACKET BALANCE: ISSUES DETECTED')
