import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
main_js = max(scripts, key=len)

td_start = main_js.find('TEAMS_DATA')
td_end = main_js.find('];', td_start) + 2
td_section = main_js[td_start:td_end]

bt = td_section.count(chr(96))  # backtick
te = td_section.count('$' + '{')  # template expr
sc = td_section.count('</script>')

print('Backticks in TEAMS_DATA:', bt)
print('Template expressions in TEAMS_DATA:', te)
print('</script> in TEAMS_DATA:', sc)

# Also check for \\u2028 and \\u2029
u2028 = td_section.count('\u2028')
u2029 = td_section.count('\u2029')
print('U+2028 in TEAMS_DATA:', u2028)
print('U+2029 in TEAMS_DATA:', u2029)

# Check for lone \r (carriage return) that might cause issues
cr = td_section.count('\r')
lf = td_section.count('\n')
print('CR in TEAMS_DATA:', cr)
print('LF in TEAMS_DATA:', lf)
