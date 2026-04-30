import urllib.request, json, sys, re

sys.stdout.reconfigure(encoding='utf-8')

# 1. Read playerMoves from Firebase
base = 'https://fc26-league-47ef8-default-rtdb.asia-southeast1.firebasedatabase.app'
r = urllib.request.urlopen(base + '/playerMoves.json', timeout=10)
moves = json.loads(r.read().decode('utf-8'))
print(f'Loaded {len(moves)} playerMoves from Firebase')

# 2. Read TEAMS_DATA from local index.html
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
        if depth == 0:
            arr_end = i
            break

teams = json.loads(html[arr_start:arr_end+1])
print(f'Parsed {len(teams)} teams')

# 3. Build team name alias map
team_alias = {
    '曼联': '曼彻斯特联',
    '曼城': '曼彻斯特城',
    '伯恩茅斯': 'AFC伯恩茅斯',
    '狼队': '伍尔弗汉普顿流浪者',
    '维拉': '阿斯顿维拉',
    '传奇皇马': '传奇皇家马德里',
    '传奇巴萨': '传奇巴塞罗那',
    '传奇阿森纳': '传奇阿森纳',
}

def resolve_team(name, teams):
    """Resolve team name, handling aliases"""
    for t in teams:
        if t['team'] == name:
            return t
    # Try alias
    if name in team_alias:
        for t in teams:
            if t['team'] == team_alias[name]:
                return t
    # Try substring match
    for t in teams:
        if name in t['team'] or t['team'] in name:
            return t
    return None

# Build player search across all teams
def find_player_all(name, teams):
    """Find player across all teams, return (team, index, player)"""
    for t in teams:
        for i, p in enumerate(t['players']):
            if p['name'] == name:
                return (t, i, p)
    return None

# 4. Apply moves in order
applied = 0
skipped = 0
for move in moves:
    player_name = move['name']
    to_team_name = move['to']

    # Find player in any team (not just 'from', since Firebase replay may have already moved them)
    result = find_player_all(player_name, teams)
    if not result:
        print(f'  SKIP: {player_name} not found in any team')
        skipped += 1
        continue

    from_team, pidx, player_data = result
    to_team = resolve_team(to_team_name, teams)

    if not to_team:
        print(f'  SKIP: dest team not found: {to_team_name} (for {player_name})')
        skipped += 1
        continue

    # Remove from source, add to dest
    from_team['players'].pop(pidx)
    to_team['players'].append(player_data)
    applied += 1
    print(f'  OK: {player_name}: {from_team["team"]} -> {to_team["team"]}')

print(f'\nApplied: {applied}, Skipped: {skipped}')

# 5. Write back
new_teams_json = json.dumps(teams, ensure_ascii=False, indent=2)
new_html = html[:arr_start] + new_teams_json + html[arr_end+1:]

# Check size change
print(f'Size: {len(html)} -> {len(new_html)}')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

# 6. Verify
with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    vhtml = f.read()

vidx = vhtml.find('TEAMS_DATA')
vas = vhtml.find('[', vidx)
depth = 0
vae = -1
for i in range(vas, min(vas + 500000, len(vhtml))):
    if vhtml[i] == '[': depth += 1
    elif vhtml[i] == ']':
        depth -= 1
        if depth == 0: vae = i; break

vteams = json.loads(vhtml[vas:vae+1])
ptmap = {}
for t in vteams:
    for p in t.get('players', []):
        ptmap[p['name']] = t['team']

wrong = 0
for move in moves:
    actual = ptmap.get(move['name'], 'NOT FOUND')
    to_resolved = team_alias.get(move['to'], move['to'])
    # Also try substring match for verification
    ok = False
    if actual == move['to']:
        ok = True
    elif actual == to_resolved:
        ok = True
    elif move['to'] in actual or actual in move['to']:
        ok = True
    if not ok:
        wrong += 1
        print(f'  WRONG: {move["name"]} should be {move["to"]}, is {actual}')

print(f'\nResult: {len(moves) - wrong}/{len(moves)} correct')
if wrong == 0:
    print('ALL MOVES APPLIED SUCCESSFULLY!')
