import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'E:\FC26传奇联赛\deploy\_tmp_full.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[:80], 1):
    print(f'{i:5d}: {line.rstrip()[:150]}')
