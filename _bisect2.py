import subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\_tmp_full.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

total = len(lines)
print(f'Total lines: {total}')

def check_syntax(lines_subset):
    """Check if given lines have syntax errors by wrapping in a function"""
    code = ''.join(lines_subset)
    with open(r'E:\FC26传奇联赛\deploy\_tmp_half.js', 'w', encoding='utf-8') as f:
        f.write(code)
    result = subprocess.run(
        ['C:\\Program Files\\nodejs\\node.exe', '--check', r'E:\FC26传奇联赛\deploy\_tmp_half.js'],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    return result.returncode == 0

# Better binary search: only report error when the code up to line N is 
# NOT valid (not just truncated mid-statement)
lo, hi = 1, total
found = False

# First pass: find where syntax first breaks
# Try each chunk of 100 lines
chunk_size = 100
for start in range(0, total, chunk_size):
    end = min(start + chunk_size, total)
    ok = check_syntax(lines[:end])
    if not ok:
        # Error is somewhere in [start, end)
        print(f'Syntax error in lines {start+1}-{end}')
        # Binary search within this chunk
        clo, chi = start, end
        while clo < chi:
            cmid = (clo + chi) // 2
            cok = check_syntax(lines[:cmid])
            if cok:
                clo = cmid + 1
            else:
                chi = cmid
        print(f'First error at line: {clo+1}')
        # Show context
        for i in range(max(0, clo-3), min(total, clo+8)):
            marker = '>>>' if i == clo else '   '
            print(f'{marker} {i+1:5d}: {lines[i].rstrip()[:150]}')
        found = True
        break

if not found:
    print('No syntax error found in any chunk!')
