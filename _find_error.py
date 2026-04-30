import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all <script>...</script> blocks (not src ones)
blocks = []
pattern = r'<script>(.*?)</script>'
for m in re.finditer(pattern, html, re.DOTALL):
    blocks.append(m.group(1))

print(f'Found {len(blocks)} inline script blocks')
for i, b in enumerate(blocks):
    lines = b.split('\n')
    print(f'  Block {i}: {len(lines)} lines, {len(b)} chars')

# Check the biggest block
if blocks:
    biggest = max(blocks, key=len)
    lines = biggest.split('\n')
    line_num = 11718
    if line_num < len(lines):
        start = max(0, line_num - 5)
        end = min(len(lines), line_num + 5)
        for i in range(start, end):
            marker = '>>>' if i == line_num else '   '
            print(f'{marker} {i}: {lines[i][:200]}')
    else:
        print(f'Line {line_num} out of range (max {len(lines)-1})')
        # Show last few lines
        for i in range(max(0, len(lines)-10), len(lines)):
            print(f'   {i}: {lines[i][:200]}')
