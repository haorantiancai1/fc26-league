import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Count brackets
counts = {
    '(': content.count('('),
    ')': content.count(')'),
    '[': content.count('['),
    ']': content.count(']'),
    '{': content.count('{'),
    '}': content.count('}'),
}

ok = True
for open_b, close_b in [('(', ')'), ('[', ']'), ('{', '}')]:
    diff = counts[open_b] - counts[close_b]
    status = 'OK' if diff == 0 else f'MISMATCH (diff={diff})'
    print(f'{open_b}{close_b}: open={counts[open_b]}, close={counts[close_b]} -> {status}')
    if diff != 0:
        ok = False

print(f'\nTotal: {"ALL BALANCED" if ok else "ERROR!"}')
