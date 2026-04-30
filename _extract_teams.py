import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the try-catch block containing TEAMS_DATA
# Find "try {" before TEAMS_DATA
idx = html.find('TEAMS_DATA = [')
try_start = html.rfind('try {', max(0, idx - 100), idx)
if try_start < 0:
    print('try block not found before TEAMS_DATA')
    sys.exit(1)

# Find matching catch
# Find the end - look for "} catch(e) {"
catch_start = html.find('} catch(e) {', idx)
if catch_start < 0:
    print('catch block not found after TEAMS_DATA')
    sys.exit(1)

# Find the end of catch block
catch_end = html.find('}', catch_start + 13)
catch_end = html.find('\n', catch_end) + 1  # include newline after closing }

block = html[try_start:catch_end]
print(f'Extracted block: {len(block)} chars')

with open(r'E:\FC26传奇联赛\deploy\_tmp_teams_block.js', 'w', encoding='utf-8') as f:
    f.write(block)

print('Written to _tmp_teams_block.js')
