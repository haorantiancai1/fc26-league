import urllib.request, re, sys
sys.stdout.reconfigure(encoding='utf-8')

r = urllib.request.urlopen('https://haorantiancai1.github.io/fc26-league/')
html = r.read().decode('utf-8')

m = re.search(r"var _cv = '(\d+)'", html)
print('_cv:', m.group(1) if m else 'NOT FOUND')

idx = html.find('firebase.initializeApp')
if idx > -1:
    context = html[max(0,idx-100):idx+50]
    print('Has try-catch:', 'try {' in context)
else:
    print('firebase.initializeApp NOT FOUND')

r2 = urllib.request.urlopen('https://haorantiancai1.github.io/fc26-league/version.txt')
v = r2.read()
print('version.txt content:', v)
print('BOM-free:', not v.startswith(b'\xff') and not v.startswith(b'\xef'))
