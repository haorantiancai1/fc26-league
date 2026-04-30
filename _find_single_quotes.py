import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('TEAMS_DATA = [')
arr_start = html.find('[', idx)
depth = 0
arr_end = -1
for i in range(arr_start, min(arr_start + 500000, len(html))):
    if html[i] == '[': depth += 1
    elif html[i] == ']':
        depth -= 1
        if depth == 0: arr_end = i; break

teams_json = html[arr_start:arr_end+1]

# Find all single quotes with context
for i, ch in enumerate(teams_json):
    if ch == "'":
        start = max(0, i-30)
        end = min(len(teams_json), i+30)
        line_num = teams_json[:i].count('\n') + 1
        print(f'Line {line_num}, pos {i}: ...{teams_json[start:end]}...')
