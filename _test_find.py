# -*- coding: utf-8 -*-
import urllib.request, json

# 1. Read TEAMS_DATA
f = open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8')
html = f.read()
f.close()

# Find the player
idx = html.find('"name": "\u738b\u94b0\u680b"')
if idx >= 0:
    print("Found at index:", idx)
    print(repr(html[idx-50:idx+50]))
else:
    print("NOT FOUND! Searching for partial...")
    idx = html.find('\u738b\u94b0\u680b')
    print("Partial found at:", idx)
    if idx >= 0:
        print(repr(html[idx-30:idx+30]))

# 2. Fetch Firebase
url = 'https://fc26-league-47ef8-default-rtdb.asia-southeast1.firebasedatabase.app/playerUpgrades.json'
resp = urllib.request.urlopen(url)
upgrades = json.loads(resp.read().decode())
print("\nFirebase upgrades:")
for u in upgrades:
    print("  name:", repr(u['name']))
