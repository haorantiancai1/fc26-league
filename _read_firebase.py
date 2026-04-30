import urllib.request, json, sys

sys.stdout.reconfigure(encoding='utf-8')

# Firebase REST API - read pendingOps
base = 'https://fc26-league-47ef8-default-rtdb.asia-southeast1.firebasedatabase.app'

paths = ['pendingOps', 'playerMoves', 'budgets', 'bteams']
for path in paths:
    try:
        url = base + '/' + path + '.json'
        r = urllib.request.urlopen(url, timeout=10)
        data = json.loads(r.read().decode('utf-8'))
        if data:
            if isinstance(data, dict):
                print(f'\n=== {path} ({len(data)} entries) ===')
                for k, v in list(data.items())[:10]:
                    print(f'  {k}: {json.dumps(v, ensure_ascii=False)[:200]}')
                if len(data) > 10:
                    print(f'  ... and {len(data)-10} more entries')
            else:
                print(f'\n=== {path} ===')
                print(json.dumps(data, ensure_ascii=False)[:500])
        else:
            print(f'{path}: null/empty')
    except Exception as e:
        print(f'{path}: ERROR - {e}')
