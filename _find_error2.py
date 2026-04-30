import sys, re, subprocess
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract main inline script
blocks = list(re.finditer(r'<script>(.*?)</script>', html, re.DOTALL))
main_script = max(blocks, key=lambda m: len(m.group(1))).group(1)

node = r'C:\Program Files\nodejs\node.exe'
fname = r'E:\FC26传奇联赛\deploy\_tmp_main.js'
with open(fname, 'w', encoding='utf-8') as f:
    f.write(main_script)

# Binary search for the error line
lines = main_script.split('\n')
total = len(lines)
print(f'Total lines: {total}')

lo, hi = 0, total
while hi - lo > 10:
    mid = (lo + hi) // 2
    chunk = '\n'.join(lines[:mid])
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(chunk)
    result = subprocess.run([node, '--check', fname], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode != 0:
        hi = mid
    else:
        lo = mid
    print(f'  Range: {lo}-{hi}')

# Show the problematic area
print(f'\nError is around lines {lo}-{hi}:')
for i in range(max(0, lo-2), min(total, hi+2)):
    print(f'  {i}: {lines[i][:200]}')
