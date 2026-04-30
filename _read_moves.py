import urllib.request, json, sys

sys.stdout.reconfigure(encoding='utf-8')

base = 'https://fc26-league-47ef8-default-rtdb.asia-southeast1.firebasedatabase.app'

url = base + '/playerMoves.json'
r = urllib.request.urlopen(url, timeout=10)
data = json.loads(r.read().decode('utf-8'))

print(f'Total playerMoves: {len(data)}')
for i, m in enumerate(data):
    print(f'{i+1}. {m["from"]} → {m["to"]}: {m["name"]}')
