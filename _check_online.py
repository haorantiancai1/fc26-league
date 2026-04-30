import urllib.request, re

url = 'https://haorantiancai1.github.io/fc26-league/'
html = urllib.request.urlopen(url).read().decode('utf-8')

m = re.search(r"var _cv = '(\d+)'", html)
print('_cv:', m.group(1) if m else 'NOT FOUND')

m = re.search(r"const APP_VERSION = '([^']+)'", html)
print('APP_VERSION:', m.group(1) if m else 'NOT FOUND')

idx = html.find('firebase.initializeApp')
if idx > -1:
    context = html[max(0,idx-100):idx+100]
    print('Has try-catch around firebase.initializeApp:', 'try' in context[:100])

# Check size
print('File size:', len(html))
