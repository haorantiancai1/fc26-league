import re, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the main script block (the big one)
# Find all script blocks
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f'Total script blocks: {len(scripts)}')

# Find the main one (largest)
main_idx = max(range(len(scripts)), key=lambda i: len(scripts[i]))
main_js = scripts[main_idx]
print(f'Main script: block {main_idx}, size: {len(main_js)} chars')

# Write it to a temp file for Node to check
with open(r'E:\FC26传奇联赛\deploy\_tmp_full.js', 'w', encoding='utf-8') as f:
    f.write(main_js)

# Now run Node --check
result = subprocess.run(
    ['C:\\Program Files\\nodejs\\node.exe', '--check', r'E:\FC26传奇联赛\deploy\_tmp_full.js'],
    capture_output=True, text=True
)
print('STDOUT:', result.stdout)
print('STDERR:', result.stderr)
print('Return code:', result.returncode)
