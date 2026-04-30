import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

teams = [('切尔西', 'chelsea'), ('利物浦', 'liverpool'), ('曼彻斯特城', 'mancity'), ('曼彻斯特联', 'manutd')]

for cn_name, en_name in teams:
    # Find team entry
    pattern = 'team:"' + cn_name + '"'
    idx = html.find(pattern)
    if idx < 0:
        pattern = "team:'" + cn_name + "'"
        idx = html.find(pattern)
    if idx < 0:
        print(f'{en_name}: NOT FOUND')
        continue
    
    chunk = html[idx:idx+100000]
    # Find players:[
    pi = chunk.find('players:[')
    if pi < 0:
        print(f'{en_name}: no players array found')
        continue
    
    players_section = chunk[pi:]
    # Count name: entries until we hit the closing ]
    depth = 0
    count = 0
    i = 0
    in_players = False
    for i, ch in enumerate(players_section):
        if ch == '[':
            depth += 1
            in_players = True
        elif ch == ']':
            depth -= 1
            if depth == 0 and in_players:
                break
        if players_section[i:i+5] == 'name:' and in_players:
            count += 1
    
    print(f'{en_name} ({cn_name}): {count} players')
