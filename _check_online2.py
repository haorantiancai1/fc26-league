import urllib.request, re, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://haorantiancai1.github.io/fc26-league/'
html = urllib.request.urlopen(url).read().decode('utf-8')

# Find renderSettlement
idx = html.find('function renderSettlement(')
if idx > -1:
    end = html.find('\nfunction ', idx + 10)
    func = html[idx:end]
    print('renderSettlement length:', len(func))

    # Check for collapse-related code
    checks = ['_showAll', '查看更早', '收起', '_extra', 'max-height', '_toggle', 'collapse']
    for c in checks:
        print(f'  {c}: {"YES" if c in func else "NO"}')

    # Print the last part of the function (after items loop)
    # Find the collapse section
    cidx = func.find('_showAll')
    if cidx > -1:
        print('\n--- Collapse section ---')
        print(func[cidx:cidx+800])
