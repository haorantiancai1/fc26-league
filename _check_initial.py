import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
main_js = max(scripts, key=len)

start_marker = 'TEAMS_DATA = ['
start_idx = main_js.find(start_marker)
depth = 0
end_idx = start_idx + len(start_marker) - 1
for i in range(start_idx + len(start_marker) - 1, len(main_js)):
    if main_js[i] == '[':
        depth += 1
    elif main_js[i] == ']':
        depth -= 1
        if depth == 0:
            end_idx = i + 1
            break

teams_json = main_js[start_idx + len('TEAMS_DATA = '):end_idx]
teams = json.loads(teams_json)

# Count initial players in each of the 4 teams
for name in ['切尔西', '利物浦', '曼彻斯特城', '曼彻斯特联']:
    team = next((t for t in teams if t['team'] == name), None)
    if team:
        players = team.get('players', [])
        print(f'{name}: {len(players)} players (initial)')
        for p in players:
            print(f'  {p["name"]}')

# Also check 传奇 teams
print('\n传奇球队:')
for t in teams:
    if '传奇' in t['team']:
        players = t.get('players', [])
        has_transfer = any(p['name'] in ['梅西','贝克汉姆','维埃拉'] for p in players)
        if has_transfer:
            print(f'{t["team"]}: {len(players)} players')
            for p in players:
                print(f'  {p["name"]}')
