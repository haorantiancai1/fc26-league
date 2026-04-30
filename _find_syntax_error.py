import re, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract main script (the largest one)
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
main_js = max(scripts, key=len)
lines = main_js.split('\n')
print(f'Main script: {len(lines)} lines')

# Binary search for syntax error - but this time we add "var firebase = {};" at the top
# to avoid ReferenceError on firebase.initializeApp
prefix = "var firebase = {initializeApp: function(){}, database: function(){return {ref: function(){return {set:function(){},on:function(){}};}};}};\n"

total = len(lines)
lo, hi = 1, total

# Check if the prefix makes the full script valid
with open(r'E:\FC26传奇联赛\deploy\_tmp_test.js', 'w', encoding='utf-8') as f:
    f.write(prefix + main_js)
result = subprocess.run(
    ['C:\\Program Files\\nodejs\\node.exe', '--check', r'E:\FC26传奇联赛\deploy\_tmp_test.js'],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
print(f'Full script with firebase stub: {result.returncode}')
if result.stderr:
    print(f'Error: {result.stderr[:300]}')
