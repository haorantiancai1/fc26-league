import re, subprocess, sys, os

sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the main script block (the big one)
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f'Total script blocks: {len(scripts)}')

main_idx = max(range(len(scripts)), key=lambda i: len(scripts[i]))
main_js = scripts[main_idx]
print(f'Main script: block {main_idx}, size: {len(main_js)} chars')

with open(r'E:\FC26传奇联赛\deploy\_tmp_full.js', 'w', encoding='utf-8') as f:
    f.write(main_js)

# Run Node --check with UTF-8 env
env = os.environ.copy()
env['NODE_OPTIONS'] = ''
result = subprocess.run(
    ['C:\\Program Files\\nodejs\\node.exe', '--check', r'E:\FC26传奇联赛\deploy\_tmp_full.js'],
    capture_output=True,
    encoding='utf-8',
    errors='replace',
    env=env
)
print('STDOUT:', result.stdout)
print('STDERR:', result.stderr)
print('Return code:', result.returncode)
