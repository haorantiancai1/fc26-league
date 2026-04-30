import json, sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('TEAMS_DATA')
arr_start = html.find('[', idx)
depth = 0
arr_end = -1
for i in range(arr_start, min(arr_start + 500000, len(html))):
    if html[i] == '[': depth += 1
    elif html[i] == ']':
        depth -= 1
        if depth == 0: arr_end = i; break

teams = json.loads(html[arr_start:arr_end+1])

# Find all players named 席尔瓦
print('All players with 席尔瓦 in name:')
for t in teams:
    for p in t['players']:
        if '席尔瓦' in p['name']:
            print(f'  {t["team"]}: {p["name"]} ({p.get("position","")}) OVR={p.get("overall","")}')
