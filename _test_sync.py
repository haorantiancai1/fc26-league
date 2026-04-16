import urllib.request, json

# 1. Read TEAMS_DATA from index.html
f = open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8')
html = f.read()
f.close()

start = html.index('TEAMS_DATA = [')
json_start = start + 14
depth = 0
end = json_start
for i in range(json_start, len(html)):
    if html[i] == '[': depth += 1
    elif html[i] == ']': depth -= 1
    if depth == 0:
        end = i + 1
        break

teams_json = html[json_start:end]
teams_data = json.loads(teams_json)
print('TEAMS_DATA parsed OK, teams:', len(teams_data))

# Find all players with name containing 钰栋 or Yudong
for t in teams_data:
    for p in t['players']:
        n = p.get('name','')
        ne = p.get('name_en','')
        if '\u94b0\u680b' in n or 'Yudong' in ne:
            print(f'Player: name="{n}" name_en="{ne}" team={t["team"]} OVR={p["overall"]}')

# 2. Fetch Firebase playerUpgrades
url = 'https://fc26-league-47ef8-default-rtdb.asia-southeast1.firebasedatabase.app/playerUpgrades.json'
resp = urllib.request.urlopen(url)
upgrades = json.loads(resp.read().decode())
print('\nFirebase upgrades:', len(upgrades), 'records')
for u in upgrades:
    print(f'  name="{u["name"]}" new_overall={u["new_overall"]}')

# 3. Replay
print('\n--- Replay ---')
for u in upgrades:
    name = u['name']
    matched = False
    for t in teams_data:
        for p in t['players']:
            if p['name'] == name:
                matched = True
                old = p['overall']
                p['overall'] = u['new_overall']
                p['market_price'] = u['new_market_price']
                p['sell_price'] = u['new_sell_price']
                print(f'  MATCHED: "{name}" in {t["team"]} OVR {old} -> {u["new_overall"]}')
    if not matched:
        print(f'  NOT MATCHED: "{name}"')

# 4. Final
print('\n--- Final state ---')
for t in teams_data:
    for p in t['players']:
        if '\u94b0\u680b' in p.get('name','') or 'Yudong' in p.get('name_en',''):
            print(f'  "{p["name"]}" OVR={p["overall"]} team={t["team"]}')
