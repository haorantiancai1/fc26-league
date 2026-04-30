import urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://haorantiancai1.github.io/fc26-league/'
html = urllib.request.urlopen(url).read().decode('utf-8')

# Check the exact collapse section
idx = html.find('if(!_showAll)')
chunk = html[idx:idx+600]
print(repr(chunk[:600]))
