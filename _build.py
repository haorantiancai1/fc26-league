import os

# Read components
with open(r'E:\FC26传奇联赛\deploy\_new_css.css', 'r', encoding='utf-8') as f:
    css = f.read()

with open(r'E:\FC26传奇联赛\deploy\_new_body.html', 'r', encoding='utf-8') as f:
    body_html = f.read()

with open(r'E:\FC26传奇联赛\deploy\_js_script_only.txt', 'r', encoding='utf-8') as f:
    js_script = f.read()

# Build parts
head_meta = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>FC26 \u4f20\u5947\u8054\u8d5b - \u7efc\u5408\u7ba1\u7406\u5de5\u5177</title>
<style>
"""
foot = """</style>
</head>
<body>
"""

closing = """
</body>
</html>
"""

final = head_meta + css + foot + body_html.strip() + "\n" + js_script + closing

with open(r'E:\FC26传奇联赛\deploy\index.html', 'w', encoding='utf-8') as f:
    f.write(final)

size_kb = os.path.getsize(r'E:\FC26传奇联赛\deploy\index.html') / 1024
line_count = final.count('\n') + 1
print(f'Done! File size: {size_kb:.1f} KB')
print(f'Total lines: {line_count}')
