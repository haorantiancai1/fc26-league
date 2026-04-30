import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

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

for search in ['库尼亚', '马丁内斯', '阿马德', '马奎尔', '塞什科']:
    found = []
    for t in teams:
        for p in t.get('players', []):
            if search in p['name']:
                found.append(t['team'] + ': ' + p['name'])
    print(search + ': ' + str(found) if found else search + ': NOT FOUND')
