import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the main script
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
main_js = max(scripts, key=len)

# Extract TEAMS_DATA - find the start
start_marker = 'TEAMS_DATA = ['
start_idx = main_js.find(start_marker)
if start_idx < 0:
    print('TEAMS_DATA start not found')
    sys.exit(1)

# Find matching ] by counting brackets
depth = 0
end_idx = start_idx + len(start_marker) - 1  # at the [
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

# Focus on 4 main teams
main_teams = ['切尔西', '利物浦', '曼彻斯特城', '曼彻斯特联']

print('=' * 60)
print('结算清单核对：球员是否在该在的球队')
print('=' * 60)

for team in teams:
    if team['team'] not in main_teams:
        continue
    players = team.get('players', [])
    print(f"\n【{team['team']}】 共 {len(players)} 人:")
    for p in sorted(players, key=lambda x: (-x.get('overall',0), x.get('name',''))):
        is_player = p.get('is_player', False)
        is_legend = p.get('is_legend', False)
        tag = ''
        if is_player: tag = ' [玩家]'
        if is_legend: tag = ' [传奇]'
        print(f"  {p['name']:12s} {p.get('position',''):4s} OVR {p.get('overall',0):2d}{tag}")

print('\n' + '=' * 60)
print('转会操作验证：')
print('=' * 60)

# Build a quick lookup
player_locations = {}
for team in teams:
    for p in team.get('players', []):
        player_locations[p['name']] = team['team']

# All transfers from settle list
transfers = [
    # Chelsea sells
    ('阿达拉比奥尤', '切尔西', '伯恩茅斯', '售出'),
    ('巴迪亚西勒', '切尔西', '伯恩茅斯', '售出'),
    ('埃苏戈', '切尔西', '伯恩茅斯', '售出'),
    ('约恩森', '切尔西', '伯恩茅斯', '售出'),
    # Liverpool
    ('阿利松', '利物浦', '切尔西', '互换'),  # swapped with 伊萨克
    ('萨拉赫', '利物浦', '传奇皇马', '售出'),
    ('布拉德利', '利物浦', '传奇皇马', '售出'),
    ('梅西', '传奇巴萨', '利物浦', '购入'),
    # Man Utd sells
    ('库尼亚', '曼联', '狼队', '售出'),
    ('马丁内斯', '曼联', '狼队', '售出'),
    ('阿马德', '曼联', '狼队', '售出'),
    ('马奎尔', '曼联', '狼队', '售出'),
    ('塞什科', '曼联', '狼队', '售出'),
    # Man City
    ('福登', '曼城', '伯恩利', '售出'),
    ('席尔瓦', '曼城', '伯恩利', '售出'),
    ('萨维尼奥', '曼城', '伯恩利', '售出'),
    ('维埃拉', '传奇阿森纳', '曼城', '购入'),
    ('贝克汉姆', '传奇皇马', '曼城', '购入'),
    # Swap: 伊萨克 should now be at Liverpool
    ('伊萨克', '切尔西', '利物浦', '互换'),
]

all_ok = True
for name, from_team, to_team, op in transfers:
    actual = player_locations.get(name, '❌ 不在任何球队')
    expected = to_team
    ok = actual == expected
    status = '✅' if ok else '❌'
    if not ok:
        all_ok = False
    print(f"  {status} {name:10s} 应在[{expected:8s}] 实际在[{actual:10s}] ({op})")

# Also check sold players are NOT in their original teams
print('\n已售出球员确认已离开原队：')
sold_players = [
    ('阿达拉比奥尤', '切尔西'),
    ('巴迪亚西勒', '切尔西'),
    ('埃苏戈', '切尔西'),
    ('约恩森', '切尔西'),
    ('萨拉赫', '利物浦'),
    ('布拉德利', '利物浦'),
    ('阿利松', '利物浦'),
    ('库尼亚', '曼联'),
    ('马丁内斯', '曼联'),
    ('阿马德', '曼联'),
    ('马奎尔', '曼联'),
    ('塞什科', '曼联'),
    ('福登', '曼城'),
    ('席尔瓦', '曼城'),
    ('萨维尼奥', '曼城'),
]
for name, orig_team in sold_players:
    actual = player_locations.get(name, '不在任何球队')
    ok = actual != orig_team
    status = '✅' if ok else '❌'
    if not ok:
        all_ok = False
    print(f"  {status} {name:10s} 已离开[{orig_team:8s}] 当前在[{actual}]")

if all_ok:
    print('\n🎉 全部核对通过！所有球员都在正确的位置。')
else:
    print('\n⚠️ 有球员位置不对，请检查上面标记 ❌ 的条目。')
