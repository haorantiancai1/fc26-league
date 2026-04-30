import urllib.request, json, sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Read playerMoves
base = 'https://fc26-league-47ef8-default-rtdb.asia-southeast1.firebasedatabase.app'
r = urllib.request.urlopen(base + '/playerMoves.json', timeout=10)
moves = json.loads(r.read().decode('utf-8'))

# 2. Read HTML
with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 3. Parse TEAMS_DATA
import re
idx = html.find('TEAMS_DATA = [')
arr_start = html.find('[', idx)
depth = 0; arr_end = -1
for i in range(arr_start, min(arr_start+500000, len(html))):
    if html[i]=='[': depth+=1
    elif html[i]==']':
        depth-=1
        if depth==0: arr_end=i; break

teams = json.loads(html[arr_start:arr_end+1])
print(f'Parsed {len(teams)} teams')

# 4. Team alias resolution
team_alias = {
    '曼联': '曼彻斯特联',
    '曼城': '曼彻斯特城',
    '伯恩茅斯': 'AFC伯恩茅斯',
    '狼队': '狼队',
    '维拉': '阿斯顿维拉',
    '传奇皇马': '传奇皇家马德里',
    '传奇巴萨': '传奇巴萨',
    '传奇阿森纳': '传奇阿森纳',
}

def resolve(name):
    return team_alias.get(name, name)

# 5. Apply moves - find player by (from_team, name) combo to handle duplicates
applied = 0
for move in moves:
    pname = move['name']
    from_name = resolve(move['from'])
    to_name = resolve(move['to'])

    # Find the source team
    src_team = None
    dst_team = None
    for t in teams:
        if t['team'] == from_name:
            src_team = t
        if t['team'] == to_name:
            dst_team = t

    if not src_team:
        print(f'  SKIP: source team not found: {from_name} (for {pname})')
        continue
    if not dst_team:
        print(f'  SKIP: dest team not found: {to_name} (for {pname})')
        continue

    # Find player in source team by name
    pidx = -1
    player_obj = None
    for i, p in enumerate(src_team['players']):
        if p['name'] == pname:
            pidx = i
            player_obj = p
            break

    if pidx < 0:
        # Player not in source team - might already be moved by a previous move
        # Search all teams for this player
        found_anywhere = False
        for t in teams:
            for i, p in enumerate(t['players']):
                if p['name'] == pname:
                    player_obj = t['players'].pop(i)
                    dst_team['players'].append(player_obj)
                    print(f'  MOVED (found in {t["team"]}): {pname} -> {to_name}')
                    applied += 1
                    found_anywhere = True
                    break
            if found_anywhere:
                break
        if not found_anywhere:
            print(f'  SKIP: {pname} not found anywhere')
    else:
        src_team['players'].pop(pidx)
        dst_team['players'].append(player_obj)
        print(f'  MOVED: {pname}: {from_name} -> {to_name}')
        applied += 1

print(f'\nTotal applied: {applied}/{len(moves)}')

# 6. Serialize back - use indent=2 to match original format
new_json = json.dumps(teams, ensure_ascii=False, indent=2)
# Ensure it ends with a newline after ]
new_html = html[:arr_start] + new_json + html[arr_end+1:]

with open(r'E:\FC26传奇联赛\deploy\index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print(f'Written. Size: {len(html)} -> {len(new_html)}')

# 7. Verify
with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    vhtml = f.read()
vidx = vhtml.find('TEAMS_DATA = [')
vas = vhtml.find('[', vidx)
depth = 0; vae = -1
for i in range(vas, min(vas+500000, len(vhtml))):
    if vhtml[i]=='[': depth+=1
    elif vhtml[i]==']':
        depth-=1
        if depth==0: vae=i; break

vteams = json.loads(vhtml[vas:vae+1])

# Check for each player's final position
# Rebuild final positions
final = {}
for move in moves:
    final[move['name']] = resolve(move['to'])

# But if a player has multiple moves, only the last one counts
# Actually we should compute net effect
from collections import OrderedDict
net = {}
for move in moves:
    net[move['name']] = resolve(move['to'])

ptmap = {}
for t in vteams:
    for p in t.get('players', []):
        if p['name'] in net:
            ptmap[p['name']] = t['team']

wrong = 0
for name, expected in net.items():
    actual = ptmap.get(name, 'NOT FOUND')
    if actual != expected:
        wrong += 1
        print(f'  WRONG: {name} should be {expected}, is {actual}')

print(f'\nVerification: {len(net)-wrong}/{len(net)} correct')
if wrong == 0:
    print('ALL CORRECT!')
