with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-16') as f:
    content = f.read()
with open(r'E:\FC26传奇联赛\deploy\index.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
print('Converted to UTF-8')
