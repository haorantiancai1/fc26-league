import subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\_tmp_full.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

total = len(lines)
print(f'Total lines: {total}')

# Binary search for the error line
lo, hi = 1, total
while lo < hi:
    mid = (lo + hi) // 2
    # Write first `mid` lines
    with open(r'E:\FC26传奇联赛\deploy\_tmp_half.js', 'w', encoding='utf-8') as f:
        # Add closing to make it valid
        f.write(''.join(lines[:mid]))
    
    result = subprocess.run(
        ['C:\\Program Files\\nodejs\\node.exe', '--check', r'E:\FC26传奇联赛\deploy\_tmp_half.js'],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    
    if result.returncode == 0:
        # Error is after mid
        lo = mid + 1
    else:
        # Error is at or before mid
        hi = mid

print(f'First error around line: {lo}')
# Show context
for i in range(max(0, lo-5), min(total, lo+5)):
    marker = '>>>' if i == lo-1 else '   '
    print(f'{marker} {i+1}: {lines[i].rstrip()[:120]}')
