import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('TEAMS_DATA = [')
arr_start = html.find('[', idx)
depth = 0; arr_end = -1
for i in range(arr_start, min(arr_start+500000, len(html))):
    if html[i]=='[': depth+=1
    elif html[i]==']': depth-=1
    if depth==0: arr_end=i; break

teams = json.loads(html[arr_start:arr_end+1])

for t in teams:
    if '曼城' in t['team'] and '传奇' not in t['team'] and t.get('is_player_team'):
        print('Team:', t['team'])
        for p in t['players']:
            if '席尔瓦' in p['name']:
                print('  Player:', p['name'], '|', p.get('position',''), '| OVR=', p.get('overall',''))
