import urllib.request, json, sys, re

sys.stdout.reconfigure(encoding='utf-8')

# 1. Read playerMoves from Firebase
base = 'https://fc26-league-47ef8-default-rtdb.asia-southeast1.firebasedatabase.app'
r = urllib.request.urlopen(base + '/playerMoves.json', timeout=10)
moves = json.loads(r.read().decode('utf-8'))

# 2. Compute final state: for each player, determine which team they should end up in
# Apply moves in order
from collections import OrderedDict
player_final = {}  # player_name -> to_team

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

def resolve_name(name):
    return team_alias.get(name, name)

for move in moves:
    player_final[move['name']] = resolve_name(move['to'])

print('Final player positions:')
for name, team in player_final.items():
    print(f'  {name} -> {team}')

# 3. Read the HTML file
with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 4. Parse TEAMS_DATA to find each player's current team
# Use regex to find each player object in the JSON
# Player format: {"name": "PLAYER_NAME", ...}

# First, build a list of (player_name, full_team_name, position_in_file)
# We'll do this by parsing the JSON properly but NOT reformatting
idx = html.find('TEAMS_DATA = [')
arr_start = html.find('[', idx)
depth = 0
arr_end = -1
for i in range(arr_start, min(arr_start + 500000, len(html))):
    if html[i] == '[': depth += 1
    elif html[i] == ']':
        depth -= 1
        if depth == 0: arr_end = i; break

teams_json_str = html[arr_start:arr_end+1]
teams = json.loads(teams_json_str)

# Build player -> current team map
player_current_team = {}
for t in teams:
    for p in t.get('players', []):
        player_current_team[p['name']] = t['team']

# 5. For each player that needs to move, find their JSON object in the HTML
# and move it from source team's players array to dest team's players array
# Strategy: Remove the player JSON object from source, add to dest

# Parse the teams structure to find exact positions in the HTML
# We need to find each team block and its players array

# Better approach: Build the new teams JSON string WITHOUT reformatting
# We just move player objects between teams

for name, dest_team in player_final.items():
    current_team = player_current_team.get(name)
    if current_team == dest_team:
        print(f'  SKIP (already there): {name} in {dest_team}')
        continue

    # Find the player object in the source team
    src_team_obj = None
    dst_team_obj = None
    player_obj = None
    player_idx = -1

    for t in teams:
        if t['team'] == current_team:
            src_team_obj = t
            for i, p in enumerate(t['players']):
                if p['name'] == name:
                    player_obj = p
                    player_idx = i
                    break
        if t['team'] == dest_team:
            dst_team_obj = t

    if not src_team_obj or not dst_team_obj or not player_obj:
        print(f'  ERROR: could not find {name}')
        continue

    # Move
    src_team_obj['players'].pop(player_idx)
    dst_team_obj['players'].append(player_obj)
    print(f'  MOVED: {name}: {current_team} -> {dest_team}')

# Now we need to write the teams back WITHOUT changing the JSON format
# The problem is json.dumps changes the format. Let's use a different approach:
# We'll serialize each team object individually and match the original format

# Actually, the simplest safe approach: use json.dumps but with ensure_ascii=True
# and separators without spaces to match the compact format
new_teams_json = json.dumps(teams, ensure_ascii=True, separators=(',', ':'))
# Wait, the original uses indented format... Let me check the original format
first_team_start = html.find('{', arr_start + 1)
first_500 = html[first_team_start:first_team_start+500]
# Check if indented or compact
is_compact = '\n' not in first_500 or first_500.count('\n') < 3
print(f'\nOriginal format compact: {is_compact}')
print(f'First 200 chars of original: {repr(first_500[:200])}')

# Actually let's check the indentation level
lines_before_teams = html[arr_start-200:arr_start]
print(f'\nBefore TEAMS_DATA: {repr(lines_before_teams[-50:])}')
