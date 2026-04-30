import urllib.request, re, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://haorantiancai1.github.io/fc26-league/'
online = urllib.request.urlopen(url).read().decode('utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    local = f.read()

print('Online size:', len(online))
print('Local size:', len(local))

for key in ['renderSettlement', 'BADGE_VERBS', 'FUN_EVENTS', 'archiveSeason', '赛前解说', '赛后总结']:
    online_has = key in online
    local_has = key in local
    tag = 'OK' if online_has == local_has else 'DIFF'
    if online_has != local_has:
        print(f'{tag} {key}: online={online_has}, local={local_has}')

# Check collapse toggle
toggle_online = '查看更早' in online or '收起' in online
toggle_local = '查看更早' in local or '收起' in local
print(f'Collapse toggle: online={toggle_online}, local={toggle_local}')

m1 = re.search(r"var _cv = '(\d+)'", online)
m2 = re.search(r"var _cv = '(\d+)'", local)
print(f'Online _cv: {m1.group(1) if m1 else "?"}, Local _cv: {m2.group(1) if m2 else "?"}')
