import urllib.request, re, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://haorantiancai1.github.io/fc26-league/'
html = urllib.request.urlopen(url).read().decode('utf-8')

# Find renderSettlement
idx = html.find('function renderSettlement(')
end = html.find('\nfunction ', idx + 10)
func = html[idx:end]

# Find _showAll and look for the toggle section after items loop
toggle_idx = func.find('if(!_showAll)')
if toggle_idx > -1:
    print('--- if(!_showAll) section ---')
    print(func[toggle_idx:toggle_idx+500])
else:
    print('No if(!_showAll) section found')
    # Try to find where items end
    idx2 = func.find('html += \'</div>\';')
    if idx2 > -1:
        print('--- After items loop ---')
        print(func[idx2-100:idx2+300])
