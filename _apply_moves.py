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

teams_json = html[arr_start:arr_end+1]
teams = json.loads(teams_json)
print(f'Parsed {len(teams)} teams')

# Build team lookup
team_lookup = {}
for t in teams:
    team_lookup[t['team']] = t

# 3. Apply moves in order
# For each move: remove player from source team, add to dest team
# But we need to handle "to" field - it could be full team name
def find_team(name):
    """Find team by full name or partial match"""
    if name in team_lookup:
        return team_lookup[name]
    # Try partial match
    for tname, t in team_lookup.items():
        if name in tname or tname in name:
            return t
    return None

applied = 0
skipped = 0
for move in moves:
    from_team_name = move['from']
    to_team_name = move['to']
    player_name = move['name']

    from_team = find_team(from_team_name)
    to_team = find_team(to_team_name)

    if not from_team:
        print(f'  SKIP: source team not found for {player_name}: {from_team_name}')
        skipped += 1
        continue
    if not to_team:
        print(f'  SKIP: dest team not found for {player_name}: {to_team_name}')
        skipped += 1
        continue

    # Find and remove player from source
    found = False
    for i, p in enumerate(from_team['players']):
        if p['name'] == player_name:
            player_data = from_team['players'].pop(i)
            to_team['players'].append(player_data)
            found = True
            applied += 1
            print(f'  OK: {player_name}: {from_team_name} -> {to_team_name}')
            break
    if not found:
        print(f'  SKIP: player not found in {from_team_name}: {player_name}')
        skipped += 1

print(f'\nApplied: {applied}, Skipped: {skipped}')

# 4. Write back to HTML
new_teams_json = json.dumps(teams, ensure_ascii=False, indent=2)
new_html = html[:arr_start] + new_teams_json + html[arr_end+1:]

with open(r'E:\FC26传奇联赛\deploy\index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f'\nUpdated index.html written')
print(f'Original size: {len(html)}, New size: {len(new_html)}')

# 5. Verify
with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    verify_html = f.read()

# Re-parse and check
idx2 = verify_html.find('TEAMS_DATA')
arr_start2 = verify_html.find('[', idx2)
depth = 0
arr_end2 = -1
for i in range(arr_start2, min(arr_start2 + 500000, len(verify_html))):
    if verify_html[i] == '[': depth += 1
    elif verify_html[i] == ']':
        depth -= 1
        if depth == 0:
            arr_end2 = i
            break

verify_teams = json.loads(verify_html[arr_start2:arr_end2+1])

# Rebuild player map
player_team_map = {}
for t in verify_teams:
    for p in t.get('players', []):
        player_team_map[p['name']] = t['team']

mismatches = 0
for move in moves:
    actual = player_team_map.get(move['name'], 'NOT FOUND')
    if actual != move['to']:
        mismatches += 1
        print(f'  STILL WRONG: {move["name"]} should be {move["to"]}, is {actual}')

print(f'\nVerification: {len(moves) - mismatches}/{len(moves)} correct')
if mismatches == 0:
    print('ALL MOVES APPLIED SUCCESSFULLY!')
